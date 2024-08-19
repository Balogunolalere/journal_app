from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Define constants
DEFAULT_TAGS = []
DEFAULT_CREATED_AT = datetime.now()
DEFAULT_UPDATED_AT = datetime.now()

# Define a base model for journal entries
class JournalEntryBase(BaseModel):
    title: str
    content: str
    tags: List[str] = DEFAULT_TAGS
    created_at: datetime = DEFAULT_CREATED_AT
    updated_at: datetime = DEFAULT_UPDATED_AT
    embedding: Optional[List[float]] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.date().isoformat()
        }

# Define a model for creating journal entries
class JournalEntryCreate(JournalEntryBase):
    pass

# Define a model for journal entries
class JournalEntry(JournalEntryBase):
    key: str
    user_key: str

# Define a model for updating journal entries
class JournalEntryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None
