import ply.yacc as yacc
from scanner import tokens
from TestCobra import TestC
import sys
from symbol_table import functions_dir
from stack import Stack
from cube import semantic_cube
from quad_generator import *

functions_directory = functions_dir()
# Precedence rules for the arithmetic operators
precedence = (
    ('nonassoc', 'AND', 'OR'),  # Nonassociative operators
    ('nonassoc', 'LESS', 'GREATER', 'EQUALS_EQUALS', 'GREATER_EQUALS', 'LESS_EQUALS', 'NOT_EQUALS'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE', 'MOD', 'PERCENTAGE'),
    # ('right','UMINUS'),
)

generator = QuadGenerator('output.txt')

# ********************* Diagram program *********************
def p_program(p):
    '''program : pre_variables functions main
                | functions main
                | pre_variables main
                | main'''
    p[0] = 'ok'

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

# ********************* Diagram delcaration *********************
def p_declaration(p):
    'declaration : types set_type inter_declaration required_eol'

def p_set_type(p):
    'set_type :'
    functions_directory.set_type(p[-1])

def p_inter_declaration(p):
    'inter_declaration: identifier cycle_declaration'

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
    'main : MAIN required_eol pre_variables block END_MAIN optional_eol'
    
# ********************* Diagram block *********************
def p_block(p):
    'block : statement post_block'
    
def p_post_block(p):
    '''post_block : block
                    | empty'''

# ********************* Diagram call_function *********************
def p_call_function(p):
    'call_function :  ID validate_function_call LEFT_PARENTHESIS post_call_function'

# Validates call to a function
def p_validate_function_call(p):
    'validate_function_call :'
    functions_directory.validate_function(p[-1])

def p_post_call_function(p):
    ''' post_call_function : arguments RIGHT_PARENTHESIS
                            | RIGHT_PARENTHESIS'''
                            
# ********************* Diagram arguments *********************
def p_arguments(p):
    'arguments : cond post_arguments'

def p_post_arguments(p):
    '''post_arguments : COMMA arguments 
                            | empty'''

# ********************* Diagram function *********************
def p_function(p):
    'function : FUNC func_types ID register_function LEFT_PARENTHESIS post_function'

def p_func_types(p):
    '''func_types : INT
            | DOUBLE
            | STRING
            | BOOL
            | VOID'''

def p_register_function(p):
    'register_function :'
    functions_directory.add_function(p[-1])
    functions_directory.set_return_type(p[-2])
    functions_directory.set_scope(p[-1])

def p_post_function(p):
    '''post_function : parameters RIGHT_PARENTHESIS required_eol post_variables func_return
                          | RIGHT_PARENTHESIS required_eol post_variables func_return'''

def p_func_return(p):
    '''func_return : void_return 
                    | value_return'''
                   
def p_void_return(p):
    'void_return : block post_void_return'

def p_post_void_return(p):
    '''post_void_return : END reset_scope required_eol 
                        | RETURN required_eol END reset_scope required_eol'''

def p_value_return(p):
    '''value_return : block RETURN cond required_eol END reset_scope required_eol
                    | RETURN cond required_eol END reset_scope required_eol'''

def p_reset_scope(p):
    'reset_scope :'
    functions_directory.reset_scope()

# ********* DEPRECATED (now all functions have a type and it is registered after get the ID of the function)
#
# # Adds to functions directory de return type of the function
# # Resets the scope of functions directory after
# def p_set_void_return(p):
#     'set_void_return :'
#     functions_directory.set_return_type('void')
#     functions_directory.reset_scope()

# def p_set_value_return(p):
#     'set_value_return :'
#     functions_directory.set_return_type('value')
#     functions_directory.reset_scope()
                    
# ********************* Diagram parameters *********************
def p_parameters(p):
    'parameters : types set_type identifier update_function_parameters post_parameters'

# Increases the quantity of expected arguments by a function
def p_update_function_parameters(p):
    'update_function_parameters :'
    functions_directory.increase_expected_arguments()
    # Registers the expected argument in the function variables directory
    functions_directory.add_var(variable_id=p[-1], var_type=functions_directory.last_type)

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
    'assignment : start_evaluating identifier assignment_operator cond finish_evaluating'

# ********************* Diagram assignment_operator *********************
def p_assignment_operator(p):
    '''assignment_operator : EQUALS
                            | TIMES_EQUALS
                            | DIVIDE_EQUALS
                            | PLUS_EQUALS
                            | MINUS_EQUALS'''

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
    if generator.popper.top() == 'and' or generator.popper.top() == 'or':
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
    if generator.popper.top() in relops:
        generator.generate_quad()

def p_post_expression(p):
    '''post_expression : relational_operator push_relop exp
                        | empty'''

def p_push_relop(p):
    'push_relop :'
    generator.popper.push(p[-1])

# ********************* Diagram relational_operator *********************
def p_relational_operator(p):
    '''relational_operator : LESS
                            | GREATER
                            | GREATER_EQUALS
                            | LESS_EQUALS
                            | EQUALS_EQUALS
                            | NOT_EQUALS'''

# ********************* Diagram exp *********************
def p_exp(p):
    'exp : term pop_exp post_exp'

def p_pop_exp(p):
    'pop_exp :'
    if generator.popper.top() == '+' or generator.popper.top() == '-':
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
    if generator.popper.top() in operators:
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
    '''variable_constant : identifier
                        | INT_CONSTANT
                        | DOUBLE_CONSTANT
                        | STRING_CONSTANT
                        | BOOL_CONSTANT '''

def p_process_variable(p):
    'process_variable :'
    # Checks if the variable to validate is in array notation
    if functions_directory.evaluating:
        functions_directory.validate_variable(p[-1])
    else:
        functions_directory.add_var(variable_id=p[-1], var_type=functions_directory.last_type)

# ********************* Diagram condition *********************
def p_condition(p):
    'condition : IF cond COLON optional_eol block post_condition END'


def p_post_condition(p):
    '''post_condition : else
                        | empty'''

# else
def p_else(p):
    'else : ELSE COLON optional_eol block'

# ********************* Diagram print *********************
def p_print(p):
    'print : PRINT start_evaluating cond post_print finish_evaluating'

def p_post_print(p):
    '''post_print :  COMMA STRING_CONSTANT 
                    | empty'''

# ********************* Diagram read *********************
def p_read(p):
    'read : READ LEFT_PARENTHESIS RIGHT_PARENTHESIS '

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
    'for : FOR identifier FROM exp TO exp post_cycle'

# while
def p_while(p):
    'while : WHILE start_evaluating cond  finish_evaluating post_cycle'

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
    


# Build the parser
parser = yacc.yacc()

welcome = '''Project Cobra '''
if __name__ == '__main__':
    print(welcome)
    if (len(sys.argv) > 1):
    # Obtiene el archivo
        if (sys.argv[1] == 'test'):
            t = TestC()
            t.set_up(parser)
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
                print s
            except EOFError:
                break
            if not s:
                continue
            if s == 'exit()':
                break
            yacc.parse(s)