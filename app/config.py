"""
Central configuration for FleetFit.
Reads values from a `.env` file (see .env.example) so secrets and the
database connection string never need to be hardcoded in source.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Default to a local SQLite file so the project runs with zero setup.
    # Swap to a PostgreSQL URL in .env for production, e.g.:
    # postgresql://user:password@localhost:5432/fleetfit
    database_url: str = "sqlite:///./fleetfit.db"

    secret_key: str = "change-this-to-a-long-random-secret-string-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
