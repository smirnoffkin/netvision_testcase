import uuid

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TEXT, UUID

from app.db.postgres.connection import Base


class Post(Base):
    __tablename__ = "posts"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = Column(TEXT)
