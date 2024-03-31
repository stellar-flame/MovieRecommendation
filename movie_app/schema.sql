DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS rating;
DROP TABLE IF EXISTS movie;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE rating(
    userId INTEGER,
    movieId INTEGER,
    rating FLOAT,
    timestamp TIMESTAMP
);

CREATE TABLE movie(
    movieId INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    genres TEXT
);