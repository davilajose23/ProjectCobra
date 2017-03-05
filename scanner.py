# ------------------------------------------------------------
#
# tokenizer for Project Cobra Language
# ------------------------------------------------------------
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
	'not': 'NOT',
	'for': 'FOR',
	'return': 'RETURN',
	'start': 'START',
	'true': 'TRUE',
	'false': 'FALSE',
	'bool': 'BOOL',
	'int': 'INT',
	'double': 'DOUBLE'
	'string': 'STRING',
	'void': 'VOID',
	'break': 'BREAK',
	'from': 'FROM',
	'to': 'TO',
	'mod': 'MOD',
	'use': 'USE',
	'lang': 'LANG',
	'es': 'SPANISH',
	'en': 'ENGLISH'
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
   'LPARENTHESIS',
   'RPARENTHESIS',
   'LBRACKET',
   'RBRACKET',
   'COMMENT',
   'EOL',
   'SPACE',
   'COMMA',
   'COLON'
] + list(reserved.values())


# Build the parser
parser = yacc.yacc()

while True:
   try:
       s = raw_input('> ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)