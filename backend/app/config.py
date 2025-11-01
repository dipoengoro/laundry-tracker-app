from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr, AnyHttpUrl

class Settings(BaseSettings):
    # Variabel Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    
    # Variabel JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_USERNAME: str | None = None
    MAIL_PASSWORD: str | None = None
    MAIL_FROM: EmailStr

    MINIO_ENDPOINT: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_BUCKET: str
    MINIO_USE_SSL: bool
    MINIO_PUBLIC_ENDPOINT: str

    # Memberitahu Pydantic untuk membaca dari file .env
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()