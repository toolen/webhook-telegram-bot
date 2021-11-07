"""This file contains application exception classes."""


class RepositoryBotException(Exception):
    """Base application exception."""

    pass


class DatabaseUnconfiguredException(RepositoryBotException):
    """Exception for unconfigured database."""

    pass
