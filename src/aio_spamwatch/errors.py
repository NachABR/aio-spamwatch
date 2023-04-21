from datetime import datetime

from .types import Token


class SpamWatchError(Exception):
    pass


class APIError(SpamWatchError):
    def __init__(self, code: int, message: str, url: str) -> None:
        self.status_code = code
        self.error_message = message
        self.url = url
        message = f"API error ({code}): {message}. URL: {url}"
        super().__init__(message)


class UnauthorizedError(SpamWatchError):
    def __init__(self, message: str, url: str) -> None:
        super().__init__(f"Unauthorized: {message}. URL: {url}")


class NotFoundError(SpamWatchError):
    def __init__(self, message: str, url: str) -> None:
        super().__init__(f"Not found: {message}. URL: {url}")


class ForbiddenError(SpamWatchError):
    def __init__(self, token: Token, url: str) -> None:
        super().__init__(
            f"Insufficient permission level ({token.permission}). URL: {url}"
        )


class TooManyRequestsError(SpamWatchError):
    def __init__(self, method: str, retry_after: int, url: str) -> None:
        retry_after_delta = datetime.fromtimestamp(retry_after) - datetime.now()
        super().__init__(
            f"Too many requests for method {method}. "
            f"Retry after {retry_after_delta.total_seconds():.1f} seconds. URL: {url}"
        )
