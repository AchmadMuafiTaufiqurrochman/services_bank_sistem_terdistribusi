# app/core/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DB_HOST: str = os.getenv("DB_HOST")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_PORT: int = os.getenv("DB_PORT")
    ENDPOINT_API_MIDDLEWARE: str | None = os.getenv("ENDPOINT_API_MIDDLEWARE")
    MIDDLEWARE_SECRET_KEY: str | None = os.getenv("API_KEY_MID")

settings = Settings()