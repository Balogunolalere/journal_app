from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from typing import List
from pydantic import ValidationError
from app.models.journal import JournalEntryCreate, JournalEntry, JournalEntryUpdate
from app.services.journal import create_journal_entry, get_journal_entry, update_journal_entry, delete_journal_entry, get_all_journal_entries
from app.services.transcription import transcribe_audio
from app.core.security import get_current_user
from app.models.user import User
from datetime import datetime
from fastapi.responses import JSONResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/entries", response_model=JournalEntry)
async def create_entry(entry: JournalEntryCreate, current_user: User = Depends(get_current_user)):
    try:
        return create_journal_entry(entry, current_user.key)
    except Exception as e:
        logger.error(f"Error creating journal entry: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while creating the journal entry")

@router.get("/entries/{entry_id}", response_model=JournalEntry)
async def read_entry(entry_id: str, current_user: User = Depends(get_current_user)):
    try:
        entry = get_journal_entry(entry_id, current_user.key)
        if entry is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")
        return entry
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving journal entry: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while retrieving the journal entry")

@router.put("/entries/{entry_id}", response_model=JournalEntry)
async def update_entry(entry_id: str, entry_update: JournalEntryUpdate, current_user: User = Depends(get_current_user)):
    try:
        updated_entry = update_journal_entry(entry_id, current_user.key, entry_update)
        if updated_entry is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")
        return updated_entry
    except ValidationError as ve:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve))
    except Exception as e:
        logger.error(f"Error updating journal entry: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while updating the journal entry")

@router.delete("/entries/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_entry(entry_id: str, current_user: User = Depends(get_current_user)):
    try:
        deleted = delete_journal_entry(entry_id, current_user.key)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting journal entry: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while deleting the journal entry")

@router.get("/entries", response_model=List[JournalEntry])
async def read_entries(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
):
    try:
        entries = get_all_journal_entries(current_user.key)
        return entries[skip : skip + limit]
    except Exception as e:
        logger.error(f"Error retrieving journal entries: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while retrieving journal entries")

@router.post("/entries/transcribe", response_model=JournalEntry)
async def transcribe_audio_entry(
    file: UploadFile = File(...),
    entry_name: str = Form(...),
    current_user: User = Depends(get_current_user)
):
    try:
        if not file.filename.lower().endswith(('.mp3', '.wav', '.ogg', '.flac')):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported file format")

        content = await file.read()
        if len(content) > 10 * 1024 * 1024:  # 10 MB limit
            raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File too large")

        transcribed_text = transcribe_audio(content, file.filename)
        if not transcribed_text:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Failed to transcribe audio")

        entry_create = JournalEntryCreate(
            title=entry_name,
            content=transcribed_text,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        return create_journal_entry(entry_create, current_user.key)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error transcribing audio entry: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while transcribing the audio entry")