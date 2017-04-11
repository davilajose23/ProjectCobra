import ply.yacc as yacc
from scanner import tokens
import sys
from symbol_table import FunctionsDir
from stack import Stack
from cube import semantic_cube
from quad_generator import Variable, Quadruple, QuadGenerator

functions_directory = FunctionsDir()
# Precedence rules for the arithmetic operators
precedence = (
    ('nonassoc', 'AND', 'OR'),  # Nonassociative operators
    ('nonassoc', 'LESS', 'GREATER', 'EQUALS_EQUALS', 'GREATER_EQUALS', 'LESS_EQUALS', 'NOT_EQUALS'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD', 'PERCENTAGE'),
    # ('right','UMINUS'),
)

generator = QuadGenerator('output.txt')
def debug(x):
    '''Funcion de ayuda para debugging'''
    print(x)
# ********************* Diagram program *********************
def p_init(p):
    'init : push_goto program'

def p_program(p):
    '''program : pre_variables functions main
                | functions main
                | pre_variables main
                | main'''
    p[0] = 'ok'
    debug(generator.printeame())
    debug(functions_directory.printeame())

def p_pre_variables(p):
    'pre_variables : declaration post_variables'

def p_post_variables(p):
    '''post_variables : pre_variables
                        | empty'''

# ********************* Diagram EOL helpers *********************
def p_required_eol(p):
    'required_eol : EOL optional_eol'

def p_optional_eol(p):
    '''optional_eol : empty
                | required_eol'''

# ********************* Diagram types *********************
def p_types(p):
    '''types : INT
            | DOUBLE
            | STRING
            | BOOL'''
   
    functions_directory.set_type(p[1])
# ********************* Diagram delcaration *********************
def p_declaration(p):
    'declaration : finish_evaluating types set_type inter_declaration required_eol start_evaluating'

def p_set_type(p):
    'set_type :'

def p_inter_declaration(p):
    'inter_declaration : identifier cycle_declaration'

def p_cycle_declaration(p):
    '''cycle_declaration : COMMA inter_declaration
                        | empty'''

# ********************* Diagram functions *********************
def p_functions(p):
    'functions : function post_functions'

def p_post_functions(p):
    '''post_functions : functions
                    | empty'''

# ********************* Diagram main *********************
def p_main(p):
    'main : MAIN fill_goto set_main_scope required_eol pre_variables block END_MAIN push_end optional_eol'

def p_push_end(p):
    'push_end :'
    generator.finish()

def p_set_main_scope(p):
    'set_main_scope :'
    functions_directory.add_function(p[-1])
    functions_directory.set_scope(p[-1])
    functions_directory.set_return_type('void')

# ********************* Diagram block *********************
def p_block(p):
    'block : statement post_block'

def p_post_block(p):
    '''post_block : block
                    | empty'''

# ********************* Diagram call_function *********************
def p_call_function(p):
    'call_function :  ID validate_function_call LEFT_PARENTHESIS push_paren post_call_function'

# Validates call to a function
def p_validate_function_call(p):
    'validate_function_call :'
    functions_directory.validate_function(p[-1])
    generator.generate_era(p[-1])
    # Settea el id de la funcion que va a ser llamada
    functions_directory.set_call_function(p[-1])

def p_post_call_function(p):
    ''' post_call_function : arguments RIGHT_PARENTHESIS pop_paren validate_call_arguments
                            | RIGHT_PARENTHESIS pop_paren validate_call_arguments'''

def p_validate_call_arguments(p):
    # Valida solamente que la cantidad de argumentos coincida con la cantidad que se espera recibir
    'validate_call_arguments :'
    func_name = functions_directory.validate_call_arguments()
    generator.generate_gosub(func_name)
    func_type = functions_directory.functions[func_name].get_return_type()
    if func_type != 'void':
        val = functions_directory.functions['global'].variables_dict[func_name][0]
        generator.generate_func_assign(func_name, func_type, val)

# ********************* Diagram arguments *********************
def p_arguments(p):
    'arguments : cond increase_call_arguments post_arguments'

# Funcion que incrementa la cantidad de argumentos con los que es llamada una funcion
def p_increase_call_arguments(p):
    'increase_call_arguments :'
    functions_directory.increase_call_arguments()
    argument = generator.pile_o.pop()
    tmp_param = functions_directory.validate_arg_type(argument.get_type())
    param = Variable(tmp_param[0], -1, tmp_param[1])
    generator.generate_param(argument, param)

def p_post_arguments(p):
    '''post_arguments : COMMA arguments
                            | empty'''

# ********************* Diagram function *********************
def p_function(p):
    'function : FUNC func_types set_type ID register_function LEFT_PARENTHESIS post_function'

def p_func_types(p):
    '''func_types : types
            | VOID'''

    if p[1] == 'void':
        functions_directory.set_type('void')

def p_register_function(p):
    'register_function :'
    functions_directory.add_function(p[-1])
    if functions_directory.last_type != 'void':
        functions_directory.add_var(p[-1], functions_directory.last_type)
    functions_directory.set_scope(p[-1])
    functions_directory.set_return_type(functions_directory.last_type)
    functions_directory.set_func_quad(generator.cont)


def p_post_function(p):
    '''post_function : parameters RIGHT_PARENTHESIS required_eol post_variables func_return
                          | RIGHT_PARENTHESIS required_eol post_variables func_return'''
    generator.generate_endproc()
def p_func_return(p):
    '''func_return : void_return
                    | value_return'''

def p_void_return(p):
    'void_return : block post_void_return'

def p_post_void_return(p):
    '''post_void_return : END reset_scope required_eol
                        | RETURN required_eol END reset_scope required_eol'''

def p_value_return(p):
    '''value_return : block RETURN cond create_return required_eol END reset_scope required_eol
                    | RETURN cond create_return required_eol END reset_scope required_eol'''

def p_create_return(p):
    'create_return :'
    val = generator.generate_return()
    functions_directory.functions['global'].variables_dict[functions_directory.current_scope][0] = val

def p_reset_scope(p):
    'reset_scope :'
    functions_directory.reset_scope()
    generator.reset_temporal_id()

# ********************* Diagram parameters *********************
def p_parameters(p):
    'parameters : finish_evaluating start_params types set_type identifier update_function_parameters post_parameters finish_params start_evaluating'

def p_start_params(p):
    'start_params :'
    functions_directory.updating_params = True

def p_finish_params(p):
    'finish_params :'
    functions_directory.updating_params = False

# Increases the quantity of expected arguments by a function
def p_update_function_parameters(p):
    'update_function_parameters :'
    functions_directory.increase_expected_arguments()

def p_post_parameters(p):
    '''post_parameters : COMMA parameters
                        | empty'''

# ********************* Diagram statement *********************
def p_statement(p):
    ''' statement : assignment required_eol
                    | condition required_eol
                    | print required_eol
                    | read required_eol
                    | loop required_eol
                    | call_function required_eol'''

# ********************* Diagram assignment *********************

def p_assignment(p):
    'assignment : ID validate_var push_var array_notation assignment_operator cond pop_assignment'

def p_validate_var(p):
    'validate_var :'
    functions_directory.validate_variable(p[-1])

def p_push_var(p):
    'push_var :'
    if functions_directory.get_var(p[-2]) is not None:
        # A list with value and var_type is returned
        res = functions_directory.get_var(p[-2])
        # Create variable
        var = Variable(name=p[-2], value=res[0], var_type=res[1])
        generator.pile_o.push(var)

def p_array_notation(p):
    '''array_notation : LEFT_BRACKET exp RIGHT_BRACKET
                        | empty'''

# ********************* Diagram assignment_operator *********************
def p_assignment_operator(p):
    '''assignment_operator : EQUALS push_assignment
                            | TIMES_EQUALS push_assignment
                            | DIVIDE_EQUALS push_assignment
                            | PLUS_EQUALS push_assignment
                            | MINUS_EQUALS push_assignment'''

def p_push_assignment(p):
    'push_assignment :'
    generator.popper.push(p[-1])

def p_pop_assignment(p):
    'pop_assignment :'
    assignment_operators = ['=', '*=', '/=', '+=', '-=']
    if generator.popper.top in assignment_operators:
        generator.generate_quad()

def p_start_evaluating(p):
    'start_evaluating :'
    functions_directory.start_evaluating()

def p_finish_evaluating(p):
    'finish_evaluating :'
    functions_directory.finish_evaluating()

# ********************* Diagram cond *********************
def p_cond(p):
    'cond : expression pop_op_and_or post_cond'

def p_pop_op_and_or(p):
    'pop_op_and_or :'
    if generator.popper.top == 'and' or generator.popper.top == 'or':
        generator.generate_quad()

def p_post_cond(p):
    '''post_cond : AND push_op_and_or cond
                | OR  push_op_and_or cond
                | empty'''

def p_push_op_and_or(p):
    'push_op_and_or :'
    generator.popper.push(p[-1])

# ********************* Diagram expression *********************
def p_expression(p):
    'expression : exp pop_relop post_expression'

def p_pop_relop(p):
    'pop_relop :'
    relops = ['<', '>', '<=', '>=', '!=']
    if generator.popper.top in relops:
        generator.generate_quad()

def p_post_expression(p):
    '''post_expression : relational_operator expression
                        | empty'''

def p_push_relop(p):
    'push_relop :'
    generator.popper.push(p[-1])

# ********************* Diagram relational_operator *********************
def p_relational_operator(p):
    '''relational_operator : LESS push_relop
                            | GREATER push_relop
                            | GREATER_EQUALS push_relop
                            | LESS_EQUALS push_relop
                            | EQUALS_EQUALS push_relop
                            | NOT_EQUALS push_relop'''

# ********************* Diagram exp *********************
def p_exp(p):
    'exp : term pop_exp post_exp'

def p_pop_exp(p):
    'pop_exp :'
    if generator.popper.top == '+' or generator.popper.top == '-':
        generator.generate_quad()

def p_post_exp(p):
    ''' post_exp : PLUS push_exp exp
                | MINUS push_exp exp
                | empty'''

def p_push_exp(p):
    'push_exp :'
    generator.popper.push(p[-1])

# ********************* Diagram term *********************
def p_term(p):
    'term : factor pop_term post_term'

def p_pop_term(p):
    'pop_term :'
    operators = ['*', '/', '%', 'mod']
    if generator.popper.top in operators:
        generator.generate_quad()

def p_post_term(p):
    ''' post_term : TIMES push_term term
                | DIVIDE push_term term
                | PERCENTAGE push_term term
                | MOD push_term term
                | empty'''

def p_push_term(p):
    'push_term :'
    generator.popper.push(p[-1])

# ********************* Diagram factor *********************
def p_factor(p):
    '''factor : LEFT_PARENTHESIS push_paren cond RIGHT_PARENTHESIS pop_paren
                | variable_constant
                | MINUS variable_constant
                | call_function'''

def p_push_paren(p):
    'push_paren :'
    generator.popper.push(p[-1])

def p_pop_paren(p):
    'pop_paren :'
    generator.popper.pop()

# ********************* Diagram variable_constant *********************
def p_variable_constant(p):
    '''variable_constant : ID process_variable array_notation
                        | INT_CONSTANT
                        | DOUBLE_CONSTANT
                        | STRING_CONSTANT
                        | BOOL_CONSTANT '''
    p[0] = p[1]
    if functions_directory.get_var(p[1]) is not None:
        # A list with value and var_type is returned
        res = functions_directory.get_var(p[1])
        # Create variable
        var = Variable(name=p[1], value=res[0], var_type=res[1])
        generator.pile_o.push(var)
    else:
        var = Variable(name='constant', value=p[1], var_type=get_type(p[1]))
        generator.pile_o.push(var)

def p_process_variable(p):
    'process_variable :'
    # Checks if the variable to validate is in array notation
    if  functions_directory.evaluating:
        functions_directory.validate_variable(p[-1])
        if functions_directory.reading:
            functions_directory.last_id = p[-1]
    else:
        functions_directory.add_var(variable_id=p[-1], var_type=functions_directory.last_type)
        if functions_directory.updating_params:
            functions_directory.update_function_params(var_id=p[-1], var_type=functions_directory.last_type)

# ********************* Diagram condition *********************
def p_condition(p):
    'condition : IF cond COLON push_gotoF optional_eol block post_condition END'

def p_push_gotoF(p):
    'push_gotoF :'
    generator.generate_gotoF()

def p_fill_goto(p):
    'fill_goto :'
    generator.fill_goto()


def p_post_condition(p):
    '''post_condition : else
                        | fill_goto empty'''

# else
def p_else(p):
    'else : ELSE fill_goto_else COLON push_goto optional_eol block fill_goto'

def p_fill_goto_else(p):
    'fill_goto_else :'
    generator.fill_goto_else()

def p_push_goto(p):
    'push_goto :'
    generator.generate_goto()

# ********************* Diagram print *********************
def p_print(p):
    'print : PRINT cond post_print'

def p_post_print(p):
    '''post_print : print_mod
                    | print_default'''

def p_print_mod(p):
    '''print_mod : COMMA STRING_CONSTANT print_post_mod'''

def p_print_post_mod(p):
    'print_post_mod :'
    generator.generate_print(p[-1])

def p_print_default(p):
    'print_default : empty'
    generator.generate_print()

# ********************* Diagram read *********************
def p_read(p):
    'read : READ start_read LEFT_PARENTHESIS identifier RIGHT_PARENTHESIS read_var'

def p_start_read(p):
    'start_read :'
    functions_directory.reading = True

def p_read_var(p):
    'read_var :'
    tmp = functions_directory.get_var(functions_directory.last_id)
    var = Variable(functions_directory.last_id, tmp[0], tmp[1])
    generator.generate_read(var)
    functions_directory.reading = False
    functions_directory.last_id = None


# ********************* Diagram identifier *********************
def p_identifier(p):
    'identifier : ID process_variable post_identifier'

def p_post_identifier(p):
    '''post_identifier : LEFT_BRACKET exp RIGHT_BRACKET
                        | empty'''

# ********************* Diagram loop *********************
def p_loop(p):
    '''loop : for
            | while'''

# for
def p_for(p):
    'for : FOR ID add_var FROM exp init_var TO exp push_cycle post_cycle create_pending_goto'

def p_add_var(p):
    'add_var :'
    functions_directory.add_var(variable_id=p[-1], var_type='int')
    var = Variable(name=p[-1], value=-1, var_type='int')
    # generator.pile_o.push(var)

def p_init_var(p):
    'init_var :'
    # generator.generate_for_quad()

# while
def p_while(p):
    'while : WHILE push_cycle cond push_gotoF post_cycle fill_goto create_pending_goto'

def p_push_cycle(p):
    'push_cycle :'
    generator.pcycles.push(generator.cont)

def p_create_pending_goto(p):
    'create_pending_goto :'
    generator.generate_pending_goto()

# Cycle common grammar
def p_post_cycle(p):
    'post_cycle : COLON optional_eol block END'

def p_BOOL_CONSTANT(p):
    '''BOOL_CONSTANT : TRUE
                    | FALSE'''

def p_empty(p):
    'empty :'
    pass

'''def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'''

# Error rule for syntax errors
def p_error(p):
    print("Syntax error at '%s'" % repr(p)) #p.value)
    # While there are syntax errors, turn off the semantics reporting
    
def get_type(symbol):
  if symbol == 'TRUE' or symbol == 'FALSE':
    return 'bool'
  res = str(type(symbol))[7:10]
  if res == 'int':
    return 'int'
  elif res == 'flo':
    return 'double'
  elif res == 'str':
    return 'string'

# Build the parser
parser = yacc.yacc()

welcome = '''Project Cobra '''
if __name__ == '__main__':
    print(welcome)
    if (len(sys.argv) > 1):
    # Obtiene el archivo
        if (sys.argv[1] == 'test'):
            t = TestC()
            t.init(parser)
            t.setUp()
            t.run()
        else:
            file = sys.argv[1]
            try:
                f = open(file,'r')
                data = f.read()
                f.close()
                #Se aplica la gramatica
                parser.parse(data, tracking=True)
                print('ok')
            except EOFError:
                print(EOFError)
    else:
        print(welcome)
        while True:
            try:
                s = raw_input('>>> ')
                print(s)
            except EOFError:
                break
            if not s:
                continue
            if s == 'exit()':
                break
            yacc.parse(s)
