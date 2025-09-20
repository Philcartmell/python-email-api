from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional

class EmailRequest(BaseModel):
    to: List[EmailStr]
    from_email: EmailStr
    subject: str
    plain_body: str
    html_body: Optional[str] = None
    
    @validator("to")
    def validate_to_list(cls, v):
        if not v or len(v) == 0:
            raise ValueError("At least one recipient is required")
        return v
    
    @validator("subject")
    def validate_subject(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("Subject cannot be empty")
        return v.strip()
    
    @validator("plain_body")
    def validate_plain_body(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("Plain body cannot be empty")
        return v.strip()
