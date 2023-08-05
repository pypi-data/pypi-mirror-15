# Copyright 2016 Capital One Services, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""S3 Resource Manager

Filters:

The generic Values filters (jmespath) expression and Or filter are
available with all resources, including buckets, we include several
additonal bucket data (Tags, Replication, Acl, Policy) as keys within
a bucket representation.

Actions:

 encrypt-keys

   Scan all keys in a bucket and optionally encrypt them in place.

 global-grants

   Check bucket acls for global grants
  
 encryption-policy

   Attach an encryption required policy to a bucket, this will break
   applications that are not using encryption, including aws log
   delivery.

"""
from botocore.client import Config
from botocore.exceptions import ClientError
from concurrent.futures import as_completed

import json
import itertools
import logging
import os
import time

from c7n import executor
from c7n.actions import ActionRegistry, BaseAction
from c7n.filters import FilterRegistry, Filter
from c7n.manager import ResourceManager, resources
from c7n.utils import chunks, local_session, set_annotation, type_schema

"""
TODO:
 - How does replication status effect in place encryption.
 - Test glacier support
"""

log = logging.getLogger('custodian.s3')

filters = FilterRegistry('s3.filters')
actions = ActionRegistry('s3.actions')


@resources.register('s3')
class S3(ResourceManager):

    executor_factory = executor.ThreadPoolExecutor
    filter_registry = filters
    action_registry = actions
    
    def __init__(self, ctx, data):
        super(S3, self).__init__(ctx, data)
        self.log_dir = ctx.log_dir

    def get_resources(self, resource_ids):
        with self.executor_factory(
                max_workers=min((5, len(resource_ids)))) as w:
            buckets = {'Name': r for r in resource_ids}
            results = w.map(
                assemble_bucket,
                zip(itertools.repeat(self.session_factory), buckets))
            results = filter(None, results)
        return results
        
    def resources(self):
        c = self.session_factory().client('s3')
        log.debug('Retrieving buckets')
        response = c.list_buckets()
        buckets = response['Buckets']
        log.debug('Got %d buckets' % len(buckets))
        log.debug('Assembling bucket documents')
        with self.executor_factory(max_workers=10) as w:
            results = w.map(
                assemble_bucket,
                zip(itertools.repeat(self.session_factory), buckets))
            results = filter(None, results)
        return self.filter_resources(results)

    
def assemble_bucket(item):
    """Assemble a document representing all the config state around a bucket.
    """
    factory, b = item

    s = factory()
    c = s.client('s3')

    methods = [
        ('get_bucket_location', 'Location', None, None),
        ('get_bucket_tagging', 'Tags', [], 'TagSet'),
        ('get_bucket_policy',  'Policy', None, None),   
        ('get_bucket_acl', 'Acl', None, None),
        ('get_bucket_replication', 'Replication', None, None),
        ('get_bucket_versioning', 'Versioning', None, None),
        ('get_bucket_website', 'Website', None, None)
#        ('get_bucket_lifecycle', 'Lifecycle', None, None),
#        ('get_bucket_cors', 'Cors'),        
#        ('get_bucket_notification_configuration', 'Notification')
    ]

    # Bucket Location, Current Client Location, Default Location
    b_location = c_location = location = "us-east-1"
    
    for m, k, default, select in methods:
        try:
            method = getattr(c, m)
            v = method(Bucket=b['Name'])
            v.pop('ResponseMetadata')
            if select is not None:
                v = v[select]
        except ClientError, e:
            code =  e.response['Error']['Code']
            if code.startswith("NoSuch") or "NotFound" in code:
                v = default
            elif code == 'PermanentRedirect':
                # log.warning(e.response)
                s = factory()
                c = bucket_client(s, b)
                # Requeue with the correct region given location constraint
                methods.append((m, k))
                continue
            else:
                log.warning("Bucket:%s unable to invoke method:%s error:%s " % (
                    b['Name'], m, e.response['Error']['Message']))
                return None
        # As soon as we learn location (which generally works)
        if k == 'Location' and v is not None:
            b_location = v.get('LocationConstraint')
            if v and v != c_location:
                c = s.client('s3', region_name=b_location)
            elif c_location != location:
                c = s.client('s3', region_name=location)
        b[k] = v
    return b


def bucket_client(session, b, kms=False):
    location = b.get('Location')
    if location is None:
        region = 'us-east-1'
    else:
        region = location['LocationConstraint'] or 'us-east-1'
    if kms:
        # Need v4 signature for aws:kms crypto
        config = Config(signature_version='s3v4')
    else:
        config = None
    return session.client(
        's3', region_name=region,        
        config=config)


@filters.register('global-grants')        
class NoGlobalGrants(Filter):

    schema = type_schema('global-grants')

    GLOBAL_ALL = "http://acs.amazonaws.com/groups/global/AllUsers"
    AUTH_ALL = "http://acs.amazonaws.com/groups/global/AuthenticatedUsers"
    
    def process(self, buckets, event=None):
        with self.executor_factory(max_workers=5) as w:
            results = w.map(self.process_bucket, buckets)
            results = filter(None, list(results))
            return results

    def process_bucket(self, b):
        acl = b.get('Acl', {'Grants': []})
        if not acl or not acl['Grants']:
            return
        results = []
        for grant in acl['Grants']:
            if 'URI' not in grant.get("Grantee", {}):
                continue
            if grant['Grantee']['URI'] in [self.AUTH_ALL, self.GLOBAL_ALL]:
                if grant['Permission'] == 'READ' and b['Website']:
                    continue
                results.append(grant['Permission'])

        c = bucket_client(self.manager.session_factory(), b)

        if results:
            set_annotation(b, 'GlobalPermissions', results)
            return b


class BucketActionBase(BaseAction):

    def get_permissions(self):
        return self.permissions

    
@actions.register('encrypted-prefix')
class EncryptedPrefix(BucketActionBase):

    permissions = ("s3:GetObject", "s3:PutObject")
    
    def process(self, buckets):
        prefix = self.data.get('prefix')
        with self.executor_factory(max_workers=5) as w:
            results = w.map(self.process_bucket, buckets)
            results = filter(None, list(results))
            return results

    def process_bucket(self, b):
        s3 = bucket_client(self.manager.session_factory(), b)
        k = self.data.get('prefix', 'AWSLogs')

        create = True
        try:
            data = s3.head_object(Bucket=b['Name'], Key=k)
            create = False
            if 'ServerSideEncryption' in data:
                return None
        except ClientError, e:
            if e.response['Error']['Code'] != '404':
                raise

        crypto_method = self.data.get('crypto', 'AES256')
        if create:
            content = "Path Prefix Object For Sub Path Encryption"
            s3.put_object(
                Bucket=b['Name'],
                Key=k,
                ACL="bucket-owner-full-control",
                Body=content,
                ServerSideEncryption=crypto_method)
            return {'Bucket': b['Name'], 'Prefix': k, 'State': 'Created'}

        # Note on copy we lose individual key acl grants        
        s3.copy_object(
            Bucket=b['Name'], Key=k,
            CopySource="/%s/%s" % (b, k),
            MetadataDirective='COPY',
            ServerSideEncryption=crypto_method)
        return {'Bucket': b['Name'], 'Prefix': k, 'State': 'Updated'}
        

@filters.register('missing-policy-statement')
class MissingPolicyStatementFilter(Filter):
    """Find buckets missing a set of named policy statements."""

    schema = type_schema(
        'missing-policy-statement',
        statement_ids={'type': 'array', 'items': {'type': 'string'}})

    def process(self, buckets, event=None):
        with self.executor_factory(max_workers=5) as w:
            results = w.map(self.process_bucket, buckets)
            results = filter(None, list(results))
            return results

    def process_bucket(self, b):
        p = b['Policy']
        if p is None:
            return b

        p = json.loads(p['Policy'])

        required = list(self.data.get('statement_ids', []))
        statements = p.get('Statement', [])
        
        for s in list(statements):
            if s['StatementId'] in required:
                required.remove(s['StatementId'])
        if not required:
            return None
        return b

    
@actions.register('no-op')
class NoOp(BucketActionBase):

    schema = type_schema('no-op')
    
    def process(self, buckets):
        return None
            
            
@actions.register('encryption-policy')    
class EncryptionRequiredPolicy(BucketActionBase):

    permissions = ("s3:GetBucketPolicy", "s3:PutBucketPolicy")

    schema = type_schema('encryption-policy')

    def __init__(self, data=None, manager=None):
        self.data = data or {}
        self.manager = manager
        
    def process(self, buckets):
        with self.executor_factory(max_workers=3) as w:
            results = w.map(self.process_bucket, buckets)
            results = filter(None, list(results))
            return results

    def process_bucket(self, b):
        p = b['Policy']
        if p is None:
            log.info("No policy found, creating new")
            p = {'Version': "2012-10-17", "Statements": []}
        else:
            p = json.loads(p['Policy'])
            
        statements = p.get('Statement', [])
        found = False
        for s in list(statements):
            if s['Sid'] == 'RequireEncryptedPutObject':
                log.debug(
                    "Bucket:%s Found extant Encryption Policy" % b['Name'])
                return
        
        session = self.manager.session_factory()
        s3 = bucket_client(session, b)

        statements.append(
            {'Sid': 'RequireEncryptedPutObject',
             'Effect': 'Deny',
             'Principal': '*',
             'Action': 's3:PutObject',
             "Resource":"arn:aws:s3:::%s/*" % b['Name'],
             "Condition":{
                 # AWS Managed Keys or KMS keys, note policy language
                 # does not support custom kms (todo add issue)
                 "StringNotEquals":{
                     "s3:x-amz-server-side-encryption": ["AES256", "aws:kms"]}}
             })
        p['Statement'] = statements
        log.info('Bucket:%s attached encryption policy' % b['Name'])

        s3.put_bucket_policy(
            Bucket=b['Name'],
            Policy=json.dumps(p))
        return {'Name': b['Name'], 'State': 'PolicyAttached'}

        
class BucketScanLog(object):
    """Offload remediated key ids to a disk file in batches
    
    A bucket keyspace is effectively infinite, we need to store partial
    results out of memory, this class provides for a json log on disk
    with partial write support.

    json output format:
     - [list_of_serialized_keys],
     - [] # Empty list of keys at end when we close the buffer
    
    """
    def __init__(self, log_dir, name):
        self.log_dir = log_dir
        self.name = name
        self.fh = None
        self.count = 0

    @property
    def path(self):
        return os.path.join(self.log_dir, "%s.json" % self.name)
    
    def __enter__(self):
        self.fh = open(self.path, 'w')
        self.fh.write("[\n")
        return self
    
    def __exit__(self, exc_type=None, exc_value=None, exc_frame=None):
        # we need an empty marker list at end to avoid trailing commas
        self.fh.write("[]")
        # and close the surrounding list
        self.fh.write("\n]")
        self.fh.close()
        if not self.count:
            os.remove(self.fh.name)
        self.fh = None
        return False
        
    def add(self, keys):
        self.count += len(keys)
        self.fh.write(json.dumps(keys))
        self.fh.write(",\n")


class ScanBucket(BucketActionBase):

    permissions = ("s3:ListBucket",)

    bucket_ops = {
        'standard': {
            'iterator': 'list_objects',
            'contents_key': 'Contents',
            'key_processor': 'process_key'
            },
        'versioned': {
            'iterator': 'list_object_versions',
            'contents_key': 'Versions',
            'key_processor': 'process_version'
            }
        }

    def get_bucket_style(self, b):
        return (
            b.get('Versioning', {'Status': ''}).get('Status') == 'Enabled'
            and 'versioned' or 'standard')
    
    def get_bucket_op(self, b, op_name):
        bucket_style = self.get_bucket_style(b)
        op = self.bucket_ops[bucket_style][op_name]
        if op_name == 'key_processor':
            return getattr(self, op)
        return op

    def process(self, buckets):
        results = []
        with self.executor_factory(max_workers=3) as w:
            results.extend(
                f for f in w.map(self, buckets) if f)
        return results

    def process_bucket(self, b):
        log.info(
            "Scanning bucket:%s visitor:%s style:%s" % (
                b['Name'], self.__class__.__name__, self.get_bucket_style(b)))
        s = self.manager.session_factory()
        s3 = bucket_client(s, b)

        # The bulk of _process_bucket function executes inline in
        # calling thread/worker context, neither paginator nor
        # bucketscan log should be used across worker boundary.
        p = s3.get_paginator(
            self.get_bucket_op(b, 'iterator')).paginate(Bucket=b['Name'])
        with BucketScanLog(self.manager.log_dir, b['Name']) as key_log:
            with self.executor_factory(max_workers=10) as w:
                try:
                    return self._process_bucket(b, p, key_log, w)
                except ClientError as e:
                    if e.response['Error']['Code'] == 'NoSuchBucket':
                        log.warning(
                            "Bucket:%s removed while scanning" % b['Name'])
                        return
                    log.exception(
                        "Error processing bucket:%s paginator:%s" % (
                            b['Name'], p))

    __call__ = process_bucket
    
    def _process_bucket(self, b, p, key_log, w):
        content_key = self.get_bucket_op(b, 'contents_key')
        count = 0
        for key_set in p:
            count += len(key_set.get(content_key, []))

            # Empty bucket check
            if not content_key in key_set and not key_set['IsTruncated']:
                return {'Bucket': b['Name'],
                        'Remediated': key_log.count,
                        'Count': count}
            futures = []
            for batch in chunks(key_set.get(content_key, []), size=100):
                if not batch:
                    continue
                futures.append(w.submit(self.process_chunk, batch, b))

            for f in as_completed(futures):
                if f.exception():
                    log.exception("Exception Processing bucket:%s key batch %s" % (
                        b['Name'], f.exception()))
                    continue
                r = f.result()
                if r:
                    key_log.add(r)

            # Log completion at info level, progress at debug level
            if key_set['IsTruncated']:
                log.debug('Scan progress bucket:%s keys:%d remediated:%d ...',
                         b['Name'], count, key_log.count)
            else:
                log.info('Scan Complete bucket:%s keys:%d remediated:%d',
                         b['Name'], count, key_log.count)

        return {'Bucket': b['Name'], 'Remediated': key_log.count, 'Count': count}

    def process_chunk(self, batch, bucket):
        raise NotImplementedError()

    def process_key(self, s3, key, bucket_name, info=None):
        raise NotImplementedError()

    def process_version(self, s3, bucket, key):
        raise NotImplementedError()
    

@actions.register('encrypt-keys')    
class EncryptExtantKeys(ScanBucket):

    permissions = (
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObjectVersion",
        "s3:RestoreObject",
    ) + ScanBucket.permissions

    schema = {
        'type': 'object',
        'additonalProperties': False,
        'properties': {
            'report-only': {'type': 'boolean'},
            'crypto': {'enum': ['AES256', 'aws:kms']}
            }
        }

    def process(self, buckets):
        t = time.time()
        results = super(EncryptExtantKeys, self).process(buckets)
        run_time = time.time() - t
        remediated_count = object_count = 0
        for r in results:
            object_count += r['Count']
            remediated_count += r['Remediated']
            self.manager.ctx.metrics.put_metric(
                "Unencrypted", r['Remediated'], "Count", Scope=r['Bucket'],
                buffer=True)

        self.manager.ctx.metrics.put_metric(
            "Unencrypted", remediated_count, "Count", Scope="Account",
            buffer=True
        )
        self.manager.ctx.metrics.put_metric(
            "Total Keys", object_count, "Count", Scope="Account",
            buffer=True
        )
        self.manager.ctx.metrics.flush()
                
        log.info(
            ("EncryptExtant Complete keys:%d "
             "remediated:%d rate:%0.2f/s time:%0.2fs"),
            object_count,
            remediated_count,
            float(object_count) / run_time,
            run_time)
        return results

    def process_chunk(self, batch, bucket):
        crypto_method = self.data.get('crypto', 'AES256')
        s3 = bucket_client(
            local_session(self.manager.session_factory), bucket,
            kms=(crypto_method == 'aws:kms'))
        b = bucket['Name']
        results = []
        key_processor = self.get_bucket_op(bucket, 'key_processor')
        for key in batch:
            r = key_processor(s3, key, b)
            if r:
                results.append(r)
        return results

    def process_key(self, s3, key, bucket_name, info=None):
        k = key['Key']

        if info is None:
            info = s3.head_object(Bucket=bucket_name, Key=k)

        if 'ServerSideEncryption' in info:
            return False

        if self.data.get('report-only'):
            return k

        storage_class = key['StorageClass']
        
        if storage_class == 'GLACIER':
            if not 'Restore' in info:
                # This takes multiple hours, we let the next c7n
                # run take care of followups.
                s3.restore_object(
                    Bucket=bucket_name,
                    Key=k,
                    RestoreRequest={'Days': 30})
                return False
            elif not restore_complete(info['Restore']):
                return False
            storage_class == 'STANDARD'

        crypto_method = self.data.get('crypto', 'AES256')
        # Note on copy we lose individual object acl grants
        params = {'Bucket': bucket_name,
                  'Key': k,
                  'CopySource': "/%s/%s" % (bucket_name, k),
                  'MetadataDirective': 'COPY',
                  'StorageClass': storage_class,
                  'ServerSideEncryption': crypto_method}
        s3.copy_object(**params)
        return k

    def process_version(self, s3, key, bucket_name):
        info = s3.head_object(
            Bucket=bucket_name,
            Key=key['Key'],
            VersionId=key['VersionId'])

        if 'ServerSideEncryption' in info:
            return False

        if self.data.get('report-only'):
            return key['Key'], key['VersionId']

        if key['IsLatest']:
            r = self.process_key(s3, key, bucket_name, info)
            # Glacier request processing, wait till we have the restored object
            if not r:
                return r
        s3.delete_object(
            Bucket=bucket_name,
            Key=key['Key'],
            VersionId=key['VersionId'])
        return key['Key'], key['VersionId']


def restore_complete(restore):
    if ',' in restore:
        ongoing, avail = restore.split(',', 1)
    else:
        ongoing = restore
    return 'false' in ongoing
