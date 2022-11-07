import sys
from tkinter import Tk

from PyQt6.QtWidgets import QApplication

from src.model_object import ModelObject
from src.parser import Parser
from src.qt_window import Blender


def main():
    parser = Parser()
    parser.parse(r"D:\projects\akg_app\media\ob.obj")

    model_object = ModelObject(local_cords=parser.v_array, indices=parser.f_array)

    app = QApplication([])
    ex = Blender(model_object)
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
