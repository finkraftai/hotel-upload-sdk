# from urllib.parse import urlparse

# def validate_cloud_url(url: str) -> bool:
#     """
#     Accepts AWS S3 / CloudFront / Azure Blob URLs.
#     """
#     parsed = urlparse(url)

#     if not parsed.scheme.startswith("http"):
#         return False

#     # Minimal checks
#     if any(x in parsed.netloc for x in ["amazonaws.com", "cloudfront.net", "blob.core.windows.net"]):
#         return True

#     return False


from urllib.parse import urlparse

def validate_cloud_url(url: str) -> bool:
    """
    Accepts AWS S3 (standard + regional), CloudFront, or Azure Blob URLs.
    Strict validation for tests.
    """
    if not url:
        return False

    try:
        parsed = urlparse(url)
    except Exception:
        return False

    scheme = parsed.scheme.lower()
    host = parsed.netloc.lower()

    # Only allow HTTP/HTTPS
    if scheme not in ("http", "https"):
        return False

    # AWS S3 standard: bucket.s3.amazonaws.com
    if host.endswith(".s3.amazonaws.com"):
        return True

    # AWS S3 regional: bucket.s3.region.amazonaws.com
    if ".s3." in host and host.endswith(".amazonaws.com"):
        return True

    # AWS CloudFront
    if host.endswith(".cloudfront.net"):
        return True

    # Azure Blob storage
    if host.endswith(".blob.core.windows.net"):
        return True

    # Anything else is invalid
    return False
