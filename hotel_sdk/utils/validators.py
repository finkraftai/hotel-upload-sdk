"""
URL validation utilities - accepts all HTTP/HTTPS URLs
"""
from urllib.parse import urlparse


def validate_cloud_url(url: str) -> bool:
    """
    Accepts any valid HTTP/HTTPS URL.
    Removed cloud provider restrictions to support all storage providers.
    
    Args:
        url: URL string to validate
        
    Returns:
        bool: True if valid HTTP/HTTPS URL with domain and path
    """
    if not url:
        return False

    try:
        parsed = urlparse(url)
    except Exception:
        return False

    scheme = parsed.scheme.lower()
    
    # Only check for valid HTTP/HTTPS protocol
    if scheme not in ("http", "https"):
        return False
    
    # Must have a domain
    if not parsed.netloc:
        return False
    
    # Must have a path
    if not parsed.path or parsed.path == "/":
        return False

    return True