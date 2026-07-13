from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OLLAMA_URL:   str = "http://ollama:11434"
    OLLAMA_MODEL: str = "qwen2.5:1.5b"
    VLLM_URL:     str = "http://vllm:8000"
    LLM_PROVIDER: str = "ollama"

    class Config:
        env_file = ".env",
        extra="ignore"
        
settings = Settings()