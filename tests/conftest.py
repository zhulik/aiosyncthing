"""Test helper functions."""

import pytest
from aioresponses import aioresponses as responses
from aiosyncthing import Syncthing


@pytest.fixture
async def syncthing_client():
    """Yield a Syncthing client."""
    client = Syncthing("token")
    yield client
    await client.close()


@pytest.fixture
def aioresponses():
    """Yield aioresponses."""
    with responses() as m:
        yield m
