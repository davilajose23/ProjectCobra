from stack import Stack
from cube import semantic_cube

class Variable(object):
    """docstring for Variable"""
    def __init__(self, name, value, var_type):
        super(Variable, self).__init__()
        self.name = name
        self.value = value
        self.type = var_type

    def __str__(self):
       
        return 'VAR. NAME: {0}, VALUE: {1}, TYPE: {2}'.format(self.name, self.value, self.type)

    def get_type(self):
        return self.type

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value

class Quadruple(object):
    """docstring for Quadruple"""
    def __init__(self, id, op, left_operand, right_operand, res):
        super(Quadruple, self).__init__()
        self.id = id
        self.op = op
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.res = res

    def printeame(self):
        return '({0}, {1}, {2}, {3})'.format(self.op, self.left_operand, self.right_operand, self.res)

class QuadGenerator(object):
    """docstring for QuadGenerator"""
    def __init__(self, filename):
        super(QuadGenerator, self).__init__()
        # Operands pile
        self.pile_o = Stack()
        # Operators pile
        self.popper = Stack()
        # Pending jumps
        self.pjumps = Stack()
        # File to write list of quadruples
        self.file = filename
        # Id of temporal vars
        self.temporal_id = 1
        # List of quadruples
        self.quadruples = []
        # Quadruple counter
        self.cont = 0

    def printeame(self):
        for i in self.quadruples:
            print (i.printeame())

    def read_operand(self, operand):
        # Push Variable
        self.pile_o.push(operand)

    def read_operator(self, operator):
        self.popper.push(operator)     

    def generate_quad(self):
        # checa si el op es uno de los siguientes operadores
        op = self.popper.top()
        if op in ['+=', '-=', '*=', '/=']:
            self.generate_assignment_op_quad()
            return
        
        op = self.popper.pop()
        if op == '=':
            left_operand = self.pile_o.pop()
            right_operand = self.pile_o.pop()
        else:
            right_operand = self.pile_o.pop()
            left_operand = self.pile_o.pop()
        
        # print(self.pile_o)
       
        res = semantic_cube[right_operand.get_type()][left_operand.get_type()][op]

        if res != 'Error':
            # Genera variable temporal
            temp = Variable(name='t' + str(self.temporal_id), value=None, var_type=res)
            # Aumenta id de temporales
            self.temporal_id += 1
            # Obtiene el nombre o valor de los operandoss
            name_left = left_operand.get_name()
            name_right = right_operand.get_name()
            if name_left == 'constant':
                name_left = left_operand.get_value()
            if name_right == 'constant':
                name_right = right_operand.get_value()
            # Genera cuadruplo
            if op == '=':
                quad = Quadruple(id=self.cont, op=op, left_operand=name_left, right_operand="", res=name_right)
            else:
                quad = Quadruple(id=self.cont, op=op, left_operand=name_left, right_operand=name_right, res=temp.get_name())
            # Insert cuadruplo en la lista de cuadruplos
            self.quadruples.append(quad)
            self.cont += 1
            # pushea temporal a pila de operandos
            self.pile_o.push(temp)
        else:
            raise TypeError('Type missmatch ' + str(type(left_operand)) + ' and ' + str(type(right_operand)) + ' for operator: ' + op)

    def generate_assignment_op_quad(self):
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


    def generate_gotoF(self):
        last_operand = self.pile_o.pop()
        if last_operand.get_type() != 'bool':
            raise TypeError('Type missmatch. Non bool variables in condition')
        else:
            quad = Quadruple(id=self.cont, op='GotoF', left_operand=last_operand, right_operand=None, res=None)
            self.quadruples.append(quad)
            self.pjumps.push(self.cont)
            self.cont += 1

    def generate_goto(self):
        quad = Quadruple(id=self.cont, op='Goto', left_operand=None, right_operand=None, res=None)
        self.quadruples.append(quad)
        self.pjumps.push(self.cont)
        self.cont += 1

    def fill_goto(self):
        # Obtiene indice de cuadruplo pendiente en la lista de cuadruplos
        pending = self.pjumps.pop()
        self.quadruples[pending].res = self.cont


    def export(self):
        f = open(self.file, 'w')
        for q in self.quadruples:
            f.write(q.repr())
        f.close()  # you can omit in most cases as the destructor will call it