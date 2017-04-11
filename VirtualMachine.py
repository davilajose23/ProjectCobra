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
                # TODO: mover todo a una funcion: buscar si existe la constante y si no existe agregarla
                left = quad.left_operand.rstrip().lstrip()
                if RepresentsInt(left):
                    self.memory.integers.constants[left] = int(left)
                    valor = int(left)
                elif RepresentsDouble(left):
                    self.memory.doubles.constants[left] = float(left)
                    valor = float(left) 
                elif left[0] == "\"":
                    self.memory.strings.constants[left[1:-1]] = left[1:-1]
                    valor = left[1:-1]
                elif left == 'true':
                    self.memory.booleans.constants[left] = True
                    valor = True
                elif left == 'false':
                    self.memory.booleans.constants[left] = False
                    valor = False
                # si no es constante se busca el valor en la memoria
                else:
                    valor = self.memory.get_val(left)
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

    def getVal(dir):
        return self.dir_func.get(dir, None)