import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Journal App"
    PROJECT_VERSION: str = "1.0.0"
    
    DETA_PROJECT_KEY: str = os.getenv("DETA_PROJECT_KEY")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    SENTENCE_TRANSFORMER_MODEL: str = "all-MiniLM-L6-v2"
    
    EMBEDDING_DIM: int = 384  # Dimension of all-MiniLM-L6-v2 embeddings

settings = Settings()