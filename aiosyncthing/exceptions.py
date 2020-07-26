"""Exceptions for the Syncthing REST API."""


class SyncthingError(Exception):
    """Base Syncthing Exception class."""


class PingError(SyncthingError):
    """When server does not respond to ping."""
