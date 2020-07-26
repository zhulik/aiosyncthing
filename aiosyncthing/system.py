"""Entrypoint for the system Syncthing REST API."""

from .exceptions import PingError


class System:
    """Entrypoint class for the system Syncthing REST API."""

    def __init__(self, api):
        """Initialize the client."""
        self._api = api

    async def ping(self):
        """Check server availability."""
        try:
            result = await self._api.raw_request("/rest/system/ping")
            if (
                not isinstance(result, dict)
                or "ping" not in result
                or result["ping"] != "pong"
            ):
                raise PingError
        except Exception as error:
            raise PingError from error

    async def config(self):
        """Get server config."""
        return await self._api.request("/rest/system/config")

    async def status(self):
        """Get server config."""
        return await self._api.request("/rest/system/status")
