from stack import Stack
from cube import semantic_cube

class Chunk(object):
    'clase chunk para los pedazos de memoria'
    def __init__(self, name):
        'Metodo para inicializar la clase Chunk'
        self.name = name
        # Diccionario de variables locales (main)
        self.local_variables = {}
        # Pila de diccionarios de variables temporales (funciones)
        self.temporal = Stack()
        self.temporal.push({})
        # Diccionario de variables globales
        self.global_variables = {}
        # Diccionario de variables constantes
        self.constants = {}

    def get_val(self, direccion, param=False):
        segment = direccion[0]
        direccion = direccion[1:]
        is_dim = False
        chunk = None

        if '.' in direccion:
            res = direccion.split('.')
            var = res[0]
            index = res[1]
            is_dim = True

        if segment == 'l':
            if is_dim:
                chunk = self.local_variables.get(var, 'ERROR get_val: 458')
            else:
                chunk = self.local_variables.get(direccion, 'ERROR get_val: 458')

        elif segment == 't':
            if param:
                chunk = self.temporal.top2
            else:
                chunk = self.temporal.top

            if is_dim:
                chunk = chunk.get(var, 'ERROR get_val: 458')
            else:
                chunk = chunk.get(direccion, 'ERROR get_val: 458')

        elif segment == 'g':
            if is_dim:
                chunk = self.global_variables.get(var, 'ERROR get_val: 458')
            else:
                chunk = self.global_variables.get(direccion, 'ERROR get_val: 458')

        elif segment == 'c':
            if is_dim:
                chunk = self.constants.get(var, 'ERROR get_val: 458')
            else:
                chunk = self.constants.get(direccion, 'ERROR get_val: 458')

        if not is_dim:
            return chunk
        else:
            return chunk.get(index, 'ERROR get_val: 459')
        #return chunk.getVal(direccion[1:])

    def set_val(self, direccion, val):
        segment = direccion[0]
        direccion = direccion[1:]
        is_dim = False

        if '.' in direccion:
            res = direccion.split('.')
            var = res[0]
            index = res[1]
            is_dim = True

        if segment == 'l':
            if is_dim:
                if self.local_variables.get(var, None) is None:
                    self.local_variables[var] = {}
                self.local_variables[var][index] = val
            self.local_variables[direccion] = val

        elif segment == 't':
            if is_dim:
                if self.temporal.top.get(var, None) is None:
                    self.temporal.top[var] = {}
                self.temporal.top[var][index] = val
            self.temporal.top[direccion] = val

        elif segment == 'g':
            if is_dim:
                if self.global_variables.get(var, None) is None:
                    self.global_variables[var] = {}
                self.global_variables[var][index] = val
            self.global_variables[direccion] = val

        elif segment == 'c':
            if is_dim:
                if self.constants.get(var, None) is None:
                    self.constants[var] = {}
                self.constants[var][index] = val
            self.constants[direccion] = val
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
    def get_val(self, direccion, param=False):
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
        return chunk.get_val(direccion[1:], param)

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
