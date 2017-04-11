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
                #TODO agregar el segundo parametro del print
                val = self.memory.get_val(quad.left_operand)
                print(val)
            #basic operations +, - , *, /
            elif op == '+':
                self.execute(quad, '+')
            elif op == '-':
                self.execute(quad, '-')
            elif op == '*':
                pass
            elif op == '/':
                pass
            elif op == '=':
                left = quad.left_operand.rstrip().lstrip()
                valor = self.get_memory_val(left)
                self.memory.set_val(quad.res.rstrip().lstrip(), valor)

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

    def get_memory_val(self, base):
        if RepresentsInt(base):
            if self.memory.integers.constants.get(base, None) is None:
                self.memory.integers.constants[base] = int(base)
            valor = self.memory.integers.constants[base]
        elif RepresentsDouble(base):
            if self.memory.doubles.constants.get(base, None) is None:
                self.memory.doubles.constants[base] = float(base)
            valor = self.memory.doubles.constants[base]
        elif base[0] == "\"":
            if self.memory.strings.constants.get(base[1:-1], None) is None:
                self.memory.strings.constants[base[1:-1]] = base[1:-1]
            valor = self.memory.strings.constants[base[1:-1]]
        elif base == 'true':
            if self.memory.booleans.constants.get(base, None) is None:
                self.memory.booleans.constants[base] = True
            valor = self.memory.booleans.constants[base]
        elif base == 'false':
            if self.memory.booleans.constants.get(base, None) is None:
                self.memory.booleans.constants[base] = False
            valor = self.memory.booleans.constants[base]
        # si no es constante se busca el valor en la memoria
        else:
            valor = self.memory.get_val(base)
        return valor

    def execute(self, quad, op):
        left = quad.left_operand.rstrip().lstrip()
        right = quad.right_operand.rstrip().lstrip()
        left_val = self.get_memory_val(left)
        right_val = self.get_memory_val(right)

        if op == '+':
            res = left_val + right_val
        elif op == '-':
            res = left_val - right_val

        self.memory.set_val(quad.res.rstrip().lstrip(), res)

