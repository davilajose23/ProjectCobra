'''Modulo que define la clase quadruple'''
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
