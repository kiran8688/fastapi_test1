from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "postgresql://postgres:12345678@localhost/Fastapi_test1" # create the database url connection string

engine = create_engine(DATABASE_URL, echo= True) # create the engine which is used to connect to the database

SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind=engine) # create the session local which is used to create the session

Base = declarative_base() # create the base class which is used to create the tables

def get_db(): # create the get db function which is used to get the session
    db= SessionLocal() # create the session local
    try:
        yield db # yield the session local
    finally:
        db.close() # close the session local



#skip connection to database if you are not using sqlalchemy, because we are using sqlalchemy ORM we don't need to connect to the database using psycopg

# import psycopg
# import time
# from psycopg.rows import dict_row


# while True:
#     try:
#         conn = psycopg.connect(host="localhost", dbname="Fastapi_test1", user="postgres", password="12345678", row_factory=dict_row) # connect to the database using psycopg and row_factory=dict_row to get the data in the form of dictionary
#         cursor = conn.cursor() # create the cursor to execute the sql queries
#         print('Database connection was successful')
#         break
#     except Exception as error: # catch the exception if the database connection fails
#         print('connectiong to database failed')
#         print('Error :', error)
#         time.sleep(5)
