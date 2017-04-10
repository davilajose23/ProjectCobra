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


class Memory(object):
    'Clase de memoria para la Maquina Virtual'

    def __init__(self):
        self.integers = Chunk('int')
        self.doubles = Chunk('double')
        self.strings = Chunk('string')
        self.boolean = Chunk('bool')

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
            chunk = self.boolean
        else:
            return 'ERROR'
        return chunk.get_val(direccion[1:])


