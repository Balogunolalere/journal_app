from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from typing import List
from pydantic import ValidationError
from app.models.journal import JournalEntryCreate, JournalEntry, JournalEntryUpdate
from app.services.journal import (
    create_journal_entry, get_journal_entry, update_journal_entry, delete_journal_entry, get_all_journal_entries
)
from app.services.transcription import transcribe_audio
from app.core.security import get_current_user
from app.models.user import User
from datetime import datetime
from fastapi.responses import JSONResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Define constants
FILE_SIZE_LIMIT = 10 * 1024 * 1024  # 10 MB
SUPPORTED_FILE_FORMATS = ['.mp3', '.wav', '.ogg', '.flac']

# Define custom exception
class EntryNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entry not found"
        )

# Define a function to handle exceptions
def handle_exception(exception: Exception):
    logger.error(f"An error occurred: {str(exception)}")
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred")

# Define a function to validate file format
def validate_file_format(file: UploadFile):
    if not file.filename.lower().endswith(SUPPORTED_FILE_FORMATS):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported file format")

# Define a function to validate file size
def validate_file_size(file: UploadFile):
    if len(file.file.read()) > FILE_SIZE_LIMIT:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File too large")

@router.post("/entries", response_model=JournalEntry)
async def create_entry(entry: JournalEntryCreate, current_user: User = Depends(get_current_user)):
    """Create a new journal entry."""
    try:
        return create_journal_entry(entry, current_user.key)
    except Exception as e:
        handle_exception(e)

@router.get("/entries/{entry_id}", response_model=JournalEntry)
async def read_entry(entry_id: str, current_user: User = Depends(get_current_user)):
    """Get a journal entry by ID."""
    try:
        entry = get_journal_entry(entry_id, current_user.key)
        if entry is None:
            raise EntryNotFoundException
        return entry
    except Exception as e:
        handle_exception(e)

@router.put("/entries/{entry_id}", response_model=JournalEntry)
async def update_entry(entry_id: str, entry_update: JournalEntryUpdate, current_user: User = Depends(get_current_user)):
    """Update a journal entry."""
    try:
        updated_entry = update_journal_entry(entry_id, current_user.key, entry_update)
        if updated_entry is None:
            raise EntryNotFoundException
        return updated_entry
    except ValidationError as ve:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve))
    except Exception as e:
        handle_exception(e)

@router.delete("/entries/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_entry(entry_id: str, current_user: User = Depends(get_current_user)):
    """Delete a journal entry."""
    try:
        deleted = delete_journal_entry(entry_id, current_user.key)
        if not deleted:
            raise EntryNotFoundException
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        handle_exception(e)

@router.get("/entries", response_model=List[JournalEntry])
async def read_entries(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
):
    """Get all journal entries."""
    try:
        entries = get_all_journal_entries(current_user.key)
        return entries[skip : skip + limit]
    except Exception as e:
        handle_exception(e)

@router.post("/entries/transcribe", response_model=JournalEntry)
async def transcribe_audio_entry(
    file: UploadFile = File(...),
    entry_name: str = Form(...),
    current_user: User = Depends(get_current_user)
):
    """Transcribe an audio file and create a new journal entry."""
    try:
        validate_file_format(file)
        validate_file_size(file)
        transcribed_text = transcribe_audio(file.file.read(), file.filename)
        if not transcribed_text:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Failed to transcribe audio")
        entry_create = JournalEntryCreate(
            title=entry_name,
            content=transcribed_text,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        return create_journal_entry(entry_create, current_user.key)
    except Exception as e:
        handle_exception(e)
