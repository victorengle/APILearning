from os import access
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..import database, schemas, models, utils, oauth2


router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.TokenResponse)
def loginuser(usercredentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    # OAuth2PasswordRequestForm = stores the inputed information from the user in a dictionary. In this instance the "Email" will be stored as "username", and Password will be stored as "password" in the dictionary. This can be used instead of creating a schema structure for the inputed information
    curr_user = db.query(models.User).filter(
        models.User.Email == usercredentials.username).first()

    if not curr_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credential")

    if not utils.verifypassword(usercredentials.password, curr_user.Password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credential")

    access_token = oauth2.create_access_token(data={"user_id": curr_user.Id})

    return{"Token_Type": "Bearer", "Access_Token": access_token}
