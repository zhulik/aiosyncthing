"""Entrypoint for the system Syncthing REST API."""

from .exceptions import PingError


class System:
    """Entrypoint class for the system Syncthing REST API."""

    def __init__(self, api):
        """Initialize the client."""
        self._api = api

    async def ping(self):
        """Initialize the client."""
        try:
            result = await self._api.request("/rest/system/ping")
            if (
                not isinstance(result, dict)
                or "ping" not in result
                or result["ping"] != "pong"
            ):
                raise PingError
        except Exception as error:
            raise PingError from error
