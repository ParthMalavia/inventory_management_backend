import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()

class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = os.getenv("DB_PORT", 5432)
    DB_USER: str = os.getenv("DB_USER", "user")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "password")
    DB_NAME: str = os.getenv("DB_NAME", "inventory")

    # class Config:
    #     env_file = ".env"


settings = Settings()
