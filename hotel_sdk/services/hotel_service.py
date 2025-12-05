from hotel_sdk.models.hotel_upload import HotelUpload
from hotel_sdk.database.connection import get_connection
from hotel_sdk.database.queries import INSERT_HOTEL_UPLOAD, CHECK_DUPLICATE_FILE_HASH
from hotel_sdk.utils.retry import retry
from hotel_sdk.utils.exceptions import DuplicateError, UploadFailed, ConnectionError as DBConnectionError
import psycopg2


class HotelUploadService:

    @staticmethod
    def store(data: dict):
        """
        Validates request and inserts into PostgreSQL.
        Returns structured response with status and upload_id.
        """
        # Validate + convert into model
        upload = HotelUpload(**data)

        # def check_duplicate():
        #     """Check if source_id already exists."""
        #     try:
        #         conn = get_connection()
        #         cur = conn.cursor()
        #         cur.execute(CHECK_DUPLICATE_SOURCE_ID, {"source_id": upload.source_id})
        #         result = cur.fetchone()
        #         cur.close()
        #         conn.close()
        #         return result["count"] if result else 0
        #     except psycopg2.Error as e:
        #         raise DBConnectionError(f"Database connection failed during duplicate check: {e}")

        def check_file_hash_duplicate():
            """Check if file_hash already exists."""
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute(CHECK_DUPLICATE_FILE_HASH, {"file_hash": upload.file_hash})
                result = cur.fetchone()
                cur.close()
                conn.close()
                return result["count"] if result else 0
            except psycopg2.Error as e:
                raise DBConnectionError(f"Database connection failed during file_hash duplicate check: {e}")

        def insert():
            """Insert hotel upload record."""
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute(INSERT_HOTEL_UPLOAD, upload.model_dump())
                result = cur.fetchone()
                conn.commit()
                cur.close()
                conn.close()
                
                if not result:
                    raise UploadFailed("Insert operation returned NULL")
                
                return result
            except psycopg2.IntegrityError as e:
                raise DuplicateError(f"source_id hash already exists: {upload.source_id}")
            except psycopg2.Error as e:
                raise UploadFailed(f"Insert operation failed: {e}")

        # Check for duplicates first
        # duplicate_count = retry(check_duplicate)
        # if duplicate_count > 0:
        #     raise DuplicateError(f"source_id hash already exists: {upload.source_id}")

        # Check for file_hash duplicates
        file_hash_duplicate_count = retry(check_file_hash_duplicate)
        if file_hash_duplicate_count > 0:
            raise DuplicateError(f"file_hash already exists: {upload.file_hash}")

        # Perform insert with retry logic
        result = retry(insert)
        
        # Return structured response
        return {
            "status": "success",
            "upload_id": result.get("file_hash") if isinstance(result, dict) else result[0]
        }


# Alias for compatibility with README examples
HotelService = HotelUploadService


# from hotel_sdk.models.hotel_upload import HotelUpload
# from hotel_sdk.database.connection import get_connection
# from hotel_sdk.database.queries import INSERT_HOTEL_UPLOAD, CHECK_DUPLICATE_FILE_HASH
# from hotel_sdk.utils.retry import retry
# from hotel_sdk.utils.exceptions import DuplicateError, UploadFailed, ConnectionError as DBConnectionError
# import psycopg2


# class HotelUploadService:

#     @staticmethod
#     def store(data: dict):
#         """
#         Validates request and inserts into PostgreSQL.
#         Returns structured response with status and upload_id.
#         """
#         upload = HotelUpload(**data)

#         def check_file_hash_duplicate():
#             """Check if file_hash already exists."""
#             try:
#                 conn = get_connection()
#                 cur = conn.cursor()
#                 cur.execute(CHECK_DUPLICATE_FILE_HASH, {"file_hash": upload.file_hash})
#                 result = cur.fetchone()
#                 cur.close()
#                 conn.close()

#                 # FIX 1: avoid KeyError ('count') during tests
#                 return result.get("count", 0) if result else 0

#             except psycopg2.Error as e:
#                 raise DBConnectionError(
#                     f"Database connection failed during file_hash duplicate check: {e}"
#                 )

#         def insert():
#             """Insert hotel upload record."""
#             try:
#                 conn = get_connection()
#                 cur = conn.cursor()
#                 cur.execute(INSERT_HOTEL_UPLOAD, upload.model_dump())

#                 try:
#                     # FIX 2: catch StopIteration from mocked cursor
#                     result = cur.fetchone()
#                 except StopIteration:
#                     raise UploadFailed("Insert failed: no DB row returned")

#                 conn.commit()
#                 cur.close()
#                 conn.close()

#                 if not result:
#                     raise UploadFailed("Insert operation returned NULL")

#                 return result

#             except psycopg2.IntegrityError:
#                 raise DuplicateError(
#                     f"source_id hash already exists: {upload.source_id}"
#                 )
#             except psycopg2.Error as e:
#                 raise UploadFailed(f"Insert operation failed: {e}")

#         # Check file_hash duplicates first
#         file_hash_duplicate_count = retry(check_file_hash_duplicate)
#         if file_hash_duplicate_count > 0:
#             raise DuplicateError(f"file_hash already exists: {upload.file_hash}")

#         # Insert with retry logic
#         result = retry(insert)

#         # Return structured response
#         return {
#             "status": "success",
#             "upload_id": (
#                 result.get("file_hash")
#                 if isinstance(result, dict)
#                 else result[0]
#             )
#         }


# HotelService = HotelUploadService
