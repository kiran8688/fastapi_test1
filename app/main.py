from app.database import engine
from app import models
from fastapi import FastAPI
from app.routers import post, user, auth, vote
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware



# models.Base.metadata.create_all(bind= engine) # create all the tables if not exists 

app = FastAPI() # create the fast api app 

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router) # include the employee router
app.include_router(user.router) # include the user router
app.include_router(auth.router) # include the auth router
app.include_router(vote.router) # include the vote router


@app.get("/") # get the root url
def read_root():
    return {"Hello": "World"}


# @router.get("/employees/latest") # get the latest employee (app.get("/employees/latest") in main.py)

# def get_latest_employee():
#     employee = my_emps[len(my_emps) - 1]
#     return {"employee_detail": employee}