import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    # Model names – keep key names so you don't have to touch other files
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "llama3.2")
    EMBED_MODEL: str = os.getenv("EMBED_MODEL", "nomic-embed-text")

    # Database configuration (used for logging only)
    MYSQL_HOST: str = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT: int = int(os.getenv("MYSQL_PORT", "3306"))
    MYSQL_USER: str = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DB: str = os.getenv("MYSQL_DB", "forecastgpt")

    # Data / scraping
    DATA_DIR: str = os.getenv("DATA_DIR", "data/cache")
    USER_AGENT: str = os.getenv("USER_AGENT", "ForecastGPT/1.0")

settings = Settings()

# Ensure data directory always exists so PDF downloads never fail on missing folder
os.makedirs(settings.DATA_DIR, exist_ok=True)
