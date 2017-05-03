"""This Module define a Function Class that is used in the Functions
Directory.
-----------------------------------------------------------------
Compilers Design Project
Tec de Monterrey
Julio Cesar Aguilar Villanueva  A01152537
Jose Fernando Davila Orta       A00999281
-----------------------------------------------------------------

DOCUMENTATION: For complete Documentation see UserManual.pdf"""

class Function(object):
    '''Function object'''
    def __init__(self):
        '''Metodo para inicializar un objeto funcion'''
        self.return_type = None
        self.expected_arguments = 0
        self.params = []
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

    def update_params(self, var_id, var_type):
        '''Agrega tipo de variable y id a la lista de parametros'''
        self.params.append((var_id, var_type))

    def set_func_quad(self, quad_num):
        '''Establece el numero de cuadruplo en el que inicia la funcion'''
        self.function_quad_start = quad_num

    def get_function_quad(self):
        '''Retorna el numero de cuadruplo donde se define a la funcion'''
        return self.function_quad_start
