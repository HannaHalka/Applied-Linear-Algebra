import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds
import matplotlib.pyplot as plt


df = pd.read_csv('ml-latest-small/ratings.csv')
# print(df.head())
#    userId  movieId  rating  timestamp
# 0       1        1     4.0  964982703
# 1       1        3     4.0  964981247
# 2       1        6     4.0  964982224
# 3       1       47     5.0  964983815
# 4       1       50     5.0  964982931
# print(df.shape[0])
# 100836

ratings_matrix = df.pivot(index='userId', columns='movieId', values='rating')
# print(ratings_matrix.head())
#  movieId  1       2       3       4       ...  193583  193585  193587  193609
# userId                                   ...
# 1           4.0     NaN     4.0     NaN  ...     NaN     NaN     NaN     NaN
# 2           NaN     NaN     NaN     NaN  ...     NaN     NaN     NaN     NaN
# 3           NaN     NaN     NaN     NaN  ...     NaN     NaN     NaN     NaN
# 4           NaN     NaN     NaN     NaN  ...     NaN     NaN     NaN     NaN
# 5           4.0     NaN     NaN     NaN  ...     NaN     NaN     NaN     NaN

# keep users with 200+ ratings, keep movis with 100+ ratings
ratings_matrix = ratings_matrix.dropna(thresh=100, axis=0)
ratings_matrix = ratings_matrix.dropna(thresh=50, axis=1)

# replace NaN with average rating which is 2.5
ratings_matrix_filled = ratings_matrix.fillna(2.5)
# print(ratings_matrix_filled.head())
#  movieId  260   296   356   1196  1210  2571
# userId
# 1         5.0   3.0   4.0   5.0   5.0   5.0
# 4         5.0   1.0   2.5   5.0   2.5   1.0
# 6         2.5   2.0   5.0   2.5   2.5   2.5
# 18        4.0   4.0   4.5   4.0   4.5   4.5
# 19        4.0   2.5   2.0   4.0   3.0   4.0

R = ratings_matrix_filled.values
# print(R)
# [[5.  3.  4.  5.  5.  5. ]
#  [5.  1.  2.5 5.  2.5 1. ]
#  [2.5 2.  5.  2.5 2.5 2.5]...

# average rating given by user across all movies they have rated
user_ratings_mean = np.mean(R, axis=1)
# print(user_ratings_mean)
# [4.5        2.83333333 2.83333333 4.25       3.25       2.5 ...

# demeaning the data
R_demeaned = R - user_ratings_mean.reshape(-1, 1)
# print(R_demeaned)
# [[ 0.5        -1.5        -0.5         0.5         0.5         0.5       ]
#  [ 2.16666667 -1.83333333 -0.33333333  2.16666667 -0.33333333 -1.83333333]
#  [-0.33333333 -0.83333333  2.16666667 -0.33333333 -0.33333333 -0.33333333]...

U, sigma, Vt = svds(R_demeaned, k=3)
# print(U)
# [[-0.11701519 -0.0486775   0.10423191]
#  [ 0.11847179 -0.08575014  0.25393107]
#  [ 0.04659884 -0.2114704  -0.06167357]...

# visualisation of firs 15 users
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')  # 111 - 1 row, 1 column, 1 subplot
ax.scatter(U[:15, 0], U[:15, 1], U[:15, 2], c='b', marker='o')
ax.set_title('user preferences similarity')
plt.show()

# visualisation of firs 15 films
V = Vt.T
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')  # 111 - 1 row, 1 column, 1 subplot
ax.scatter(V[:15, 0], V[:15, 1], V[:15, 2], c='r', marker='*')
ax.set_title('film preferences similarity')
plt.show()
