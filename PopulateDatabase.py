import pandas as pd
import os
from movie_app.models.models import Movie
from movie_app.models.models import Rating
from movie_app.database import Base
from movie_app.database import db_session
from movie_app.database import engine

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def populate_movies():
    path = os.path.join(os.path.dirname(__file__), 'data', 'movies.csv')
    movies_df = pd.read_csv(path)
    movie_data = movies_df.to_dict(orient='records')  # Convert DataFrame to list of dicts
    db_session.bulk_insert_mappings(Movie, movie_data)
    db_session.commit()

def populate_ratings():
    path = os.path.join(os.path.dirname(__file__), 'data', 'ratings.csv')
    ratings_df = pd.read_csv(path)
    chunk_size = 1000  # You can adjust the chunk size based on your memory and performance needs
    for start in range(0, len(ratings_df), chunk_size):
        end = min(start + chunk_size, len(ratings_df))
        rating_data = ratings_df.iloc[start:end].to_dict(orient='records')
        db_session.bulk_insert_mappings(Rating, rating_data)
        db_session.commit()
        print(f"Processed {end} of {len(ratings_df)} ratings.")


def main():
    init_db()
    print("Populating movies...")
    populate_movies()
    print("Populating ratings...")
    populate_ratings()
    print("Database population complete!")


if __name__ == '__main__':
    main()
