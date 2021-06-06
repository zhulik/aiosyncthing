"""Test helper functions."""

import pytest
from aioresponses import aioresponses as responses

from aiosyncthing import Syncthing


@pytest.fixture
async def syncthing_client():
    """Yield a Syncthing client."""
    async with Syncthing("token") as client:
        yield client


@pytest.fixture
def aioresponses():
    """Yield aioresponses."""
    with responses() as m:
        yield m
