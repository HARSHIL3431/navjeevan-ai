import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    groq_model: str = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    data_gov_api_key: str = os.getenv("DATA_GOV_API_KEY", "")
    groq_timeout_seconds: int = int(os.getenv("GROQ_TIMEOUT_SECONDS", "12"))
    external_api_timeout_seconds: int = int(os.getenv("EXTERNAL_API_TIMEOUT_SECONDS", "15"))


settings = Settings()
