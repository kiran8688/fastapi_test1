from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy import TIMESTAMP
from sqlalchemy import text
from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Post(Base): # create the employee table
    __tablename__ = "posts" # table name
    id = Column(Integer, primary_key=True, index=True) # primary key
    title = Column(String, nullable=False) # name column
    content = Column(String, nullable=False) # place column
    published = Column(Boolean, server_default=text('true')) # employed column
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')) # created at column
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")

class User(Base): # create the user table
    __tablename__ = "users" # table name
    id = Column(Integer, primary_key=True, index=True) # primary key
    email = Column(String, nullable=False, unique=True) # email column
    password = Column(String, nullable=False) # password column
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')) # created at column


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
