import pandas as pd
import os

path = os.path.join(os.path.dirname(__file__), 'data', 'ratings.csv')
movies_df = pd.read_csv(path)
movie_data = movies_df.to_dict(orient='records')  # Convert DataFrame to list of dicts
print(movie_data)