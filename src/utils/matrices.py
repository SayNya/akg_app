import numpy as np

from src.utils.settings import settings
from src.utils.utils import normalize


def get_translation_matrix(x, y, z):
    return np.array([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ])


def get_scale_matrix(scale):
    return np.array([
        [scale, 0, 0, 0],
        [0, scale, 0, 0],
        [0, 0, scale, 0],
        [0, 0, 0, 1],
    ])


def get_x_rotate_matrix(angle):
    return np.array([
        [1, 0, 0, 0],
        [0, np.cos(angle), -np.sin(angle), 0],
        [0, np.sin(angle), np.cos(angle), 0],
        [0, 0, 0, 1],
    ])


def get_y_rotate_matrix(angle):
    return np.array([
        [np.cos(angle), 0, np.sin(angle), 0],
        [0, 1, 0, 0],
        [-np.sin(angle), 0, np.cos(angle), 0],
        [0, 0, 0, 1],
    ])


def get_z_rotate_matrix(angle):
    return np.array([
        [np.cos(angle), -np.sin(angle), 0, 0],
        [np.sin(angle), np.cos(angle), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])


def get_model_matrix(x_translation, y_translation, z_translation, x_angle, y_angle, z_angle, scale):
    return (
            get_translation_matrix(x_translation, y_translation, z_translation) @
            get_x_rotate_matrix(z_angle) @
            get_y_rotate_matrix(y_angle) @
            get_z_rotate_matrix(x_angle) @
            get_scale_matrix(scale)
    )


def get_view_matrix(eye, pitch, yaw):
    cos_pitch = np.cos(pitch)
    sin_pitch = np.sin(pitch)
    cos_yaw = np.cos(yaw)
    sin_yaw = np.sin(yaw)

    x_axis = np.array([cos_yaw, 0, -sin_yaw])
    y_axis = np.array([sin_yaw * sin_pitch, cos_pitch, cos_yaw * sin_pitch])
    z_axis = np.array([sin_yaw * cos_pitch, -sin_pitch, cos_pitch * cos_yaw])

    return np.array([
        [x_axis[0], x_axis[1], x_axis[2], -(x_axis @ eye)],
        [y_axis[0], y_axis[1], y_axis[2], -(y_axis @ eye)],
        [z_axis[0], z_axis[1], z_axis[2], -(z_axis @ eye)],
        [0, 0, 0, 1],
    ])


def get_projection_matrix(fov, z_near=1, z_far=10):
    return np.array([
        [1 / (settings.width / settings.height * np.tan(fov / 2)), 0, 0, 0],
        [0, 1 / np.tan(fov / 2), 0, 0],
        [0, 0, z_far / (z_near - z_far), (z_near * z_far) / (z_near - z_far)],
        [0, 0, -1, 0],
    ])


def get_projection_matrix_test():
    z_near = 0
    z_far = 255
    return np.array([
        [2 / settings.width, 0, 0, 0],
        [0, 2 / settings.height, 0, 0],
        [0, 0, 1 / (z_near - z_far), z_near / (z_near - z_far)],
        [0, 0, 0, 1],
    ])


def get_viewport_matrix(x_min, y_min):
    return np.array([
        [settings.width / 2, 0, 0, x_min + (settings.width / 2)],
        [0, -settings.height / 2, 0, y_min + (settings.height / 2)],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])
