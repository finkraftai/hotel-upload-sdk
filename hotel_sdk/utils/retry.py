import time
from hotel_sdk.config.config import settings

def retry(operation, attempts=None, delay=None):
    """Retry operation with exponential backoff."""
    attempts = attempts or settings.max_retries
    delay = delay or settings.retry_backoff
    
    for attempt in range(attempts):
        try:
            return operation()
        except Exception as e:
            if attempt == attempts - 1:
                raise e
            # Exponential backoff: delay * (2 ** attempt)
            backoff = delay * (2 ** attempt)
            time.sleep(backoff)
