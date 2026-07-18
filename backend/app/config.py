# backend/app/config.py
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App General Settings
    APP_NAME: str = "IdeaOS Backend"
    ENV: str = os.getenv("IDEASOS_PROFILE", "local")  # local, production
    
    # Storage Paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR: str = os.path.join(BASE_DIR, "data")
    
    # Relational Database URL
    @property
    def DATABASE_URL(self) -> str:
        os.makedirs(self.DATA_DIR, exist_ok=True)
        db_path = os.path.join(self.DATA_DIR, "ideaos.db")
        # Ensure forward slashes for Windows compatibility in SQLite URLs
        normalized_path = db_path.replace("\\", "/")
        return f"sqlite:///{normalized_path}"

    # LLM Settings (via LiteLLM / Ollama)
    LITELLM_MODEL: str = os.getenv("IDEASOS_LLM_MODEL", "ollama/llama3")
    OLLAMA_API_BASE: str = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    
    # Enable fake simulator agents for testing out-of-the-box
    ENABLE_MOCK_AGENTS: bool = os.getenv("ENABLE_MOCK_AGENTS", "true").lower() == "true"

    class Config:
        case_sensitive = True

settings = Settings()
# Create required storage directories
os.makedirs(settings.DATA_DIR, exist_ok=True)
