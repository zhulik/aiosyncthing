import os

import aiohttp
import asyncio
import async_timeout

from yarl import URL

from .exceptions import SSLCertFileNotFound


class API:

    DEFAULT_TIMEOUT = 60

    def __init__(
        self,
        api_key,
        url="http://127.0.0.1:8384",
        timeout=DEFAULT_TIMEOUT,
        verify_ssl=True,
        ssl_cert_file=None,
        loop=None,
        session=None,
    ):
        self._api_key = api_key
        self._url = URL(url)
        self._timeout = timeout
        self._verify_ssl = verify_ssl
        self._ssl_cert_file = ssl_cert_file

        if ssl_cert_file:
            if not os.path.ifile(ssl_cert_file):
                raise SSLCertFileNotFound(
                    "ssl_cert_file does not exist at location, %s" % ssl_cert_file
                )

        self._loop = loop or asyncio.get_event_loop()
        self._session = session

        if self._session is None:
            self._session = aiohttp.ClientSession(loop=self._loop)
            self._close_session = True

    async def request(self, uri, data=None, method="GET"):
        with async_timeout.timeout(self._timeout):
            response = await self._session.request(
                method,
                self._url.join(URL(uri)),
                json=data,
                headers={"Accept": "application/json", "X-API-Key": self._api_key,},
            )
            response.raise_for_status()
            return await response.json()

    async def close(self):
        """Close open client session."""
        if self._session and self._close_session:
            await self._session.close()
