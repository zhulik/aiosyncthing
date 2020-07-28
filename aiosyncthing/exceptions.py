"""Exceptions for the Syncthing REST API."""


class SyncthingError(Exception):
    """Base Syncthing Exception class."""


class PingError(SyncthingError):
    """When the server does not respond to ping."""


class UnauthorizedError(SyncthingError):
    """When the server does not accept the API token."""
