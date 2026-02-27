import models, schemas, utils
from database import get_db
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi import status, HTTPException

# create the router for user (app.include_router(user.router) in main.py) @app will be replaced by router
router = APIRouter(  
    prefix = "/users", # prefix for the router helps to reduce the code
    tags = ["Users"] # tags for the router helps to group the router
) 



@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schemas.UserOut) # create a new user (app.post("/users") in main.py)
def create_user(user: schemas.AddUser, db: Session= Depends(get_db)):

    hashed_pw = utils.hash_password(user.password) # hash the password
    user.password = hashed_pw # set the hashed password

    new_user = models.User(**user.dict()) # create the new user
    db.add(new_user) # add the new user to the database
    db.commit() # commit the transaction
    db.refresh(new_user) # refresh the new user
    return new_user


@router.get("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model = schemas.UserOut) # get a user by id (app.get("/users/{id}") in main.py)
def get_user(id: int, db: Session= Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first() # get the user by id
    if not user: # check if the user is not found
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found") # raise the http exception
    return user # return the user
