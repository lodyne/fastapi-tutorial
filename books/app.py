from sqlalchemy.orm import sessionmaker

from models import Author,engine

Session = sessionmaker(bind=engine)
session= Session()

# authors = session.query(Author).
author1 = Author(name="John Doe",age=78)
author2 = Author(name="Lee Smith",age=45)

author1.authors.extend(author1,author2)

session.add(author1)
session.add(author2)
session.commit()

print(f"{author1.authors=}")
print(f"{author2.authors=}")