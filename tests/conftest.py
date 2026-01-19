"""Test helper functions."""

import pytest_asyncio
from aioresponses import aioresponses as responses

from aiosyncthing import Syncthing


@pytest_asyncio.fixture
async def syncthing_client():
    """Yield a Syncthing client."""
    async with Syncthing("token") as client:
        yield client


@pytest_asyncio.fixture
def aioresponses():
    """Yield aioresponses."""
    with responses() as m:
        yield m
