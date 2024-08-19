from groq import Groq
from app.core.config import settings
import tempfile

# Define constants
GROQ_API_KEY = settings.GROQ_API_KEY
MODEL = "whisper-large-v3"
RESPONSE_FORMAT = "verbose_json"

# Initialize the Groq client
client = Groq(api_key=GROQ_API_KEY)

def transcribe_audio(file, filename):
    """Transcribe an audio file using the Groq API."""
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix=filename) as temp_file:
            # Write the bytes content to the temporary file
            temp_file.write(file)
            temp_file.seek(0)
            
            # Open the file in binary read mode
            with open(temp_file.name, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    file=audio_file,
                    model=MODEL,
                    response_format=RESPONSE_FORMAT,
                )
        
        return transcription.text
    except Exception as e:
        # Handle any exceptions that occur during transcription
        raise Exception(f"Error transcribing audio: {str(e)}")
