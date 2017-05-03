"""This module is a Simple Scanner using ply
-----------------------------------------------------------------
Compilers Design Project
Tec de Monterrey
Julio Cesar Aguilar Villanueva  A01152537
Jose Fernando Davila Orta       A00999281
-----------------------------------------------------------------

DOCUMENTATION: For complete Documentation see UserManual.pdf"""
from __future__ import print_function
from quad_generator import QuadGenerator
from variable import Variable
from quadruple import Quadruple
from functions_dir import FunctionsDir
from Memory import Memory
from cube import semantic_cube
from stack import Stack
from graphics_constructor import GraphicsConstructor
custom_functions = [
    'vgdrawText',
    'vgdrawLine',
    'vgdrawCircle',
    'vgdrawOval',
    'vgdrawTriangle',
    'vgdrawRectangle',
    'vgdrawDot',
    'vgdrawCurve',
    'vginsertImage'
]

def get_type(symbol):
    '''Retorna el tipo que python identifica de un simbolo'''
    if symbol == 'true' or symbol == 'false':
        return 'bool'
    res = str(type(symbol))[7:10]
    if res == 'int':
        return 'int'
    elif res == 'flo':
        return 'double'
    elif res == 'str':
        return 'string'

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
    '''Clase virtual machine para ejecutar cuadruplos
    Recibe functions directory(fd) como apoyo'''
    def __init__(self, fd):
        #Lista de cuadruplos
        self.quadruples = []
        # Program counter
        self.pc = 0
        # Directorio de funciones
        self.fd = fd
        # Diccionario auxiliar
        self.temporal = {}
        # Instancia de memoria
        self.memory = Memory()
        # Scope del programa
        self.scope = 'main'
        # Ultima funcion llamada
        self.last_func = None
        # Stack de contadores pendientes
        self.PCS = Stack()
        self.pibool = False
        # Bool para saber si se llamaron metodos graficos
        self.called_graphics = False
        # Instancia de graficas
        self.window = GraphicsConstructor()

    def orderParams(self):
        '''Parsea cuadruplos para mejor ejecucion de llamadas a funciones'''
        aux = Stack()
        pc = 0
        while self.quadruples[pc].op != 'END':
            quad = self.quadruples[pc]

            if quad.op == 'Param':
                aux.top.append(quad)
                del self.quadruples[pc]
            elif quad.op == 'Gosub':
                self.quadruples = self.quadruples[:pc] + aux.top + self.quadruples[pc:]
                pc = pc + 1 + len(aux.top)
                aux.pop()
            elif quad.op == 'ERA':
                aux.push([])
                pc += 1
            else:
                pc += 1

    def readFiles(self):
        '''Lee output y actualiza lista de cuadruplos'''
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
        self.orderParams()
        # self.fd.printeame()
        # for i in self.quadruples:
        #     print(i.printeame())
        #cycle until read the last quadruple 'END'
        while self.quadruples[self.pc].op != 'END':

            # get the current quad according to Program Counter(pc)
            quad = self.quadruples[self.pc]
            operation = quad.op

            # check all posible operations and do something according to
            if operation == 'ERA':
                # saves the name of the last function to use in Params and Gosub
                self.last_func = quad.left_operand

            elif operation == 'EndProc':
                # release the memory used in the function
                self.memory.endproc()
                # stablish pc with the value that called the function
                self.pc = self.PCS.pop()
                self.scope = 'main'

            elif operation == 'Return':
                self.set_memory_val(quad, 'Return')

            elif operation == 'Param':

                if self.pibool == False:
                    # allocate memory for the function that is going to be called
                    self.memory.era()
                    self.pibool = True

                self.set_memory_val(quad, 'Param')

            elif operation == 'Verify':
                valor = self.get_memory_val(quad.left_operand)
                if valor < int(quad.right_operand) or valor >= int(quad.res):
                    raise IndexError('Error 7002: Index out of range')

            elif operation == 'Print':
                val = self.get_memory_val(quad.left_operand)
                # obtiene como quiere terminar el print
                endprint = quad.right_operand

                if endprint == '\\n':
                    print(val)
                else:
                    print(val, end=endprint[1:-1])

            elif operation == 'Read':
                var_type = None
                # se realiza el input en formato raw
                temp = raw_input(">>> ")
                # verifica si va a guardar en una variable dimensionada
                if '.' in quad.res:
                    # parsea para variable dimensionada
                    if quad.res.count('.') > 1:
                        components = quad.res.split('.')
                        while len(components) > 2:
                            index = components.pop()
                            index = self.get_memory_val(index)
                            var = components.pop()
                            aux = var + '.' + str(index)
                            val = self.memory.get_val(aux)
                            components.append(str(val))
                        index = self.get_memory_val(components[1])
                        helper = components[0] + '.' + str(index)

                        # se obtiene el size y type de la variable a la que se va a guardar ya sea
                        # en el scope global o alguno local
                        if self.fd.functions[self.scope].variables_dict.get(components[0][2:], None) is None:
                            variable = self.fd.functions['global'].variables_dict.get(components[0][2:])
                            var_size = variable.size
                            var_type = variable.type
                        else:
                            variable = self.fd.functions[self.scope].variablest_dict.get(components[0][2:])
                            var_size = variable.size
                            var_type = variable.type
                    else:
                        # cuando estan varias variables dimensionadas anidadas
                        res = quad.res.split('.')
                        var = res[0]
                        index = self.get_memory_val(res[1])
                        helper = var + '.' + str(index)

                        # se obtiene el size y type de la variable a la que se va a guardar ya sea
                        # en el scope global o alguno local

                        if self.fd.functions[self.scope].variables_dict.get(var[2:], None) is None:
                            variable = self.fd.functions['global'].variables_dict.get(var[2:])
                            var_size = variable.size
                            var_type = variable.type
                        else:
                            variable = self.fd.functions[self.scope].variables_dict.get(var[2:])
                            var_size = variable.size
                            var_type = variable.type

                    # si la variable a la que se va a guardar es de tipo booleano se manda llamar un error
                    if var_type == 'bool':
                        raise TypeError("Error 6005: Can't read to bool variable")
                    try:
                        # se intenta castear el valor del usuario al tipo de la variable en donde se va a guardar
                        if var_type == 'int':
                            temp = int(temp)
                        elif var_type == 'float':
                            temp = float(temp)
                    except Exception:
                        raise TypeError("Error 6004: Invalid Input Type")

                    self.memory.set_val(helper, temp, var_size)
                else:
                    # si no es un arreglo se obtiene el var type
                    if self.fd.functions[self.scope].variables_dict.get(quad.res[2:], None) is None:
                        variable = self.fd.functions['global'].variables_dict.get(quad.res[2:])
                        var_type = variable.type
                    else:
                        variable = self.fd.functions[self.scope].variables_dict.get(quad.res[2:])
                        var_type = variable.type
                    # si la variable a la que se va a guardar es de tipo booleano se manda llamar un error
                    if var_type == 'bool':
                        raise TypeError("Error 6005: Can't read to bool variable")
                    try:
                        # se intenta castear el valor del usuario al tipo de la variable en donde se va a guardar
                        if var_type == 'int':
                            temp = int(temp)
                        elif var_type == 'float':
                            temp = float(temp)
                    except Exception:
                        raise TypeError("Error 6004: Invalid Input Type")

                    self.memory.set_val(quad.res, temp)

            #basic operations +, - , *, /
            elif operation == '+':
                self.execute(quad, '+')
            elif operation == '-':
                self.execute(quad, '-')
            elif operation == '*':
                self.execute(quad, '*')
            elif operation == '/':
                # muestra un error cuando se intenta hacer una division entre 0
                if quad.right_operand == "0" or quad.right_operand == "0.0":
                    raise ZeroDivisionError("Error 6003: Division by zero")
                self.execute(quad, '/')
            elif operation == '%' or operation == 'mod':
                # muestra error cuando se intenta hacer un modulo 0
                if quad.right_operand == "0" or quad.right_operand == "0.0":
                    raise ZeroDivisionError("Error 6006: Module by zero")
                self.execute(quad, '%')

            #assignment
            elif operation == '=':
                self.set_memory_val(quad, '=')

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
            elif operation == '!=':
                self.execute(quad, '!=')
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
                self.pibool = False
                # si el gosub es a una funcion especial
                if quad.left_operand in custom_functions:
                    self.called_graphics = True
                    params_dict = self.memory.doubles.temporal.top.copy()
                    params_dict.update(self.memory.strings.temporal.top.copy())
                    params_dict.update(self.memory.integers.temporal.top.copy())
                    self.window.construct(quad.left_operand, params_dict)
                    self.memory.endproc()
                else:
                    self.scope = quad.left_operand[2:]
                    self.PCS.push(self.pc)
                    self.pc = int(self.quadruples[self.pc].res)
                    continue
            # print self.quadruples[self.pc].printeame()
            self.pc += 1

        if self.called_graphics:
            self.window.display()

    def set_memory_val(self, quad, op):
        left = quad.left_operand
        if op == 'Param':
            valor = self.get_memory_val(left, True)
        else:
            valor = self.get_memory_val(left)
        res = quad.res
        # se intenta castear a float o a int dependiendo de la variable donde se va a guardar
        if res[0] == "d":
            valor = float(valor)
        if res[0] == "i":
            valor = int(valor)

        if op == 'Return':
            self.memory.set_val(self.last_func, valor)
        elif op == 'Param' or op == '=' or op == 'Read':
            is_param = False
            if op == 'Param':
                is_param = True
            # parsea si es una variable dimensionada
            if '.' in quad.res:
                if quad.res.count('.') > 1:
                    components = quad.res.split('.')
                    while len(components) > 2:
                        index = components.pop()
                        index = self.get_memory_val(index, is_param)
                        var = components.pop()
                        aux = var + '.' + str(index)
                        val = self.memory.get_val(aux, is_param)
                        components.append(str(val))
                    index = self.get_memory_val(components[1], is_param)
                    helper = components[0] + '.' + str(index)

                    # obtiene el size de la variable
                    if self.fd.functions[self.scope].variables_dict.get(components[0][2:], None) is None:
                        var_size = self.fd.functions['global'].variables_dict.get(components[0][2:]).size
                    else:
                        var_size = self.fd.functions[self.scope].variablest_dict.get(components[0][2:]).size
                else:
                    res = quad.res.split('.')
                    var = res[0]
                    index = self.get_memory_val(res[1], is_param)
                    helper = var + '.' + str(index)
                    # obtiene el size de la variable
                    if self.fd.functions[self.scope].variables_dict.get(var[2:], None) is None:
                        var_size = self.fd.functions['global'].variables_dict.get(var[2:]).size
                    else:
                        var_size = self.fd.functions[self.scope].variables_dict.get(var[2:]).size

                self.memory.set_val(helper, valor, var_size)
            else:
                self.memory.set_val(quad.res, valor)

    def get_memory_val(self, base, param=False):
        # intenta obtener valores de constantes
        if RepresentsInt(base):
            if self.memory.integers.constants.get(base, None) is None:
                self.memory.integers.constants[base] = int(base)
            valor = self.memory.integers.constants[base]
        elif RepresentsDouble(base):
            if self.memory.doubles.constants.get(base, None) is None:
                self.memory.doubles.constants[base] = float(base)
            valor = self.memory.doubles.constants[base]
        elif base[0] == "\"" or base[0] == "\'":
            if self.memory.strings.constants.get(base[1:-1], None) is None:
                self.memory.strings.constants[base[1:-1]] = base[1:-1]
            valor = self.memory.strings.constants[base[1:-1]]
        elif base == 'true':
            if self.memory.booleans.constants.get(base, None) is None:
                self.memory.booleans.constants[base] = 'true'
            valor = self.memory.booleans.constants[base]
        elif base == 'false':
            if self.memory.booleans.constants.get(base, None) is None:
                self.memory.booleans.constants[base] = 'false'
            valor = self.memory.booleans.constants[base]
        # si no es constante se busca el valor en la memoria
        else:
            # parsea cuando una variable es dimensionada
            if '.' in base:
                if base.count('.') > 1:
                    components = base.split('.')
                    while len(components) > 2:
                        index = components.pop()
                        index = self.get_memory_val(index, param)
                        var = components.pop()
                        aux = var + '.' + str(index)
                        val = self.memory.get_val(aux, param)
                        components.append(str(val))
                    index = self.get_memory_val(components[1], param)
                    base = components[0] + '.' + str(index)
                else:
                    res = base.split('.')
                    var = res[0]
                    index = self.get_memory_val(res[1], param)
                    base = var + '.' + str(index)
            # trae el valor desde memoria
            valor = self.memory.get_val(base, param)
        return valor

    def execute(self, quad, op):
        left = quad.left_operand
        right = quad.right_operand
        left_val = self.get_memory_val(left)
        right_val = self.get_memory_val(right)

        if left_val == 'ERROR get_val: 458':
            raise MemoryError('Error 5001: Error getting Value')
        elif right_val == 'ERROR get_val: 458':
            raise MemoryError('Error 5001: Error getting Value')
        else:
            if op == '+':
                res = left_val + right_val
            elif op == '-':
                res = left_val - right_val
            elif op == '*':
                res = left_val * right_val
            elif op == '/':
                if right_val == 0 or right_val == 0.0:
                    raise ZeroDivisionError("Error 6003: Division by zero")
                res = left_val / right_val
            elif op == '%':
                res = left_val % right_val
            elif op == '<':
                res = left_val < right_val
            elif op == '>':
                res = left_val > right_val
            elif op == '==':
                res = left_val == right_val
            elif op == '!=':
                res = left_val != right_val
            elif op == '<=':
                res = left_val <= right_val
            elif op == '>=':
                res = left_val >= right_val
            elif op == 'and':
                res = left_val and right_val
            elif op == 'or':
                res = left_val or right_val

        self.memory.set_val(quad.res, res)