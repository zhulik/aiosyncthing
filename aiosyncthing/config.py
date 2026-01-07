"""Entrypoint for the config Syncthing REST API."""

class Config:
    """Entrypoint class for the config Syncthing REST API."""

    def __init__(self, api):
        """Initialize the client."""
        self._api = api

    async def config(self):
        """Get server config."""
        return await self._api.request("rest/config")

    async def folders(self, folder_id=None):
        """Get folders config."""
        return await self._api.request(
            "rest/config/folders" if folder_id is None else f"rest/config/folders/{folder_id}"
        )

    async def devices(self, device_id=None):
        """Get devices config."""
        return await self._api.request(
            "rest/config/devices" if device_id is None else f"rest/config/devices/{device_id}"
        )
