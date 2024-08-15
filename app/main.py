from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, journal, search, summarization
from app.core.config import settings
import time

app = FastAPI(
    title=settings.PROJECT_NAME, 
    version=settings.PROJECT_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    )

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


app.include_router(auth.router, tags=["authentication"])
app.include_router(journal.router, prefix="/journal", tags=["journal"])
app.include_router(search.router, prefix="/journal", tags=["search"])
app.include_router(summarization.router, prefix="/summarization", tags=["summarization"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Journal App API"}

@app.get("/api/health", tags=["💓 Health Check"])
async def health_check():
    return {"status": "healthy", "timestamp": time.time()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)