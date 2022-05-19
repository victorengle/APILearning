from typing import List
from fastapi import status, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(prefix="/sqlalchemy/votes", tags=["Votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.CreateVote, db: Session = Depends(get_db),  get_curr_user: int = Depends(oauth2.get_current_user)):

    vote_query = db.query(models.Vote).filter(
        models.Vote.Post_Id == vote.Post_Id, models.Vote.User_Id == get_curr_user.Id)

    postquery = db.query(models.Post).filter(
        models.Post.Id == vote.Post_Id)

    found_post = postquery.first()
    found_vote = vote_query.first()

    if not found_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post With Id : {vote.Post_Id} Not Found")

    if(vote.Vote_Dir == 1):
        if(found_vote):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User {get_curr_user.Id} Already Has A Vote On This Post")
        new_vote = models.Vote(Post_Id=vote.Post_Id, User_Id=get_curr_user.Id)
        db.add(new_vote)
        db.commit()

        return {"message": "Successfully Added Vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote Does Not Exist")

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully Deleted Vote"}
