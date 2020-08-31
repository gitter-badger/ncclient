# Copyright 2015 Austin Cormier
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import functools
import logging, sys
from ncclient import manager
if sys.version_info.major > 2:
    import asyncio

logger = logging.getLogger('ncclient.asyncio_manager')


def add_rpc_asyncio_event_support(rpc, loop):
    """ Patch the RPC class in order to use an asyncio.Event
    Create an asyncio.Event which is bound to the event loop. Patch the
    existing RPC._event.set so that it invokes the set() (thread-safely)
    on the newly created asyncio event.
    The only two methods that set the RPC._event attribute are
    RPC.deliver_reply and RPC.deliver_error.  After patching
    when they attempt to set the Event, our wait() coroutine will awaken.
    Arguments:
        rpc - An RPC instance
        loop - The asyncio loop to create the asyncio.Event on
    Returns:
        The created asyncio.Event
    """
    event = asyncio.Event(loop=loop)

    def set_asyncio_event():
        logger.debug("Setting asyncio.Event flag")
        loop.call_soon_threadsafe(event.set)

    rpc._event.set = set_asyncio_event

    return event

class AsyncioManager(manager.Manager):
    """ This class provides an ayncio interface which is subclassed from ncclient.Manager
    This class attempts to take advantage of the ncclient async_mode features to
    provide a complete asyncio interface which maps directory to the existing
    Manager interface.  All blocking operations are wrapped in coroutines.
    """
    def __init__(self, session, device_handler=None, manager_params=None, loop=None):
        """ Create a AyncIOManager instanace
        Arguments:
            session - The connected SSHSession instance
            device_handler - DeviceHandler instance
            manager_params - Manager parameters
            loop - asyncio.BaseEventLoop instance
        """
        super().__init__(
            session=session,
            device_handler=device_handler,
            manager_params=manager_params,
        )

        self._loop = loop if loop is not None else asyncio.get_event_loop()

    async def execute(self, cls, *args, **kwargs):
        """ Execute the netconf operation
        All Manager operations are wrappers around execute
        (see manager.py:OpExecutor()). This follows the same approach
        as request when creating the request (the cls() call).
        After creating the request object we patch the RPC instance (rpc.py) so
        that the event uses the asyncio.Event intead of Threading.Event.
        This allows us to use the asyncio.Event.wait() coroutine to wait until
        the request is completed.
        The only two methods that then interact with the RPC _event attribute is
        RPC.deliver_event and RPC.deliver_error.
        Arguments:
            cls - The RPC operation subclass (see manager.py:OPERATIONS)
            *args - Positional arguments to pass into RPC.request
            **kwargs - Keyword arguments to pass into RPC.request
        """
        rpc = cls(self._session,
                  device_handler=self._device_handler,
                  async_mode=self._async_mode,
                  timeout=self._timeout,
                  raise_mode=self._raise_mode,
                  huge_tree=self._huge_tree)

        event = add_rpc_asyncio_event_support(rpc, self._loop)

        # Start the request
        rpc.request(*args, **kwargs)

        # Wrap the Event.wait() coroutine in a wait_for() to give
        # the ability to time-out if request doesn't complete in a reasonable
        # amount of time.
        await asyncio.wait_for(
                event.wait(),
                timeout=self._timeout,
                loop=self._loop,
                )

        # If an error was set, then re-raise so the exeception will
        # propogate up the stack.
        if rpc._error is not None:
            raise rpc._error

        return rpc._reply


async def asyncio_connect(loop=None, *args, **kwargs):
    """ Wraps synchronous ncclient.manager.connect within a coroutine
    Once the Manager.connect() returns with a Manager instance, create
    an equivelent AsyncioManager instance with the now connected session.
    Arguments:
        loop - asyncio.BaseEventLoop instance
        *args - Positional arguments into Manager.connect
        **kwargs - Keyword arguments into Manager.connect
     Returns:
        An AsyncioManager instance
    """
    manager_params = manager._extract_manager_params(kwargs)
    loop = loop if loop is not None else asyncio.get_event_loop()
    mgr = await loop.run_in_executor(
        executor=None,
        func=functools.partial(manager.sync_connect, *args, **kwargs))

    return AsyncioManager(mgr._session,
                          mgr._device_handler,
                          manager_params=manager_params,
                          loop=loop)

def async_connect(*args, **kwds):
    loop = asyncio.get_event_loop()
    task = loop.create_task(asyncio_connect(loop=loop, *args, **kwds))
    try:
        return loop.run_until_complete(task)
    except Exception as e:
        loop.close()
        raise

