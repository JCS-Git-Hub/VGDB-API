from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str = "GameHub API"

    app_description: str = (
        "API REST para gestionar videojuegos "
        "y géneros"
    )

    app_version: str = "1.0.0"
    debug: bool = True
    database_url: str = "sqlite:///./gamehub.db"

    cors_origins: list[str] = [
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ]

    allow_credentials: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()