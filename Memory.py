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
        # Variables para manejar el limite de memoria
        self.local_variables_size = 0
        self.local_variables_limit = 1000

        self.temporal_size = 0
        self.temporal_limit = 1000

        self.global_variables_size = 0
        self.global_variables_limit = 100

        self.constants_size = 0
        self.constants_limit = 100

    def get_val(self, direccion, param=False):
        '''Funcion que obtiene el valor guardado en memoria'''
        # Separa segmento de direccion
        segment = direccion[0]
        direccion = direccion[1:]

        # Verifica si es dimensionada
        is_dim = False
        chunk = None

        # Separa valores para acceder al valor de arreglo
        if '.' in direccion:
            res = direccion.split('.')
            var = res[0]
            index = res[1]
            is_dim = True

        # Accede dependiendo del segmento
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

        # Retorna valor
        if not is_dim:
            return chunk
        else:
            return chunk.get(index, 'ERROR get_val: 459')

    def set_val(self, direccion, val, size=1):
        '''Funcion que asigna valor a un pedazo de memoria'''
        # Separa segmento y direccion
        segment = direccion[0]
        direccion = direccion[1:]
        is_dim = False
        # Separa en caso de que sea dimensionada
        if '.' in direccion:
            res = direccion.split('.')
            var = res[0]
            index = res[1]
            is_dim = True

        # Escoge el segmento
        if segment == 'l':
            if is_dim:
                # Registra e incrementa tamanio del arreglo a contadores
                if self.local_variables.get(var, None) is None:
                    self.local_variables[var] = {}
                    self.local_variables_size += size

                self.local_variables[var][index] = val

            # Incrementa el tamanio de memoria de local
            if self.local_variables.get(direccion, None) is None:
                self.local_variables_size += 1
            self.local_variables[direccion] = val

        elif segment == 't':
            if is_dim:
                # Registra e incrementa tamanio del arreglo a contadores
                if self.temporal.top.get(var, None) is None:
                    self.temporal.top[var] = {}
                    self.temporal_size += size

                self.temporal.top[var][index] = val

            # Incrementa el tamanio de memoria de temporales
            if self.temporal.top.get(direccion, None)  is None:
                self.temporal_size += 1
            self.temporal.top[direccion] = val

        elif segment == 'g':
            if is_dim:
                # Registra e incrementa tamanio del arreglo a contadores
                if self.global_variables.get(var, None) is None:
                    self.global_variables[var] = {}
                    self.global_variables_size += size

                self.global_variables[var][index] = val

            # Incrementa el tamanio de memoria de variables globales
            if self.global_variables.get(direccion, None):
                self.global_variables_size += 1
            self.global_variables[direccion] = val

        elif segment == 'c':
            if is_dim:
                # Registra e incrementa tamanio del arreglo a contadores
                if self.constants.get(var, None) is None:
                    self.constants[var] = {}
                    self.constants_size += size

                self.constants[var][index] = val

            # Incrementa el tamanio de memoria de constantes
            if self.constants.get(direccion, None) is None:
                self.constants_size += 1
            self.constants[direccion] = val
        else:
            print('ERROR in chunk 1248')
        #return chunk.getVal(direccion[1:])
        self.checkLimits()


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
        '''Pushea diccionario al stack de temporales para funciones'''
        self.temporal.push({})

    def EndProc(self):
        '''Elimina stacks y resta de los tamanios'''
        self.temporal_size -= len(self.temporal.top)
        self.temporal.pop()

    def checkLimits(self):
        '''Funcion para checar los limites del chunk'''
        if self.local_variables_size >= self.local_variables_limit:
            raise Exception('ERROR 5004 Memory limit reached: Local Variables')

        elif self.temporal_size >= self.temporal_limit:
            raise Exception('ERROR 5005 Memory limit reached: Global Variables')

        elif self.global_variables_size >= self.global_variables_limit:
            raise Exception('ERROR 5006 Memory limit reached: Temporal Variables')

        elif self.constants_size >= self.constants_limit:
            raise Exception('ERROR 5007 Memory limit reached: constants')


class Memory(object):
    'Clase de memoria para la Maquina Virtual'

    def __init__(self):
        self.integers = Chunk('int')
        self.doubles = Chunk('double')
        self.strings = Chunk('string')
        self.booleans = Chunk('bool')

    # direccion = TypeSegmentID
    def get_val(self, direccion, param=False):
        '''Obtiene valor de memoria con chunk'''
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

    def set_val(self, direccion, val, size=1):
        '''Asigna valor de memoria con chunk'''
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
        chunk.set_val(direccion[1:], val, size)

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
        '''Pushea stacks para funciones'''
        self.integers.Era()
        self.doubles.Era()
        self.strings.Era()
        self.booleans.Era()

    def endproc(self):
        '''Pop de stacks de funciones'''
        self.integers.EndProc()
        self.doubles.EndProc()
        self.strings.EndProc()
        self.booleans.EndProc()
