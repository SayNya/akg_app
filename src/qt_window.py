import time
from itertools import combinations
from math import ceil

import numpy as np
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import Qt

from src.model_object import ModelObject
from src.utils.settings import settings
from src.utils.utils import timeit


class Blender(QtWidgets.QWidget):
    def __init__(self, model_object: ModelObject):
        super().__init__()
        self.initUI()

        self.image = QtGui.QImage(self.size(), QtGui.QImage.Format.Format_RGB32)
        self.image.fill(Qt.GlobalColor.black)
        self.painter = QtGui.QPainter(self.image)

        self.brushSize = 1
        self.brushStyle = Qt.PenStyle.SolidLine
        self.brushCap = Qt.PenCapStyle.RoundCap
        self.brushJoin = Qt.PenJoinStyle.RoundJoin
        self.brushColor = Qt.GlobalColor.white

        self.eye = np.array([0, 0, 2], dtype=np.float32)

        self.pitch = 0
        self.yaw = 0

        self.model_object = model_object
        self.model_object.calc_world_cords()
        self.model_object.calc_window_cords(self.eye, self.pitch, self.yaw)
        self.model_object.calc_lighting_intensity()

    def initUI(self):
        self.setMinimumSize(settings.width, settings.height)
        self.setMaximumSize(settings.width, settings.height)
        self.setWindowTitle('Blender')
        self.show()

    def paintEvent(self, e):
        canvas_painter = QtGui.QPainter(self)
        canvas_painter.drawImage(self.rect(), self.image, self.image.rect())

    def clear(self):
        self.image.fill(Qt.GlobalColor.black)
        self.update()

    def dda(self, x0, y0, x1, y1):
        sub_x = (x1 - x0)
        sub_y = (y1 - y0)
        l = round(abs(sub_x) + 1) if abs(sub_x) > abs(sub_y) else round(abs(sub_y) + 1)
        x = x0
        y = y0
        for i in range(l):
            self.painter.drawPoint(round(x), round(y))
            x += sub_x / l
            y += sub_y / l

    def draw_hr_line(self, x1, x2, y):
        start, end = (x1, x2) if x1 < x2 else (x2, x1)
        for i in range(start, end + 1):
            self.painter.drawPoint(i, y)

    def draw_triangle(self, points):
        p1, p2, p3, *_ = points

        if p1[1] == p3[1]:
            self.fill_top_triangle(p1, p2, p3)
        elif p1[1] == p2[1]:
            self.fill_bottom_triangle(p1, p2, p3)
        else:
            x = p1[0] + ((p2[1] - p1[1]) / (p3[1] - p1[1])) * (p3[0] - p1[0])
            y = p2[1]

            self.fill_top_triangle(p1, p2, (x, y))
            self.fill_bottom_triangle(p2, (x, y), p3)

    def fill_bottom_triangle(self, p1, p2, p3):
        invslope_1 = (p3[0] - p1[0]) / (p3[1] - p1[1])
        invslope_2 = (p3[0] - p2[0]) / (p3[1] - p2[1])

        cur_x_1 = cur_x_2 = p3[0]

        scanline_y = p3[1]
        while scanline_y > p1[1]:
            self.draw_hr_line(round(cur_x_1), round(cur_x_2), scanline_y)
            cur_x_1 -= invslope_1
            cur_x_2 -= invslope_2
            scanline_y -= 1

    def fill_top_triangle(self, p1, p2, p3):
        invslope_1 = (p2[0] - p1[0]) / (p2[1] - p1[1])
        invslope_2 = (p3[0] - p1[0]) / (p3[1] - p1[1])

        cur_x_1 = cur_x_2 = p1[0]

        scanline_y = round(p1[1])
        while scanline_y <= p2[1]:
            self.draw_hr_line(round(cur_x_1), round(cur_x_2), scanline_y)
            cur_x_1 += invslope_1
            cur_x_2 += invslope_2
            scanline_y += 1

    def new_triangle(self, points):
        p0, p1, p2, *_ = points
        total_height = p2[1] - p0[1]
        for i in range(total_height):
            second_half = i > (p1[1] - p0[1]) or p1[1] == p0[1]
            segment_height = p2[1] - p1[1] if second_half else p1[1] - p0[1]
            alpha = i / total_height
            beta = (i - (p1[1] - p0[1] if second_half else 0)) / segment_height

            a = p0 + np.ceil((p2 - p1) * alpha).astype(np.int32)
            b = p1 + np.ceil((p2 - p1) * beta).astype(np.int32) if second_half else p0 + np.ceil((p1 - p0) * beta).astype(np.int32)
            if a[0] > b[0]:
                a, b = b, a
            for j in range(a[0], b[0] + 1):
                phi = j - a[0] / b[0] - a[0] if a[0] != b[0] else 1
                p = a + np.ceil((b - a) * phi).astype(np.int32)
                p[0] = j
                p[1] = p0[1] + i
                self.painter.drawPoint(p[0], p[1])

    def keyPressEvent(self, event):
        self.clear()
        key = event.key()
        match key:
            case Qt.Key.Key_Right:
                self.eye += np.array([np.cos(self.yaw) * 0.6, 0, -np.sin(self.yaw) * 0.6])
            case Qt.Key.Key_Left:
                self.eye += np.array([-np.cos(self.yaw) * 0.6, 0, np.sin(self.yaw) * 0.6])
            case Qt.Key.Key_Down:
                self.eye += np.array([0, -0.6, 0])
            case Qt.Key.Key_Up:
                self.eye += np.array([0, 0.6, 0])
            case Qt.Key.Key_Q:
                self.yaw += np.pi / 8
            case Qt.Key.Key_R:
                self.pitch += np.pi / 8
            case Qt.Key.Key_F:
                self.pitch -= np.pi / 8
            case Qt.Key.Key_E:
                self.yaw -= np.pi / 8
            case Qt.Key.Key_W:
                self.eye += np.array([-np.sin(self.yaw) * 0.6, np.sin(self.pitch), -np.cos(self.yaw) * 0.6])
            case Qt.Key.Key_S:
                self.eye += np.array([np.sin(self.yaw) * 0.6, -np.sin(self.pitch), np.cos(self.yaw) * 0.6])

        self.model_object.calc_world_cords()
        self.model_object.calc_window_cords(self.eye, self.pitch, self.yaw)
        self.model_object.calc_lighting_intensity()

        self.painter.setPen(
            QtGui.QPen(
                QtGui.QColor.fromRgb(255, 255, 255),
                self.brushSize,
                self.brushStyle,
                self.brushCap,
                self.brushJoin
            )
        )
        print(self.eye)
        self.draw_points()
        # for intensity, indices in zip(self.model_object.lighting_intensity, self.model_object.triangle_indices):
        #     color = round(255 * intensity)
        #     if color > 0:
        #         self.painter.setPen(
        #             QtGui.QPen(
        #                 QtGui.QColor.fromRgb(color, color, color),
        #                 self.brushSize,
        #                 self.brushStyle,
        #                 self.brushCap,
        #                 self.brushJoin)
        #         )
        #         cords = sorted(np.array([np.resize(self.model_object.window_cords[idx], 3) for idx in indices]), key=lambda i: i[1])
        #         self.new_triangle(cords)
        self.update()

    def draw_points(self):
        index_set = set()
        for indices in self.model_object.triangle_indices:
            for first, second in combinations(indices, 2):
                if (first, second) in index_set:
                    continue
                index_set.add((first, second))
                index_set.add((second, first))
                start = self.model_object.window_cords[first]
                end = self.model_object.window_cords[second]
                x0, y0, *_ = start
                x1, y1, *_ = end
                first_point = (0 <= x0 <= settings.width and 0 <= y0 <= settings.height)
                second_point = (0 <= x1 <= settings.width and 0 <= y1 <= settings.height)
                if not (first_point or second_point):
                    continue
                sub_x = (x1 - x0)
                sub_y = (y1 - y0)
                l = round(abs(sub_x) + 1) if abs(sub_x) > abs(sub_y) else round(abs(sub_y) + 1)
                x = x0
                y = y0
                for i in range(l):
                    self.painter.drawPoint(round(x), round(y))
                    x += sub_x / l
                    y += sub_y / l
