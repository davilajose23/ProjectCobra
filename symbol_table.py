'''Importa clase stack'''
from stack import Stack

class Function(object):
    '''Function object'''
    def __init__(self):
        '''Metodo para inicializar un objeto funcion'''
        self.return_type = None
        self.expected_arguments = 0
        self.parameters_specification = []
        self.variables_dict = {}
        self.function_quad_start = -1

    def set_return_type(self, return_type):
        '''Asigna tipo de retorno a un objeto funcion'''
        self.return_type = return_type

    def get_return_type(self):
        '''Regresa el tipo de retorno de una funcion'''
        return self.return_type

    def increase_expected_arguments(self):
        '''Incrementa la cantidad de argumentos que espera recibir una funcion'''
        self.expected_arguments += 1

    def get_expected_arguments(self):
        '''Regresa la cantidad de argumentos que espera una funcion'''
        return self.expected_arguments

    def update_params(self, var_type, var_id):
        '''Agrega tipo de variable y id a la lista de parametros'''
        self.parameters_specification.append((var_type, var_id))

    def set_func_quad(self, quad_num):
        '''Establece el numero de cuadruplo en el que inicia la funcion'''
        self.function_quad_start = quad_num

    def get_function_quad(self):
        '''Retorna el numero de cuadruplo donde se define a la funcion'''
        return self.function_quad_start

class FunctionsDir(object):
    '''
        Las funciones son entradas en el diccionario functions.
        A cada funcion le corresponde de valor una lista.
        Esta lista contiene otro diccionario para varibales, y un return type, y cantidad de args
        Scope global del programa se inicia con diccionario de variables globales vacio.
        No se tiene un return type para el scope global.
        Scope es el function_id de cada funcion.
    '''
    def __init__(self):
        '''Metodo de inicializacion'''
        self.functions = {}
        self.functions['global'] = Function()
        self.scope = 'global'

        # Define si se esta evaluando la existencia de variables o se estan agregando al directorio
        self.evaluating = False

        # Ultimo token de tipo que fue leido por el directorio de funciones
        self.last_type = None

        '''Funciones que estan siendo llamadas.
        Se utiliza una pila para llamadas nesteadas a funciones'''
        self.call_function = Stack()

        '''Cantidad de argumentos que estan siendo utilizados al llamar a una funcion.
        Se utiliza una pilla para llamadas nesteadas'''
        self.call_arguments = Stack()

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
    def add_var(self, variable_id, var_type, value=0):
        '''Agrega variable a el diccionario de variables de una Funcion'''
        if self.functions[self.scope].variables_dict.get(variable_id, None) is None:
            self.functions[self.scope].variables_dict[variable_id] = [value, var_type]
        else:
            msg = 'Variable already declared! VAR: ' + str(variable_id) + '. TYPE: ' + str(self.functions[self.scope].variables_dict[variable_id][1])
            raise KeyError(msg)

    def validate_variable(self, variable_id):
        '''Busca variable en el scope actual'''
        if self.functions[self.scope].variables_dict.get(variable_id, None) is None:
            # Busca variable en el scope global
            if self.functions['global'].variables_dict.get(variable_id, None) is None:
                raise ValueError('Variable not declared! VAR: ' + str(variable_id))

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
        elif variable_id  in self.functions['global'].variables_dict:
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
            self.call_function.pop()

    @property
    def current_scope(self):
        '''Propiedad del directorio de funciones para obtener el scope actual'''
        return self.scope

    def printeame(self):
        '''Funcion auxiliar para imprimir el contenido del directorio de funciones'''
        print('************ Functions Directory ************\n')
        for key, val in self.functions.iteritems():
            print(str(val.return_type) + ' ' + str(key) + '(): quad_num ' + str(val.get_function_quad()))
            for k, vals in val.variables_dict.iteritems():
                print('\t' + str(vals[1]) + ' ' + str(k) + ' = ' + str(vals[0]))
            print('')
        print('*********************************************')
