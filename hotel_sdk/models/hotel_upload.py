from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime, timezone
from uuid import UUID
from hotel_sdk.utils.validators import validate_cloud_url
from hotel_sdk.utils.exceptions import ValidationError

class HotelUpload(BaseModel):
    # 1. Use UUID type for strict validation
    id: UUID 
    file_url: str
    source: str 
    source_id: str = Field(..., min_length=1)   
    client_name: str
    file_hash: str = Field(..., min_length=1)   
    status: str
    
    # 2. Use timezone-aware defaults for created_on (Matches timestamptz)
    created_on: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # 3. For updated_on, if your DB is 'without time zone', 
    # keep it as naive or handle conversion in the repository layer.
    updated_on: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(from_attributes=True)

    @field_validator('file_url')
    @classmethod
    def validate_file_url(cls, v):
        if not validate_cloud_url(str(v)):
            raise ValidationError(f"Invalid cloud URL: {v}")
        return v
    
    
    
    
    
    
    
# from pydantic import BaseModel, HttpUrl, Field, field_validator
# from datetime import datetime
# from hotel_sdk.utils.validators import validate_cloud_url
# from hotel_sdk.utils.exceptions import ValidationError


# class HotelUpload(BaseModel):
#     id: str
#     file_url: str
#     source: str 
#     source_id: str = Field(..., min_length=1)   
#     client_name: str
#     file_hash: str = Field(..., min_length=1)   
#     status: str
#     created_on: datetime = Field(default_factory=datetime.utcnow)
#     updated_on: datetime = Field(default_factory=datetime.utcnow)

#     @field_validator('file_url')
#     @classmethod
#     def validate_file_url(cls, v):
#         """Validate that file_url is an AWS S3, CloudFront, or Azure Blob URL."""
#         if not validate_cloud_url(str(v)):
#             raise ValidationError(
#                 f"Invalid cloud URL. Must be AWS S3 or Azure Blob URL: {v}"
#             )
#         return v
