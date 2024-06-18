import pandas as pd
import numpy as np

from scipy.sparse.linalg import svds

class MovieRecommender:
    def __init__(self, rating_path, movie_path):
        df = pd.read_csv(rating_path)
        self.ratings = df[df['user_id'] < 10000]
        self.movies = pd.read_csv(movie_path)
        self.predictions = self.calculate_recommendations()

    def get_ratings_for_user(self, user_id):
        user_rating = self.ratings[self.ratings['user_id'] == user_id]
        ratings = user_rating.merge(self.movies, how='left', left_on='movie_id', right_on='id')
        return ratings.to_dict(orient='records')

    def get_recommendations_for_user(self, user_id):
        # Get and sort the user's predictions
        user_row_number = user_id - 1  # UserID starts at 1, not 0
        sorted_user_predictions = self.predictions.iloc[user_row_number].sort_values(ascending=False)

        # Get the user's data and merge in the movie information
        user_ratings = self.ratings[self.ratings.user_id == user_id]
        user_full = (user_ratings.merge(self.movies, how='left', left_on='movie_id', right_on='id').
                     sort_values(['rating'], ascending=False))

        # Recommend the highest predicted rating movies that the user hasn't seen yet
        recommendations = (self.movies[~self.movies['id'].isin(user_full['movie_id'])].
                           merge(pd.DataFrame(sorted_user_predictions).reset_index(), how='left',
                                 left_on='id',
                                 right_on='movie_id').
                           rename(columns={user_id: 'Predictions'}).
                           sort_values('Predictions', ascending=False).
                           iloc[:10])
        return recommendations.to_dict(orient='records')


    def calculate_recommendations(self):
        df = self.ratings[['user_id', 'movie_id', 'rating']]

        ratings_matrix = df.pivot_table(index='user_id', columns='movie_id', values='rating')
        ratings_matrix.fillna(0, inplace=True)  # Replace NaNs with 0s for missing ratings

        # Choose the number of factors to keep
        k = 50
        # Perform SVD
        u, s, vt = svds(ratings_matrix.to_numpy(), k=k)
        # Convert the Sigma (s) into a diagonal matrix
        sigma = np.diag(s)

        predicted_ratings = np.dot(np.dot(u, sigma), vt) + ratings_matrix.mean(axis=1).values.reshape(-1, 1)
        return pd.DataFrame(predicted_ratings, index=ratings_matrix.index, columns=ratings_matrix.columns)
