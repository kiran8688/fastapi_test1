from fastapi import FastAPI, Depends, Response, status, HTTPException, APIRouter
from schemas import Vote
from database import get_db
from sqlalchemy.orm import Session
from models import Post, Vote, User
from oauth2 import get_current_user


router = APIRouter(
    prefix="/vote",
    tags=["vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def vote(vote: Vote, db: Session= Depends(get_db), current_user: int = Depends(get_current_user)):

    if vote.dir == 1:
        db.query(Vote).filter(Vote.post_id == vote.post_id, Vote.user_id == current_user.id)
