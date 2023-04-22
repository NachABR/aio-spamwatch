"""Convenience imports"""
from .client import SpamWatchAPI
from .errors import (
    ForbiddenError,
    NotFoundError,
    SpamWatchError,
    TooManyRequestsError,
    UnauthorizedError,
)
from .types import Ban, Permission, Token

__version__ = "0.0.6"
__all__ = (
    "SpamWatchAPI",
    "Ban",
    "Permission",
    "Token",
    "ForbiddenError",
    "NotFoundError",
    "SpamWatchError",
    "TooManyRequestsError",
    "UnauthorizedError",
)
