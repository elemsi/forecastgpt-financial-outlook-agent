import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    # Ollama model name (kept key name to avoid touching other files)
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "llama3.1")

    MYSQL_HOST: str = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT: int = int(os.getenv("MYSQL_PORT", "3306"))
    MYSQL_USER: str = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DB: str = os.getenv("MYSQL_DB", "forecastgpt")

    DATA_DIR: str = os.getenv("DATA_DIR", "data/cache")
    USER_AGENT: str = os.getenv("USER_AGENT", "ForecastGPT/1.0")

settings = Settings()
