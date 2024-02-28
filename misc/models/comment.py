from pydantic import BaseModel, Field, HttpUrl


class Comment(BaseModel):
    id: int
    url: HttpUrl
    text: str = Field(...)
