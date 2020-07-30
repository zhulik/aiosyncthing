"""Tests for System."""

import pytest
from aiosyncthing.exceptions import PingError, SyncthingError
from expects import be_none, equal, expect

# pylint: disable=redefined-outer-name


@pytest.fixture
def system(syncthing_client):
    """Return system namespace client."""
    return syncthing_client.system


@pytest.mark.asyncio
async def test_ping_happy(system, aioresponses):
    """Test happy path."""
    aioresponses.get("http://127.0.0.1:8384/rest/system/ping", payload={"ping": "pong"})
    expect(await system.ping()).to(be_none)


@pytest.mark.asyncio
async def test_ping_error(system, aioresponses):
    """Test error."""
    aioresponses.get("http://127.0.0.1:8384/rest/system/ping", status=500)

    with pytest.raises(PingError):
        await system.ping()


@pytest.mark.asyncio
async def test_config_happy(system, aioresponses):
    """Test happy path."""
    aioresponses.get(
        "http://127.0.0.1:8384/rest/system/config",
        payload={"version": 31, "folders": []},
    )
    expect(await system.config()).to(equal({"version": 31, "folders": []}))


@pytest.mark.asyncio
async def test_config_error(system, aioresponses):
    """Test happy path."""
    aioresponses.get("http://127.0.0.1:8384/rest/system/config", status=500)
    with pytest.raises(SyncthingError):
        await system.ping()


@pytest.mark.asyncio
async def test_status_happy(system, aioresponses):
    """Test happy path."""
    aioresponses.get(
        "http://127.0.0.1:8384/rest/system/status",
        payload={"alloc": 147081968, "connectionServiceStatus": {}},
    )
    expect(await system.status()).to(
        equal({"alloc": 147081968, "connectionServiceStatus": {}})
    )


@pytest.mark.asyncio
async def test_system_error(system, aioresponses):
    """Test happy path."""
    aioresponses.get("http://127.0.0.1:8384/rest/system/status", status=500)
    with pytest.raises(SyncthingError):
        await system.status()
