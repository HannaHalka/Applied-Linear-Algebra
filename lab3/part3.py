import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds
import matplotlib.pyplot as plt


df = pd.read_csv('ml-latest-small/ratings.csv')

origin_rating = df.pivot(index='userId', columns='movieId', values='rating')

ratings_matrix = origin_rating.dropna(thresh=50, axis=0)
ratings_matrix = ratings_matrix.dropna(thresh=50, axis=1)

ratings_matrix_filled = ratings_matrix.fillna(2.5)

R = ratings_matrix_filled.values
# print(R)
# [[4.  2.5 4.  ... 2.5 2.5 2.5]
#  [2.5 2.5 2.5 ... 2.5 2.5 2.5]
#  [2.5 4.  4.  ... 2.5 2.5 2.5]...

user_ratings_mean = np.mean(R, axis=1)

R_demeaned = R - user_ratings_mean.reshape(-1, 1)

U, sigma, Vt = svds(R_demeaned, k=3)

sigma = np.diag(sigma)

all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
# print(all_user_predicted_ratings)
# [[3.70267932 2.8270766  3.34960118 ... 2.56709684 2.57190806 2.49423637]
#  [2.78080814 2.4797083  2.80419013 ... 2.45856947 2.4525548  2.37233206]
#  [3.71374758 3.38243678 3.06611445 ... 2.25287115 2.38442272 2.55768707]...
preds_df = pd.DataFrame(all_user_predicted_ratings, columns=ratings_matrix.columns, index=ratings_matrix.index)
# print(preds_df)
#  movieId    1         2         6       ...    99114     109487    112852
# userId                                 ...
# 1        3.702679  2.827077  3.349601  ...  2.567097  2.571908  2.494236
# 4        2.780808  2.479708  2.804190  ...  2.458569  2.452555  2.372332
# 6        3.713748  3.382437  3.066114  ...  2.252871  2.384423  2.557687...

only_predict_ratings = pd.DataFrame(np.nan, columns=ratings_matrix_filled.columns, index=ratings_matrix_filled.index)
for user in preds_df.index:
    for movie in preds_df.columns:
        if np.isnan(origin_rating.loc[user, movie]):
            only_predict_ratings.loc[user, movie] = preds_df.loc[user, movie]

# print(only_predict_ratings)
# movieId    1         2         6       ...    99114     109487    112852
# userId                                 ...
# 1             NaN  2.827077       NaN  ...  2.567097  2.571908  2.494236
# 4        2.780808  2.479708  2.804190  ...  2.458569  2.452555  2.372332
# 6        3.713748       NaN       NaN  ...  2.252871  2.384423  2.557687
# 7             NaN  2.833002  2.869716  ...  2.673380  2.676529  2.723465
# 10       2.551153  2.646240  2.503658  ...  2.720197       NaN  2.751794 ...

df2 = pd.read_csv('ml-latest-small/movies.csv')


def get_top_10_recommendations(user_id):
    user_predictions = only_predict_ratings.loc[user_id].dropna().sort_values(ascending=False).head(10)
    top_10_movies = user_predictions.index.tolist()
    top_10_movies_info = df2[df2['movieId'].isin(top_10_movies)]

    result_df = top_10_movies_info[['title', 'genres']]
    return result_df


user_id = 1
top_10_recommendations = get_top_10_recommendations(user_id)
print(top_10_recommendations)
