"""Tests for Config."""

import pytest
import pytest_asyncio
from expects import equal, expect

from aiosyncthing import Syncthing
from aiosyncthing.exceptions import NotFoundError, SyncthingError

# pylint: disable=redefined-outer-name


@pytest_asyncio.fixture
def config(syncthing_client):
    """Return config namespace client."""
    return syncthing_client.config


@pytest.mark.asyncio
async def test_config_happy(config, aioresponses):
    """Test happy path for config retrieval."""
    aioresponses.get(
        "http://127.0.0.1:8384/rest/config",
        payload={"version": 31, "folders": [], "devices": []},
    )
    expect(await config.config()).to(equal({"version": 31, "folders": [], "devices": []}))


@pytest.mark.asyncio
async def test_config_with_syncthing_namespaced(aioresponses):
    """Test config path when client is namespaced."""
    aioresponses.get("http://127.0.0.1:8384/syncthing/rest/config", payload={"version": 31})

    async with Syncthing("token", "http://127.0.0.1:8384/syncthing/") as client:
        expect(await client.config.config()).to(equal({"version": 31}))


@pytest.mark.asyncio
async def test_config_error(config, aioresponses):
    """Test error path for config retrieval."""
    aioresponses.get("http://127.0.0.1:8384/rest/config", status=500)
    with pytest.raises(SyncthingError):
        await config.config()


@pytest.mark.asyncio
async def test_folders_happy(config, aioresponses):
    """Test happy path for folders list."""
    aioresponses.get(
        "http://127.0.0.1:8384/rest/config/folders",
        payload=[{"id": "folder1"}],
    )
    expect(await config.folders()).to(equal([{"id": "folder1"}]))


@pytest.mark.asyncio
async def test_folder_by_id_happy(config, aioresponses):
    """Test happy path for single folder retrieval."""
    aioresponses.get("http://127.0.0.1:8384/rest/config/folders/folder_id", payload={"id": "folder_id"})
    expect(await config.folders("folder_id")).to(equal({"id": "folder_id"}))


@pytest.mark.asyncio
async def test_folder_by_id_not_found(config, aioresponses):
    """Test not found for folder by id."""
    aioresponses.get("http://127.0.0.1:8384/rest/config/folders/folder_id", status=404)
    with pytest.raises(NotFoundError):
        await config.folders("folder_id")


@pytest.mark.asyncio
async def test_devices_happy(config, aioresponses):
    """Test happy path for devices list."""
    aioresponses.get(
        "http://127.0.0.1:8384/rest/config/devices",
        payload=[{"id": "device1"}],
    )
    expect(await config.devices()).to(equal([{"id": "device1"}]))


@pytest.mark.asyncio
async def test_device_by_id_happy(config, aioresponses):
    """Test happy path for single device retrieval."""
    aioresponses.get("http://127.0.0.1:8384/rest/config/devices/device_id", payload={"id": "device_id"})
    expect(await config.devices("device_id")).to(equal({"id": "device_id"}))


@pytest.mark.asyncio
async def test_device_by_id_not_found(config, aioresponses):
    """Test not found for device by id."""
    aioresponses.get("http://127.0.0.1:8384/rest/config/devices/device_id", status=404)
    with pytest.raises(NotFoundError):
        await config.devices("device_id")
