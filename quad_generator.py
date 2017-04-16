'''Modulo que define el funcionamiento de la clase QuadGenerator.
Clase encargada de la generacion de cuadruplos.'''

from stack import Stack
from cube import semantic_cube
from variable import Variable
from quadruple import Quadruple

def get_var_type(var_type):
    if var_type == 'int':
        return 'i'
    elif var_type == 'double':
        return 'd'
    elif var_type == 'string':
        return 's'
    elif var_type == 'bool':
        return 'b'

def get_var_scope(scope):
    if scope == 'global':
        return 'g'
    elif scope == 'main':
        return 'l'
    else:
        return 't'

def createParam(param):
    res = ''
    res = get_var_type(param.get_type())+ 't' + param.get_name()
    return res

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
        # Pending loop vars stack
        self.ploop_vars = Stack()
        # Pila dimensionada
        self.pdim = Stack()
        # File to write list of quadruples
        self.file = filename
        # Id of temporal vars
        self.temporal_id = 1
        # List of quadruples
        self.quadruples = []
        # Quadruple counter
        self.cont = 0
        # Scope for quads
        self.scope = 'global'
        # Diccionary for initial quadruple of each function
        self.func_counter = {}

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
                temp_name = get_var_type(res) + get_var_scope(self.scope) + 't' + str(self.temporal_id)
                temp = Variable(temp_name, None, res, self.scope, 1)
                # Aumenta id de temporales
                self.temporal_id += 1
                quad = Quadruple(self.cont, op, name_left, name_right, temp.get_name())
                # pushea temporal a pila de operandos
                self.pile_o.push(temp)

            # Insert cuadruplo en la lista de cuadruplos
            self.quadruples.append(quad)
            self.cont += 1
        else:
            left_type = left_operand.get_type()
            right_type = right_operand.get_type()
            msg = 'Type missmatch ' + left_type + ' and ' + right_type + ' for operator: ' + str(op)
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

    def generate_print(self, modifier='\\n'):
        '''Funcion para generar el cuadruplo de un print'''
        last_operand = self.pile_o.pop()

        if last_operand.get_name() == 'constant':
            last_operand = last_operand.get_value()
        else:
            last_operand = last_operand.get_name()
        #s = self.pile_o.top.get_value()
        quad = Quadruple(id=self.cont, op='Print', left_operand=last_operand, right_operand=modifier, res='')
        self.cont += 1
        self.quadruples.append(quad)

    def generate_read(self, var):
        '''Funcion para generar cuadruplo de read'''
        if var.get_name() == 'constant':
            name = var.get_value()
        else:
            name = var.get_name()

        quad = Quadruple(self.cont, 'Read', None, None, name)
        self.quadruples.append(quad)
        self.cont += 1

    # TODO: agregar a donde van a saltar la operacion gosub
    def generate_era(self, function_id):
        func_type = self.func_counter.get(function_id, 'void')[1]
        res_type = get_var_type(func_type)
        quad = Quadruple(self.cont, 'ERA', res_type + 'g' + function_id, '', '')
        self.quadruples.append(quad)
        self.cont += 1

    def generate_gosub(self, name, func_type):
        res_type = get_var_type(func_type)
        initial_address = self.func_counter.get(name, '')[0]
        quad = Quadruple(self.cont, 'Gosub', res_type + 'g' + name, '', initial_address)

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
        quad = Quadruple(self.cont, 'Param', argument, '', createParam(param))
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

    def generate_func_assign(self, func_name, func_type, value):
        res_type = get_var_type(func_type)
        curr_scope = get_var_scope(self.scope)
        temp_name = res_type + curr_scope + 't' + str(self.temporal_id)
        func_var = Variable(res_type + 'g' + func_name, value, func_type, 'global', 1)
        tmp_var = Variable(temp_name, None, func_type, self.scope, 1)
        self.temporal_id += 1
        quad = Quadruple(self.cont, '=', func_var.get_name(), None, tmp_var.get_name())
        self.quadruples.append(quad)
        self.pile_o.push(tmp_var)
        self.cont += 1

    def generate_return(self):
        var = self.pile_o.pop()
        if var.get_name() == 'constat':
            name = var.get_value()
        else:
            name = var.get_name()
        quad = Quadruple(self.cont, 'Return', name, None, None)
        self.quadruples.append(quad)
        self.cont += 1
        return var.get_value()

    def generate_verify(self):
        var = self.pdim.top[1]
        tmp = self.pile_o.pop()

        if tmp.get_name() == 'constant':
            tmp_name = tmp.get_value()
        else:
            tmp_name = tmp.get_name()

        quad = Quadruple(self.cont, 'Verify', tmp_name, 0, var.size)
        self.quadruples.append(quad)
        self.cont += 1
        # Concatena el nombre de la variable junto con la temporal o constante de resultado para acceso al arreglo
        aux = Variable(var.name, var.value, var.type, var.scope, var.size, var.is_dim)
        aux.name = var.name + '.' + str(tmp_name)
        self.pile_o.push(aux)
        self.popper.pop()
        self.pdim.pop()

    def fill_goto(self):
        '''Funcion que llena los cuadruplos de goto pendientes'''
        # Obtiene indice de cuadruplo pendiente en la lista de cuadruplos
        pending = self.pjumps.pop()
        # Dependiendo de si es un cuadruplo de gotoF o goto llena con un valor de contador
        self.quadruples[pending].res = self.cont

    def fill_goto_plus(self):
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
            f.write(q.printeame() + '\n')
        f.close()  # you can omit in most cases as the destructor will call it

    def add_function(self, name, func_type):
        self.func_counter[name] = (self.cont, func_type)


