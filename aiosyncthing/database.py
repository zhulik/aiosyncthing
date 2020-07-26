"""Entrypoint for the database Syncthing REST API."""


class Database:
    """Entrypoint class for the database Syncthing REST API."""

    def __init__(self, api):
        """Initialize the client."""
        self._api = api

    async def status(self, folder_id):
        """Get folder status."""
        return await self._api.request("/rest/db/status", params={"folder": folder_id})
