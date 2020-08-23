"""Entrypoint for the database Syncthing REST API."""

import aiohttp

from .exceptions import SyncthingError, UnknownFolderError


class Database:
    """Entrypoint class for the database Syncthing REST API."""

    def __init__(self, api):
        """Initialize the client."""
        self._api = api

    async def status(self, folder_id):
        """Get folder status."""
        try:
            return await self._api.request(
                "rest/db/status", params={"folder": folder_id}
            )
        except SyncthingError as error:
            cause = error.__cause__
            if isinstance(cause, aiohttp.client_exceptions.ClientResponseError):
                if cause.status == 404:  # pylint: disable=no-member
                    raise UnknownFolderError
            raise error
