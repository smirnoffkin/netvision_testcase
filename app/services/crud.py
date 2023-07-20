from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgres.models import Post


class PostCRUD:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_post(self, uuid: UUID, text: str) -> Post:
        new_post = Post(uuid=uuid, text=text)
        self.db_session.add(new_post)
        await self.db_session.commit()
        return new_post

    async def get_post_by_uuid(self, post_uuid: UUID) -> Post | None:
        query = select(Post).where(Post.uuid == post_uuid)
        res = await self.db_session.execute(query)
        post_row = res.fetchone()
        if post_row is not None:
            return post_row[0]

    async def get_all_posts(self) -> list:
        query = select(Post)
        res = await self.db_session.execute(query)
        posts = list(res.scalars().all())
        return posts

    async def delete_post(self, post_uuid: UUID) -> UUID | None:
        query = delete(Post).where(Post.uuid == post_uuid).returning(Post.uuid)
        res = await self.db_session.execute(query)
        deleted_post_row = res.fetchone()
        if deleted_post_row is not None:
            return deleted_post_row[0]
