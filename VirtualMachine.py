from quad_generator import Variable, Quadruple, QuadGenerator
from symbol_table import FunctionsDir
from Memory import Memory

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def RepresentsDouble(s):
    try: 
        float(s)
        return True
    except ValueError:
        return False

class VirtualMachine():
    def __init__(self, dir_func):
        self.quadruples = []
        self.pc = 0
        self.dir_func = dir_func
        self.temporal = {}
        self.memory = Memory()
        self.scope = 'main'

    def readFiles(self):
        cont = 0
        f = open('output.cob', 'r')
        for line in f:
            # print(line),
            q = line[1:-2].split(',')
            quad = Quadruple(cont, q[0], q[1], q[2], q[3])
            cont += 1
            self.quadruples.append(quad)
        f.close()
    
    def run(self):
        self.readFiles()

        while self.quadruples[self.pc].op != 'END':
            quad = self.quadruples[self.pc]
            
            op = quad.op
            if op == 'Print':

                dir = quad.left_operand[1:]
                print(self.dir_func.get_var(dir)[0])
                # print("{0}{1}").format(quad.left_operand, quad.right_operand[2:-1])

            #basic operations +, - , *, /
            elif op == '+':
                pass
                
            elif op == '-':
                pass
            elif op == '*':
                pass
            elif op == '/':
                pass
            elif op == '=':
                pass
                
                #constantes
                left = quad.left_operand
                if RepresentsInt(left):
                    self.memory.integers.constants[left] = int(left)
                elif RepresentsDouble(left):
                    self.memory.doubles.constants[left] = float(left)
                elif left[0] == "\"":
                    self.memory.strings.constants[left[1:-1]] = left[1:-1]
                elif left == 'true':
                    self.memory.booleans.constants[left] = True
                elif left == 'false':
                    self.memory.booleans.constants[left] = False
                else:
                    self.memory.

            #logic operations
            elif op == 'and':
                pass
            elif op == 'or':
                pass
            elif op == '>=':
                pass
            elif op == '<=':
                pass
            elif op == '==':
                pass
            elif op == '>':
                pass
            elif op == '<':
                pass
            # gotos
            elif op == 'Goto':
                self.pc = int(self.quadruples[self.pc].res)
                continue
            elif op == 'GotoF':
                dir = quad.left_operand
                # if memory.getVal(dir) == 'false':
                #     self.pc = quad.res
            elif op == 'GotoV':
                dir = quad.left_operand
                # if memory.getVal(dir) == 'true':
                #     self.pc = quad.res

            # print self.quadruples[self.pc].printeame()
            self.pc += 1

        def getVal(dir):
            
            return self.dir_func.get(dir, None)