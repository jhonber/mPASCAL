#!/usr/bin/python
# -*- coding: UTF-8 -*-
#------------------------------------------------------------
# lex.py
#
# tokenizer
# ------------------------------------------------------------
import sys
import re
import ply.lex as lex

reserved = (
# Reserverd words
'ELSE','IF','INT','FLOAT','RETURN','WHILE','FUN','BEGIN','DONE','DO','THEN',
'END','MAIN','PRINT','READ','WRITE','SKIP','BREAK','AND','OR','NOT',
)

reserved_map = { }
for r in reserved:
	reserved_map[r] = r

# List of token names.   
tokens = reserved + (
# Symbols
'PLUS','MINUS','DIVIDE','MULT','LESS','LESSEQUAL','GREATER','GREATEREQUAL',
'DEQUAL','DISTINT','SEMICOLON','COMMA','LPAREN','RPAREN','COLON','LBRACKET',
'RBRACKET','COLONEQUAL','QUOTE','ASLASHASTERISCO','CSLASHASTERISCO','SLASHCOMILLA',
'SLASHN','SLASHSLASH',

# Others   
'ID', 
'INUMBER',
'FNUMBER',
'CHARACTER',
'TEXT',
)

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_DIVIDE = r'/'
t_MULT = r'\*'
t_LESSEQUAL = r'<='
t_GREATEREQUAL  = r'>='
t_DEQUAL = r'=='
t_DISTINT = r'!='
t_COLONEQUAL = r':='
t_GREATER = r'>'
t_LESS = r'<'
t_SEMICOLON = r';'
t_COMMA = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COLON = r':'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_QUOTE = r'\"'
#t_ASLASHASTERISCO = r'\/*'
#t_CSLASHASTERISCO = r'\*/'
t_SLASHCOMILLA = r'\\"'
#t_SLASHN = r''
t_SLASHSLASH = r'\//'

def t_ID(t):
    r'[A-Za-z_][\w]*'
    t.type = reserved_map.get(t.value.upper(),'ID')    # Check for reserved words
    return t

def t_INUMBER(t):
    r'0(?!\d)|([1-9]\d*)'
    try:
        t.value = int(t.value)    
    except ValueError:
        print "Linea %d: Numero %s es muy grande!" % (t.lineno,t.value)
        t.value = 0
    return t

def t_FNUMBER(t):
    r'((0(?!\d))|([1-9]\d*))((\.\d+(e[+-]?\d+)?)|(e[+-]?\d+))'
    return t

def t_malformed_inumber(t):
    r'0\d+'
    print "Linea %d. Entero mal formado '%s'" % (t.lineno, t.value)

def t_malformed_fnumber(t):
    r'(0\d+)((\.\d+(e[+-]?\d+)?)|(e[+-]?\d+))'
    print "Linea %d. Malformado numero float '%s'" % (t.lineno, t.value)

def t_TEXT(t):
    r'"[^\n]*?(?<!\\)"'
    temp_str = t.value.replace(r'\\', '')
    m = re.search(r'\\[^n"]', temp_str)
    if m != None:
        print "Linea %d. Caracter de escape no soportado %s en string." % (t.lineno, m.group(0))
    return t

def t_CHARACTER(t):
    r"'\w'"
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


