from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

from pathlib import Path
from dotenv import load_dotenv
import os

env_path = Path('.', '.env')
load_dotenv(dotenv_path=env_path)


DB_URL = 'mariadb+mariadbconnector://kangsan:{}@{}:{}/{}'.format(os.environ.get('PASSWORD'),os.environ.get('HOST'),os.environ.get('PORT'),os.environ.get('DBNAME'))
# DB_URL = 'mariadb+mariadbconnector://{}:{}@{}:{}/{}'.format(os.environ.get('USERNAME'),os.environ.get('PASSWORD'),os.environ.get('HOST'),os.environ.get('PORT'),os.environ.get('DBNAME'))
engine = create_engine(
    DB_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try :
        yield db
    finally:
        db.close()
