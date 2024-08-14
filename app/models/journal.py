from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class JournalEntryCreate(BaseModel):
    title: str
    content: str
    tags: List[str] = []
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    embedding: Optional[List[float]] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.date().isoformat()
        }

class JournalEntry(BaseModel):
    key: str
    title: str
    content: str
    user_key: str
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    embedding: Optional[List[float]] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.date().isoformat()
        }

class JournalEntryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None