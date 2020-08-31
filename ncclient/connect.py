import sys
from ncclient import manager

if sys.version_info.major > 2:
    from ncclient import asyncio_manager

def connect(*args, **kwds):
    """
    A common API for connecting to server and getting manager instance

    Arguments:

        *args - Position arguments into Manager.sync_connect or
                AsyncioManager.async_connect

        **kwds - Keyword arguments into Manager.sync_connect or
                 AsyncioManager.async_connect

    Returns:

        A Manager or AsyncioManager instance depends on async_mode
    """
    manager_params = kwds.get("manager_params", {"async_mode": False})
    if manager_params.get("async_mode") is True and sys.version_info.major > 2:
        return asyncio_manager.async_connect(*args, **kwds)
    else:
        return manager.sync_connect(*args, **kwds)

