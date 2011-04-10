#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#------------------------------------------------------------
# yacc.py
#
# parser
# ------------------------------------------------------------

import sys

import ply.yacc as yacc

from mpaslex import tokens

#Defino la clase NODE
class Node:
	def __init__(self, name, children = None, leaf = None):
		self.name = name
		if children == None:
			children = []
		self.children = children
		self.leaf = leaf
	
	def append (self, Node):
		self.children.append(Node)

	def __str__(self):
		return "<%s>" % self.name

	def __repr__(self):
		return "<%s>" % self.name


#
# Funcion para mostrar el AST
#
def dump_tree(node, ident = ""):
	if not hasattr(node, "datatype"):
		datatype = ""
	else:
		datatype = node.datatype

	if not node.leaf:
		print "%s%s  %s" % (ident, node.name, datatype)
	else:
		print "%s%s (%s)  %s" % (ident, node.name, node.leaf, datatype)

	ident = ident.replace("-", " ")
	ident = ident.replace("+", " ")

	for i in range(len(node.children)):
		c = node.children[i]
		if i == len(node.children) - 1:
			dump_tree(c, ident + "  +-- ")
		else:
			dump_tree(c, ident + "  |-- ")


#Defino las precedencias
precedence =(
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIVIDE'),
	('right', 'UMINUS','NOT','ELSE'),
    )

def p_program(p):
	'''program : list_functions main'''
	#p[1].append(p[2])
	p[0] = Node('program',[p[1],p[2]])

def p_program_2(p):
	'''program : '''

def p_list_functions_1(p):
	'''list_functions : list_functions func'''
	p[1].append(p[2])
	p[0] = p[1]

def p_list_functions_2(p):
	'''list_functions : empty'''
	p[0] = Node('list_functions',[])

def p_func(p):
	'''func : FUN ID LPAREN arguments RPAREN locals BEGIN staments END'''
	a = Node('f_name',[],[p[2]])
	#b = Node('staments',[p[8]])
	p[0] = Node('func',[a,p[4],p[6],p[8]])

def p_main(p):
	"main : FUN MAIN LPAREN arguments RPAREN locals BEGIN staments END"
	a = Node('f_name',[],[p[2]])
	b = Node('staments',[p[8]])
	c = Node('locals',[p[6]])
	p[0] = Node('main',[a,p[4],c,b])

def p_arguments_1(p):
	''' arguments : declaration_variables'''
	p[0] = p[1]

def p_argument_2(p):
	'''arguments : empty'''
	p[0] = Node('arguments - []',[])

def p_locals_1(p):
	'''locals : declaration_locals'''
	#p[1].append(p[2])
	p[0] = p[1]
	#p[0] = Node('locals',[p[1]])

def p_locals_2(p):
	'''locals : declaration_functions'''
	#p[1].append(p[2])
	p[0] = p[1]

def p_locals_3(p):
	'''locals : empty'''
	p[0] = Node('locals - []',[])

def p_declaration_variables_1(p):
	'''declaration_variables : ID COLON tipo'''
	a = Node('type',[],[p[3]])
	b = Node('name',[],[p[1]])
	c = Node('d_var',[a,b])
	p[0] = Node('arguments',[c])

def p_declaration_variables_2(p):
	'''declaration_variables : ID COLON tipo LBRACKET INUMBER RBRACKET'''
	a = Node('type',[],[p[3]])
	b = Node('name',[],[p[1]])
	c = Node('sub-i',[],[p[5]])
	d = Node('d_vec',[a,b,c])
	p[0] = Node('arguments',[d])

def p_declaration_variables_3(p):
	'''declaration_variables : arguments COMMA ID COLON tipo'''
	a = Node('type',[],[p[5]])
	b = Node('name',[],[p[3]])
	p[1].append(Node('d_var',[a,b]))
	p[0] = p[1]

def p_declaration_variables_4(p):
	'''declaration_variables : arguments COMMA ID COLON tipo LBRACKET INUMBER RBRACKET'''
	a = Node('type',[],[p[5]])
	b = Node('name',[],[p[3]])
	c = Node('sub-i',[],[p[7]])
	p[1].append(Node('d_vec',[a,b,c]))
	p[0] = p[1]

def p_tipo(p):
	'''tipo : INT
     		| FLOAT'''
	p[0] = p[1]

def p_declaration_functions(p):
	'''declaration_functions : FUN ID LPAREN arguments RPAREN locals BEGIN staments END SEMICOLON'''
	pass

def p_declaration_locals_1(p):
	'''declaration_locals : locals ID COLON tipo SEMICOLON'''
	a = Node('type',[],[p[4]])
	b = Node('name',[],[p[2]])
	c = Node('d_var',[a,b])
	p[1].append(c)
	p[0] = p[1]
	#p[0] = Node('locals*',[p[1],c])

def p_declaration_locals_2(p):
	'''declaration_locals : locals ID COLON tipo LBRACKET INUMBER RBRACKET SEMICOLON'''
	a = Node('type',[],[p[2]])
	b = Node('name',[],[p[4]])
	c = Node('sub-i',[],[p[6]])
	p[1].append(Node('d_vec',[a,b,c]))
	p[0] = p[1]

def p_staments(p):
	'''staments : stament'''
	p[0] = p[1]

def p_staments_2(p):
	'''staments : staments SEMICOLON stament'''

def p_stament_1(p):
	'''stament : while
               | if
               | assign
               | print
               | write
               | read
               | return
               | ID LPAREN expression_list RPAREN 
			   | BEGIN staments END
               | BREAK'''
	pass

def p_stament_2(p):
	'''stament : SKIP'''
	p[0] = Node('skip',[],[p[1]])

def p_while(p):
	'''while : WHILE relation DO stament'''
	pass

def p_if(p):
	'''if : IF relation THEN stament else'''
	pass

def p_else(p):
	'''else : ELSE stament
			| empty'''
	pass	

def p_assign(p):
	'''assign : ID COLONEQUAL expression
			  | ID LBRACKET expression RBRACKET COLONEQUAL expression'''
	pass

def p_print(p):
	'''print : PRINT LPAREN TEXT RPAREN'''
	pass

def p_write(p):
	'''write : WRITE LPAREN expression RPAREN'''
	pass

def p_read(p):
	'''read : READ LPAREN location_read RPAREN'''
	pass

def p_return(p):
	'''return : RETURN expression'''
	pass

def p_location_read(p):
	''' location_read : ID
                      | ID LBRACKET expression RBRACKET'''
	pass

def p_expression(p):
	'''expression : expression PLUS expression
    	            | expression DIVIDE expression
        	        | expression MULT expression
        	        | expression MINUS expression
        	        | MINUS expression %prec UMINUS
        	        | LPAREN expression RPAREN
        	        | ID LPAREN expression_list RPAREN
        	        | ID
        	        | ID LBRACKET expression RBRACKET
        	        | INUMBER
        	        | FNUMBER'''
	pass

def p_expression_list(p):
	'''expression_list : expression
						| expression_list COMMA expression'''
	pass


def p_relation(p):
	'''relation : expression GREATER expression
                | expression LESS expression
                | expression GREATEREQUAL expression
                | expression LESSEQUAL expression
				| expression DEQUAL expression
                | expression DISTINT expression
                | expression NOT expression
                | expression OR expression
                | expression AND expression
                | NOT expression
                | LPAREN expression RPAREN
				| INUMBER'''
	pass

def p_empty(p):
	"empty :"
	pass

def p_error(p):
	print "Error cuiado { %s }" % p.value,
	print "En %i" % p.lexer.lineno


parser = yacc.yacc(debug=1)

f = open(sys.argv[1])
res = parser.parse(f.read())

if f:
	print "--AST--"
	dump_tree(res)
