from app.env import load_dotenv

load_dotenv()

from fastapi import FastAPI, Depends, Form
from app import schemas, crud, pwd
from app.database import SessionLocal
from os import environ
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
import base64

app = FastAPI()

SECRET_KEY = base64.b64decode(environ.get("JWT_SECRET"))
PUBLIC_KEY = base64.b64decode(environ.get("JWT_PUBLIC"))
ALGORITHM = environ.get("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(environ.get("JWT_EXPIRE_MINUTES"))

def create_access_token(user_id: int, expires_delta: Optional[timedelta] = None):
    to_encode = {"sub": "%d" % (user_id,)} 
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user_id(token: str) -> Optional[int]:
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM])
        if payload.get("sub") is None:
            return None
        try:
            user_id = int(payload.get("sub"))
            if user_id <= 0:
                return None
            return user_id
        except ValueError:
            return None
    except JWTError:
        return None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/auth/password", response_model=schemas.AuthResponse, operation_id="authByPassword")
def auth_by_password(request : schemas.AuthByPasswordRequest, db: SessionLocal = Depends(get_db)) \
        -> schemas.AuthResponse:
    response = schemas.AuthResponse(ok = False)
    user = crud.get_user_by_email(db, request.username)
    if user is None:
        return response
    if not pwd.verify(plain_password=request.password, hashed_password=user.password_hash):
        return response
    response.ok = True
    response.token = create_access_token(user.user_id)
    return response

@app.post("/token/refresh", response_model=schemas.AuthResponse, operation_id="me")
def me(token: str = Form(...), db: SessionLocal = Depends(get_db)) \
        -> schemas.AuthResponse:
    response = schemas.AuthResponse(ok = False)
    user_id = get_user_id(token)
    if user_id is None:
        return response
    if crud.get_user_by_id(db, user_id) is None:
        return response
    response.ok = True
    response.token = create_access_token(user_id)
    return response

@app.post("/users", response_model=schemas.Profiles, operation_id="users")
def users(filters: schemas.Filters, db: SessionLocal = Depends(get_db)) \
        -> schemas.Profiles:
    response = schemas.Profiles(items=[])
    for user in crud.find(db, filters.ids):
        response.items.append(schemas.Profile(uid=user.user_id, name=user.name))
    return response
