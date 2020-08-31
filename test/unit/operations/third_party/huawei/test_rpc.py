import unittest
from mock import patch
from ncclient import manager
import ncclient.transport
from ncclient.operations.third_party.h3c.rpc import *


class TestRPC(unittest.TestCase):
    def setUp(self):
        self.device_handler = manager.make_device_handler({'name': 'huawei'})
     
    @patch('ncclient.operations.third_party.huawei.rpc.RPC._request')
    def test_cLI(self, mock_request):
        mock_request.return_value = 'huawei'
        excepted = 'huawei'
        session = ncclient.transport.SSHSession(self.device_handler)
        obj = CLI(session, self.device_handler)
        command = '<get>devices-name</get>'
        actual = obj.request(command=command)
        self.assertEqual(excepted, actual)

    @patch('ncclient.operations.third_party.huawei.rpc.RPC._request')
    def test_action(self, mock_request):
        mock_request.return_value = 'huawei'
        excepted = 'huawei'
        session = ncclient.transport.SSHSession(self.device_handler)
        obj = Action(session, self.device_handler)
        action = '<get>devices-name</get>'
        actual = obj.request(action=action)
        self.assertEqual(excepted, actual)

