# ------------------------------------------------------------
# duck.py
#
# tokenizer for Project Cobra Language
# ------------------------------------------------------------

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