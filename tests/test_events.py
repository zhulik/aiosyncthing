"""Tests for System."""

import asyncio

import pytest
from aiosyncthing.exceptions import SyncthingError
from expects import be_false, be_true, equal, expect

# pylint: disable=redefined-outer-name


@pytest.fixture
def events(syncthing_client):
    """Return database namespace client."""
    return syncthing_client.events


@pytest.mark.asyncio
async def test_listen_happy(events, aioresponses):
    """Test happy path."""
    aioresponses.get(
        "http://127.0.0.1:8384/rest/events?since=0", payload=[{"id": 123}],
    )
    aioresponses.get(
        "http://127.0.0.1:8384/rest/events?since=123", payload=[{"id": 124}],
    )
    async for event in events.listen():
        if event["id"] == 123:
            expect(events.running).to(be_true)
            expect(events.last_seen_id).to(equal(0))
        if event["id"] == 124:
            expect(events.last_seen_id).to(equal(123))
            events.stop()
    expect(events.last_seen_id).to(equal(124))
    expect(events.running).to(be_false)


@pytest.mark.asyncio
async def test_listen_error(events, mocker):
    """Test error path."""

    def mock_load(*args):
        raise Exception

    mocker.patch(
        # Dataset is in slow.py, but imported to main.py
        "aiosyncthing.API.raw_request",
        mock_load,
    )
    with pytest.raises(SyncthingError):
        async for _ in events.listen():
            pass


@pytest.mark.asyncio
async def test_listen_cancel(events, mocker):
    """Test error path."""

    def mock_load(*args, **kwargs):
        raise asyncio.CancelledError

    mocker.patch(
        # Dataset is in slow.py, but imported to main.py
        "aiosyncthing.API.raw_request",
        mock_load,
    )
    async for _ in events.listen():
        pass
