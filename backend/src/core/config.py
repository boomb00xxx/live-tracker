# import os
# from pathlib import Path
#
# from dotenv import load_dotenv
#
#
# load_dotenv()
#
#
# BASE_DIR = Path(__file__).resolve().parent.parent.parent
#
#
# DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = os.getenv("DB_PASSWORD", "secret")
# DB_HOST = os.getenv("DB_HOST", "localhost")
# DB_PORT = os.getenv("DB_PORT", "5432")
# DB_NAME = os.getenv("DB_NAME", "mydb")
#
# DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
#
#
#
# SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
# DEBUG = os.getenv("DEBUG", "False").lower() == "true"

from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

env_paths = [
    Path(__file__).resolve().parents[2] / ".env",
]
load_dotenv(dotenv_path=env_paths[0])

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_paths, env_file_encoding="utf-8")
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    SECRET_KEY: str
    DEBUG: bool = False

    @property
    def DB_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()
