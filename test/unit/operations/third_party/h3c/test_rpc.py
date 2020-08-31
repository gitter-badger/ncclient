import unittest
from mock import patch
from ncclient import manager
import ncclient.transport
from ncclient.operations.third_party.h3c.rpc import *


class TestRPC(unittest.TestCase):
    def setUp(self):
        self.device_handler = manager.make_device_handler({'name': 'h3c'})
    
    @patch('ncclient.operations.third_party.h3c.rpc.RPC._request')
    def test_getBulk(self, mock_request):
        mock_request.return_value = 'h3c'
        excepted = 'h3c'
        session = ncclient.transport.SSHSession(self.device_handler)
        obj = GetBulk(session, self.device_handler)
        actual = obj.request()
        self.assertEqual(excepted, actual)

        filter = '<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"></filter>'
        actual = obj.request(filter=filter)
        self.assertEqual(excepted, actual)

    @patch('ncclient.operations.third_party.h3c.rpc.RPC._request')
    def test_getBulkConfig(self, mock_request):
        mock_request.return_value = 'h3c'
        excepted = 'h3c'
        session = ncclient.transport.SSHSession(self.device_handler)
        obj = GetBulkConfig(session, self.device_handler)
        source = 'devices-name'
        actual = obj.request(source=source)
        self.assertEqual(excepted, actual)
        
        filter='<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"></filter>'
        actual = obj.request(source=source, filter=filter)
        self.assertEqual(excepted, actual)
        
    @patch('ncclient.operations.third_party.h3c.rpc.RPC._request')
    def test_cLI(self, mock_request):
        mock_request.return_value = 'h3c'
        excepted = 'h3c'
        session = ncclient.transport.SSHSession(self.device_handler)
        obj = CLI(session, self.device_handler)
        command = '<get>devices-name</get>'
        actual = obj.request(command=command)
        self.assertEqual(excepted, actual)

    @patch('ncclient.operations.third_party.h3c.rpc.RPC._request')
    def test_action(self, mock_request):
        mock_request.return_value = 'h3c'
        excepted = 'h3c'
        session = ncclient.transport.SSHSession(self.device_handler)
        obj = Action(session, self.device_handler)
        action = '<get>devices-name</get>'
        actual = obj.request(action=action)
        self.assertEqual(excepted, actual)

    @patch('ncclient.operations.third_party.h3c.rpc.RPC._request')
    def test_save(self, mock_request):
        mock_request.return_value = 'h3c'
        excepted = 'h3c'
        session = ncclient.transport.SSHSession(self.device_handler)
        obj = Save(session, self.device_handler)
        actual = obj.request()
        self.assertEqual(excepted, actual)

        file = 'devices-name'
        actual = obj.request(file=file)
        self.assertEqual(excepted, actual)

    @patch('ncclient.operations.third_party.h3c.rpc.RPC._request')
    def test_load(self, mock_request):
        mock_request.return_value = 'h3c'
        excepted = 'h3c'
        session = ncclient.transport.SSHSession(self.device_handler)
        obj = Load(session, self.device_handler)
        actual = obj.request()
        self.assertEqual(excepted, actual)

        file = 'devices-name'
        actual = obj.request(file=file)
        self.assertEqual(excepted, actual)

    @patch('ncclient.operations.third_party.h3c.rpc.RPC._request')
    def test_rollback(self, mock_request):
        mock_request.return_value = 'h3c'
        excepted = 'h3c'
        session = ncclient.transport.SSHSession(self.device_handler)
        obj = Rollback(session, self.device_handler)
        actual = obj.request()
        self.assertEqual(excepted, actual)

        file = 'devices-name'
        actual = obj.request(file=file)
        self.assertEqual(excepted, actual)
