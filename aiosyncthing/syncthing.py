"""Entrypoint for the Syncthing REST API."""

from .api import API
from .database import Database
from .events import Events
from .system import System
from .config import Config

class Syncthing:
    """Entrypoint class."""

    def __init__(self, *args, **kwargs):
        """Initialize the client."""
        self._api = API(*args, **kwargs)

        self._system = System(self._api)
        self._config = Config(self._api)
        self._database = Database(self._api)
        self._events = Events(self._api)

    @property
    def url(self):
        """Get URL."""
        return self._api.url

    @property
    def system(self):
        """Get system api."""
        return self._system

    @property
    def config(self):
        """Get config api."""
        return self._config

    @property
    def database(self):
        """Get database api."""
        return self._database

    @property
    def events(self):
        """Get events api."""
        return self._events

    async def close(self):
        """Close open client session."""
        await self._api.close()

    async def __aenter__(self):
        """Async enter."""
        return self

    async def __aexit__(self, *exc_info):
        """Async exit."""
        await self.close()
