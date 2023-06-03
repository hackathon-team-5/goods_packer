from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..database import get_db
from .models import User as DBUser
from .schemas import UserCreate, UserLogin, UserUpdate
from .utils import create_access_token

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get('/users')
async def get_users(db: Session = Depends(get_db)):
    users = db.query(DBUser).all()
    return users


@router.post('/users')
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    db_user = DBUser(
        username=user.username,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {'message': 'Create user'}


@router.get('/users/{user_id}')
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@router.put("/users/{user_id}")
async def update_user(user_id: int,
                      user_update: UserUpdate,
                      db: Session = Depends(get_db)):
    user = db.query(DBUser).filter(DBUser.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.password:
        hashed_password = pwd_context.hash(user_update.password)
        user.password = hashed_password

    if user_update.username:
        user.username = user_update.username

    db.commit()
    db.refresh(user)

    return {"message": "User updated successfully"}


@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}


@router.post("/login")
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(DBUser).filter(
        DBUser.username == user_data.username
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not pwd_context.verify(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    access_token = create_access_token(
        {"username": user.username},
        timedelta(hours=24)
    )
    return {"access_token": access_token}
