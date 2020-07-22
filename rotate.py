import sys
sys.path.append(".")
import re
import numpy as np
import argparse
from refpoints import REFPOINTS
from gcode_parser import GCODEPARSER

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Gunpla Gcode Processing Program")

    # add argument
    parser.add_argument("filename", type=str, nargs = 1, metavar = "file_name",
                        default=None, help = "gcode (.nc) file to process.")

    parser.add_argument("-r","--rotate",default=False,action='store_true')
    parser.add_argument("-x","--flipx",default=False,action='store_true')
    parser.add_argument("-z","--limitz",type=float,nargs=1)
    parser.add_argument("-s","--speed",type=int,nargs=1)

    # parse the arguments from standard input
    args = parser.parse_args()
    gcode_filename = args.filename[0]

    if args.rotate:
        print("A_ref coordinate: 0.0, 0.0, 0.0")
        b_ref_string = input("enter B ref coordinate: ")
        b_ref = np.array(list(map(float,re.split(',+',b_ref_string))))
        print(b_ref)
        c_ref_string = input("enter C ref coordinate: ")
        c_ref = np.array(list(map(float,re.split(',+',c_ref_string))))
        print(c_ref)

        # a_real_string = input("enter A real coordinate: ")
        # a_real = np.array(list(map(float,re.split(',+',a_real_string))))
        # print(a_real)
        b_real_string = input("enter B real coordinate: ")
        b_real = np.array(list(map(float,re.split(',+',b_real_string))))
        print(b_real)
        c_real_string = input("enter C real coordinate: ")
        c_real = np.array(list(map(float,re.split(',+',c_real_string))))
        print(c_real)
        ref_points = REFPOINTS(b_ref,c_ref,b_real,c_real)

        gcodes = GCODEPARSER(gcode_filename)
        gcodes.rotate(ref_points.rot_matrix)
        gcodes.output_gcode_file(gcode_filename.replace(".nc","_rotate.nc"))

    if args.flipx:
        gcodes = GCODEPARSER(gcode_filename)
        gcodes.flipx()
        gcodes.output_gcode_file(gcode_filename.replace(".nc","_flipx.nc"))

    if args.limitz != None:
        z_limit = args.limitz[0]
        gcodes = GCODEPARSER(gcode_filename)
        gcodes.limitz(z_limit)
        gcodes.output_gcode_file(gcode_filename.replace(".nc","_limitz.nc"))

    if args.speed != None:
        speed = args.speed[0]
        gcodes = GCODEPARSER(gcode_filename)
        gcodes.setspeed(speed)
        gcodes.output_gcode_file(gcode_filename.replace(".nc","_speed.nc"))
