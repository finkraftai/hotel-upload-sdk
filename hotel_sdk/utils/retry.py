import time
from hotel_sdk.config.config import settings

def retry(operation, attempts=None, delay=None, ignored_exceptions=None):
    """
    Retry operation with exponential backoff.
    
    Args:
        operation: Callable to execute
        attempts: Max number of attempts
        delay: Initial delay in seconds
        ignored_exceptions: Tuple of exceptions to NOT retry (permanent errors)
    """
    attempts = attempts or settings.max_retries
    delay = delay or settings.retry_backoff
    
    for attempt in range(attempts):
        try:
            return operation()
        except Exception as e:
            # If it's a permanent error (like DuplicateError), don't retry
            if ignored_exceptions and isinstance(e, ignored_exceptions):
                raise e
                
            if attempt == attempts - 1:
                raise e
                
            backoff = delay * (2 ** attempt)
            time.sleep(backoff)