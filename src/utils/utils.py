import numpy as np
from numpy.linalg import norm


def normalize(vector):
    return vector / norm(vector)


def convert_point(point, matrix):
    new_point = matrix @ point
    return np.resize(new_point / new_point[3], 3)
