import numpy as np


def svd_matrix(matrix):
    transposed_matrix = matrix.transpose()

    u_matrix = np.dot(matrix, transposed_matrix)
    eigenvalues_u, eigenvectors_u = np.linalg.eig(u_matrix)  # matrix ia already normalized
    sorted_eigenvalues = np.argsort(eigenvalues_u)[::-1]
    u_matrix = eigenvectors_u[:, sorted_eigenvalues]
                    # module
    sigma = np.sqrt(np.abs(eigenvalues_u[sorted_eigenvalues]))

    v_matrix = []
    for i in range(len(sigma)):
        if sigma[i] > 1e-10:  # avoid zero division
            v_matrix.append(np.dot(transposed_matrix, u_matrix[:, i]) / sigma[i])
        else:
            v_matrix.append(np.zeros(transposed_matrix[:, 0]))

    v_matrix = np.array(v_matrix).transpose()  # for sigma_matrix

    sigma_matrix = np.zeros((u_matrix.shape[0], v_matrix.shape[1]))
    for i in range(min(u_matrix.shape[0], v_matrix.shape[1])):
        sigma_matrix[i, i] = sigma[i]

    return u_matrix, sigma_matrix, v_matrix.transpose()


matrix_a = np.array([[0, 2, 0],
                     [1, 0, 6]])

u, sigma_matrix, v_t = svd_matrix(matrix_a)

a_reconstructed = u @ sigma_matrix @ v_t
print(a_reconstructed)
