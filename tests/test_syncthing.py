"""Tests for System."""

import pytest
from expects import be_a, equal, expect

import aiosyncthing


def test_url(syncthing_client):
    """Test."""
    expect(syncthing_client.url).to(equal("http://127.0.0.1:8384"))


def test_database(syncthing_client):
    """Test."""
    expect(syncthing_client.database).to(be_a(aiosyncthing.Database))


def test_system(syncthing_client):
    """Test."""
    expect(syncthing_client.system).to(be_a(aiosyncthing.System))


def test_events(syncthing_client):
    """Test."""
    expect(syncthing_client.events).to(be_a(aiosyncthing.Events))
