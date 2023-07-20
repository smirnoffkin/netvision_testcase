from uuid import UUID

import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.parametrize("post_data", [
    ({"uuid": "7366dce1-60c9-4245-9181-f284d13b1230", "text": "some text"}),
    ({"uuid": "da4f4f07-72dc-4143-9f0c-084d777a5d94", "text": "another text"})
])
async def test_create_post(client: AsyncClient, post_data: dict):
    res = await client.post("/new", json=post_data)
    data = res.json()
    assert res.status_code == status.HTTP_201_CREATED
    assert data["uuid"] == post_data["uuid"]
    assert data["text"] == post_data["text"]


@pytest.mark.parametrize("post_data", [
    ({"uuid": "7366dce1-60c9-4245-9181-f284d13b1230", "text": "some text"}),
    ({"uuid": "da4f4f07-72dc-4143-9f0c-084d777a5d94", "text": "another text"})
])
async def test_get_post_by_uuid(client: AsyncClient, post_data: dict):
    res = await client.get(f"/post/{post_data['uuid']}")
    data = res.json()
    assert res.status_code == status.HTTP_200_OK
    assert data["uuid"] == post_data["uuid"]
    assert data["text"] == post_data["text"]


@pytest.mark.parametrize("post_uuid", [
    ("dce620e8-c870-4ba0-90d9-2dc2bf1dcb3a"),
    ("7dec5c3d-a9ed-4bcd-82fd-51242eb612f9")
])
async def test_get_post_not_exists(client: AsyncClient, post_uuid: UUID):
    res = await client.get(f"/post/{post_uuid}")
    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert res.json() == {"detail": f"Post with uuid {post_uuid} not found."}


@pytest.mark.parametrize("posts", [
    ([
        {"uuid": "7366dce1-60c9-4245-9181-f284d13b1230", "text": "some text"},
        {"uuid": "da4f4f07-72dc-4143-9f0c-084d777a5d94", "text": "another text"}
    ])
])
async def test_get_all_posts(client: AsyncClient, posts: list[dict]):
    res = await client.get(f"/posts/all")
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == posts


@pytest.mark.parametrize("post_uuid", [
    ("7366dce1-60c9-4245-9181-f284d13b1230"),
    ("da4f4f07-72dc-4143-9f0c-084d777a5d94")
])
async def test_delete_post(client: AsyncClient, post_uuid: UUID):
    res = await client.delete(f"/post/{post_uuid}")
    data = res.json()
    assert res.status_code == status.HTTP_200_OK
    assert data["success"]
    assert data["deleted_post_uuid"] == post_uuid


@pytest.mark.parametrize("post_uuid", [
    ("dce620e8-c870-4ba0-90d9-2dc2bf1dcb3a"),
    ("7dec5c3d-a9ed-4bcd-82fd-51242eb612f9")
])
async def test_delete_post_not_exists(client: AsyncClient, post_uuid: UUID):
    res = await client.delete(f"/post/{post_uuid}")
    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert res.json() == {"detail": f"Post with uuid {post_uuid} not found."}
