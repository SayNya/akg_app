import numpy as np


class Parser:
    def __init__(self):
        self.f_array = None
        self.vn_array = None
        self.vt_array = None
        self.v_array = None

    def parse(self, filename: str):
        v_array = []
        vt_array = []
        vn_array = []
        f_array = []
        with open(filename, "r") as file_object:
            lines = file_object.readlines()
            for line in lines:
                if not line.strip():
                    continue
                split_line = line.split()

                if split_line[0] == "v":
                    cords = [float(i) for i in split_line[1:]]
                    cords.append(1)
                    v_array.append(cords)
                elif split_line[0] == "vt":
                    vt_array.append([float(i) for i in split_line[1:]])
                elif split_line[0] == "vn":
                    vn_array.append([float(i) for i in split_line[1:]])
                elif split_line[0] == "f":
                    f_array.append([int(i.split("/")[0]) - 1 for i in split_line[1:]])

        self.v_array = np.array(v_array)
        self.vt_array = np.array(vt_array)
        self.vn_array = np.array(vn_array)
        self.f_array = np.array(f_array)
