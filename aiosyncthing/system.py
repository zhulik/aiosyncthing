"""Entrypoint for the system Syncthing REST API."""

import aiohttp

from .exceptions import PingError, SyncthingError, UnknownDevice


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

    async def version(self):
        """Get server version."""
        return await self._api.request("/rest/system/version")

    async def pause(self, device_id=None):
        """Pause synchronization."""
        params = {}
        if device_id is not None:
            params["device"] = device_id
        try:
            await self._api.request("/rest/system/pause", method="POST", params=params)
        except SyncthingError as error:
            cause = error.__cause__
            if isinstance(cause, aiohttp.client_exceptions.ClientResponseError):
                if cause.status == 404:  # pylint: disable=no-member
                    raise UnknownDevice
            raise error

    async def resume(self, device_id=None):
        """Resume synchronization."""
        params = {}
        if device_id is not None:
            params["device"] = device_id
        try:
            await self._api.request("/rest/system/resume", method="POST", params=params)
        except SyncthingError as error:
            cause = error.__cause__
            if isinstance(cause, aiohttp.client_exceptions.ClientResponseError):
                if cause.status == 404:  # pylint: disable=no-member
                    raise UnknownDevice
            raise error
