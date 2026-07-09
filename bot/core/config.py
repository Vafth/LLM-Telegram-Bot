from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    TOKEN: str = "1234567890"
    GATEWAY_URL: str = "http://gateway:8080"
    
    class Config:
        env_file = ".env"

settings = Settings()