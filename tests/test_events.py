"""Tests for System."""

import asyncio

import pytest
import pytest_asyncio
from expects import be_false, be_true, equal, expect

from aiosyncthing.api import API
from aiosyncthing.exceptions import SyncthingError

# pylint: disable=redefined-outer-name


@pytest_asyncio.fixture
def events(syncthing_client):
    """Return database namespace client."""
    return syncthing_client.events


@pytest.mark.asyncio
async def test_listen_happy(events, aioresponses):
    """Test happy path."""
    aioresponses.get(
        "http://127.0.0.1:8384/rest/events?since=0",
        payload=[{"id": 123}],
    )
    aioresponses.get(
        "http://127.0.0.1:8384/rest/events?since=123",
        payload=[{"id": 124}],
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


@pytest.mark.asyncio
async def test_listen_with_only_current(events, aioresponses):
    """Test listen for only current events."""
    aioresponses.get(
        "http://127.0.0.1:8384/rest/events?since=0",
        payload=[{"id": 123}],
    )
    aioresponses.get(
        "http://127.0.0.1:8384/rest/events?since=123",
        payload=[{"id": 124}],
    )
    ait = aiter(events.listen(since=123, listen=False))
    event = await anext(ait)
    expect(events.last_seen_id).to(equal(123))
    expect(event["id"]).to(equal(124))
    with pytest.raises(StopAsyncIteration):
        await anext(ait)

    expect(events.last_seen_id).to(equal(124))
    expect(events.running).to(be_false)


@pytest.mark.asyncio
async def test_listen_timeout_then_recover(events, mocker):
    """Test timeout handling followed by recovery."""
    calls = 0

    async def mock_load(*args, **kwargs):
        nonlocal calls
        calls += 1
        if calls < 5:
            raise asyncio.TimeoutError
        return [{"id": 123}]

    mocker.patch(
        "aiosyncthing.API.raw_request",
        mock_load,
    )

    async for event in events.listen():
        expect(event["id"]).to(equal(123))
        events.stop()

    expect(calls).to(equal(5))


@pytest.mark.asyncio
async def test_listen_timeout_exits_when_not_running(events, mocker):
    """Test timeout handling for current events."""
    calls = 0

    async def mock_load(*args, **kwargs):
        nonlocal calls
        calls += 1
        if calls == 1:
            raise asyncio.TimeoutError
        return [{"id": 123}]

    mocker.patch(
        "aiosyncthing.API.raw_request",
        mock_load,
    )

    ait = aiter(events.listen(listen=False))
    with pytest.raises(StopAsyncIteration):
        await anext(ait)

    expect(calls).to(equal(1))


@pytest.mark.asyncio
async def test_listen_timeout_exits_when_stop(events, mocker):
    """Test stop function during continous timeouts."""
    loop_started = asyncio.Event()

    async def mock_load(*args, **kwargs):
        loop_started.set()
        await asyncio.sleep(API.DEFAULT_TIMEOUT)
        raise asyncio.TimeoutError

    mocker.patch(
        "aiosyncthing.API.raw_request",
        mock_load,
    )

    async def consume():
        async for _ in events.listen():
            pass

    task = asyncio.create_task(consume())
    await loop_started.wait()
    events.stop()

    await asyncio.wait_for(task, timeout=1)

    expect(events.running).to(equal(False))
