from sentence_transformers import SentenceTransformer
from app.core.config import settings

model = SentenceTransformer(settings.SENTENCE_TRANSFORMER_MODEL)

def get_embedding(text: str):
    return model.encode(text).tolist()