from database import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi import Depends
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import PyJWTError
from schemas import TokenData
from fastapi.security import OAuth2PasswordBearer
from fastapi import status
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
import models
from config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire= datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credential_exception
        token_data = TokenData(id = id)
    except PyJWTError:
        raise credential_exception
    return token_data

def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_excepetion= HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_excepetion)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
