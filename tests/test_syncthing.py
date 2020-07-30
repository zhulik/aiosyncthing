"""Tests for System."""

import aiosyncthing
import pytest
from expects import be_a, expect


@pytest.mark.asyncio
def test_database(syncthing_client):
    """Test."""
    expect(syncthing_client.database).to(be_a(aiosyncthing.Database))


@pytest.mark.asyncio
def test_system(syncthing_client):
    """Test."""
    expect(syncthing_client.system).to(be_a(aiosyncthing.System))


@pytest.mark.asyncio
def test_events(syncthing_client):
    """Test."""
    expect(syncthing_client.events).to(be_a(aiosyncthing.Events))
