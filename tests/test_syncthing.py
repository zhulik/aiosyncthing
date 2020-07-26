"""Tests for Syncthing."""

import pytest
from aioresponses import aioresponses
from aiosyncthing import Syncthing


@pytest.mark.asyncio
async def test_ping():
    """Tests."""
    with aioresponses() as m:
        m.get("http://127.0.0.1:8384/rest/system/ping", payload={"ping": "pong"})

        async with Syncthing("token") as client:
            await client.system.ping()
