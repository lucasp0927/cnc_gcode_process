import re
import numpy as np
def find_para(s,char):
    start = s.find(char)
    if start == -1:
        return None
    else:
        end = s.find(' ',start)
        if end == -1:
            end = len(s)
        return float(s[start+1:end])

def remove_para(s,char):
    start = s.find(char)
    if start != -1:
        end = s.find(' ',start)
        if end == -1:
            end = len(s)
        return re.sub(' +',' ',s[:start]+s[end:]).strip()
    else:
        return s

#Movement command
class G0:
    #rapid move
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def parse(self,code,state):
        flag = False
        if code[0] == 'G':
            if code[0:2] == "G0":
                code = code[2:].strip()
                flag = True
        elif state.last_gcode == "G0":
            flag = True

        if flag:
            x = find_para(code,'X')
            y = find_para(code,'Y')
            z = find_para(code,'Z')
            if x == None:
                x = state.x
            if y == None:
                y = state.y
            if z == None:
                z = state.z
            state.x = x
            state.y = y
            state.z = z
            code = remove_para(code,'X')
            code = remove_para(code,'Y')
            code = remove_para(code,'Z')
            g = G0(x,y,z)
            state.last_gcode = "G0"
        else:
            g = None
        return (code,g,state)

    def code_str(self,):
        output = "G0 X{:.3f} Y{:.3f} Z{:.3f}".format(self.x, self.y, self.z)
        return output

    def flipx(self,):
        self.x = -1*self.x

    def limitz(self,z_limit):
        if self.z > z_limit:
            print("G0 limit z ",self.z," to ",z_limit)
            self.z = z_limit

    def rotate(self, rot_matrix):
        vec = np.array([self.x,self.y,self.z])
        vec_after = rot_matrix.dot(vec)
        self.x = vec_after[0]
        self.y = vec_after[1]
        self.z = vec_after[2]

class G1:
    #rapid move
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def parse(self,code,state):
        flag = False
        if code[0] == 'G':
            if code[0:2] == "G1":
                code = code[2:].strip()
                flag = True
        elif state.last_gcode == "G1":
            flag = True

        if flag:
            x = find_para(code,'X')
            y = find_para(code,'Y')
            z = find_para(code,'Z')
            if x == None:
                x = state.x
            if y == None:
                y = state.y
            if z == None:
                z = state.z
            state.x = x
            state.y = y
            state.z = z
            code = remove_para(code,'X')
            code = remove_para(code,'Y')
            code = remove_para(code,'Z')
            g = G1(x,y,z)
            state.last_gcode = "G1"
        else:
            g = None
        return (code,g,state)

    def code_str(self,):
        output = "G1 X{:.3f} Y{:.3f} Z{:.3f}".format(self.x, self.y, self.z)
        return output

    def flipx(self,):
        self.x = -1*self.x

    def limitz(self,z_limit):
        if self.z > z_limit:
            print("G1 limit z ",self.z," to ",z_limit)
            self.z = z_limit

    def rotate(self, rot_matrix):
        vec = np.array([self.x,self.y,self.z])
        vec_after = rot_matrix.dot(vec)
        self.x = vec_after[0]
        self.y = vec_after[1]
        self.z = vec_after[2]

#state command
class S:
    #spindle speed
    def __init__(self,speed):
        self.speed = speed

    @classmethod
    def parse(self,code,state):
        if "S" in code:
            speed = int(find_para(code,'S'))
            assert(speed != None)
            g=S(speed)
            code = remove_para(code,'S')
            state.spindle_speed = speed
        else:
            g=None
        return(code,g,state)
    def code_str(self,):
        return "S{:d}".format(self.speed)
    def flipx(self,):
        pass
    def limitz(self,z_limit):
        pass
    def rotate(self, rot_matrix):
        pass
class F:
    #feedrate
    def __init__(self,feed):
        self.feed = feed

    @classmethod
    def parse(self,code,state):
        if "F" in code:
            feed = int(find_para(code,'F'))
            assert(feed != None)
            g=F(feed)
            code = remove_para(code,'F')
            state.feed = feed
        else:
            g=None
        return(code,g,state)
    def code_str(self,):
        return "F{:d}".format(self.feed)
    def flipx(self,):
        pass
    def limitz(self,z_limit):
        pass
    def rotate(self, rot_matrix):
        pass
class M30:
    #absolute distance mode
    def __init__(self,):
        pass

    @classmethod
    def parse(self,code,state):
        if "M30" in code:
            g=M30()
            code = code.replace("M30","").strip()
        else:
            g=None
        return(code,g,state)

    def code_str(self,):
        return "M30"
    def flipx(self,):
        pass
    def limitz(self,z_limit):
        pass
    def rotate(self, rot_matrix):
        pass
class M3:
    #absolute distance mode
    def __init__(self,):
        pass

    @classmethod
    def parse(self,code,state):
        if "M3" in code:
            g=M3()
            code = code.replace("M3","").strip()
            state.spindle_on = True
        else:
            g=None
        return(code,g,state)

    def code_str(self,):
        return "M3"
    def flipx(self,):
        pass
    def limitz(self,z_limit):
        pass
    def rotate(self, rot_matrix):
        pass
class M5:
    #absolute distance mode
    def __init__(self,):
        pass

    @classmethod
    def parse(self,code,state):
        if "M5" in code:
            g=M5()
            code = code.replace("M5","").strip()
            state.spindle_on = False
        else:
            g=None
        return(code,g,state)

    def code_str(self,):
        return "M5"
    def flipx(self,):
        pass
    def limitz(self,z_limit):
        pass
    def rotate(self, rot_matrix):
        pass
class G90:
    #absolute distance mode
    def __init__(self,):
        pass

    @classmethod
    def parse(self,code,state):
        if "G90" in code:
            g=G90()
            code = code.replace("G90","").strip()
        else:
            g=None
        return(code,g,state)

    def code_str(self,):
        return "G90"
    def flipx(self,):
        pass
    def limitz(self,z_limit):
        pass
    def rotate(self, rot_matrix):
        pass
class G54:
    #select coordinate system1
    def __init__(self,):
        pass

    @classmethod
    def parse(self,code,state):
        if "G54" in code:
            g=G54()
            code = code.replace("G54","").strip()
        else:
            g=None
        return(code,g,state)

    def code_str(self,):
        return "G54"
    def flipx(self,):
        pass
    def limitz(self,z_limit):
        pass
    def rotate(self, rot_matrix):
        pass
class G17:
    #select XY plane
    def __init__(self,):
        pass

    @classmethod
    def parse(self,code,state):
        if "G17" in code:
            g=G17()
            code = code.replace("G17","").strip()
        else:
            g=None
        return(code,g,state)

    def code_str(self,):
        return "G17"
    def flipx(self,):
        pass
    def limitz(self,z_limit):
        pass
    def rotate(self, rot_matrix):
        pass
class G20:
    #use inches for unit
    def __init__(self,):
        pass

    @classmethod
    def parse(self,code,state):
        if "G20" in code:
            g=G20()
            code = code.replace("G20","").strip()
        else:
            g=None
        return(code,g,state)

    def code_str(self,):
        return "G20"
    def flipx(self,):
        pass
    def limitz(self,z_limit):
        pass
    def rotate(self, rot_matrix):
        pass
class G21:
    #use mm for unit
    def __init__(self,):
        pass

    @classmethod
    def parse(self,code,state):
        if "G21" in code:
            g=G21()
            code = code.replace("G21","").strip()
        else:
            g=None
        return(code,g,state)

    def code_str(self,):
        return "G21"
    def flipx(self,):
        pass
    def limitz(self,z_limit):
        pass
    def rotate(self, rot_matrix):
        pass
class G17:
    #select XY plane
    def __init__(self,):
        pass

    @classmethod
    def parse(self,code,state):
        if "G17" in code:
            g=G17()
            code = code.replace("G17","").strip()
        else:
            g=None
        return(code,g,state)

    def code_str(self,):
        return "G17"
    def flipx(self,):
        pass
    def limitz(self,z_limit):
        pass
    def rotate(self, rot_matrix):
        pass
class G94:
    #feedrate: unit per minute mode
    def __init__(self,):
        pass

    @classmethod
    def parse(self,code,state):
        if "G94" in code:
            g=G94()
            code = code.replace("G94","").strip()
        else:
            g=None
        return(code,g,state)

    def code_str(self,):
        return "G94"
    def flipx(self,):
        pass
    def limitz(self,z_limit):
        pass
    def rotate(self, rot_matrix):
        pass
#ignore command
class T1:
    #rapid move to home
    def __init__(self,):
        pass

    @classmethod
    def parse(self,code,state):
        if "T1" in code:
            g=None
            code = code.replace("T1","").strip()
        else:
            g=None
        return(code,g,state)

    def code_str(self,):
        return "T1"
    def flipx(self,):
        pass
    def limitz(self,z_limit):
        pass
    def rotate(self, rot_matrix):
        pass
class G28:
    #rapid move to home
    def __init__(self,):
        pass

    @classmethod
    def parse(self,code,state):
        if "G28" in code:
            g=None
            code = code.replace("G28","").strip()
        else:
            g=None
        return(code,g,state)

    def code_str(self,):
        return "G28"
    def flipx(self,):
        pass
    def limitz(self,z_limit):
        pass
    def rotate(self, rot_matrix):
        pass
# class G53:
#     def __init__(self,):
#         pass

#     @classmethod
#     def parse(self,code,state):
#         if "G53" in code:
#             g=None
#             code = code.replace("G53","").strip()
#         else:
#             g=None
#         return(code,g,state)

class G91:
    #incremental distance mode
    def __init__(self,):
        pass

    @classmethod
    def parse(self,code,state):
        if "G91" in code:
            g=None
            code = code.replace("G91","").strip()
            code = remove_para(code,'X')
            code = remove_para(code,'Y')
            code = remove_para(code,'Z')
        else:
            g=None
        return(code,g,state)
    def code_str(self,):
        return "G91"
    def flipx(self,):
        pass
    def limitz(self,z_limit):
        pass
    def rotate(self, rot_matrix):
        pass
