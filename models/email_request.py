from pydantic import BaseModel, EmailStr, field_validator
from typing import List, Optional

class EmailRequest(BaseModel):
    to: List[EmailStr]
    from_email: EmailStr
    subject: str
    plain_body: str
    html_body: Optional[str] = None
    
    @field_validator("to")
    @classmethod
    def validate_to_list(cls, v):
        if not v or len(v) == 0:
            raise ValueError("At least one recipient is required")
        return v
    
    @field_validator("subject")
    @classmethod
    def validate_subject(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("Subject cannot be empty")
        return v.strip()
    
    @field_validator("plain_body")
    @classmethod
    def validate_plain_body(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("Plain body cannot be empty")
        return v.strip()