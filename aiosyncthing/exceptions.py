"""Exceptions for the Syncthing REST API."""


class SyncthingError(Exception):
    """Base Syncthing Exception class."""


class PingError(SyncthingError):
    """When the server does not respond to ping."""


class UnauthorizedError(SyncthingError):
    """When the server does not accept the API token."""


class NotFoundError(SyncthingError):
    """When the server responds with 404."""


class UnknownFolderError(NotFoundError):
    """When the server cannot find a folder by id."""


class UnknownDeviceError(NotFoundError):
    """When the server cannot find a device by id."""
