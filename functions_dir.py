"""Modulo que contiene la clase directorio de funciones
-----------------------------------------------------------------
Compilers Design Project
Tec de Monterrey
Julio Cesar Aguilar Villanueva  A01152537
Jose Fernando Davila Orta       A00999281
-----------------------------------------------------------------

DOCUMENTATION: For complete Documentation see UserManual.pdf"""

from stack import Stack
from function import Function
from variable import Variable

def get_var_type(var_type):
    '''retorna el identificador de cada tipo de variable'''
    if var_type == 'int':
        return 'i'
    elif var_type == 'double':
        return 'd'
    elif var_type == 'string':
        return 's'
    elif var_type == 'bool':
        return 'b'

def get_var_scope(scope):
    '''retorna el identificador de cada tipo de scope'''
    if scope == 'global':
        return 'g'
    elif scope == 'main':
        return 'l'
    else:
        return 't'

def get_var_name(var_type, scope, var_name):
    '''construct the direccion of a variable based on
        the type, scope and variable name.'''
    name_type = get_var_type(var_type)
    name_scope = get_var_scope(scope)
    name = name_type + name_scope + var_name
    return name

class FunctionsDir(object):
    '''Las funciones son entradas en el diccionario functions.
        A cada funcion le corresponde de valor una lista.

        Esta lista contiene otro diccionario para varibales,
        y un return type, y cantidad de args

        Scope global del programa se inicia con diccionario
        de variables globales vacio.

        No se tiene un return type para el scope global.
        Scope es el function_id de cada funcion.'''

    def __init__(self):
        '''Metodo de inicializacion'''
        self.functions = {}
        self.functions['global'] = Function()
        self.scope = 'global'

        # Define si se esta evaluando la existencia de variables o se estan agregando al directorio
        self.evaluating = True

        # Indica si es necesario acutlaizar la lista de prametros de una funcion
        self.updating_params = False

        # Indica si se va a leer variable con funcion read
        self.reading = False

        # Ultimo token ID, usado para el read
        self.last_id = Stack()

        # Ultimo token de tipo que fue leido por el directorio de funciones
        self.last_type = None

        '''Funciones que estan siendo llamadas.
        Se utiliza una pila para llamadas nesteadas a funciones'''
        self.call_function = Stack()

        '''Cantidad de argumentos que estan siendo utilizados al llamar a una funcion.
        Se utiliza una pilla para llamadas nesteadas'''
        self.call_arguments = Stack()

        self.last_read = Stack()

    def add_function(self, function_id):
        '''Add function to fuctions directory. Verify if function already exists'''
        if self.functions.get(function_id, None) is not None:
            raise NameError('Function already declared! Function: ' + str(function_id))
        else:
            self.functions[function_id] = Function()

    def validate_function(self, function_id):
        '''Validate function exists'''
        if self.functions.get(function_id, None) is None:
            raise ValueError('Function not declared! Name: ' + str(function_id))

    def increase_expected_arguments(self):
        '''Manda llamar el metodo increase expected arguments de la clase Function'''
        self.functions[self.scope].increase_expected_arguments()

    def update_function_params(self, var_id, var_type):
        '''Manda llamar metodo update params de la clase Funcion'''
        self.functions[self.scope].update_params(var_id, var_type)

    def set_return_type(self, function_return_type):
        '''Manda llamar el metodo set return type de la clase Function'''
        self.functions[self.scope].set_return_type(function_return_type)

    def set_func_quad(self, func_quad):
        '''Manda llamar el metodo set_func_quad de la clase Function'''
        self.functions[self.scope].set_func_quad(func_quad)

    def set_scope(self, scope):
        '''Cambia el scope actual del directorio de funciones al scope que recibe'''
        self.scope = scope

    def reset_scope(self):
        '''Reset del scope a global scope'''
        self.scope = 'global'

    # Add variable to current function scope
    def add_var(self, variable_id, var_type, value=0, size=1):
        '''Agrega variable a el diccionario de variables de una Funcion'''
        if self.functions[self.scope].variables_dict.get(variable_id, None) is None:
            var_name = get_var_name(var_type, self.scope, variable_id)
            self.functions[self.scope].variables_dict[variable_id] = Variable(var_name, value, var_type, self.scope, size)
        else:
            variable_type = self.functions[self.scope].variables_dict[variable_id].get_type()
            msg = 'Variable already declared! VAR: ' + str(variable_id) + '. TYPE: ' + variable_type
            raise KeyError(msg)

    def add_for_var(self, variable_id, var_type):
        '''Agrega variable al diccionario del current scope, si ya existe sobreescribe valor
        Marca error si existe y no es tipo int'''
        if self.functions[self.scope].variables_dict.get(variable_id, None) is None:
            var_name = get_var_name(var_type, self.scope, variable_id)
            self.functions[self.scope].variables_dict[variable_id] = Variable(var_name, -1, var_type, self.scope, 1)
        else:
            variable_type = self.functions[self.scope].variables_dict[variable_id].get_type()
            if variable_type != 'int':
                msg = 'Variable already declared! VAR: ' + str(variable_id) + '. TYPE: ' + variable_type
                raise KeyError(msg)
            else:
                self.functions[self.scope].variables_dict[variable_id].value = -1

    def validate_variable(self, variable_id):
        '''Busca variable en el scope actual'''
        if self.functions[self.scope].variables_dict.get(variable_id, None) is None:
            # Busca variable en el scope global
            if self.functions['global'].variables_dict.get(variable_id, None) is None:
                raise ValueError('Variable not declared! VAR: ' + variable_id)

    def start_evaluating(self):
        '''Indica que el directorio de funciones esta evaluando la existencia de variables'''
        self.evaluating = True

    def finish_evaluating(self):
        '''Indica que el directorio de funciones deja de evaluar funciones'''
        self.evaluating = False

    def set_type(self, last_type):
        '''Set del ultimo token de tipo que fue leido'''
        self.last_type = last_type

    def get_func_dir(self):
        '''Obtiene el diccionario de funciones'''
        return self.functions

    def get_var(self, variable_id):
        '''Obtiene la lista con los datos de la variable del
        diccionario de funciones en el scope actual o el global'''
        if variable_id in self.functions[self.scope].variables_dict:
            return self.functions[self.scope].variables_dict.get(variable_id)
        elif variable_id in self.functions['global'].variables_dict:
            return self.functions['global'].variables_dict.get(variable_id)
        return None

    def set_call_function(self, function_id):
        '''Set del id de la funcion que esta siendo llamada
        una vez que se valido su existencia en el diccionario de funciones'''
        self.call_function.push(function_id)
        self.call_arguments.push(0)

    def increase_call_arguments(self):
        '''# Incrementa la cantidad de argumentos que estan siendo usados para llamar una funcion.
        Obtiene el tope de la pila, aumenta y vuelve a insertar en la pila'''
        curr = self.call_arguments.pop()
        curr += 1
        self.call_arguments.push(curr)

    def update_var_size(self, size):
        '''Actualiza el size de una variable en caso de ser dimensionada'''
        if size <= 0:
            raise ValueError('Array size must be a positive integer')
        else:
            self.functions[self.scope].variables_dict[self.last_id.top].size = size
            self.functions[self.scope].variables_dict[self.last_id.top].is_dim = True

    def validate_call_arguments(self):
        '''Funcion que valida que la cantidad de argumentos utilizados en una llamada a funcion
         sea igual a los parametros que espera recibir'''
        if self.functions[self.call_function.top].expected_arguments != self.call_arguments.top:

            if self.functions[self.call_function.top].expected_arguments > self.call_arguments.top:
                msg = 'Missing arguments in function call for function: ' + str(self.call_function)
            elif self.functions[self.call_function.top].expected_arguments < self.call_arguments.top:
                msg = 'Too many arguments in function call for function: ' + str(self.call_function)
            msg += '. Expected arguments: ' + str(self.functions[self.call_function.top].expected_arguments) + '. Got: ' + str(self.call_arguments.top)
            self.call_arguments.pop()
            self.call_function.pop()
            raise TypeError(msg)
        else:
            self.call_arguments.pop()
            return self.call_function.pop()

    def validate_arg_type(self, var_type):
        '''Funcion que valida que el tipo de argumento que se manda sea del tipo esperado'''
        expected_type = self.functions[self.call_function.top].params[self.call_arguments.top - 1][1]
        if var_type != expected_type:
            msg = 'Expected type in function call ' + str(self.scope) + ': ' + expected_type
            msg += '. Got: ' + var_type
            raise TypeError(msg)
        return self.functions[self.call_function.top].params[self.call_arguments.top - 1]

    def verify_var_dim(self):
        '''Verifica que el id de una variable sea dimensionada'''
        var = self.get_var(self.last_id.top)
        if not var.is_dim:
            raise ValueError('Variable is not array')

    @property
    def current_scope(self):
        '''Propiedad del directorio de funciones para obtener el scope actual'''
        return self.scope

    def printeame(self):
        '''Funcion auxiliar para imprimir el contenido del directorio de funciones'''
        print('************ Functions Directory ************\n')
        for key, val in self.functions.iteritems():
            print(str(val.return_type) + ' ' + str(key) + '('),
            for var in val.params:
                print(str(var[1]) + ' ' + str(var[0]) + ', '),
            print('): quad_num ' + str(val.get_function_quad()))
            for k, vals in val.variables_dict.iteritems():
                print('\t' + vals.get_type() + ' ' + k + ' = ' + str(vals.get_value()) + ' size: ' + str(vals.get_size()))
            print('')
        print('*********************************************')
