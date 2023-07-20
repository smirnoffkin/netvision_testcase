from logging import getLogger
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgres.connection import get_db
from app.schemas.post import (
    CreatePostRequest,
    DeletePostResponse,
    PostResponse
)
from app.services.post import (
    _create_new_post,
    _delete_post,
    _get_post_by_id,
    _get_all_posts
)

logger = getLogger(__name__)

router = APIRouter(tags=["Post"])


@router.post(
    "/new",
    description="Create post",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_post(
    body: CreatePostRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        new_post = await _create_new_post(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This post is already exists"
        )
    return new_post


@router.get(
    "/post/{uuid}",
    description="Get post by id",
    response_model=PostResponse,
    status_code=status.HTTP_200_OK
)
@cache(expire=10)
async def get_post(
    uuid: UUID,
    db: AsyncSession = Depends(get_db)
):
    post = await _get_post_by_id(uuid, db)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with uuid {uuid} not found."
        )
    return post


@router.get(
    "/posts/all",
    description="Get a list of all posts",
    status_code=status.HTTP_200_OK
)
@cache(expire=10)
async def get_all_posts(db: AsyncSession = Depends(get_db)):
    posts = await _get_all_posts(db)
    return posts


@router.get(
    "/post_with_count/{count}",
    description="Get count of posts",
    status_code=status.HTTP_200_OK
)
@cache(expire=10)
async def get_posts_with_count_limit(
    count: int,
    db: AsyncSession = Depends(get_db)
):
    posts = await _get_all_posts(db)
    if len(posts) < count:
        return posts[:len(posts)]
    return posts[:count]


@router.delete(
    "/post/{uuid}",
    description="Delete post",
    response_model=DeletePostResponse,
    status_code=status.HTTP_200_OK
)
async def delete_post(
    uuid: UUID,
    db: AsyncSession = Depends(get_db)
):
    deleted_post_uuid = await _delete_post(uuid, db)
    if deleted_post_uuid is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with uuid {uuid} not found."
        )
    return {"success": True, "deleted_post_uuid": deleted_post_uuid}
