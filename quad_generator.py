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
        self.pile_o = Stack()
        self.popper = Stack()
        self.file = filename
        self.temporal_id = 1
        self.operations = ('+',  '-', '*', '/', '+=', '-=', '*=', '/=', '%', 'mod', '<', '>', '!=', '==', '<=', '>=', 'and', 'not', 'or', '(', ')')
        self.false_bottom = 0
        self.quadruples = []

    def read_operand(self, operand):
            

    def read_operator(self, operator):
        if not self.popper.length and self.validate_operator(operator):
            self.popper.push(operator)
        else:
            # Checks for pending * / mod %
            if self.popper.top() in set(['*', '/', 'mod', '%']):
                if self.false_bottom > 0:

                else:


            elif self.popper.top() in set(['+', '-']):
                if self.false_bottom > 0:

                else:

            elif self.popper.top() in set(['<', '>', '!=', '==', '<=', '>=']):
                if self.false_bottom > 0:

                else:


    def write_quad(self):
        if self.false_bottom > 0:
            op = self.popper.top().pop()
            right_operand = self.pile_o.pop()
            left_operand = self.pile_o.pop()
        else:
            op = self.popper.pop()
            right_operand = self.pile_o.pop()
            left_operand = self.pile_o.pop()



    def validate_operator(self, operator):
        return operator in self.operations
