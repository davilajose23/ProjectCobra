from stack import Stack
from cube import semantic_cube

class Quadruple(object):
    """docstring for Quadruple"""
    def __init__(self, op, left_operand, right_operand, res):
        super(Quadruple, self).__init__()
        self.op = op
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.res = res

    def repr(self):
        return '({0}, {1}, {2}, {3})'.format(op, left_operand, right_operand, res)

class QuadGenerator(object):
    """docstring for QuadGenerator"""
    def __init__(self, filename):
        super(QuadGenerator, self).__init__()
        # Operands pile
        self.pile_o = Stack()
        # Operators pile
        self.popper = Stack()
        # File to write list of quadruples
        self.file = filename
        # Id of temporal vars
        self.temporal_id = 1
        # Valid operators
        self.operations = ('+',  '-', '*', '/', '+=', '-=', '*=', '/=', '%', 'mod', '<', '>', '!=', '==', '<=', '>=', 'and', 'not', 'or', '(', ')')
        # False bottoms counter
        self.false_bottom = 0
        # List of quadruples
        self.quadruples = []

    def read_operand(self, operand):
        self.pile_o.push(operand)

    def read_operator(self, operator):
        if operator in self.operations:
            if self.false_bottom > 0:
                    if operator == '(':
                        t = Stack()
                        self.popper.push(t)
                        self.false_bottom += 1
                    elif operator == ')':
                        self.popper.pop()
                        self.false_bottom -= 1
                    else:
                        self.popper.top().push(operator)
            else:
                self.popper.push(operator)
        else:
            print('Invalid operator ' + str(operator))
                

    def write_quad(self):
        if self.false_bottom > 0:
            op = self.popper.top().pop()
        else:
            op = self.popper.pop()

        right_operand = self.pile_o.pop()
        left_operand = self.pile_o.pop()
        res = semantic_cube[type(left_operand)][type(right_operand)][op]

        if res != 'Error':
            quad = Quadruple(op=op, left_operand=left_operand, right_operand=right_operand, res='t' + str(self.temporal_id))
            self.quadruples.append(quad)
        else:
            print('Type missmatch ' + str(type(left_operand)) + ' and ' + str(type(right_operand)) + ' for operator: ' + op)

    def validate_operator(self, operator):
        return operator in self.operations

    def export(self):
        f = open(self.file, 'w')
        for q in self.quadruples:
            f.write(q.repr())
        f.close()  # you can omit in most cases as the destructor will call it