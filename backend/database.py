from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from pathlib import Path
from dotenv import load_dotenv
import os

env_path = Path('.', '.env')
load_dotenv(dotenv_path=env_path)

DB_URL = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(os.environ.get('USERNAME'),os.environ.get('PASSWORD'),os.environ.get('HOST'),os.environ.get('PORT'),os.environ.get('DBNAME'))
engine = create_engine(
    DB_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try :
        yield db
    finally:
        db.close()
