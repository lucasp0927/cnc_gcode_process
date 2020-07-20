import numpy as np
from gcode_command import G0,G1,G90,G17,G20,G21,G94,G28,G91,T1,S,M3,G54,F,M5,M30
#TODO: issue parsing command that are substring of other command. M3, M30
class STATE:
    def __init__(self, x, y, z, feed, spindle_speed, spindle_on, last_gcode):
        self.x = x
        self.y = y
        self.z = z
        self.feed = feed
        self.spindle_speed = spindle_speed
        self.spindle_on = spindle_on
        self.last_gcode = last_gcode

    def print_state(self,):
        print("X: ",self.x)
        print("Y: ",self.y)
        print("Z: ",self.z)
        print("feed: ",self.feed)
        print("spindle_speed: ",self.spindle_speed)
        print("spindle_on: ",self.spindle_on)
        print("last_gcode: ", self.last_gcode)

STATE_COMMAND_LIST = [G90, G94, G17, G20, G21, G28, G91, T1, S, M30, M3, M5, G54, F]
#MOTION_COMMAND = ["G0", "G1", "G2", "G3", "G4"]
MOTION_COMMAND_LIST = [G0,G1]
class GCODE_LINE:
     def __init__(self, fullcode, state):
         (code, comment) = self.parse_comment(fullcode)
         self.code = code
         self.comment = comment
         self.start_state = state
         self.parse()

     def parse_comment(self, fullcode):
         s = fullcode
         if s.find("(") == -1 and s.find(")") == -1: # no comment
             code = fullcode
             comment = ""
         elif s.find("(") != -1 and s.find(")") != -1: #comment
             code = s[:s.find("(")] + s[s.find(")")+1:]
             comment = s[s.find("(")+1:s.find(")")]
         else:
             raise ValueError('Malformed comment.')
         code = code.upper()
         return (code.strip(), comment.strip())

     def parse(self,):
         self.gcode = []
         code = self.code
         state = self.start_state

         if code.strip() == "":
             self.end_state = state
             return

         for command in STATE_COMMAND_LIST:
             (code,g,state) = command.parse(code,state)
             if g != None:
                 self.gcode.append(g)
             if code.strip() == "":
                 break
         else:
             for command in MOTION_COMMAND_LIST:
                 (code,g,state) = command.parse(code,state)
                 if g != None:
                     self.gcode.append(g)
                 if code.strip() == "":
                     break
             else:
                 raise ValueError('Unkown command.', code)
         self.end_state = state

     def code_str(self,):
         output = ""
         for g in self.gcode:
             output += g.code_str()+" "
         if self.comment != "":
             output += "("+self.comment+")"
         return output.strip()

     def rotate(self, rot_matrix):
         for g in self.gcode:
             g.rotate(rot_matrix)

class GCODEPARSER:
    def __init__(self, filename):
        try:
            f = open(filename)
            self.line_num = 0
            self.gcodes = self.read_gcode_file(f)
        except FileNotFoundError:
            print("File not accessible")
        finally:
            f.close()

    def read_gcode_file(self, f):
        lines = f.readlines()
        self.line_num = len(lines)

        gcodes = []
        state = STATE(0,0,0,0,0,False,None)
        for line in lines:
            gl = GCODE_LINE(line,state)
            state = gl.end_state
            gcodes.append(gl)

        print(self.line_num)
        print(len(gcodes))
        # for line in lines:
        #     print(line)
        return gcodes

    def output_gcode_file(self, filename):
        f = open(filename,'w')
        for gc in self.gcodes:
            f.write(gc.code_str()+"\n")
        f.close()

    def rotate(self, rot_matrix):
        for gc in self.gcodes:
            gc.rotate(rot_matrix)
