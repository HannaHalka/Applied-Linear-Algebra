import numpy as np


def encrypt_message(message, key_matrix):
    message_vector = np.array([ord(char) for char in message])
    eigenvalues, eigenvectors = np.linalg.eig(key_matrix)
    # A = PdP^-1
    diagonalized_key_matrix = np.dot(np.dot(eigenvectors, np.diag(eigenvalues)), np.linalg.inv(eigenvectors))
    encrypt_vector = np.dot(diagonalized_key_matrix, message_vector)
    return encrypt_vector


def decrypt_message(encrypted_vector, key_matrix):
    eigenvalues, eigenvectors = np.linalg.eig(key_matrix)
    diagonalized_key_matrix = np.dot(np.dot(eigenvectors, np.diag(eigenvalues)), np.linalg.inv(eigenvectors))
    diagonalized_key_matrix_inv = np.linalg.inv(diagonalized_key_matrix)
    decrypted_vector = np.dot(diagonalized_key_matrix_inv, encrypted_vector)
    decrypted_message = ''.join(chr(int(np.round(num))) for num in decrypted_vector)
    return decrypted_message


message = 'The quick brown fox jumps over the lazy dog'
key_matrix = np.random.randint(0, 256, (len(message), len(message)))
encrypted = encrypt_message(message, key_matrix)
print(decrypt_message(encrypted, key_matrix))