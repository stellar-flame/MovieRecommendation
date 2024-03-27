import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('movies', __name__)

import pandas as pd
@bp.route('/')
def index():
    all_ratings = pd.read_csv(os.path.join(bp.root_path, '../moviedata', 'ratings.csv'))
    all_movies = pd.read_csv(os.path.join(bp.root_path, '../moviedata', 'movies.csv'))
    #change to real user-id
    user_rating = all_ratings[all_ratings['userId'] == 1]
    ratings = user_rating.merge(all_movies, how='left', left_on='movieId', right_on='movieId')
    ratings = ratings.to_dict(orient='records')

    return render_template('movies/index.html', ratings=ratings)