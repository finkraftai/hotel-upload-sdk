# 📦 Hotel-Uploads SDK

A lightweight, robust, and production-ready Python SDK for handling **hotel file uploads** with comprehensive validation and duplicate prevention.

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🚀 Quick Start

### Installation

```bash
pip install git+https://github.com/<username>/hotel-sdk.git
```

---

## ✨ Key Features

### ✔️ Dual Hash Duplicate Prevention

- **source_id** uniqueness check
- **file_hash** uniqueness check
- Prevents duplicate file uploads at multiple levels

### ✔️ Cloud URL Validation

- AWS S3 URLs (`s3.amazonaws.com`)
- CloudFront URLs (`cloudfront.net`)
- Azure Blob Storage (`blob.core.windows.net`)

### ✔️ Robust Retry Logic

- Exponential backoff algorithm
- Configurable retry attempts (default: 3)
- Configurable backoff delay (default: 0.5s)

### ✔️ Comprehensive Error Handling

- `ValidationError` - Invalid cloud URLs
- `DuplicateError` - Duplicate source_id or file_hash
- `UploadFailed` - Database insert failures
- `ConnectionError` - Database connection issues

### ✔️ Production-Ready Architecture

- Clean separation of concerns
- Pydantic models for type safety
- Connection pooling support
- Structured logging-ready

---

## 📁 Project Structure

```
hotel_sdk/
├── hotel_sdk/
│   ├── __init__.py              # Public API exports
│   ├── config/
│   │   └── config.py            # Environment configuration
│   ├── models/
│   │   └── hotel_upload.py      # Pydantic models
│   ├── database/
│   │   ├── connection.py        # Database connections
│   │   └── queries.py           # SQL queries
│   ├── services/
│   │   └── hotel_upload_service.py  # Business logic
│   └── utils/
│       ├── validators.py        # URL validators
│       ├── retry.py             # Retry logic
│       └── exceptions.py        # Custom exceptions
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## ⚙️ Configuration

Create a `.env` file in your project root:

```env
# Database Configuration
PG_HOST=localhost
PG_PORT=5432
PG_DB=hotels
PG_USER=your_user
PG_PASSWORD=your_password

# Retry Configuration (Optional)
MAX_RETRIES=3
RETRY_BACKOFF=0.5
```

---

## 📖 Detailed Usage

### Import the Service

```python
from hotel_sdk.services.hotel_service import HotelService
from hotel_sdk.models.hotel_upload import HotelUpload
from hotel_sdk.utils.exceptions import DuplicateError, ValidationError
```

### Upload a File Record

```python
try:
    payload = {
        "id": "unique-uuid-here",
        "file_url": "https://mybucket.s3.amazonaws.com/files/hotel_123.pdf",
        "source": "tmc",
        "source_id": "3f9c1021f4a8aa7bd840c1ff1d382aab",
        "client_name": "TataCapital",
        "file_hash": "sha256:abcdef1234567890abcdef1234567890",
        "status": "PENDING"
    }
  
    result = HotelService.store(payload)
    print(f"✅ Upload successful: {result}")
  
except ValidationError as e:
    print(f"❌ Invalid input: {e}")
  
except DuplicateError as e:
    print(f"⚠️ Duplicate found: {e}")
  
except Exception as e:
    print(f"❌ Unexpected error: {e}")
```

### Response Format

Success response:

```json
{
  "status": "success",
  "upload_id": "c0a80100-0000-0000-0000-000000000001"
}
```

---

## 🔒 Error Handling

| Exception           | Trigger                       | Example                      |
| ------------------- | ----------------------------- | ---------------------------- |
| `ValidationError` | Invalid cloud URL format      | Non-AWS/Azure URL provided   |
| `DuplicateError`  | source_id or file_hash exists | Same hash already in DB      |
| `UploadFailed`    | Database insert failure       | NULL returned from INSERT    |
| `ConnectionError` | Database connection issues    | Cannot connect to PostgreSQL |

### Error Handling Example

```python
from hotel_sdk.utils.exceptions import (
    ValidationError,
    DuplicateError,
    UploadFailed,
    ConnectionError
)

try:
    result = HotelService.store(payload)
except ValidationError:
    # Handle invalid URL or data
    print("Invalid cloud URL. Use AWS S3, CloudFront, or Azure Blob URLs.")
except DuplicateError as e:
    # Handle duplicate file_hash or source_id
    print(f"This file already exists: {e}")
except UploadFailed:
    # Handle database insert failures
    print("Failed to insert record into database.")
except ConnectionError:
    # Handle connection issues
    print("Database connection failed. Check your DATABASE_URL.")
```

---

## 🌀 Retry Mechanism

The SDK implements **exponential backoff** for transient failures:

- **Formula**: `delay × (2 ^ attempt)`
- **Default retries**: 3 attempts
- **Default backoff**: 0.5 seconds

**Example retry sequence:**

- Attempt 1: Immediate
- Attempt 2: Wait 0.5s
- Attempt 3: Wait 1.0s
- Attempt 4: Wait 2.0s

Configure via environment variables:

```env
MAX_RETRIES=5
RETRY_BACKOFF=1.0
```

---

## 🛠️ Development Setup

### Clone the Repository

```bash
git clone https://github.com/<your-org>/hotel-sdk.git
cd hotel-sdk
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔍 API Reference

### `HotelService.store(data: dict) -> dict`

Validates and stores a hotel file upload record.

**Parameters:**

- `data` (dict): Upload payload containing all required fields

**Returns:**

- `dict`: `{"status": "success", "upload_id": "<id>"}`

**Raises:**

- `ValidationError`: Invalid data or cloud URL
- `DuplicateError`: source_id or file_hash already exists
- `UploadFailed`: Database insert failed
- `ConnectionError`: Cannot connect to database

**Required Fields:**

- `id` (str): UUID for the upload
- `file_url` (str): Valid AWS/Azure cloud URL
- `source` (str): Source identifier
- `source_id` (str): Unique source identifier
- `client_name` (str): Client name
- `file_hash` (str): SHA256 file hash
- `status` (str): Upload status (e.g., "PENDING")

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
