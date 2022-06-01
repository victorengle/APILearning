from csv import Dialect
from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db, engine
from sqlalchemy import func


router = APIRouter(prefix="/sqlalchemy", tags=["Posts"])


# 'Limit' is a QUERY PARAMETER allows users to filter on how much to return
# , 'Offset' is a QUERY PARAMETER allows users to skip a certain number of records. e.g skip the first two records or pages
# Filter.'Contains' is another QUERY parameter that allows users to search for keywords
# On the url, %20 represents a ' ' (space)
@router.get("/getall", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), get_curr_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post).filter(
        models.Post.Title.contains(search)).limit(limit).offset(skip).all()
    print(posts)
    return posts

# 'Limit' is a QUERY PARAMETER allows users to filter on how much to return
# , 'Offset' is a QUERY PARAMETER allows users to skip a certain number of records. e.g skip the first two records or pages
# Filter.'Contains' can also be used as a query parameter in the url for searching for words in a property. E.g .contains(...)
# On the url, '%20' represents a ' ' (space)


@router.get("/getuserspecific", response_model=List[schemas.PostVoteResponse])
def get_user_posts(db: Session = Depends(get_db), get_curr_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    posts = db.query(models.Post, func.count(models.Vote.User_Id).label("Votes")).join(
        models.Vote, models.Vote.Post_Id == models.Post.Id, isouter=True).group_by(models.Post.Id).filter(models.Post.User_Id == get_curr_user.Id).filter(models.Post.Title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), get_curr_user: int = Depends(oauth2.get_current_user)):

    newpost = models.Post(User_Id=get_curr_user.Id, **post.dict())
    db.add(newpost)
    db.commit()
    db.refresh(newpost)
    return newpost


@router.get("/posts/{id}", response_model=schemas.PostVoteResponse)
def get_specific(id: int, response: Response,  db: Session = Depends(get_db),  get_curr_user: int = Depends(oauth2.get_current_user)):

    # getspecificpost = db.query(models.Post).filter(
    #     models.Post.Id == id).first()
    getspecificpost = db.query(models.Post, func.count(models.Vote.User_Id).label("Votes")).join(
        models.Vote, models.Vote.Post_Id == models.Post.Id, isouter=True).group_by(models.Post.Id).filter(models.Post.Id == id).first()

    if not getspecificpost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post With Id {id} Not Found")
    return getspecificpost


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_id(id: int, db: Session = Depends(get_db),  get_curr_user: int = Depends(oauth2.get_current_user)):

    deletedpost_query = db.query(models.Post).filter(models.Post.Id == id)

    deletedpost = deletedpost_query.first()

    if deletedpost == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="The Id Does Not Exist")

    if deletedpost.User_Id != get_curr_user.Id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorised To Perform This Action")

    deletedpost_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/latest")
def get_latest(db: Session = Depends(get_db)):

    getlatestpost = db.query(models.Post).order_by(
        models.Post.Created_At.desc()).first()
    return getlatestpost


@router.put("/update/{id}")
def update_stuff(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),  get_curr_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.Id == id)
    updatedpost = post_query.first()
    if updatedpost == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="The Id Does Not Exist")
    if updatedpost.User_Id != get_curr_user.Id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized To Perform This Action")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


@router.get("/allvotes", response_model=List[schemas.PostVoteResponse])
def get_votes(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    posts = db.query(models.Post, func.count(models.Vote.User_Id).label("Votes")).join(
        models.Vote, models.Vote.Post_Id == models.Post.Id, isouter=True).group_by(models.Post.Id).filter(models.Post.Title.contains(search)).limit(limit).offset(skip).all()

    return posts
