'''Modulo que define el funcionamiento de la clase QuadGenerator.
Clase encargada de la generacion de cuadruplos.'''

from stack import Stack
from cube import semantic_cube

class Variable(object):
    '''Clase Variable. Contiene nombre, tipo y valor'''
    def __init__(self, name, value, var_type):
        self.name = name
        self.value = value
        self.type = var_type

    def __str__(self):
        '''Metodo para imprimir variables'''
        return 'VAR. NAME: {0}, VALUE: {1}, TYPE: {2}'.format(self.name, self.value, self.type)

    def get_type(self):
        '''Regresa el tipo de la variable'''
        return self.type

    def get_name(self):
        '''Regresa el nombre de la variable'''
        return self.name

    def get_value(self):
        '''Regresa el valor asignado a una variable'''
        return self.value

class Quadruple(object):
    '''Clase Qudruple. Contiene id, op(operator), left_operand, right_operand y result'''
    def __init__(self, id, op, left_operand, right_operand, res):
        '''Metodo de inicializacion'''
        self.id = id
        self.op = op
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.res = res

    def printeame(self):
        '''Funcion auxiliar para imprimir contenidos del cuadruplo'''
        return '({0}, {1}, {2}, {3})'.format(self.op, self.left_operand, self.right_operand, self.res)

class QuadGenerator(object):
    '''Clase encargada de la generacion de cuadruplos'''
    def __init__(self, filename):
        '''Metodo de inicializacion de la clase'''
        # Operands pile
        self.pile_o = Stack()
        # Operators pile
        self.popper = Stack()
        # Pending jumps
        self.pjumps = Stack()
        # Pending cycle returns
        self.pcycles = Stack()
        # File to write list of quadruples
        self.file = filename
        # Id of temporal vars
        self.temporal_id = 1
        # List of quadruples
        self.quadruples = []
        # Quadruple counter
        self.cont = 0

    def printeame(self):
        '''Funcion auxiliar para imprimir contenidos de la clase'''
        for i in self.quadruples:
            print (i.printeame())

    def read_operand(self, operand):
        '''Push de una variable a la pila de operandos'''
        self.pile_o.push(operand)

    def read_operator(self, operator):
        '''Push de operador a pila de operadores'''
        self.popper.push(operator)

    def reset_temporal_id(self):
        '''Reset al contador de temporales para cuando sale de funciones'''
        self.temporal_id = 1

    def generate_quad(self):
        '''Metodo para genera cuadruplos'''
        # Checa si el op es uno de los siguientes operadores'''
        op = self.popper.top
        if op in ['+=', '-=', '*=', '/=']:
            self.generate_assignment_op_quad()
            return

        op = self.popper.pop()
        # Voltea operandos para un cuadruplo de asignacion simple
        if op == '=':
            left_operand = self.pile_o.pop()
            right_operand = self.pile_o.pop()
        else:
            right_operand = self.pile_o.pop()
            left_operand = self.pile_o.pop()

        # Verfica la validez sematica
        res = semantic_cube[right_operand.get_type()][left_operand.get_type()][op]

        # Si la sematica es valida
        if res != 'Error':
            # Obtiene el nombre o valor de los operandoss
            name_left = left_operand.get_name()
            name_right = right_operand.get_name()
            if name_left == 'constant':
                name_left = left_operand.get_value()
            if name_right == 'constant':
                name_right = right_operand.get_value()
            # Genera cuadruplo
            if op == '=':
                quad = Quadruple(self.cont, op, name_left, '', name_right)
            else:
                # Genera variable temporal
                temp = Variable(name='t' + str(self.temporal_id), value=None, var_type=res)
                # Aumenta id de temporales
                self.temporal_id += 1
                quad = Quadruple(self.cont, op, name_left, name_right, temp.get_name())
                # pushea temporal a pila de operandos
                self.pile_o.push(temp)

            # Insert cuadruplo en la lista de cuadruplos
            self.quadruples.append(quad)
            self.cont += 1
        else:
            msg = 'Type missmatch ' + str(left_operand.get_type()) + ' and ' + str(right_operand.get_type()) + ' for operator: ' + str(op)
            raise TypeError(msg)


    def generate_assignment_op_quad(self):
        '''Funcion para generar dos cuadruplos con operadores de asignacion'''
        op = self.popper.pop()
        if op in ['+=', '-=', '*=', '/=']:
            self.popper.push('=')
            self.popper.push(op[0])
            # Saca A y B de la pila para ponerlos en la siguiente forma
            # a += b  -> a = a + b
            b = self.pile_o.pop()
            a = self.pile_o.pop()
            self.pile_o.push(a)
            self.pile_o.push(a)
            self.pile_o.push(b)
            # genera el cuadruplo para +, -, * o /
            self.generate_quad()
            # genera el cuadruplo para el =
            self.generate_quad()

    def generate_print(self):
        '''Funcion para generar el cuadruplo de un print'''
        last_operand = self.pile_o.pop()
        quad = Quadruple(id=self.cont, op='Print', left_operand=last_operand, right_operand=None, res=None)
        self.cont += 1
        self.quadruples.append(quad)
        print(last_operand)

    # def generate_read(self, res):
    #     '''Funcion para generar cuadruplo de read'''
    #     temp = Variable(name='t' + str(self.temporal_id), value=None, var_type=res)
    #      # Aumenta id de temporales
    #     self.temporal_id += 1

    #     quad = Quadruple(id=self.cont, op='Read', left_operand=last_operand, right_operand=None, res=temp.get_name())
    #     self.cont += 1

    # TODO: agregar a donde van a saltar la operacion gosub
    def generate_era(self, function_id):
        quad = Quadruple(self.cont, 'ERA', function_id, '', '')
        self.quadruples.append(quad)
        self.cont += 1

    def generate_gosub(self):
        name = self.pile_o.pop()
        quad = Quadruple(self.cont, 'Gosub', name, '', '')
        self.quadruples.append(quad)
        self.cont += 1

    def generate_endproc(self):
        quad = Quadruple(self.cont, 'EndProc', '', '', '')
        self.quadruples.append(quad)
        self.cont += 1

    def generate_param(self, argument, param):
        if argument.get_name() == 'constant':
            argument = argument.get_value()
        else:
            argument = argument.get_name()
        quad = Quadruple(self.cont, 'Param', argument, '', param.get_name())
        self.quadruples.append(quad)
        self.cont += 1

    def generate_gotoF(self):
        '''Funcion para generar cuadruplos de gotoF'''
        last_operand = self.pile_o.pop()
        if last_operand.get_type() != 'bool':
            raise TypeError('Type missmatch. Non bool variables in condition')
        else:
            quad = Quadruple(self.cont, 'GotoF', last_operand.get_name(), None, None)
            self.quadruples.append(quad)
            self.pjumps.push(self.cont)
            self.cont += 1

    def generate_goto(self):
        '''Funcion para generar cuadruplos de goto'''
        quad = Quadruple(self.cont, 'Goto', None, None, None)
        self.quadruples.append(quad)
        self.pjumps.push(self.cont)
        self.cont += 1

    def fill_goto(self):
        '''Funcion que llena los cuadruplos de goto pendientes'''
        # Obtiene indice de cuadruplo pendiente en la lista de cuadruplos
        pending = self.pjumps.pop()
        # Dependiendo de si es un cuadruplo de gotoF o goto llena con un valor de contador
        self.quadruples[pending].res = self.cont

    def fill_goto_else(self):
        '''Funcion que llena los cuadruplos de goto pendiente cuando hay un else'''
        pending = self.pjumps.pop()
        # Dependiendo de si es un cuadruplo de gotoF o goto llena con un valor de contador
        self.quadruples[pending].res = self.cont + 1

    def generate_pending_goto(self):
        '''Genera cuadruplo pendiente de goto para ciclos'''
        pending = self.pcycles.pop()
        quad = Quadruple(self.cont, 'Goto', None, None, pending)
        self.quadruples.append(quad)
        self.cont += 1

    def finish(self):
        '''Crea el ultimo cuadruplo del programa'''
        quad = Quadruple(self.cont, 'END', '', '', '')
        self.quadruples.append(quad)

    def export(self):
        '''Funcion para exportar cuadruplos a un archivo al terminar de generar cuadruplos'''
        f = open(self.file, 'w')
        for q in self.quadruples:
            f.write(q.printeame())
            f.write('\n')
        f.close()  # you can omit in most cases as the destructor will call it
