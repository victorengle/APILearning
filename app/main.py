from fastapi import FastAPI
from . import models
from . database import engine
from .routers import posts, users, auth, votes
from fastapi.middleware.cors import CORSMiddleware
from .config import settings

# Commented code below Tells sqlalchemy to create whatever is in the models file if the table does not exist already
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# "*" wildcard means all (so all origins are allowed if wildcard is used)

origins = ["*"]

# origins = ["https://www.google.com"]

# to allow connections, methods or headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get("/")
def gethello():
    print("Yolo")
    return {"Message": "Seeing this message means CI/CD Is Completed"}
