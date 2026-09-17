from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "RepoPilot"
    environment: str = "development"
    database_url: str
    readonly_database_url: str | None = None  
    github_app_id: int
    github_private_key_path: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()