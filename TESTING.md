# Testing Guide

## 🧪 Running Tests

### Install Test Dependencies

```bash
pip install -r requirements.txt
```

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=hotel_sdk --cov-report=html
```

### Run Specific Test File

```bash
pytest tests/test_validators.py
pytest tests/test_models.py
pytest tests/test_service.py
```

### Run Specific Test Class

```bash
pytest tests/test_service.py::TestHotelUploadService
```

### Run Specific Test

```bash
pytest tests/test_validators.py::TestCloudURLValidator::test_valid_s3_standard_url
```

### Run with Verbose Output

```bash
pytest -v
```

### Run Integration Tests Only

```bash
pytest tests/test_integration.py -v
```

### Skip Integration Tests

```bash
pytest -m "not integration"
```

### Run Tests in Parallel

```bash
pip install pytest-xdist
pytest -n auto
```

## 📊 Test Coverage

Current test coverage targets:

| Module | Target | Tests |
|--------|--------|-------|
| **Validators** | 100% | 10 tests |
| **Models** | 95% | 9 tests |
| **Exceptions** | 100% | 8 tests |
| **Service Layer** | 90% | 6 tests |
| **Retry Logic** | 95% | 5 tests |
| **Integration** | N/A | 2 tests |
| **Overall** | >90% | 40+ tests |

## 🚀 Running Examples

### Basic Upload

```bash
python examples/basic_upload.py
```

### Batch Upload

```bash
python examples/batch_upload.py
```

### Error Handling

```bash
python examples/error_handling.py
```

### Cloud Providers

```bash
python examples/cloud_providers.py
```

## 🔧 Test Configuration

Tests are configured in `pytest.ini`:
- Test discovery pattern: `test_*.py`
- Verbose output enabled
- Integration tests marked separately

## 📝 Writing New Tests

### Test Structure

```python
import pytest
from hotel_sdk import HotelService

class TestMyFeature:
    """Test suite for my feature."""
    
    def test_something(self):
        """Test description."""
        # Arrange
        service = HotelService()
        
        # Act
        result = service.do_something()
        
        # Assert
        assert result == expected
```

### Using Fixtures

```python
def test_with_fixture(valid_hotel_data):
    """Test using shared fixture."""
    # Fixture data is automatically injected
    assert valid_hotel_data["source_id"] is not None
```

### Mocking Database Calls

```python
from unittest.mock import patch

@patch('hotel_sdk.services.hotel_upload_service.get_connection')
def test_with_mock(mock_get_conn):
    """Test with mocked database."""
    # Setup mock behavior
    mock_get_conn.return_value = mock_connection
    
    # Run test
    result = service.store(data)
    
    # Verify
    assert result["status"] == "success"
```

## ⚠️ Integration Tests

Integration tests require a configured database:

```bash
# Set environment variables
export PG_HOST=localhost
export PG_PORT=5432
export PG_DB=hotels_test
export PG_USER=test_user
export PG_PASSWORD=test_pass

# Run integration tests
pytest tests/test_integration.py -v
```

Integration tests are skipped automatically if database is not configured.

## 🐛 Debugging Tests

### Run with Debug Output

```bash
pytest -vv --tb=long
```

### Stop on First Failure

```bash
pytest -x
```

### Run Last Failed Tests

```bash
pytest --lf
```

### Enter Debugger on Failure

```bash
pytest --pdb
```

## 📈 Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest --cov=hotel_sdk
```
