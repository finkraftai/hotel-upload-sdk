# CHECK_DUPLICATE_SOURCE_ID = """
# SELECT COUNT(*) as count FROM hotel_uploads WHERE source_id = %(source_id)s;
# """

CHECK_DUPLICATE_FILE_HASH = """
SELECT COUNT(*) as count FROM hotel_invoice WHERE file_hash = %(file_hash)s;
"""

INSERT_HOTEL_UPLOAD = """
INSERT INTO hotel_invoice
(id, file_url, source, source_id, client_name, file_hash, status, created_on, updated_on)
VALUES (%(id)s, %(file_url)s, %(source)s, %(source_id)s, %(client_name)s,
        %(file_hash)s, %(status)s, %(created_on)s, %(updated_on)s)
RETURNING *;
"""
