from datetime import datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgres.models import Post
from app.schemas.post import CreatePostRequest, PostResponse
from app.services.crud import PostCRUD


async def _create_new_post(
    body: CreatePostRequest,
    db: AsyncSession
) -> Post:
    async with db.begin():
        post_crud = PostCRUD(db)
        return await post_crud.create_post(uuid=body.uuid, text=body.text)


async def _get_post_by_id(post_uuid: UUID, db: AsyncSession) -> Post | None:
    async with db.begin():
        post_crud = PostCRUD(db)
        post = await post_crud.get_post_by_uuid(post_uuid)
        return post


async def _get_all_posts(db: AsyncSession) -> list[Post]:
    async with db.begin():
        post_crud = PostCRUD(db)
        post = await post_crud.get_all_posts()
        return post


async def _delete_post(
    post_uuid: UUID,
    db: AsyncSession
) -> UUID | None:
    async with db.begin():
        post_crud = PostCRUD(db)
        deleted_post = await post_crud.delete_post(post_uuid)
        return deleted_post
