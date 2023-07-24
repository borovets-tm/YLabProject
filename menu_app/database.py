from os import getenv

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


load_dotenv()

SQLALCHEMY_URL = getenv('SQLALCHEMY_URL', 'sqlite:///./sql_app.db')

if SQLALCHEMY_URL == 'sqlite:///./sql_app.db':
    engine = create_engine(
        SQLALCHEMY_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
