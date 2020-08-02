"""Low level client for the Syncthing REST API."""

import asyncio

import aiohttp
from yarl import URL

from .exceptions import SyncthingError, UnauthorizedError


class API:
    """Low level client."""

    DEFAULT_TIMEOUT = 10

    def __init__(
        self,
        api_key,
        url="http://127.0.0.1:8384",
        timeout=DEFAULT_TIMEOUT,
        verify_ssl=True,
        loop=None,
        session=None,
    ):
        """Initialize the client."""
        self._api_key = api_key
        self._url = URL(url)
        self._timeout = aiohttp.ClientTimeout(total=timeout)
        self._verify_ssl = verify_ssl

        self._loop = loop or asyncio.get_event_loop()
        self._session = session
        self._close_session = False

        if self._session is None:
            self._session = aiohttp.ClientSession(loop=self._loop)
            self._close_session = True

    async def request(self, *args, **kwargs):
        """Perform request with error wrapping."""
        try:
            return await self.raw_request(*args, **kwargs)
        except aiohttp.client_exceptions.ClientResponseError as error:
            if error.status in [401, 403]:
                raise UnauthorizedError from error
            raise SyncthingError from error
        except Exception as error:
            raise SyncthingError from error

    async def raw_request(self, uri, params=None, data=None, method="GET"):
        """Perform request."""
        async with self._session.request(
            method,
            self._url.join(URL(uri)).update_query(params),
            json=data,
            headers={"Accept": "application/json", "X-API-Key": self._api_key,},
            timeout=self._timeout,
            verify_ssl=self._verify_ssl,
        ) as response:
            response.raise_for_status()
            if (
                "Content-Type" in response.headers
                and "application/json" in response.headers["Content-Type"]
            ):
                return await response.json()
            return await response.read()

    async def close(self):
        """Close the session."""
        if self._session and self._close_session:
            await self._session.close()
