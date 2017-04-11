'''Este modulo contiene la definicion de la clase Stack'''

class Stack(object):
    '''Clase Pila, acepta objetos de cualquier tipo.'''

    def __init__(self):
        '''Metodo para inicializar un stack'''
        super(Stack, self).__init__()
        self.stack = []

    def __str__(self):
        '''Metodo de apoyo para visualizar contenidos del stack'''
        ret = ""
        for d in reversed(self.stack):
            ret = ret + str(d) + '\n'
        return str(ret)

    @property
    def length(self):
        '''Propiedad. Regresa la cantidad de elementos en el stack'''
        return len(self.stack)

    @property
    def top(self):
        '''Regresa el elemento en tope de la pila'''
        if self.length > 0:
            return self.stack[-1]

    @property
    def top2(self):
        '''Regresa siguiente elemento al tope de la pila'''
        if self.length > 1:
            return self.stack[-2]
        return ' '

    def push(self, arg):
        '''Inserta elemento en el tope de la pila'''
        self.stack.append(arg)

    def pop(self):
        '''Remueve el elemento del tope de la pila'''
        if self.length > 0:
            return self.stack.pop()
