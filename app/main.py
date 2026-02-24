from database import engine, get_db
import models
from schemas import AddPost, Post, AddUser, UserOut
from utils import hash_password, verify_password # import the hash password and verify password functions
from fastapi import Depends
from sqlalchemy.orm import Session
from psycopg.rows import dict_row
import psycopg
from psycopg.errors import DatabaseDropped # import the database dropped error
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from typing import Optional, List
from random import randrange
import time
from routers import post, user, auth

models.Base.metadata.create_all(bind= engine) # create all the tables if not exists 

app = FastAPI() # create the fast api app 


while True:
    try:
        conn = psycopg.connect(host="localhost", dbname="Fastapi_test1", user="postgres", password="12345678", row_factory=dict_row) # connect to the database using psycopg and row_factory=dict_row to get the data in the form of dictionary
        cursor = conn.cursor() # create the cursor to execute the sql queries
        print('Database connection was successful')
        break
    except Exception as error: # catch the exception if the database connection fails
        print('connectiong to database failed')
        print('Error :', error)
        time.sleep(5)

my_emps =[{"name": "Kiran", "place": "Hyderabad", "id": 1},
            {"name": "Vamshi", "place": "Hyderabad", "id": 2},
            {"name": "Rohit", "place": "Hyderabad", "id": 3}]

def find_employee(id):
    for p in my_emps:
        if p["id"] == id:
            return p

def find_index_employee(id):
    for i, p in enumerate(my_emps):
        if p["id"] == id:
            return i

app.include_router(post.router) # include the employee router
app.include_router(user.router) # include the user router
app.include_router(auth.router) # include the auth router


@app.get("/") # get the root url
def read_root():
    return {"Hello": "World"}


# @router.get("/employees/latest") # get the latest employee (app.get("/employees/latest") in main.py)

# def get_latest_employee():
#     employee = my_emps[len(my_emps) - 1]
#     return {"employee_detail": employee}