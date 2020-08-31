import unittest
from mock import patch
from ncclient import manager
import ncclient.transport
from ncclient.operations.third_party.alu.rpc import *


class TestRPC(unittest.TestCase):
    def setUp(self):
        self.device_handler = manager.make_device_handler({'name': 'alu'})
    
    @patch('ncclient.operations.third_party.alu.rpc.RPC._request')
    def test_showCLI(self, mock_request):
        mock_request.return_value = 'alu'
        excepted = 'alu'
        session = ncclient.transport.SSHSession(self.device_handler)
        obj = ShowCLI(session, self.device_handler)
        command = 'show system users'
        actual = obj.request(command=command)
        self.assertEqual(excepted, actual)

    @patch('ncclient.operations.third_party.alu.rpc.RPC._request')
    def test_getConfiguration(self, mock_request):
        mock_request.return_value = 'alu'
        excepted = 'alu'
        session = ncclient.transport.SSHSession(self.device_handler)
        obj = GetConfiguration(session, self.device_handler)
        content = 'xml'
        actual = obj.request(content=content)
        self.assertEqual(excepted, actual)

        filter = '<get>device-name</get>'
        actual = obj.request(content=content, filter=filter)
        self.assertEqual(excepted, actual)

        content = 'cli'
        actual = obj.request(content=content, filter=filter)
        self.assertEqual(excepted, actual)
        
        detail = True
        actual = obj.request(content=content, filter=filter, detail=detail)
        self.assertEqual(excepted, actual)
        
        content = ''
        actual = obj.request(content=content, filter=filter, detail=detail)
        self.assertEqual(excepted, actual)
        
    @patch('ncclient.operations.third_party.alu.rpc.RPC._request')
    def test_loadConfiguration(self, mock_request):
        mock_request.return_value = 'alu'
        excepted = 'alu'
        session = ncclient.transport.SSHSession(self.device_handler)
        obj = LoadConfiguration(session, self.device_handler)
        default_operation = ''
        format = 'xml'
        actual = obj.request(format=format, default_operation=default_operation)
        self.assertEqual(excepted, actual)

        default_operation = 'get'
        actual=obj.request(format=format, default_operation=default_operation)
        self.assertEqual(excepted, actual)

        config = new_ele('device-name')
        actual=obj.request(format=format, default_operation=default_operation, config=config)
        self.assertEqual(excepted, actual)

        config = 'device-name'
        format = 'cli'
        actual=obj.request(format=format, default_operation=default_operation, config=config)
        self.assertEqual(excepted, actual)
        
        default_operation = ''
        actual=obj.request(format=format, default_operation=default_operation, config=config)
        self.assertEqual(excepted, actual)
