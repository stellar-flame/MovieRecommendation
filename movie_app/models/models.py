from sqlalchemy import Column, Integer, Float, String, ForeignKey
from movie_app.database import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    password = Column(String(50))

    def __init__(self, name=None, password=None):
        self.name = name
        self.password = password

    def __repr__(self):
        return f'<User {self.name!r}>'


class Movie(Base):
    __tablename__ = 'movie'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    genres = Column(String)

    def __repr__(self):
        return f'<Movie {self.title}>'

    def __init__(self, title=None, genre=None):
        self.title = title
        self.genre = genre


class Rating(Base):
    __tablename__ = 'rating'
    id = Column(Integer, primary_key=True)
    rating = Column(Float, nullable=False)
    user_id = Column(Integer, nullable=False)
    movie_id = Column(Integer, nullable=False)

    def __repr__(self):
        return f'<Rating {self.rating} by User {self.user_id} for Movie {self.movie_id}>'

    def __init__(self, rating=None, user_id=None, movie_id=None):
        self.rating = rating
        self.user_id = user_id
        self.movie_id = movie_id
