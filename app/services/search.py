from app.utils.embeddings import get_embedding
from app.services.journal import doc_index
import numpy as np

def search_entries(query: str, user_key: str, limit: int = 10):
    query_embedding = get_embedding(query)
    matches, scores = doc_index.find(
        np.array(query_embedding),
        search_field='embedding',
        limit=limit
    )
    
    results = [
        {
            "title": match.title,
            "content": match.content,
            "score": float(score),  # Convert to float for JSON serialization
        }
        for match, score in zip(matches, scores)
        if match.user_key == user_key
    ]
    
    return results

__all__ = ['search_entries']