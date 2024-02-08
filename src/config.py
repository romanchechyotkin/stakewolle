from dotenv import load_dotenv
from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings

load_dotenv()

class Config(BaseSettings):
    CORS_ORIGINS: list[str] = []
    CORS_HEADERS: list[str] = []

    POSTGRESQL_URL: PostgresDsn = "postgres://user:5432@localhost:5432/db"
    REDIS_URL: RedisDsn

    JWT_ALG: str = ""
    JWT_SECRET: str = ""


settings = Config()