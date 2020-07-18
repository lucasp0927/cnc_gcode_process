import sys
sys.path.append(".")
import re
import numpy as np
from refpoints import REFPOINTS
from gcode_parser import GCODEPARSER

if __name__ == "__main__":
    # print("A_ref coordinate: 0.0, 0.0, 0.0")
    # b_ref_string = input("enter B ref coordinate: ")
    # b_ref = np.array(list(map(float,re.split(',+',b_ref_string))))
    # print(b_ref)
    # c_ref_string = input("enter C ref coordinate: ")
    # c_ref = np.array(list(map(float,re.split(',+',c_ref_string))))
    # print(c_ref)

    # # a_real_string = input("enter A real coordinate: ")
    # # a_real = np.array(list(map(float,re.split(',+',a_real_string))))
    # # print(a_real)
    # b_real_string = input("enter B real coordinate: ")
    # b_real = np.array(list(map(float,re.split(',+',b_real_string))))
    # print(b_real)
    # c_real_string = input("enter C real coordinate: ")
    # c_real = np.array(list(map(float,re.split(',+',c_real_string))))
    # print(c_real)
    # ref_points = REFPOINTS(b_ref,c_ref,b_real,c_real)


    gcode_filename = input("enter gcode filename: ")
    gcodes = GCODEPARSER(gcode_filename)
