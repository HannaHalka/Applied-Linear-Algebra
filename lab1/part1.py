import numpy as np
import matplotlib.pyplot as plt


def plot_objects(objects, figure_title):
    plt.figure()
    for object in objects:
        pts = object[0]
        title = object[1]
        plt.plot(pts[:, 0], pts[:, 1], label=title)
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    plt.title(figure_title)
    plt.show()


def rotate(obj, angle): # clockwise, about the origin
    rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                [np.sin(angle), np.cos(angle)]])
    return obj @ rotation_matrix


def scale(obj, scale_factor):
    scale_matrix = np.array([[scale_factor, 0],
                             [0, scale_factor]])
    return obj @ scale_matrix


def reflect(obj, axis='y'):
    if axis == 'x':
        reflection_matrix = np.array([[1, 0],
                                      [0, -1]])
    elif axis == 'y':
        reflection_matrix = np.array([[-1, 0],
                                      [0, 1]])
    else:
        raise Exception('unknown axis')
    return obj @ reflection_matrix


def shear(obj, shear_factor, axis='y'):
    if axis == 'x':
        shear_matrix = np.array([[1, shear_factor],
                                [0, 1]])
    elif axis == 'y':
        shear_matrix = np.array([[1, 0],
                                [shear_factor, 1]])
    else:
        raise Exception('unknown axis')
    return obj @ shear_matrix


def transform(obj, matrix):
    return obj @ matrix


triangle = np.array([[10, 5], [20, 5], [18, 20], [10, 5]])
rectangle = np.array([[-5, -2], [-10, -2], [-10, -5], [-5, -5], [-5, -2]])

plot_objects([[triangle, 'Triangle Original'],
              [rotate(triangle, np.pi/3), 'Triangle Rotated'],
              [rectangle, 'Rectangle Original'],
              [rotate(rectangle, np.pi/3), 'Rectangle Rotated']], 'Rotation')

plot_objects([[triangle, 'Triangle Original'],
              [scale(triangle, 7), 'Triangle Scale'],
              [rectangle, 'Rectangle Original'],
              [scale(rectangle, 7), 'Rectangle Scale']], 'Scale')

plot_objects([[triangle, 'Triangle Original'],
              [reflect(triangle, 'x'), 'Triangle Mirrored'],
              [rectangle, 'Rectangle Original'],
              [reflect(rectangle), 'Rectangle Mirrored']], 'Mirrored')

plot_objects([[triangle, 'Triangle Original'],
              [shear(triangle, 2), 'Triangle Sheared'],
              [rectangle, 'Rectangle Original'],
              [shear(rectangle, 2, 'x'), 'Rectangle Sheared']], 'Sheared')

plot_objects([[triangle, 'Triangle Original'],
              [transform(triangle, [[-2, -3], [-3, -2]]), 'Triangle Transformed'],
              [rectangle, 'Rectangle Original'],
              [transform(rectangle, [[-3, -2], [-2, -3]]), 'Rectangle Transformed']], 'Transformed')
