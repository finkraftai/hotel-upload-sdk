import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from typing import Optional
from hotel_sdk.utils.exceptions import ConnectionError as DBConnectionError

# Global connection pool
_pool: Optional[pool.SimpleConnectionPool] = None
_connection_string: Optional[str] = None

def initialize_db(connection_string: str) -> None:
    """
    Initialize database pool with user's connection string.
    """
    global _connection_string, _pool
    _connection_string = connection_string
    # Clear existing pool if it exists
    if _pool:
        _pool.closeall()
        _pool = None

def _get_pool():
    """Get or create connection pool."""
    global _pool, _connection_string
    
    if _pool is not None:
        return _pool

    try:
        if _connection_string is not None:
            _pool = pool.SimpleConnectionPool(1, 10, _connection_string)
        else:
            # Fallback to SDK's config
            from hotel_sdk.config.config import settings
            _pool = pool.SimpleConnectionPool(
                1, 10,
                host=settings.pg_host,
                port=settings.pg_port,
                dbname=settings.pg_database,
                user=settings.pg_user,
                password=settings.pg_password
            )
        return _pool
    except psycopg2.Error as e:
        raise DBConnectionError(f"Failed to initialize database pool: {e}")

def get_connection():
    """Get database connection from pool."""
    try:
        p = _get_pool()
        conn = p.getconn()
        conn.cursor_factory = RealDictCursor
        return conn
    except psycopg2.Error as e:
        raise DBConnectionError(f"Database connection failed: {e}")

def release_connection(conn):
    """Release a connection back to the pool."""
    global _pool
    if _pool:
        _pool.putconn(conn)
