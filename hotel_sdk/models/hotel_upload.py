from pydantic import BaseModel, HttpUrl, Field, field_validator
from datetime import datetime
from hotel_sdk.utils.validators import validate_cloud_url
from hotel_sdk.utils.exceptions import ValidationError


class HotelUpload(BaseModel):
    id: str
    file_url: str
    source: str 
    source_id: str = Field(..., min_length=1)   
    client_name: str
    file_hash: str = Field(..., min_length=1)   
    status: str
    created_on: datetime = Field(default_factory=datetime.utcnow)
    updated_on: datetime = Field(default_factory=datetime.utcnow)

    @field_validator('file_url')
    @classmethod
    def validate_file_url(cls, v):
        """Validate that file_url is an AWS S3, CloudFront, or Azure Blob URL."""
        if not validate_cloud_url(str(v)):
            raise ValidationError(
                f"Invalid cloud URL. Must be AWS S3 or Azure Blob URL: {v}"
            )
        return v
