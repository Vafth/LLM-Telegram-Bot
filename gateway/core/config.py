from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OLLAMA_URL:   str = "http://ollama:11434"
    OLLAMA_MODEL: str = "qwen2.5:1.5b"
    
    class Config:
        env_file = ".env"  # tylko dla lokalnego uruchomienia bez Docker

settings = Settings()