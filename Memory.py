from stack import Stack
from cube import semantic_cube

class Chunk(object):
    'clase chunk para los pedazos de memoria'
    def __init__(self, name):
        'Metodo para inicializar la clase Chunk'
        self.name = 'name'
        self.local_variables = Stack()
        self.temporal = Stack()
        self.global_variables = {}
        self.constants = {}
    
    def getVal(direccion):
        segment = direccion[0]
        chunk = None
        if segment == 'l':
            chunk = self.local_variables
        elif segment == 't':
            chunk = self.temporal
        elif segment == 'g':
            chunk = self.global_variables
        elif segment == 'c':
            chunk = self.constants
        else:
            'ERROR'
        return chunk.getVal(direccion[1:])


class Memory(object):
    'Clase de memoria para la Maquina Virtual'

    def __init__(self):
        self.integers = Chunk('int')
        self.doubles = Chunk('double')
        self.strings = Chunk('string')
        self.boolean = Chunk('bool')

    # direccion = TypeSegmentID
    def getVal(direccion):
        tipo = direccion[0]
        chunk = None
        if tipo == 'i':
            chunk = self.integers
        elif tipo == 'd':
            chunk = self.doubles
        elif tipo == 's':
            chunk = self.strings
        elif tipo == 'b':
            chunk = self.boolean
        else:
            'ERROR'
        return chunk.getVal(direccion[1:])


