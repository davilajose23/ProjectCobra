# Yacc
import ply.yacc as yacc
from scanner import tokens

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

def p_program(p):
    'program : variable function statement'
    
def p_empty(p):
    'empty :'
    pass

def p_pre_call_function(p):
    'pre_call_function : ID LEFT_PARENTHESIS'
    
def p_call_function(p):
    'call_function :  pre_call_function post_call_function'

def p_post_call_function(p):
    ''' post_call_function : parameters RIGHT_PARENTHESIS 
                            | RIGHT_PARENTHESIS'''

def p_pre_def_function(p):
    'pre_def_function : FUNC ID LEFT_PARENTHESIS'

def p_function(p):
    'function : pre_def_function post_def_function'

def p_post_def_function(p):
    '''post_def_function : parameters RIGHT_PARENTHESIS statement END
                          | RIGHT_PARENTHESIS statement END'''

def p_parameters(p):
    'parameters : identifier post_parameters'

def p_post_parameters(p):
    '''post_parameters : COMMA parameters
                        | empty'''

def p_variable(p):
    ''' variable : assignment post_variable
                  | list post_variable'''

def p_post_variable(p):
    ''' post_variable : variable
                        | empty'''

def p_statement(p):
    ''' statement : assignment
                    | condition
                    | print
                    | read
                    | loop
                    | call_function'''
def p_assignment(p):
    'assignment : identifier assignment_operator cond EOL' 

def p_assignment_operator(p):
    '''assignment_operator : EQUALS
                            | TIMES_EQUALS
                            | DIVIDE_EQUALS
                            | PLUS_EQUALS
                            | MINUS_EQUALS '''

def p_cond(p):
    'cond : expression post_cond' 

def p_post_cond(p):
    '''post_cond : AND cond
                | OR  cond
                | empty'''

def p_expression(p):
    'expression : exp post_expression'

def p_post_expression(p):
    '''post_expression : relational_operator exp
                        | empty'''

def p_relational_operator(p):
    '''relational_operator : LESS
                        	| GREATER
                        	| GREATER_EQUALS
                        	| LESS_EQUALS
                        	| EQUALS_EQUALS
                        	| NOT_EQUALS'''

def p_exp(p):
    'exp : term post_exp'

def p_post_exp(p):
    ''' post_exp : PLUS exp
                | MINUS exp
                | empty'''

def p_term(p):
    'term : factor post_term'

def p_post_term(p):
    ''' post_term : TIMES term
                | DIVIDE term
                | PERCENTAGE term
                | MOD term
                | empty'''

def p_factor(p):
    '''factor : LEFT_PARENTHESIS cond RIGHT_PARENTHESIS
                | variable_constant
                | MINUS variable_constant
                | call_function'''

def p_variable_constant(p):
    '''variable_constant : identifier
                        | INT_CONSTANT
                        | DOUBLE_CONSTANT
                        | STRING_CONSTANT
                        | BOOL_CONSTANT '''

# if conditional
def p_condition(p):
    'condition : IF cond COLON post_condition '

def p_post_condition(p):
    'post_condition : statement post_post_condition'

def p_post_post_condition(p):
    '''post_post_condition : post_condition
                        | END
                        | else'''

# else
def p_else(p):
    'else : ELSE COLON post_else'

def p_post_else(p):
    'post_else : statement post_post_else'

def p_post_post_else(p):
    ''' post_post_else : post_else
                        | END'''

def p_print(p):
    'print : PRINT cond post_print'

def p_post_print(p):
    '''post_print :  COMMA STRING_CONSTANT EOL
                    | empty'''

def p_read(p):
    'read : READ LEFT_PARENTHESIS RIGHT_PARENTHESIS EOL'

def p_list(p):
    'list : identifier post_list'

def p_post_list(p):
    '''post_list : EQUALS LEFT_BRACKET exp RIGHT_BRACKET EOL
                  | EOL'''

def p_identifier(p):
    'identifier : ID post_identifier'

def p_post_identifier(p):
    '''post_identifier : LEFT_BRACKET exp RIGHT_BRACKET
                        | empty'''

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
    'post_cycle : COLON statement post_post_cycle'

def p_post_post_cycle(p):
    '''post_post_cycle : statement post_post_cycle
                        | END'''

def p_BOOL_CONSTANT(p):
	'''BOOL_CONSTANT : TRUE
					| FALSE'''

'''def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'''

# Error rule for syntax errors
def p_error(p):
    #print("Syntax error in input!")
    print("Syntax error at '%s'" % repr(p)) #p.value)


# Build the parser
parser = yacc.yacc()

# Test it out
data = '''a = 1
func hola() a = 2 end
print a
'''

result = parser.parse(data)
print(result)