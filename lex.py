# -*- coding: utf-8 -*-
#------------------------------------------------------------
# lex.py
#
# tokenizer
# ------------------------------------------------------------

import ply.lex as lex
import re

# List of token names.   
tokens = (
# Reserverd words
'ELSE',
'IF',
'INT',
'FLOAT',
'RETURN',
'WHILE',
'FUN',
'BEGIN',
'DONE',
'DO',
'THEN',
'END',
'MAIN',
'PRINT',
'READ',
'WRITE',
'SKIP',
'BREAK',
'AND',
'OR',
'NOT',
# Symbols

'PLUS',
'MINUS',
'DIVIDE',
'MULT',
'LESS',
'LESSEQUAL',
'GREATER',
'GREATEREQUAL',
'DEQUAL',
'DISTINT',
'SEMICOLON',
'COMMA',
'LPAREN',
'RPAREN',
'COLON',
'LBRACKET',
'RBRACKET',
'COLONEQUAL',
'QUOTE',
'ASLASHASTERISCO',
'CSLASHASTERISCO',
'SLASHCOMILLA',
'SLASHN',
'SLASHSLASH',

# Others   
'ID', 
'NUMBER',
)

reserved = {
    'break' : 'BREAK',
    'do' : 'DO',
    'else' : 'ELSE',
    'float' : 'FLOAT',
    'if' : 'IF',
    'int' : 'INT',
    'return' : 'RETURN',
    'while' : 'WHILE',
    'not' : 'NOT',
    'fun' : 'FUN',
    'begin' : 'BEGIN',
    'done' : 'DONE',
    'then' : 'THEN',
    'end' : 'END',
    'main' : 'MAIN',
    'print' : 'PRINT',
    'read' : 'READ',
    'write' : 'WRITE',
    'skip' : 'SKIP',
    'and' : 'AND',
    'or' : 'OR',
}

# Regular expression rules for simple tokens
#t_ID = r'[a-zA-Z_][\w_]*'
t_PLUS = r'\+'
t_MINUS = r'-'
t_DIVIDE = r'/'
t_MULT = r'\*'
t_LESS = r'<'
t_LESSEQUAL = r'<='
t_GREATER = r'>'
t_GREATEREQUAL  = r'>='
t_DEQUAL = r'=='
t_DISTINT = r'!='
t_SEMICOLON = r';'
t_COMMA = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COLON = r':'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COLONEQUAL = r':='
t_QUOTE = r'\"'
#t_ASLASHASTERISCO = r'\/*'
#t_CSLASHASTERISCO = r'\*/'
t_SLASHCOMILLA = r'\\"'
#t_SLASHN = r''
t_SLASHSLASH = r'\//'


def t_NUM(t):
    r'\d+'
    try:
        t.value = int(t.value)    
    except ValueError:
        print "Line %d: Number %s is too large!" % (t.lineno,t.value)
        t.value = 0
    return t



# Para contar el numero de lineas 
def t_newline(t):
    r'\n+'
    t.lineno += len(t.value)

# Ignored tokens
def t_whitespace(t):
    r'[ \t]+'
    pass

def t_comment(t):
    r'/\*[\w\W]*?\*/'
    t.lineno += t.value.count('\n')
    pass

# Una regla para manejar errores.
def t_error(t):
    print "Carácter ilegal: '%s'" % t.value[0]
    t.skip(1)

# Main Lexer functionality
def run_lexer():
    """This is just a debugging function that prints out a list of
    tokens, it's not actually called by the compiler or anything."""
    
    import sys
    file = open(sys.argv[1])
    lines = file.readlines()
    file.close()
    strings = ""
    for i in lines:
        strings += i
    lex.input(strings)
    while 1:
        token = lex.token()       # Get a token
        if not token: break        # No more tokens
        print "(%s,'%s',%d)" % (token.type, token.value, token.lineno)

lex.lex()

if __name__ == '__main__':
    run_lexer()

