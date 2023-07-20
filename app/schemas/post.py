from uuid import UUID

from pydantic import BaseModel


class BasePostSchema(BaseModel):
    uuid: UUID
    text: str

    class Config:
        orm_mode = True


class CreatePostRequest(BasePostSchema):
    ...


class PostResponse(BasePostSchema):
    ...


class DeletePostResponse(BaseModel):
    success: bool
    deleted_post_uuid: UUID

    class Config:
        orm_mode = True
