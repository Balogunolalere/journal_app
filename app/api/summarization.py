from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from app.core.security import get_current_user
from app.models.user import User
from app.services.journal import get_journal_entry
from groq import Groq
import os
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class SummarizationRequest(BaseModel):
    entry_id: str
    max_length: int = 100

class SummarizationResponse(BaseModel):
    summary: str

@router.post("/summarize", response_model=SummarizationResponse)
async def summarize_journal_entry(
    request: SummarizationRequest,
    current_user: User = Depends(get_current_user)
):
    try:
        # Retrieve the journal entry from the database
        entry = get_journal_entry(request.entry_id, current_user.key)
        if not entry:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Journal entry not found")

        # Combine title and content for summarization
        full_content = f"Title: {entry.title}\n\nContent: {entry.content}"

        # Generate summary using Groq
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"You are a text summarization assistant. Summarize the following journal entry in no more than {request.max_length} words:"
                },
                {
                    "role": "user",
                    "content": full_content
                }
            ],
            model="llama3-8b-8192",  # You can change this to a different model if needed
            temperature=0.5,
            max_tokens=request.max_length * 2,  # Adjust as needed
            top_p=1,
            stream=False
        )
        
        summary = chat_completion.choices[0].message.content.strip()
        return SummarizationResponse(summary=summary)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in summarization: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while summarizing the journal entry")