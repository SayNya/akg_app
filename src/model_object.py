import numpy as np

from src.utils.matrices import get_model_matrix, get_viewport_matrix, get_projection_matrix, get_view_matrix
from src.utils.utils import convert_point


class ModelObject:
    def __init__(self, local_cords, indices):
        self.local_cords = np.array(local_cords)
        self.indices = indices
        self.world_cords = None
        self.window_cords = None

    def calc_world_cords(self, x_tr=0, y_tr=0, z_tr=0, x_ang=0, y_ang=0, z_ang=0, scale=1):
        self.world_cords = np.array(
            [get_model_matrix(x_tr, y_tr, z_tr, x_ang, y_ang, z_ang, scale) @ cord for cord in self.local_cords]
        )

    def calc_window_cords(self, eye, target, fov=np.pi / 4, x_min=0, y_min=0):
        window_matrix = (
                get_viewport_matrix(x_min, y_min) @
                get_projection_matrix(fov) @
                get_view_matrix(eye, target)
        )
        self.window_cords = np.array([convert_point(cord, window_matrix) for cord in self.world_cords])
