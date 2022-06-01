from app import schemas
from jose import jwt
from app.config import settings
import pytest


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/sqlalchemy/getall/")
    print(res.json())

    def validate(post):
        return schemas.PostResponse(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/sqlalchemy/getall/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/sqlalchemy/posts/{test_posts[0].Id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/sqlalchemy/posts/88888")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/sqlalchemy/posts/{test_posts[0].Id}")
    post = schemas.PostVoteResponse(**res.json())
    print(res.json())
    assert int(post.Post.Id) == test_posts[0].Id
    assert post.Post.Content == test_posts[0].Content
    assert post.Post.Title == test_posts[0].Title


@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True),
])
def test_create_post(authorized_client, test_createuser, test_posts, title, content, published):
    res = authorized_client.post(
        "/sqlalchemy/posts", json={"Title": title, "Content": content, "Published": published})

    created_post = schemas.PostResponse(**res.json())
    print(created_post)
    assert res.status_code == 201
    assert created_post.Title == title
    assert created_post.Content == content
    assert created_post.Published == published
    assert created_post.User_Id == int(test_createuser['Id'])


def test_create_post_default_published_true(authorized_client, test_createuser, test_posts):
    res = authorized_client.post(
        "/sqlalchemy/posts", json={"Title": "arbitrary title", "Content": "aasdfjasdf"})

    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.Title == "arbitrary title"
    assert created_post.Content == "aasdfjasdf"
    assert created_post.Published == False
    assert created_post.Owner.Id == test_createuser['Id']


def test_unauthorized_user_create_post(client, test_createuser, test_posts):
    res = client.post(
        "/sqlalchemy/posts", json={"Title": "arbitrary title", "Content": "aasdfjasdf"})
    assert res.status_code == 401


def test_unauthorized_user_delete_Post(client, test_createuser, test_posts):
    res = client.delete(
        f"/sqlalchemy/posts/{test_posts[0].Id}")
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_createuser, test_posts):
    res = authorized_client.delete(
        f"/sqlalchemy/posts/{test_posts[0].Id}")

    assert res.status_code == 204


def test_delete_post_non_exist(authorized_client, test_createuser, test_posts):
    res = authorized_client.delete(
        f"/sqlalchemy/posts/8000000")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_createuser, test_posts):
    res = authorized_client.delete(
        f"/sqlalchemy/posts/{test_posts[3].Id}")
    assert res.status_code == 403


def test_update_post(authorized_client, test_createuser, test_posts):
    data = {
        "Title": "updated title",
        "Content": "updatd content",
        "Id": test_posts[0].Id

    }
    res = authorized_client.put(
        f"/sqlalchemy/update/{test_posts[0].Id}", json=data)
    updated_post = schemas.PostCreate(**res.json())
    assert res.status_code == 200
    assert updated_post.Title == data['Title']
    assert updated_post.Content == data['Content']


def test_update_other_user_post(authorized_client, test_createuser, test_createuser2, test_posts):
    data = {
        "Title": "updated title",
        "Content": "updatd content",
        "Id": test_posts[3].Id

    }
    res = authorized_client.put(
        f"/sqlalchemy/update/{test_posts[3].Id}", json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_createuser, test_posts):
    res = client.put(
        f"/sqlalchemy/update/{test_posts[0].Id}")
    assert res.status_code == 401


def test_update_post_non_exist(authorized_client, test_createuser, test_posts):
    data = {
        "Title": "updated title",
        "Content": "updatd content",
        "Id": test_posts[3].Id

    }
    res = authorized_client.put(
        f"/sqlalchemy/update/8000000", json=data)
    assert res.status_code == 404
