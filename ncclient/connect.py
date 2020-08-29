import asyncio, platform
from ncclient import manager

if platform.python_version() > "3.5":
    from ncclient import asyncio_manager

def connect(*args, **kwds):
    # use sync_mode by default
    manager_params = kwds.get("manager_params", {"async_mode": False})
    if manager_params.get("async_mode") is True:
        if platform.python_version() < '3.5':
            raise ValueError("python version must be later than 3.5 when async is used")
        return asyncio_manager.async_connect(*args, **kwds)
    else:
        return manager.sync_connect(*args, **kwds)

