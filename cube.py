operations      = ( '+',  '-', '*', '/', '+=', '-=', '*=', '/=', '%', 'mod', '<', '>', '!=', '==', '<=', '>=', 'and', 'not', 'or')
create = lambda x: dict(zip(operations, x))
create_manual = lambda x: dict(zip(operations, [x] * len(operations)))
# semantic cube
semantic_cube = {
    #                       '+',        '-',        '*',        '/',        '+=',       '-=',       '*=',       '/=',        '%',        'mod',       <,           >,          !=,         ==,        <=,          >=,         and,        not,        or
    'int': {
        'int' : create([    'int',      'int',      'int',      'int',      'int',      'int',      'int',      'int',      'int',      'int',      'bool',     'bool',     'bool',     'bool',     'bool',     'bool',     'bool',     'bool',     'bool']) ,
        'double': create([  'double',   'double',   'double',   'double',   'double',   'double',   'double',   'double',   'double',   'double',   'bool',     'bool',     'bool',     'bool',     'bool',     'bool',     'bool',     'bool',     'bool']) ,
        'string': create_manual('Error'),
        'bool': create_manual('Error'),
        'list': create_manual('Error') 
    },    
    #                       '+',        '-',        '*',        '/',        '+=',       '-=',       '*=',       '/=',        '%',        'mod',       <,           >,          !=,         ==,        <=,          >=,         and,        not,        or
    'double': {
        'int' :   create([  'double',   'double',   'double',   'double',   'double',   'double',   'double',   'double',   'double',   'double',   'bool',     'bool',     'bool',     'bool',     'bool',     'bool',     'bool',     'bool',     'bool']) ,
        'double': create([  'double',   'double',   'double',   'double',   'double',   'double',   'double',   'double',   'double',   'double',   'bool',     'bool',     'bool',     'bool',     'bool',     'bool',     'bool',     'bool',     'bool']) ,
        'string': create_manual('Error'),
        'bool': create_manual('Error'),
        'list': create_manual('Error') 
    },
    #                       '+',        '-',        '*',        '/',        '+=',       '-=',       '*=',       '/=',        '%',        'mod',       <,           >,          !=,         ==,        <=,          >=,         and,        not,        or
    'string': {
        'int' : create_manual('Error'),
        'double': create_manual('Error'),
        'string': create([  'String',   'Error',    'Error',    'Error',    'String',   'Error',    'Error',    'Error',    'Error',    'Error',    'Error',    'Error',    'bool',    'bool',    'Error',    'Error',    'Error',    'Error',    'Error']), 
        'bool': create_manual('Error'),
        'list': create_manual('Error') 
    },
     #                       '+',        '-',        '*',        '/',        '+=',       '-=',       '*=',      '/=',        '%',        'mod',       <,           >,          !=,         ==,        <=,          >=,         and,        not,        or  
    'bool': {
        'int' : create_manual('Error'),
        'double': create_manual('Error'),
        'string': create_manual('Error') ,
        'bool':  create([  'Error',     'Error',   'Error',     'Error',    'Error',    'Error',   'Error',     'Error',    'Error',    'Error',      'bool',     'bool',     'bool',     'bool',     'bool',     'bool',     'bool',     'bool',     'bool']) ,
        'list': create_manual('Error') 
    },
    #                       '+',        '-',        '*',        '/',        '+=',       '-=',       '*=',       '/=',        '%',        'mod',       <,           >,          !=,         ==,        <=,          >=,         and,        not,        or
    'list': {
        'int' : create_manual('Error'),
        'double': create_manual('Error'),
        'string': create_manual('Error'),
        'bool': create_manual('Error'),
        'list': create_manual('Error') 
    }
}