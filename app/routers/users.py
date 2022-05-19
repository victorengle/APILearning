from typing import List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db


router = APIRouter(prefix="/sqlalchemy/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_posts(user: schemas.PostUsers, db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.Password)
    user.Password = hashed_password
    newuser = models.User(**user.dict())
    db.add(newuser)
    db.commit()
    db.refresh(newuser)
    return newuser


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user_id(id: int, db: Session = Depends(get_db)):

    userdetail = db.query(models.User).filter(
        models.User.Id == id).first()
    if not userdetail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User With Id {id} Not Found")
    return userdetail
