from .api import API
from .system import System


class Syncthing:
    def __init__(self, *args, **kwargs):
        self._api = API(*args, **kwargs)

        self._system = System(self._api)

    @property
    def system(self):
        return self._system

    async def close(self):
        """Close open client session."""
        await self._api.close()

    async def __aenter__(self):
        """Async enter."""
        return self

    async def __aexit__(self, *exc_info):
        """Async exit."""
        await self.close()
