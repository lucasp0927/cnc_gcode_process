class GCODE:
    def __init__(self, code):
        self.full_code = code
        self.parse_comment()

    def parse_comment(self,):
        s = self.full_code
        if s.find("(") == -1 and s.find(")") == -1: # no comment
            self.code = self.full_code
            self.comment = ""
        elif s.find("(") != -1 and s.find(")") != -1: #comment
            self.code = s[:s.find("(")] + s[s.find(")")+1:]
            self.comment = s[s.find("(")+1:s.find(")")]
        else:
            raise ValueError('Malformed comment.')
    def printcode(self,):
        print(self.code)
        print(self.comment)


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

    def parse_gcode(self, code):
        return GCODE(code)

    def read_gcode_file(self, f):
        lines = f.readlines()
        self.line_num = len(lines)

        #gcodes = [GCODE() for i in range(self.line_num)]
        gcodes = list(map(lambda x: self.parse_gcode(x), lines))

        print(self.line_num)
        print(len(gcodes))
        # for line in lines:
        #     print(line)
        return gcodes
