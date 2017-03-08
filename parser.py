import ply.yacc as yacc
from scanner import tokens
import sys
# Precedence rules for the arithmetic operators
precedence = (
    ('nonassoc', 'AND', 'OR'),  # Nonassociative operators
    ('nonassoc', 'LESS', 'GREATER', 'EQUALS_EQUALS', 'GREATER_EQUALS', 'LESS_EQUALS', 'NOT_EQUALS'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE', 'MOD', 'PERCENTAGE'),
    # ('right','UMINUS'),
)

# dictionary of names (for storing variables)
names = { }

# ********************* Diagram program *********************
def p_program(p):
    '''program : variable functions main
                | functions main
                | variable main
                | main'''
# ********************* Diagram functions *********************
def p_functions(p):
    'functions : function post_functions'
    
    
def p_post_functions(p):
    '''post_functions : functions
                    | empty'''
    
# ********************* Diagram main *********************
def p_main(p):
    'main : MAIN block END_MAIN'
    
# ********************* Diagram block *********************
def p_block(p):
    'block : statement post_block'
    
def p_post_block(p):
    '''post_block : block
                    | empty'''

# ********************* Diagram call_function *********************
def p_call_function(p):
    'call_function :  ID LEFT_PARENTHESIS post_call_function'

def p_post_call_function(p):
    ''' post_call_function : call_parameters RIGHT_PARENTHESIS 
                            | RIGHT_PARENTHESIS'''
                            
# ********************* Diagram call_parameters *********************
def p_call_parameters(p):
    'call_parameters : cond post_call_parameters'

def p_post_call_parameters(p):
    '''post_call_parameters : COMMA call_parameters 
                            | empty'''

# ********************* Diagram function *********************
def p_function(p):
    'function : FUNC ID LEFT_PARENTHESIS post_function'

def p_post_function(p):
    '''post_function : parameters RIGHT_PARENTHESIS func_return
                          | RIGHT_PARENTHESIS func_return'''

def p_func_return(p):
    '''func_return : void_return 
                    | value_return'''
                   
def p_void_return(p):
    'void_return : block END'

def p_value_return(p):
    'value_return : block RETURN cond END'
# ********************* Diagram parameters *********************

def p_parameters(p):
    'parameters : identifier post_parameters'

def p_post_parameters(p):
    '''post_parameters : COMMA parameters
                        | empty'''

# ********************* Diagram variable *********************
def p_variable(p):
    ''' variable : assignment post_variable
                  | list post_variable'''

def p_post_variable(p):
    ''' post_variable : variable
                        | empty'''

# ********************* Diagram statement *********************
def p_statement(p):
    ''' statement : variable
                    | condition
                    | print
                    | read
                    | loop
                    | call_function'''
                    
                    
# ********************* Diagram assignment *********************

def p_assignment(p):
    'assignment : identifier assignment_operator cond ' 

# ********************* Diagram assignment_operator *********************
def p_assignment_operator(p):
    '''assignment_operator : EQUALS
                            | TIMES_EQUALS
                            | DIVIDE_EQUALS
                            | PLUS_EQUALS
                            | MINUS_EQUALS '''

# ********************* Diagram cond *********************
def p_cond(p):
    'cond : expression post_cond' 

def p_post_cond(p):
    '''post_cond : AND cond
                | OR  cond
                | empty'''

# ********************* Diagram expression *********************
def p_expression(p):
    'expression : exp post_expression'

def p_post_expression(p):
    '''post_expression : relational_operator exp
                        | empty'''

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
    'exp : term post_exp'

def p_post_exp(p):
    ''' post_exp : PLUS exp
                | MINUS exp
                | empty'''

# ********************* Diagram term *********************
def p_term(p):
    'term : factor post_term'

def p_post_term(p):
    ''' post_term : TIMES term
                | DIVIDE term
                | PERCENTAGE term
                | MOD term
                | empty'''

# ********************* Diagram factor *********************
def p_factor(p):
    '''factor : LEFT_PARENTHESIS cond RIGHT_PARENTHESIS
                | variable_constant
                | MINUS variable_constant
                | call_function'''

# ********************* Diagram variable_constant *********************
def p_variable_constant(p):
    '''variable_constant : identifier
                        | INT_CONSTANT
                        | DOUBLE_CONSTANT
                        | STRING_CONSTANT
                        | BOOL_CONSTANT '''

# ********************* Diagram condition *********************
def p_condition(p):
    'condition : IF cond COLON block post_condition END'


def p_post_condition(p):
    '''post_condition : else
                        | empty'''

# else
def p_else(p):
    'else : ELSE COLON block'

# ********************* Diagram print *********************
def p_print(p):
    'print : PRINT cond post_print'

def p_post_print(p):
    '''post_print :  COMMA STRING_CONSTANT 
                    | empty'''

# ********************* Diagram read *********************
def p_read(p):
    'read : READ LEFT_PARENTHESIS RIGHT_PARENTHESIS '

# ********************* Diagram list *********************
def p_list(p):
    'list : identifier post_list'

def p_post_list(p):
    '''post_list : EQUALS LEFT_BRACKET exp RIGHT_BRACKET 
                  | empty'''

# ********************* Diagram identifier *********************
def p_identifier(p):
    'identifier : ID post_identifier'

def p_post_identifier(p):
    '''post_identifier : LEFT_BRACKET exp RIGHT_BRACKET
                        | empty'''

# ********************* Diagram loop *********************
def p_loop(p):
    '''loop : for
            | while'''

# for
def p_for(p):
    'for : FOR identifier post_for'

def p_post_for(p):
    '''post_for : IN identifier post_cycle
                | FROM exp TO exp post_cycle'''

# while
def p_while(p):
    'while : WHILE cond post_cycle'

# Cycle common grammar
def p_post_cycle(p):
    'post_cycle : COLON block END'

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
    #print("Syntax error in input!")
    print("Syntax error at '%s'" % repr(p)) #p.value)


# Build the parser
parser = yacc.yacc()

if __name__ == '__main__':
  if (len(sys.argv) > 1):
    # Obtiene el archivo
    file = sys.argv[1]
    try:
        f = open(file,'r')
        data = f.read()
        f.close()
        #Se realiza la gramatica
        parser.parse(data, tracking=True)
        #print ('Trabajando correctamente - APROPIADO');
    except EOFError:
        print(EOFError)
  else:
    print('The file does not exist')