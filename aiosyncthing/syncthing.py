"""Entrypoint for the Syncthing REST API."""

from .api import API
from .system import System


class Syncthing:
    """Entrypoint class."""

    def __init__(self, *args, **kwargs):
        """Initialize the client."""
        self._api = API(*args, **kwargs)

        self._system = System(self._api)

    @property
    def system(self):
        """Get system api."""
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
