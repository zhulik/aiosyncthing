"""Entrypoint for the events Syncthing REST API."""

import asyncio

from .exceptions import SyncthingError


class Events:
    """Entrypoint class for the events Syncthing REST API."""

    def __init__(self, api):
        """Initialize the client."""
        self._last_seen_id = 0
        self._api = api

    @property
    def last_seen_id(self):
        """Get last seen event's id."""
        return self._last_seen_id

    async def listen(self):
        """Listen to events."""
        self._last_seen_id = 0

        while True:
            try:
                events = await self._api.raw_request(
                    "/rest/events", params={"since": self._last_seen_id}
                )
                for event in events:
                    yield event
                self._last_seen_id = events[-1]["id"]
            except asyncio.TimeoutError:
                continue
            except asyncio.CancelledError:
                return
            except Exception as error:
                raise SyncthingError from error
