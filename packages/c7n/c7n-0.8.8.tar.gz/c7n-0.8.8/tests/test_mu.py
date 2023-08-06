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
import json
import logging
import unittest
import StringIO
import zipfile

from c7n.mu import custodian_archive, LambdaManager, PolicyLambda
from c7n.policy import Policy
from .common import BaseTest, Config


class PolicyLambdaProvision(BaseTest):

    role = "arn:aws:iam::619193117841:role/lambda_basic_execution"
    
    def assert_items(self, result, expected):
        for k, v in expected.items():
            self.assertEqual(v, result[k])

    def xtest_cwe_update_no_change(self):
        session_factory = self.replay_flight_data(
            'test_cwe_update', zdata=True)
        p = Policy({
            'resource': 's3',
            'name': 's3-bucket-policy',
            'mode': {
                'type': 'cloudtrail',
                'events': ["CreateBucket"],
            },
            'filters': [
                {'type': 'missing-policy-statement',
                 'statement_ids': ['RequireEncryptedPutObject']}],
            'actions': ['no-op']
        }, Config.empty())
        pl = PolicyLambda(p)
        mgr = LambdaManager(session_factory)
        result = mgr.publish(pl, 'Dev', role=self.role)
        output = self.capture_logging('custodian.lambda', level=logging.DEBUG)
        result2 = mgr.publish(PolicyLambda(p), 'Dev', role=self.role)
        self.assertEqual(len(output.getvalue().strip().split('\n')), 1)
        self.assertEqual(result['FunctionName'], result2['FunctionName'])
        mgr.remove(pl)

    def test_cwe_trail(self):
        session_factory = self.replay_flight_data('test_cwe_trail', zdata=True)
        p = Policy({
            'resource': 's3',
            'name': 's3-bucket-policy',
            'mode': {
                'type': 'cloudtrail',
                'events': ["CreateBucket"],
            },
            'filters': [
                {'type': 'missing-policy-statement',
                 'statement_ids': ['RequireEncryptedPutObject']}],
            'actions': ['no-op']
        }, Config.empty())
        pl = PolicyLambda(p)
        mgr = LambdaManager(session_factory)
        result = mgr.publish(pl, 'Dev', role=self.role)
        
        events = pl.get_events(session_factory)
        self.assertEqual(len(events), 1)
        event = events.pop()
        self.assertEqual(
            json.loads(event.render_event_pattern()),
            {u'detail': {u'eventName': [u'CreateBucket'],
                         u'eventSource': [u'aws.s3']},
             u'detail-type': ['AWS API Call via CloudTrail']})
        
        self.assert_items(
            result,
            {'Description': 'cloud-custodian lambda policy',
             'FunctionName': 'custodian-s3-bucket-policy',
             'Handler': 'custodian_policy.run',
             'MemorySize': 512,
             'Runtime': 'python2.7',
             'Timeout': 60})
        mgr.remove(pl)
                             
    def test_cwe_instance(self):
        session_factory = self.replay_flight_data(
            'test_cwe_instance', zdata=True)
        p = Policy({
            'resource': 's3',
            'name': 'ec2-encrypted-vol',
            'mode': {
                'type': 'ec2-instance-state',
                'events': ['pending']}
        }, Config.empty())
        pl = PolicyLambda(p)
        mgr = LambdaManager(session_factory)
        result = mgr.publish(pl, 'Dev', role=self.role)
        self.assert_items(
            result,
            {'Description': 'cloud-maid lambda policy',
             'FunctionName': 'maid-ec2-encrypted-vol',
             'Handler': 'maid_policy.run',
             'MemorySize': 512,
             'Runtime': 'python2.7',
             'Timeout': 60})

        events = session_factory().client('events')
        result = events.list_rules(NamePrefix="maid-ec2-encrypted-vol")
        self.assert_items(
            result['Rules'][0],
            {"State": "ENABLED", 
             "Name": "maid-ec2-encrypted-vol"})

        self.assertEqual(
            json.loads(result['Rules'][0]['EventPattern']),
            {"source": ["aws.ec2"],
             "detail": {
                 "state": ["pending"]},
             "detail-type": ["EC2 Instance State-change Notification"]})
        mgr.remove(pl)

    def test_cwe_asg_instance(self):
        session_factory = self.replay_flight_data('test_cwe_asg', zdata=True)
        p = Policy({
            'resource': 'asg',
            'name': 'asg-spin-detector',
            'mode': {
                'type': 'asg-instance-state',
                'events': ['launch-failure']}
        }, Config.empty())
        pl = PolicyLambda(p)
        mgr = LambdaManager(session_factory)
        result = mgr.publish(pl, 'Dev', role=self.role)
        self.assert_items(
            result,
            {'FunctionName': 'maid-asg-spin-detector',
             'Handler': 'maid_policy.run',
             'MemorySize': 512,
             'Runtime': 'python2.7',
             'Timeout': 60})

        events = session_factory().client('events')
        result = events.list_rules(NamePrefix="maid-asg-spin-detector")
        self.assert_items(
            result['Rules'][0],
            {"State": "ENABLED", 
             "Name": "maid-asg-spin-detector"})

        self.assertEqual(
            json.loads(result['Rules'][0]['EventPattern']),
            {"source": ["aws.autoscaling"],
             "detail-type": ["EC2 Instance Launch Unsuccessful"]})
        mgr.remove(pl)
        
    def test_cwe_schedule(self):
        session_factory = self.replay_flight_data(
            'test_cwe_schedule', zdata=True)
        p = Policy({
            'resource': 'ec2',
            'name': 'periodic-ec2-checker',
            'mode': {
                'type': 'periodic',
                'schedule': 'rate(1 day)'
                }
        }, Config.empty())

        pl = PolicyLambda(p)
        mgr = LambdaManager(session_factory)
        result = mgr.publish(pl, 'Dev', role=self.role)
        self.assert_items(
            result,
            {'FunctionName': 'maid-periodic-ec2-checker',
             'Handler': 'maid_policy.run',
             'MemorySize': 512,
             'Runtime': 'python2.7',
             'Timeout': 60})        

        events = session_factory().client('events')
        result = events.list_rules(NamePrefix="maid-periodic-ec2-checker")
        self.assert_items(
            result['Rules'][0],
            {
                "State": "ENABLED", 
                "ScheduleExpression": "rate(1 day)", 
                "Name": "maid-periodic-ec2-checker"})
        mgr.remove(pl)


class PythonArchiveTest(unittest.TestCase):

    def test_archive_bytes(self):
        self.archive = custodian_archive()
        self.archive.create()
        self.addCleanup(self.archive.remove)
        self.archive.close()
        io = StringIO.StringIO(self.archive.get_bytes())
        reader = zipfile.ZipFile(io, mode='r')
        fileset = [n.filename for n in reader.filelist]
        self.assertTrue('c7n/__init__.py' in fileset)
        
    def test_archive_skip(self):
        self.archive = custodian_archive("*.pyc")
        self.archive.create()
        self.addCleanup(self.archive.remove)        
        self.archive.close()
        with open(self.archive.path) as fh:
            reader = zipfile.ZipFile(fh, mode='r')
            fileset = [n.filename for n in reader.filelist]
            for i in ['c7n/__init__.pyc',
                      'c7n/resources/s3.pyc',
                      'boto3/__init__.py']:
                self.assertFalse(i in fileset)
        

        
