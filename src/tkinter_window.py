from itertools import combinations
from tkinter import Frame, Canvas

import numpy as np

from src.model_object import ModelObject
from src.utils.settings import settings


class Window(Canvas):
    def __init__(self, model_object: ModelObject):
        super().__init__(
            width=settings.width, height=settings.height,
            background="white", highlightthickness=0
        )
        self.eye = np.array([0, 0, 2], dtype=np.float32)
        self.target = np.array([0, 0, 0], dtype=np.float32)

        self.model_object = model_object
        self.draw()

        self.bind_all("<Key>", self.on_key_pressed)
        self.pack()

    def on_key_pressed(self, e):
        key = e.keysym
        match key:
            case "Right":
                self.eye += np.array([-0.1, 0, 0])
                self.target += np.array([-0.1, 0, 0])
            case "Left":
                self.eye += np.array([0.1, 0, 0])
                self.target += np.array([0.1, 0, 0])
            case "Down":
                self.eye += np.array([0, -0.1, 0])
                self.target += np.array([0, -0.1, 0])
            case "Up":
                self.eye += np.array([0, 0.1, 0])
                self.target += np.array([0, 0.1, 0])
            case "w":
                self.eye += np.array([0, 0, -0.1])
                self.target += np.array([0, 0, 0.1])
            case "s":
                self.eye += np.array([0, 0, 0.1])
                self.target += np.array([0, 0, -0.1])

        self.draw()

    def draw(self):
        self.delete("all")

        self.model_object.calc_world_cords()
        self.model_object.calc_window_cords(self.eye, self.target)

        for indices in self.model_object.indices:
            for first, second in combinations(indices, 2):
                start = self.model_object.window_cords[first]
                end = self.model_object.window_cords[second]

                self.create_line(
                    start[0],
                    start[1],
                    end[0],
                    end[1],
                    fill='black'
                )


class Blender(Frame):
    def __init__(self, model_object: ModelObject):
        super().__init__()
        self.master.title("Blender")
        self.board = Window(model_object)
        self.pack()
