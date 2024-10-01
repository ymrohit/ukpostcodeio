
class PostcodesIOError(Exception):
    """Base exception for PostcodesIO errors."""
    pass


class PostcodesIOHTTPError(PostcodesIOError):
    """Exception for HTTP errors."""

    def __init__(self, status_code: int, error_message: str):
        self.status_code = status_code
        self.error_message = error_message
        super().__init__(f"HTTP {status_code}: {error_message}")


class PostcodesIOTimeoutError(PostcodesIOError):
    """Exception for timeout errors."""

    def __init__(self, timeout: int):
        self.timeout = timeout
        super().__init__(f"Request timed out after {timeout} seconds.")


class PostcodesIOValidationError(PostcodesIOError):
    """Exception for validation errors."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class PostcodesIONetworkError(PostcodesIOError):
    """Exception for network-related errors."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
