from pydantic import conint
from pydantic import BaseModel, EmailStr # import the base model and email str from pydantic
from datetime import datetime # import the datetime from datetime
from typing import Optional # import the optional from typing

class PostBase(BaseModel): # create the employee base model for request and response
    title: str
    content: str
    published: bool = True


class AddPost(PostBase): # create the employee add model for request only
    pass

class Post(PostBase): # create the employee model for response only
    id: int
    created_at: datetime
    owner_id: int
    owner: "UserOut"
    
    class Config: # create the config model for response
        orm_mode = True # enable the orm mode

class PostOut(BaseModel): # create the post out model for response only
    Post: Post # add the post model
    votes: int # add the votes model

    class Config: # create the config model for response
        orm_mode = True # enable the orm mode

class AddUser(BaseModel): # create the user add model for request only
    email: EmailStr
    password: str

class UserOut(BaseModel): # create the user model for response only
    id: int
    email: EmailStr 
    created_at: datetime

    class Config: # create the config model for response
        orm_mode = True # enable the orm mode

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token : str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)
