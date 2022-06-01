import pytest
from app import models


def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post(
        "/sqlalchemy/votes/", json={"Post_Id": test_posts[1].Id, "Vote_Dir": 1})
    assert res.status_code == 406


def test_vote_twice_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        "/sqlalchemy/votes/", json={"Post_Id": test_posts[3].Id, "Vote_Dir": 1})
    assert res.status_code == 409


def test_delete_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        "/sqlalchemy/votes/", json={"Post_Id": test_posts[3].Id, "Vote_Dir": 0})
    assert res.status_code == 201


def test_delete_vote_non_exist(authorized_client, test_posts):
    res = authorized_client.post(
        "/sqlalchemy/votes/", json={"Post_Id": test_posts[3].Id, "Vote_Dir": 0})
    assert res.status_code == 404


def test_vote_post_non_exist(authorized_client, test_posts):
    res = authorized_client.post(
        "/sqlalchemy/votes/", json={"Post_Id": 80000, "Vote_Dir": 1})
    assert res.status_code == 404


def test_vote_unauthorized_user(client, test_posts):
    res = client.post(
        "/sqlalchemy/votes/", json={"Post_Id": test_posts[3].Id, "Vote_Dir": 1})
    assert res.status_code == 401
