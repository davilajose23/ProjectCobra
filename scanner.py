"""This module is a Simple Scanner using ply
-----------------------------------------------------------------
Compilers Design Project
Tec de Monterrey
Julio Cesar Aguilar Villanueva  A01152537
Jose Fernando Davila Orta       A00999281
-----------------------------------------------------------------

DOCUMENTATION: For complete Documentation see UserManual.pdf"""

import ply.lex as lex
# List of reserved words in the leanguage

reserved = {
    'if': 'IF',
    'end': 'END',
    'while': 'WHILE',
    'print': 'PRINT',
    'read': 'READ',
    'else': 'ELSE',
    'and': 'AND',
    'or': 'OR',
    'for': 'FOR',
    'return': 'RETURN',
    'true': 'TRUE',
    'false': 'FALSE',
    'bool': 'BOOL',
    'int': 'INT',
    'double': 'DOUBLE',
    'string': 'STRING',
    'from': 'FROM',
    'to': 'TO',
    'mod': 'MOD',
    'func': 'FUNC',
    'main': 'MAIN',
    'endmain': 'END_MAIN',
    'void': 'VOID'
}

# List of token names.   This is always required
tokens = [
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LESS',
    'GREATER',
    'EQUALS',
    'EQUALS_EQUALS',
    'GREATER_EQUALS',
    'LESS_EQUALS',
    'NOT_EQUALS',
    'PLUS_EQUALS',
    'MINUS_EQUALS',
    'TIMES_EQUALS',
    'DIVIDE_EQUALS',
    'PERCENTAGE',
    'LEFT_PARENTHESIS',
    'RIGHT_PARENTHESIS',
    'LEFT_BRACKET',
    'RIGHT_BRACKET',
    'COMMA',
    'COLON',
    'ID',
    'EOL',
    'INT_CONSTANT',
    'DOUBLE_CONSTANT',
    'STRING_CONSTANT'
] + list(reserved.values())

#Regular expression rules for simple tokens
t_PLUS                  = r'\+'
t_MINUS                 = r'\-'
t_TIMES                 = r'\*'
t_DIVIDE                = r'/'
t_LESS                  = r'<'
t_GREATER               = r'>'
t_EQUALS_EQUALS         = r'=='
t_EQUALS                = r'='
t_GREATER_EQUALS         = r'>='
t_LESS_EQUALS           = r'<='
t_COMMA                 = r'\,'
t_COLON                 = r':'
t_NOT_EQUALS            = r'!='
t_PLUS_EQUALS           = r'\+='
t_MINUS_EQUALS          = r'\-='
t_TIMES_EQUALS          = r'\*='
t_DIVIDE_EQUALS         = r'/='
t_PERCENTAGE            = r'%'
t_LEFT_PARENTHESIS      = r'\('
t_RIGHT_PARENTHESIS     = r'\)'
t_LEFT_BRACKET          = r'\['
t_RIGHT_BRACKET         = r'\]'


def t_ID(t):
    r'[a-zA-Z](_?[a-zA-Z0-9]+)*'
    t.type = reserved.get(t.value, 'ID') # Check for reserved words
    return t

# Define a rule so we can track line numbers
def t_EOL(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

def t_COMMENT(t):
    r'\#.*'
    pass

def t_DOUBLE_CONSTANT(t):
    r'([-]?[0-9]+[.])[0-9]+'
    t.value = float(t.value)
    return t

def t_INT_CONSTANT(t):
    r'[-]?[0-9]+'
    t.value = int(t.value)
    return t

def t_STRING_CONSTANT(t):
    r'((\')[^\n\t\'\"]*(\')|(\")[^\n\t\'\"]*(\"))'
    t.value = str(t.value)
    return t

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
