from sqlalchemy.orm import Session
from sqlalchemy import select

from . import models
from typing import Optional, List, Iterator

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

def find(db: Session, ids: Optional[List[int]]) -> List[models.User]:
    query = db.query(models.User.user_id, models.User.name)
    if ids is not None:
        query = query.filter(models.User.user_id.in_(ids))
    return query.yield_per(20)

def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def create_user(db: Session, email: str, name: str, password_hash: str):
    user = models.User(email = email, name = name, password_hash = password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user 

def delete_user(db: Session, user: models.User):
    db.delete(user)
    db.commit()
