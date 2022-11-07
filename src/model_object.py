import numpy as np
from numpy.linalg import multi_dot

from src.utils.matrices import get_model_matrix, get_viewport_matrix, get_projection_matrix, get_view_matrix, \
    get_projection_matrix_test
from src.utils.settings import settings

from src.utils.utils import convert_point, normalize, timeit


class ModelObject:
    def __init__(self, local_cords, indices):
        self.local_cords = local_cords
        self.triangle_indices = indices
        self.world_cords = None
        self.world_cords_test = None
        self.window_cords = None
        self.lighting_intensity = None

    def calc_world_cords(self, x_tr=0, y_tr=0, z_tr=0, x_ang=0, y_ang=0, z_ang=0, scale=1):
        self.world_cords = np.dot(get_model_matrix(x_tr, y_tr, z_tr, x_ang, y_ang, z_ang, scale), self.local_cords.T).T

    def calc_window_cords(self, eye, pitch, yaw, fov=np.pi / 4, x_min=0, y_min=0):
        window_matrix = (
                get_viewport_matrix(x_min, y_min) @
                get_projection_matrix(fov) @
                get_view_matrix(eye, pitch, yaw)
        )
        b = np.dot(window_matrix, self.world_cords.T).T
        b /= b.T[3][:, None]
        self.window_cords = b
        # temp_list = []
        # for cord in self.world_cords:
        #     new_cord = np.array([
        #         (cord[0] + 1) * settings.width / 2,
        #         (cord[1] + 1) * settings.height / 2,
        #         (cord[2] + 1) * 255 / 2,
        #     ])
        #     temp_list.append(new_cord)
        # self.window_cords = np.array(temp_list).astype(np.int32)

    def calc_lighting_intensity(self):
        light_dir = np.array([0, 0, 1])
        lighting_intensity = np.zeros(len(self.triangle_indices))
        for li_idx, indices in enumerate(self.triangle_indices):
            points = [np.resize(self.world_cords[idx], 3) for idx in indices]
            lighting_intensity[li_idx] = light_dir @ normalize(
                np.cross((points[2] - points[0]), (points[2] - points[1])))
        self.lighting_intensity = lighting_intensity
