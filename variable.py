'''Modulo que define la clase variable'''
class Variable(object):
    '''Clase Variable. Contiene nombre, tipo y valor'''
    def __init__(self, name, value, var_type):
        self.name = name
        self.value = value
        self.type = var_type

    def __str__(self):
        '''Metodo para imprimir variables'''
        return 'VAR. NAME: {0}, VALUE: {1}, TYPE: {2}'.format(self.name, self.value, self.type)

    def get_type(self):
        '''Regresa el tipo de la variable'''
        return self.type

    def get_name(self):
        '''Regresa el nombre de la variable'''
        return self.name

    def get_value(self):
        '''Regresa el valor asignado a una variable'''
        return self.value