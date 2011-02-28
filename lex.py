#!/usr/bin/python
# -*- coding: UTF-8 -*-
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
'TEXT',
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
#t_LESSEQUAL = r'<='
t_GREATER = r'>'
#t_GREATEREQUAL  = r'>='
#t_DEQUAL = r'=='
#t_DISTINT = r'!='
t_SEMICOLON = r';'
t_COMMA = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COLON = r':'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
#t_COLONEQUAL = r':='
t_QUOTE = r'\"'
#t_ASLASHASTERISCO = r'\/*'
#t_CSLASHASTERISCO = r'\*/'
#t_SLASHCOMILLA = r'\\"'
#t_SLASHN = r''
#t_SLASHSLASH = r'\//'


def t_LESSEQUAL(t):
	r'<='
	return t

def t_GREATEREQUAL(t):
	r'>='
	return t

def t_DEQUAL(t):
	r'=='
	return t

def t_DISTINT(t):
	r'!='
	return t

def t_COLONEQUAL(t):
	r':='
	return t

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)    
    except ValueError:
        print "Line %d: Number %s is too large!" % (t.lineno,t.value)
        t.value = 0
    return t

def t_ELSE(t):
    r'else'
    return t

def t_IF(t):
    r'if'
    return t

def t_INT(t):
    r'int'
    return t

def t_FLOAT(t):
    r'float'
    return t

def t_RETURN(t):
    r'return'
    return t

def t_WHILE(t):
    r'while'
    return t


def t_FUN(t):
    r'fun'
    return t

def t_BEGIN(t):
    r'begin'
    return t

def t_DONE(t):
    r'done'
    return t

def t_DO(t):
    r'do'
    return t

def t_THEN(t):
    r'then'
    return t

def t_END(t):
    r'end'
    return t

def t_MAIN(t):
    r'main'
    return t

def t_PRINT(t):
    r'print'
    return t

def t_READ(t):
    r'read'
    return t

def t_WRITE(t):
    r'write'
    return t

def t_SKIP(t):
    r'skip'
    return t

def t_BREAK(t):
    r'break'
    return t

def t_AND(t):
    r'and'
    return t

def t_OR(t):
    r'or'
    return t

def t_NOT(t):
    r'not'
    return t

def t_ID(t):
#    r'\w+(_\d\w)*'
    r'[a-zA-Z_+=\*\-][a-zA-Z0-9_+\*\-]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t
    
def t_TEXT(t):
    r'\"[a-zA-ZáéíóúñÁ0-9_+\*\- :,]*\"'
    t.type = reserved.get(t.value,'TEXT')    # Check for reserved words
    return t

# Para contar el numero de lineas 
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignored tokens
t_ignore = ' \t'

def t_comments(t):
	r'/*(.|\n)*?\*/'
	t.lexer.lineno += t.value.count('\n')

# Una regla para manejar errores.
def t_error(t):
    print "Caracter ilegal: '%s'" % t.value[0]
    t.lexer.skip(1)

# Main Lexer functionality
def run_lexer():
    """This is just a debugging function that prints out a list of
    tokens, it's not actually called by the compiler or anything."""

    
    import sys
    file = open(sys.argv[1])
    lines = file.readlines()
    file.close()
    strings='''
    '''
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

