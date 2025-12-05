import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional
from hotel_sdk.utils.exceptions import ConnectionError as DBConnectionError

# Global connection string
_connection_string: Optional[str] = None

def initialize_db(connection_string: str) -> None:
    """
    Initialize database with user's connection string.
    
    Args:
        connection_string: PostgreSQL connection string
            Format: "host=... port=... dbname=... user=... password=..."
    """
    global _connection_string
    _connection_string = connection_string

def get_connection():
    """Get database connection."""
    global _connection_string
    
    # If user provided connection string, use it
    if _connection_string is not None:
        try:
            conn = psycopg2.connect(_connection_string)
            conn.cursor_factory = RealDictCursor
            return conn
        except psycopg2.Error as e:
            raise DBConnectionError(f"Database connection failed: {e}")
    
    # Fallback to SDK's config (for backward compatibility)
    from hotel_sdk.config.config import settings
    try:
        conn = psycopg2.connect(
            host=settings.pg_host,
            port=settings.pg_port,
            dbname=settings.pg_db,
            user=settings.pg_user,
            password=settings.pg_password
        )
        conn.cursor_factory = RealDictCursor
        return conn
    except psycopg2.Error as e:
        raise DBConnectionError(f"Database connection failed: {e}")
    
    
    
# import psycopg2
# from psycopg2.extras import RealDictCursor
# from hotel_sdk.config import settings

# def get_connection():
#     return psycopg2.connect(
#         host=settings.pg_host,
#         port=settings.pg_port,
#         database=settings.pg_db,
#         user=settings.pg_user,
#         password=settings.pg_password,
#         cursor_factory=RealDictCursor
#     )
