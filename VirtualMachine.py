from __future__ import print_function
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
def striptLR(s):
    return s.rstrip().lstrip()

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
            quad = Quadruple(cont, striptLR(q[0]), striptLR(q[1]), striptLR(q[2]), striptLR(q[3]))
            cont += 1
            self.quadruples.append(quad)
        f.close()

    def run(self):
        ''' Function that start reading all the quadruples and executing them'''
        # start reading the file
        self.readFiles()

        #cycle until read the last quadruple 'END'
        while self.quadruples[self.pc].op != 'END':
            # get the current quad according to Program Counter(pc)
            quad = self.quadruples[self.pc]

            operation = quad.op

            # check all posible operations and do something according to

            if operation == 'ERA':
                # saves the name of the last function to use in Params and Gosub
                self.last_func = quad.left_operand
                # allocate memory for the function that is going to be called

                self.memory.era()

            elif operation == 'EndProc':
                # release the memory used in the function
                self.memory.endproc()
                # stablish pc with the value that called the function
                self.pc = self.PCS.pop()

            elif operation == 'Return':
                self.get_final_value(quad, 'Return')

            elif operation == 'Param':
                self.get_final_value(quad, 'Param')

            elif operation == 'Print':

                #TODO agregar el segundo parametro del print
                val = self.get_memory_val(quad.left_operand)
                # obtiene como quiere terminar el print
                endprint = quad.right_operand
                
                if endprint == '\\n':
                    print(val)
                else:
                    print(val, end=endprint[1:-1])

            elif operation == 'Read':
                temp = raw_input("")
                # aqui no lo guardo en constante el valor que entra porque se va a guardar en una variable
                if temp.isdigit():
                    temp = int(temp)
                elif RepresentsDouble(temp):
                    temp = float(temp)
                #TODO: checar cubo semantico

                self.memory.set_val(quad.res, temp)
            #basic operations +, - , *, /
            elif operation == '+':
                self.execute(quad, '+')
            elif operation == '-':
                self.execute(quad, '-')
            elif operation == '*':
                self.execute(quad, '*')
            elif operation == '/':
                self.execute(quad, '/')

            #assignment

            elif operation == '=':
                #TODO: parsear a int en caso de assignacion y checar cubo semantico
                self.get_final_value(quad, '=')


            #logic operations
            elif operation == 'and':
                self.execute(quad, 'and')
            elif operation == 'or':
                self.execute(quad, 'or')
            elif operation == '>=':
                self.execute(quad, '>=')
            elif operation == '<=':
                self.execute(quad, '<=')
            elif operation == '==':
                self.execute(quad, '==')
            elif operation == '>':
                self.execute(quad, '>')
            elif operation == '<':
                self.execute(quad, '<')
            # gotos
            elif operation == 'Goto':
                self.pc = int(self.quadruples[self.pc].res)
                continue
            elif operation == 'GotoF':
                dir = quad.left_operand.lstrip().rstrip()
                if not self.get_memory_val(dir):
                    self.pc = int(quad.res)
                    continue

                # if memory.getVal(dir) == 'false':
                #     self.pc = quad.res
            elif operation == 'GotoV':
                dir = quad.left_operand.lstrip().rstrip()
                if self.get_memory_val(dir):
                    self.pc = int(quad.res)
                    continue
            elif operation == 'Gosub':
                self.PCS.push(self.pc)
                self.pc = int(self.quadruples[self.pc].res)
                continue
            # print self.quadruples[self.pc].printeame()
            self.pc += 1

    def get_final_value(self, quad, op):
        left = quad.left_operand
        if left[0] == "\'" or left[0] == "\"":
            valor = left[1:-1]
        else:
            if op == 'Param':
                valor = self.get_memory_val(left, True)
            else:
                valor = self.get_memory_val(left)
        res = quad.res

        if res[0] == "d":
            valor = float(valor)
        if res[0] == "i":
            valor = int(valor)

        if op == 'Return':
            self.memory.set_val(self.last_func, valor)
        elif op == 'Param' or op == '=':
            self.memory.set_val(quad.res, valor)

    def get_memory_val(self, base, param=False):
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
            valor = self.memory.get_val(base, param)
        return valor

    def execute(self, quad, op):
        left = quad.left_operand
        right = quad.right_operand
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

        self.memory.set_val(quad.res, res)

    def assignment(self, quad, where):
        ''' function that assign a value to a variable'''
        # get the value to be set
        left = quad.left_operand
        # check if the value is a string constant 
        if left[0] == "\'" or left[0] == "\"":
            # set value as string constant ignoring " or '
            valor = left[1:-1]
        else:
            # if left is not a string constant try to get from memory
            valor = self.get_memory_val(left)

        #TODO: check semantic cube and type of assignment
        if where[0] == "d":
            valor = float(valor)
        if where[0] == "i":
            valor = int(valor)

        # set the value in memory
        self.memory.set_val(where, valor)