from os import getenv

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


load_dotenv()
POSTGRES_USER = getenv('POSTGRES_USER', 'default')
POSTGRES_PASSWORD = getenv('POSTGRES_PASSWORD', 'defaultpassword')
POSTGRES_DB = getenv('POSTGRES_DB', 'postgres')
PORT = getenv('PORT', '5432')
HOST_DB = getenv('HOST_DB', 'db')

SQLALCHEMY_URL = (
    f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
    f'@{HOST_DB}:{PORT}/{POSTGRES_DB}'
)

engine = create_engine(SQLALCHEMY_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
