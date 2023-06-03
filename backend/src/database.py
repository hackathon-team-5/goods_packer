import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from pydantic import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .auth.models import Base

load_dotenv()


class Settings(BaseSettings):
    database_host: str = os.environ.get("POSTGRES_HOST")
    database_port: int = os.environ.get("POSTGRES_PORT")
    database_name: str = os.environ.get("POSTGRES_DB")
    database_user: str = os.environ.get("POSTGRES_USER")
    database_password: str = os.environ.get("POSTGRES_PASSWORD")

    @property
    def database_url(self) -> str:
        return (
            f'postgresql://{quote_plus(self.database_user)}'
            f':{quote_plus(self.database_password)}'
            f'@{self.database_host}:{self.database_port}/{self.database_name}')

    class Config:
        env_file = ".env"


db_settings = Settings()
DATABASE_URL = db_settings.database_url


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)
