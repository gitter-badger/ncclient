import unittest, asyncio
from mock import patch, MagicMock
from ncclient import connect, operations
from ncclient import manager, asyncio_manager

class TestAsyncioManager(unittest.TestCase):

    def _mock_manager(self, mode):
        manager_params = {'timeout': 10,
                          'async_mode': False,
                          'raise_mode': operations.RaiseMode.ALL,
                          'huge_tree': True}
        if mode == 'async_mode':
            manager_params.update({'async_mode': True})
        else:
            manager_params.update({'async_mode': False})

        conn = connect.connect(host='hostname',
                               port=22,
                               username='user',
                               password='password',
                               timeout=30,
                               hostkey_verify=False,
                               allow_agent=False,
                               device_params={'name': 'junos'},
                               manager_params=manager_params)
        return conn

    @patch('ncclient.transport.SSHSession')
    def test_ssh(self, mock_ssh):
        m = MagicMock()
        mock_ssh.return_value = m
        conn = self._mock_manager('async_mode')

        self.assertIsInstance(conn, asyncio_manager.AsyncioManager)
        self.assertEqual(conn.session, m)
        self.assertEqual(conn.timeout, 10)
        self.assertEqual(conn.raise_mode, operations.RaiseMode.ALL)
        self.assertEqual(conn.async_mode, True)
        self.assertEqual(conn.huge_tree, True)

    @patch('ncclient.transport.SSHSession')
    def test_async_mode(self, mock_ssh):
        m = MagicMock()
        mock_ssh.return_value = m
        conn = self._mock_manager('async_mode')
        expected = [
                    '<rpc-reply><data><root>This is `get` operations</root></data></rpc-reply>',
                    '<rpc-reply><data><root>This is `get-config` operations</root></data></rpc-reply>',
                    '<rpc-reply><ok/></rpc-reply>',
                    '<rpc-reply><ok/></rpc-reply>',
                    '<rpc-reply><rpc-error><error-message>Request resource already locked</error-message></rpc-error></rpc-reply>'
                   ]

        loop = asyncio.get_event_loop()
        res = loop.run_until_complete(self.multi_operations(loop, conn))
        
        self.assertIsInstance(conn, .asyncio_manager.AsyncioManager)
        for r in range(len(expected)):
            self.assertEqual(expected[r], res[r])

    async def multi_operations(self, loop, conn):
        # `conn.get()` is equivalent to self.mock_get_operation(), and so on.
        req = [
               self.mock_get_operation(),
               self.mock_get_config_operation(),
               self.mock_edit_config_operation(),
               self.mock_lock_operation(),
               self.mock_duplicate_lock_operation(),
              ]
        tasks = [loop.create_task(r) for r in req]
        return await asyncio.gather(*tasks)

    async def mock_get_operation(self):
        # mock the `get` operation
        await asyncio.sleep(1)
        return '<rpc-reply><data><root>This is `get` operations</root></data></rpc-reply>'

    async def mock_get_config_operation(self):
        # mock the `get-config` operation
        await asyncio.sleep(1)
        return '<rpc-reply><data><root>This is `get-config` operations</root></data></rpc-reply>'

    async def mock_edit_config_operation(self):
        # mock the `edit-config` operation
        await asyncio.sleep(1)
        return '<rpc-reply><ok/></rpc-reply>'

    async def mock_lock_operation(self):
        # mock the `lock` operation
        await asyncio.sleep(1)
        return '<rpc-reply><ok/></rpc-reply>'

    async def mock_duplicate_lock_operation(self):
        # mock the `lock` operation again
        await asyncio.sleep(1)
        return '<rpc-reply><rpc-error><error-message>Request resource already locked</error-message></rpc-error></rpc-reply>'

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAsyncioManager)
    unittest.TextTestRunner(verbosity=2).run(suite)
