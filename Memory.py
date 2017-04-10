from stack import Stack
from cube import semantic_cube

class Chunk(object):
    'clase chunk para los pedazos de memoria'
    def __init__(self, name):
        'Metodo para inicializar la clase Chunk'
        self.name = 'name'
        # Diccionario de variables locales (main)
        self.local_variables = {}
        # Pila de diccionarios de variables temporales (funciones)
        self.temporal = Stack()
        # Diccionario de variables globales
        self.global_variables = {}
        # Diccionario de variables constantes
        self.constants = {}

    def get_val(self, direccion):
        segment = direccion[0]
        chunk = None
        if segment == 'l':
            chunk = self.local_variables[direccion[1]]
        elif segment == 't':
            chunk = self.temporal.top[direccion[1]]
        elif segment == 'g':
            chunk = self.global_variables[direccion[1]]
        elif segment == 'c':
            chunk = self.constants[direccion[1]]
        else:
            return 'ERROR'
        return chunk
        #return chunk.getVal(direccion[1:])

    def printeame(self):
        print(' Global:')
        for k, v in self.global_variables.iteritems():
            print(k, v)
        print(' Temporal:')
        tmp = self.temporal
        while tmp.length > 0:
            d = tmp.pop()
            for k, v in d.iteritems():
                print(k, v)
        print(' Local:')
        for k, v in self.local_variables.iteritems():
            print(k, v)
        print(' Constants:')
        for k, v in self.constants.iteritems():
            print(k, v)

class Memory(object):
    'Clase de memoria para la Maquina Virtual'

    def __init__(self):
        self.integers = Chunk('int')
        self.doubles = Chunk('double')
        self.strings = Chunk('string')
        self.booleans = Chunk('bool')

    # direccion = TypeSegmentID
    def get_val(self, direccion):
        tipo = direccion[0]
        chunk = None
        if tipo == 'i':
            chunk = self.integers
        elif tipo == 'd':
            chunk = self.doubles
        elif tipo == 's':
            chunk = self.strings
        elif tipo == 'b':
            chunk = self.booleans
        else:
            return 'ERROR'
        return chunk.get_val(direccion[1:])

    def printeame(self):
        print('Integers')
        self.integers.printeame()
        print('Doubles')
        self.doubles.printeame()
        print('Strings')
        self.strings.printeame()
        print('Boolean')
        self.booleans.printeame()

def test():
    memory = Memory()
    memory.integers.constants[1] = 1
    memory.integers.constants[2] = 2
    memory.integers.local_variables['x'] = 23
    memory.integers.global_variables['x'] = 81
    memory.integers.temporal.push({'x': 25})
    memory.printeame()

# test()
