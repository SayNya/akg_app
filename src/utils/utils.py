import time
from functools import wraps

import numpy as np
from numpy.linalg import norm


def normalize(vector):
    return vector / norm(vector)


def convert_point(point, matrix):
    new_point = matrix @ point
    return np.resize(new_point / new_point[3], 3)


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result

    return timeit_wrapper
