"""Custom exceptions for hotel SDK."""


class ValidationError(Exception):
    """Raised when input validation fails (e.g., invalid URL format)."""
    pass


class DuplicateError(Exception):
    """Raised when source_id hash already exists in database."""
    pass


class UploadFailed(Exception):
    """Raised when insert operation fails or DB returns NULL."""
    pass


class ConnectionError(Exception):
    """Raised when database connection issues occur."""
    pass