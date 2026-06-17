from hotel_sdk.models.hotel_upload import HotelUpload
from hotel_sdk.database.connection import get_connection, release_connection
from hotel_sdk.database.queries import INSERT_HOTEL_UPLOAD, CHECK_DUPLICATE_FILE_HASH
from hotel_sdk.utils.retry import retry
from hotel_sdk.utils.exceptions import DuplicateError, UploadFailed, ConnectionError as DBConnectionError
import psycopg2

class HotelUploadService:

    @staticmethod
    def _execute_store_logic(upload: HotelUpload):
        """Atomic operation to check and insert."""
        conn = None
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                # 1. Check for file_hash duplicates
                cur.execute(CHECK_DUPLICATE_FILE_HASH, {"file_hash": upload.file_hash})
                result = cur.fetchone()
                if result and result["exists"]:
                    raise DuplicateError(f"file_hash already exists: {upload.file_hash}")

                # 2. Insert hotel upload record
                try:
                    cur.execute(INSERT_HOTEL_UPLOAD, upload.model_dump())
                    res = cur.fetchone()
                    conn.commit()
                    
                    if not res:
                        raise UploadFailed("Insert operation returned NULL")
                    return res
                except psycopg2.IntegrityError:
                    conn.rollback()
                    raise DuplicateError(f"source_id already exists: {upload.source_id}")
                
        except (psycopg2.Error, DBConnectionError) as e:
            if conn:
                conn.rollback()
            raise UploadFailed(f"Database operation failed: {e}")
        finally:
            if conn:
                release_connection(conn)

    @staticmethod
    def store(data: dict):
        """
        Validates request and inserts into PostgreSQL.
        """
        # Validate + convert into model
        upload = HotelUpload(**data)

        # Perform the atomic operation with retry logic
        # Ignore DuplicateError as it's a permanent failure
        result = retry(
            lambda: HotelUploadService._execute_store_logic(upload),
            ignored_exceptions=(DuplicateError,)
        )
        
        return {
            "status": "success",
            "upload_id": result.get("file_hash") if isinstance(result, dict) else result[0]
        }


# Alias for compatibility with README examples
HotelService = HotelUploadService

