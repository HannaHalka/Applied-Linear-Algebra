import numpy as np


def eigen(matrix):
    eigen_values, eigen_vectors = np.linalg.eig(matrix)

    for i in range(len(eigen_values)):
        v = eigen_vectors[:, i]
        lambda_v = eigen_values[i]

        product_Av = np.dot(matrix, v)
        product_lambda_v_v = lambda_v * v

        if np.allclose(product_Av, product_lambda_v_v):
            print(f"Eigen value : {lambda_v}",
                  f"Eigen vector : {v}",
                  f"equality ok ", sep="\n")
        else:
            print(f"equality not okay ")

    return eigen_values, eigen_vectors


matrix = np.array([[7, 8],
                   [2, 9]])

eigen_values, eigen_vectors = eigen(matrix)
