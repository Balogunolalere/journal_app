from groq import Groq
from app.core.config import settings
import os


client = Groq(api_key=settings.GROQ_API_KEY)

def transcribe_audio(file, filename):
    # Generate a temporary file name
    temp_filename = f"temp_{filename}"
    
    try:
        # Write the bytes content to a temporary file
        with open(temp_filename, "wb") as temp_file:
            temp_file.write(file)
        
        # Open the file in binary read mode
        with open(temp_filename, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-large-v3",
                response_format="verbose_json",
            )
        
        return transcription.text
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)