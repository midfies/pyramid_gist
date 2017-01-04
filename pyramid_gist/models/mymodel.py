from sqlalchemy import (
    Column,
    Index,
    Integer,
    Unicode,
)

from .meta import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode)
    password = Column(Unicode)
    first_name = Column(Unicode)
    last_name = Column(Unicode)
    email = Column(Unicode)
    fav_food = Column(Unicode)


Index('my_index', User.username, unique=True, mysql_length=255)
