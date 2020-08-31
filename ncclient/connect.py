import sys
from ncclient import manager

if sys.version_info.major > 2:
    from ncclient import asyncio_manager

def connect(*args, **kwds):
    # use sync_mode by default
    manager_params = kwds.get("manager_params", {"async_mode": False})
    if manager_params.get("async_mode") is True and sys.version_info.major > 2:
        return asyncio_manager.async_connect(*args, **kwds)
    else:
        return manager.sync_connect(*args, **kwds)

