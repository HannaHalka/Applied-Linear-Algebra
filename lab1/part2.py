import cv2
import numpy as np


def rotate(image, angle):
    # Matrix from
    # https://www.geeksforgeeks.org/python-opencv-getrotationmatrix2d-function/
    picture_width, picture_height = image.shape[0], image.shape[1]
    center = (picture_width // 2, picture_height // 2)
    cx = center[0]
    cy = center[1]
    m11 = np.cos(angle)
    m12 = -np.sin(angle)
    m13 = ((1 - m11) * cx) - (m12 * cy)
    m21 = np.sin(angle)
    m22 = np.cos(angle)
    m23 = (m21 * cx) - ((1 - m22) * cy)
    transform_matrix = np.array([[m11, m12, m13],
                                 [m21, m22, m23]])

    return cv2.warpAffine(image, transform_matrix, (picture_height, picture_width))


def scale(image, scale_factor):
    picture_width, picture_height = image.shape[0], image.shape[1]
    center = (picture_width // 2, picture_height // 2)
    cx = center[0]
    cy = center[1]
    m11 = np.cos(0) * scale_factor
    m12 = -np.sin(0) * scale_factor
    m13 = ((1 - m11) * cx) - (m12 * cy)
    m21 = np.sin(0) * scale_factor
    m22 = np.cos(0) * scale_factor
    m23 = (m21 * cx) - ((1 - m22) * cy)
    transform_matrix = np.array([[m11, m12, m13],
                                 [m21, m22, m23]])
    return cv2.warpAffine(image, transform_matrix, (picture_height, picture_width))


def reflect(image):
    picture_width, picture_height = image.shape[0], image.shape[1]
    transform_matrix = np.array([[0., 1., 0.],
                                 [1., 0., 0.]])
    return cv2.warpAffine(image, transform_matrix, (picture_height, picture_width))


def shear(image, shear_factor, axis='x'):
    picture_width, picture_height = image.shape[0], image.shape[1]
    if axis == 'x':
        transform_matrix = np.array([[1., shear_factor, 0.],
                                     [0., 1., 0.]])
    elif axis == 'y':
        transform_matrix = np.array([[1., 0., 0.],
                                    [shear_factor, 1., 0.]])
    else:
        raise Exception('unknown axis')
    return cv2.warpAffine(image, transform_matrix, (picture_height, picture_width))


def transform(image, matrix):
    picture_width, picture_height = image.shape[0], image.shape[1]
    return cv2.warpAffine(image, matrix, (picture_height, picture_width))


original_image = cv2.imread('OriginalFigures.png')

rotated_image = rotate(original_image, np.pi/3)
cv2.imshow('Rotated', rotated_image)
cv2.waitKey(0)

scaled_image = scale(original_image, 1.32)
cv2.imshow('Scaled', scaled_image)
cv2.waitKey(0)

reflect_image = reflect(original_image)
cv2.imshow('Reflected', reflect_image)
cv2.waitKey(0)

shear_image = shear(original_image, 2, 'y')
cv2.imshow('Sheared', shear_image)
cv2.waitKey(0)

translate_matrix = np.array([[1., 0., 200.],
                            [0., 1., 300.]])
transform_image = transform(original_image, translate_matrix)
cv2.imshow('Translated', transform_image)
cv2.waitKey(0)

original_frog_image = cv2.imread('Frog.jpg')
reflect_image = reflect(original_frog_image)
cv2.imshow('Original Frog', original_frog_image)
cv2.imshow('Reflected Frog', reflect_image)
cv2.waitKey(0)
