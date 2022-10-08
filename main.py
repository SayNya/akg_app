from tkinter import Tk

from src.model_object import ModelObject
from src.parser import Parser
from src.tkinter_window import Blender


def main():
    parser = Parser()
    parser.parse(r"D:\projects\akg_app\media\ob.obj")

    model_object = ModelObject(local_cords=parser.v_array, indices=parser.f_array)

    root = Tk()
    Blender(model_object)
    root.mainloop()


if __name__ == '__main__':
    main()
