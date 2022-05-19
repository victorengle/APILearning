from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import date, datetime

from sqlalchemy import Integer

# Python reads from top to bottom. Remember that!!!


class PostUsers(BaseModel):
    Email: EmailStr
    Password: str


class UserResponse(BaseModel):
    Id: str
    Email: EmailStr
    Created_At: datetime

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    Title: str
    Content: str
    Published: bool = False


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    Id: str
    Created_At: datetime
    Owner: UserResponse

    class Config:
        orm_mode = True


class PostVoteResponse(BaseModel):
    Post: PostResponse
    Votes: int

    class Config:
        orm_mode = True


class UserLogin(PostUsers):
    pass

# conint(ge , le) - allows only the boundaries (including the values provided) of numbers specified in the bracket


class CreateVote(BaseModel):
    Post_Id: str
    Vote_Dir: conint(ge=0, le=1)


class TokenData(BaseModel):
    id: Optional[str]


class TokenResponse(BaseModel):
    Access_Token: str
    Token_Type: str
