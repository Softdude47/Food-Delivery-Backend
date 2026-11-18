from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"  # Keeps Pydantic from failing if extra vars are in your .env
    )


    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    SALT_ROUNDS: int
    JWT_EXPIRATION_TIME: int = 2.592e6  # 30 days in seconds


settings = Settings()
