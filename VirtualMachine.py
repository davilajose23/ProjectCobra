from quad_generator import QuadGenerator
from variable import Variable
from quadruple import Quadruple
from functions_dir import FunctionsDir
from Memory import Memory
from cube import semantic_cube
from stack import Stack

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
        self.last_func = None
        self.PCS = Stack()

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
            
            if op == 'ERA':
                #create dict in temp
                self.last_func = quad.left_operand.rstrip().lstrip()
                self.memory.era()

            elif op == 'EndProc':
                self.memory.endproc()
                self.pc = self.PCS.pop()
            
            elif op == 'Return':
                left = quad.left_operand.rstrip().lstrip()
                if left[0] == "\'" or left[0] == "\"":
                    valor = left[1:-1]
                else:
                    valor = self.get_memory_val(left)
                res = quad.res.rstrip().lstrip()

                if res[0] == "d":
                    valor = float(valor)
                if res[0] == "i":
                    valor = int(valor)

                self.memory.set_val( self.last_func, valor)

            elif op == 'Param':
                left = quad.left_operand.rstrip().lstrip()
                if left[0] == "\'" or left[0] == "\"":
                    valor = left[1:-1]
                else:
                    valor = self.get_memory_val(left)
                res = quad.res.rstrip().lstrip()

                if res[0] == "d":
                    valor = float(valor)
                if res[0] == "i":
                    valor = int(valor)

                self.memory.set_val(quad.res.rstrip().lstrip(), valor)
            elif op == 'Print':
                #TODO agregar el segundo parametro del print

                val = self.get_memory_val(quad.left_operand.rstrip().lstrip())
                print(val)
            elif op == 'Read':
                temp = raw_input("")
                # aqui no lo guardo en constante el valor que entra porque se va a guardar en una variable
                if temp.isdigit():
                    temp = int(temp)
                elif RepresentsDouble(temp):
                    temp = float(temp)
                #TODO: checar cubo semantico

                self.memory.set_val(quad.res.rstrip().lstrip(), temp)
            #basic operations +, - , *, /
            elif op == '+':
                self.execute(quad, '+')
            elif op == '-':
                self.execute(quad, '-')
            elif op == '*':
                self.execute(quad, '*')
            elif op == '/':
                self.execute(quad, '/')

            #assignment
            elif op == '=':
                #TODO: parsear a int en caso de assignacion y checar cubo semantico
                left = quad.left_operand.rstrip().lstrip()
                if left[0] == "\'" or left[0] == "\"":
                    valor = left[1:-1]
                else:
                    valor = self.get_memory_val(left)
                res = quad.res.rstrip().lstrip()

                if res[0] == "d":
                    valor = float(valor)
                if res[0] == "i":
                    valor = int(valor)

                self.memory.set_val(quad.res.rstrip().lstrip(), valor)

            #logic operations
            elif op == 'and':
                self.execute(quad, 'and')
            elif op == 'or':
                self.execute(quad, 'or')
            elif op == '>=':
                self.execute(quad, '>=')
            elif op == '<=':
                self.execute(quad, '<=')
            elif op == '==':
                self.execute(quad, '==')
            elif op == '>':
                self.execute(quad, '>')
            elif op == '<':
                self.execute(quad, '<')
            # gotos
            elif op == 'Goto':
                self.pc = int(self.quadruples[self.pc].res)
                continue
            elif op == 'GotoF':
                dir = quad.left_operand.lstrip().rstrip()
                if not self.get_memory_val(dir):
                    self.pc = int(quad.res)
                    continue
                
                # if memory.getVal(dir) == 'false':
                #     self.pc = quad.res
            elif op == 'GotoV':
                dir = quad.left_operand.lstrip().rstrip()
                if self.get_memory_val(dir):
                    self.pc = int(quad.res)
                    continue
            elif op == 'Gosub':
                self.PCS.push(self.pc)
                self.pc = int(self.quadruples[self.pc].res)
                continue
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

        if left_val == 'ERROR get_val: 458':
            raise ValueError('ERROR get_val: 458')
        elif right_val == 'ERROR get_val: 458':
            raise ValueError('ERROR get_val: 458')
        else:
            if op == '+':
                res = left_val + right_val
            elif op == '-':
                res = left_val - right_val
            elif op == '*':
                res = left_val * right_val
            elif op == '/':
                res = left_val / right_val
            elif op == '<':
                res = left_val < right_val
            elif op == '>':
                res = left_val > right_val
            elif op == '==':
                res = left_val == right_val
            elif op == '<=':
                res = left_val <= right_val
            elif op == '>=':
                res = left_val >= right_val
            elif op == 'and':
                res = left_val and right_val
            elif op == 'or':
                res = left_val or right_val

        self.memory.set_val(quad.res.rstrip().lstrip(), res)

