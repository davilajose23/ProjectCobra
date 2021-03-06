"""This module is a semantic validator
-----------------------------------------------------------------
Compilers Design Project
Tec de Monterrey
Julio Cesar Aguilar Villanueva  A01152537
Jose Fernando Davila Orta       A00999281
-----------------------------------------------------------------

DOCUMENTATION: For complete Documentation see UserManual.pdf"""

# Create a tuple with all the operations posible
operations = ( '+',  '-', '*', '/', '+=', '-=', '*=', '/=', '%', 'mod', '<', '>', '!=', '==', '<=', '>=', 'and', 'not', 'or', '=')

# Some lambda functions
create = lambda x: dict(zip(operations, x))
create_manual = lambda x: dict(zip(operations, [x] * len(operations)))

# semantic cube
semantic_cube = {
    #                       '+',        '-',        '*',        '/',        '+=',       '-=',       '*=',       '/=',        '%',        'mod',       <,           >,          !=,         ==,        <=,          >=,         and,        not,        or,      =
    'int': {
        'int' : create([    'int',      'int',      'int',      'int',      'int',      'int',      'int',      'int',      'int',      'int',      'bool',     'bool',     'bool',     'bool',     'bool',     'bool',     'bool',     'bool',     'bool',     'int']) ,
        'double': create([  'double',   'double',   'double',   'double',   'double',   'double',   'double',   'double',   'double',   'double',   'bool',     'bool',     'bool',     'bool',     'bool',     'bool',     'bool',     'bool',     'bool',     'int']) ,
        'string': create_manual('Error'),
        'bool': create_manual('Error'),
        'list': create_manual('Error') 
    },    
    #                       '+',        '-',        '*',        '/',        '+=',       '-=',       '*=',       '/=',        '%',        'mod',       <,           >,          !=,         ==,        <=,          >=,         and,        not,        or,         =
    'double': {
        'int' :   create([  'double',   'double',   'double',   'double',   'double',   'double',   'double',   'double',   'double',   'double',   'bool',     'bool',     'bool',     'bool',     'bool',     'bool',     'bool',     'bool',     'bool',     'double']) ,
        'double': create([  'double',   'double',   'double',   'double',   'double',   'double',   'double',   'double',   'double',   'double',   'bool',     'bool',     'bool',     'bool',     'bool',     'bool',     'bool',     'bool',     'bool',     'double']) ,
        'string': create_manual('Error'),
        'bool': create_manual('Error'),
        'list': create_manual('Error') 
    },
    #                       '+',        '-',        '*',        '/',        '+=',       '-=',       '*=',       '/=',        '%',        'mod',       <,           >,          !=,         ==,        <=,          >=,         and,        not,        or,         =
    'string': {
        'int' : create_manual('Error'),
        'double': create_manual('Error'),
        'string': create([  'String',   'Error',    'Error',    'Error',    'String',   'Error',    'Error',    'Error',    'Error',    'Error',    'Error',    'Error',    'bool',    'bool',    'Error',    'Error',    'Error',    'Error',    'Error',      'string']), 
        'bool': create_manual('Error'),
        'list': create_manual('Error') 
    },
     #                       '+',        '-',        '*',        '/',        '+=',       '-=',       '*=',      '/=',        '%',        'mod',       <,           >,          !=,         ==,        <=,          >=,         and,        not,        or ,       =
    'bool': {
        'int' : create_manual('Error'),
        'double': create_manual('Error'),
        'string': create_manual('Error') ,
        'bool':  create([  'Error',     'Error',   'Error',     'Error',    'Error',    'Error',   'Error',     'Error',    'Error',    'Error',      'bool',     'bool',     'bool',     'bool',     'bool',     'bool',     'bool',     'bool',     'bool',   'bool']) ,
        'list': create_manual('Error') 
    },
    #                       '+',        '-',        '*',        '/',        '+=',       '-=',       '*=',       '/=',        '%',        'mod',       <,           >,          !=,         ==,        <=,          >=,         and,        not,        or ,        =
    'list': {
        'int' : create_manual('Error'),
        'double': create_manual('Error'),
        'string': create_manual('Error'),
        'bool': create_manual('Error'),
        'list': create_manual('Error') 
    }
}

