# import psycopg2
# import time
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


# SQLALCHEMY_DATABSE_URL = 'postgresql://<username>:<password>@<hostname:port>/<database_name>'
# SQLALCHEMY_DATABSE_URL = 'postgresql://postgres:dontforget12@localhost:5432/APILearning'

SQLALCHEMY_DATABSE_URL = f'postgresql://{settings.Database_Username}:{settings.Database_Password}@{settings.Database_Hostname}:{settings.Database_Port}/{settings.Database_Name}'


engine = create_engine(SQLALCHEMY_DATABSE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='APILearning',
#                                 user='postgres', password='dontforget12', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database Connection Was Successful!")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(3)
