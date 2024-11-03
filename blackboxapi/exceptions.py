class APIError(Exception):
    """Custom exception for API errors."""
    pass

class DatabaseError(Exception):
    """Raised when there is an error with database operations."""
    pass
