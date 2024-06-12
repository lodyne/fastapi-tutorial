from pydantic import BaseModel, Field


class Post(BaseModel):
    id: int = Field(alias="post_id", title="POST ID", description="The Post ID")
    title: str = Field(title="Post Title", description="The title of the Post")
    description: str | None = None
