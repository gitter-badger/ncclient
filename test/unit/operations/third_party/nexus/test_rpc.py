import unittest
from mock import patch
from ncclient import manager
import ncclient.transport
from ncclient.operations.third_party.h3c.rpc import *


class TestRPC(unittest.TestCase):
    def setUp(self):
        self.device_handler = manager.make_device_handler({'name': 'nexus'})
    
    @patch('ncclient.operations.third_party.nexus.rpc.RPC._request')
    def test_saveConfig(self, mock_request):
        mock_request.return_value = 'nexus'
        excepted = 'nexus'
        session = ncclient.transport.SSHSession(self.device_handler)
        obj = ShowCLI(session, self.device_handler)
        cmds = 'show devices-name'
        actual = obj.request(cmds=cmds)
        self.assertEqual(excepted, actual)

        commands = [cmd for cmd in cmds]
        actual = obj.request(cmds=commands)
        self.assertEqual(excepted, actual)
