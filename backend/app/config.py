from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    env: str = os.getenv("ENV", "dev")

    # DB
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./bank.db")

    # CORS allowed
    cors_origins: list[str] = [
        origin.strip()
        for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
        if origin.strip()
    ]

    # JWT
    jwt_secret: str = os.getenv("JWT_SECRET", "change-me-in-prod")
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    class Config:
           env_file = ".env"
           extra = "allow"


settings = Settings()
