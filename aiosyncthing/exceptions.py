class SyncthingError(Exception):
    """Base Syncthing Exception class."""


class SSLCertFileNotFound(SyncthingError):
    """When ssl cert file is not found."""


class PingError(SyncthingError):
    """When server does not respond to ping."""
