from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from books.database import Base


class BaseModel(Base):
    __abstract__ = True
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True, index=True, unique=True)


class Author(BaseModel):
    __tablename__ = "authors"

    name = Column(String)
    age = Column(Integer)
    # books = relationship("Book", back_populates="authors")


class Book(BaseModel):
    __tablename__ = "books"

    title = Column(String)
    author_id = Column(Integer, ForeignKey("authors.id"))
    authors = relationship("Author", back_populates="books")
