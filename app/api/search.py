from fastapi import APIRouter, Depends, Query
from typing import List
from app.services.search import search_entries
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/search", response_model=List[dict])
async def search(
    q: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    results = search_entries(q, current_user.key, limit)
    return results