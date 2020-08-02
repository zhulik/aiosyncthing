"""Tests for System."""

import pytest
from aiosyncthing.exceptions import UnknownFolderError
from expects import equal, expect

# pylint: disable=redefined-outer-name


@pytest.fixture
def database(syncthing_client):
    """Return database namespace client."""
    return syncthing_client.database


@pytest.mark.asyncio
async def test_status_happy(database, aioresponses):
    """Test happy path."""
    aioresponses.get(
        "http://127.0.0.1:8384/rest/db/status?folder=folder-id",
        payload={"errors": 0, "globalBytes": 0},
    )
    expect(await database.status("folder-id")).to(
        equal({"errors": 0, "globalBytes": 0})
    )


@pytest.mark.asyncio
async def test_status_unknown_folder(database, aioresponses):
    """Test happy path."""
    aioresponses.get(
        "http://127.0.0.1:8384/rest/db/status?folder=folder-id", status=404
    )
    with pytest.raises(UnknownFolderError):
        await database.status("folder-id")
