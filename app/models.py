from enum import unique
from . database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text, null
from sqlalchemy import Column, ForeignKey, Integer, PrimaryKeyConstraint, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP

# When creating __tablename__ , try to not use the "" for the tables. See if it works. On Posgres, the table names are saved using the quotes. so table names are literally e.g saved as "Posts" or "Base" etc


class Post(Base):
    __tablename__ = "Posts"

    Id = Column(Integer, primary_key=True, nullable=False)
    Title = Column(String, nullable=False)
    Content = Column(String, nullable=False)
    Published = Column(Boolean, server_default='True', nullable=False)
    Created_At = Column(TIMESTAMP(timezone=True),
                        server_default=text('NOW()'), nullable=False)
    User_Id = Column(Integer, ForeignKey(
        "Users.Id", ondelete="CASCADE"), nullable=False)

    # "relationship" helps to return the class from another table
    Owner = relationship("User")


class User(Base):
    __tablename__ = "Users"

    Id = Column(Integer, primary_key=True, nullable=False)
    Email = Column(String, nullable=False, unique=True)
    Password = Column(String, nullable=False)
    Created_At = Column(TIMESTAMP(timezone=True),
                        server_default=text('NOW()'), nullable=False)


class Vote(Base):
    __tablename__ = ("Votes")

    Post_Id = Column(Integer, ForeignKey(
        "Posts.Id", ondelete="CASCADE"), primary_key=True, nullable=False)
    User_Id = Column(Integer, ForeignKey(
        "Users.Id", ondelete="CASCADE"), primary_key=True, nullable=False)
