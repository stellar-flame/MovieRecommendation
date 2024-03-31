import os

from movie_app.models.movie_recommender import MovieRecommender

from flask import (
    Blueprint, render_template
)

bp = Blueprint('movies', __name__)
recommender = MovieRecommender(os.path.join(bp.root_path, '../data', 'ratings.csv'),
                               os.path.join(bp.root_path, '../data', 'movies.csv'))

@bp.route('/')
def index():
    ratings = recommender.get_ratings_for_user(1)
    recommendations = recommender.get_recommendations_for_user(1)
    return render_template('movies/index.html', ratings=ratings, recommendations=recommendations)