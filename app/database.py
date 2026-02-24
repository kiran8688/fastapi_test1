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
