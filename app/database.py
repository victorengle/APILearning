from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


# SQLALCHEMY_DATABSE_URL = 'postgresql://<username>:<password>@<hostname:port>/<database_name>'
# SQLALCHEMY_DATABSE_URL = 'postgresql://postgres:dontforget12@localhost:5432/APILearning'
# print(pyodbc.drivers())


# conn_str = urllib.parse.quote_plus(
#     f"Driver={'ODBC+Driver+17+for+SQL+Server'}; Server=tcp: {config.settings.Database_Server}, 1433; Database={config.settings.Database_Name}; Uid={config.settings.Database_Uid}; Pwd={config.settings.Database_Password}; Encrypt=yes; TrustServerCertificate=no; Connection Timeout=30; ")

# SQLALCHEMY_DATABSE_URL = 'mssql+pyodbc:///odbc_connect={}'.format(conn_str)

# engine = create_engine(SQLALCHEMY_DATABSE_URL)


SQLALCHEMY_DATABSE_URL = f'postgresql+psycopg2://{settings.Database_Username}:{settings.Database_Password}@{settings.Database_Hostname}:{settings.Database_Port}/{settings.Database_Name}'

engine = create_engine(SQLALCHEMY_DATABSE_URL)


# engine.execute("SELECT 1")

# conn = engine.connect()
# conn.close()

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
