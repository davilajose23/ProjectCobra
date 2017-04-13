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
        self.temporal.push({})
        # Diccionario de variables globales
        self.global_variables = {}
        # Diccionario de variables constantes
        self.constants = {}

    def get_val(self, direccion):
        segment = direccion[0]
        chunk = None
        if segment == 'l':
            chunk = self.local_variables.get(direccion[1:], 'ERROR get_val: 458')
        elif segment == 't':
            chunk = self.temporal.top
            chunk = chunk.get(direccion[1:], 'ERROR get_val: 458')
        elif segment == 'g':
            chunk = self.global_variables.get(direccion[1:], 'ERROR get_val: 458')
        elif segment == 'c':
            chunk = self.constants.get(direccion[1:], 'ERROR get_val: 458')
        return chunk
        #return chunk.getVal(direccion[1:])
    

    def set_val(self, direccion, val):
        segment = direccion[0]
        chunk = None
        if segment == 'l':
            self.local_variables[direccion[1:]] = val
        elif segment == 't':
            self.temporal.top[direccion[1:]] = val
        elif segment == 'g':
            self.global_variables[direccion[1:]] = val
        elif segment == 'c':
            self.constants[direccion[1:]] = val
        else:
            print('ERROR in chunk 1248')
        #return chunk.getVal(direccion[1:])

    def printeame(self):
        print(' Global:')
        for k, v in self.global_variables.iteritems():
            print(k, v)
        print(' Temporal:')
        tmp = self.temporal
        while tmp.length > 0:
            print('  Stack' + str(tmp.length))
            d = tmp.pop()
            for k, v in d.iteritems():
                print(k, v)
        print(' Local:')
        for k, v in self.local_variables.iteritems():
            print(k, v)
        print(' Constants:')
        for k, v in self.constants.iteritems():
            print(k, v)
        
    def Era(self):
        self.temporal.push({})

    def EndProc(self):
        self.temporal.pop()

class Memory(object):
    'Clase de memoria para la Maquina Virtual'

    def __init__(self):
        self.integers = Chunk('int')
        self.doubles = Chunk('double')
        self.strings = Chunk('string')
        self.booleans = Chunk('bool')

    # direccion = TypeSegmentID
    def get_val(self, direccion):
        direccion = direccion.rstrip().lstrip()
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
            return 'ERROR get_val:458'
        return chunk.get_val(direccion[1:])

    def set_val(self, direccion, val):
        tipo = direccion[0].rstrip().lstrip()
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
            print('ERROR Memory 5214')
        chunk.set_val(direccion[1:], val)

    def printeame(self):
        print('Integers')
        self.integers.printeame()
        print('Doubles')
        self.doubles.printeame()
        print('Strings')
        self.strings.printeame()
        print('Boolean')
        self.booleans.printeame()
    
    def era(self):
        self.integers.Era()
        self.doubles.Era()
        self.strings.Era()
        self.booleans.Era()
    
    def endproc(self):
        self.integers.EndProc()
        self.doubles.EndProc()
        self.strings.EndProc()
        self.booleans.EndProc()
# def test():
#     memory = Memory()
#     memory.integers.constants[1] = 1
#     memory.integers.constants[2] = 2
#     memory.integers.local_variables['x'] = 23
#     memory.integers.global_variables['x'] = 81
#     memory.integers.temporal.push({'x': 25})
#     memory.printeame()

# test()
