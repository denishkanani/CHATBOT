import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID", "")

    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///ai.db")

    # AI Model
    MODEL_NAME = os.getenv("MODEL_NAME", "llama3")

    # Server
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Create a single config object
config = Config()