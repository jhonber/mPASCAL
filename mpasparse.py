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

#
#Defino la clase NODE
#
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

#
#Defino las precedencias
#
precedence =(
	('left', 'OR'),
	('left', 'AND'),
    ('left', 'NOT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIVIDE'),
	('right', 'UMINUS','ELSE'),
    )

#
#Definicion de la gramatica y contruccion del AST
#
def p_program_1(p):
	'''program : function'''
	#p[0] = Node('program',[#p[1],p[2]])

def p_program_2(p):
	'''program : program function'''
	#p[0] = Node('program',[#p[1],p[2]])

def p_function(p):
	'''function : FUN ID arguments locals BEGIN staments END'''
	##p[1].append(p[2])
	#p[0] = #p[1]

def p_arguments_1(p):
	''' arguments : LPAREN RPAREN '''
	#p[0] = #p[1]

def p_argument_2(p):
	'''arguments : LPAREN declaration_variables RPAREN'''
	#p[0] = Node('arguments - []',[])

def p_declaration_variables_1(p):
	'''declaration_variables : param'''
	#p[0] = Node('arguments - []',[])

def p_declaration_variables_2(p):
	'''declaration_variables : declaration_variables COMMA param'''
	#p[0] = Node('arguments - []',[])

def p_param_1(p):
	'''param : ID COLON type'''
	#p[0] = #p[1]

def p_param_2(p):
	'''param : ID COLON ID'''
	#p[0] = #p[1]

def p_locals_1(p):
	'''locals : dec_list SEMICOLON'''
	#p[0] = #p[1]

def p_locals_2(p):
	'''locals : empty'''
	#p[0] = Node('locals - []',[])

def p_dec_list(p):
	'''dec_list : var_dec
				| dec_list SEMICOLON var_dec'''

def p_var_dec_1(p):
	'''var_dec : param'''
	#p[0] = Node('locals - []',[])

def p_var_dec_2(p):
	'''var_dec : function'''
	#p[0] = Node('locals - []',[])

def p_type_1(p):
	'''type : INT'''
	#p[0] = Node('locals - []',[])

def p_type_2(p):
	'''type : FLOAT'''
	#p[0] = Node('locals - []',[])

def p_type_3(p):
	'''type : INT LBRACKET expression RBRACKET'''
	#p[0] = Node('locals - []',[])

def p_type_4(p):
	'''type : FLOAT LBRACKET expression RBRACKET'''
	#p[0] = Node('locals - []',[])

def p_staments_1(p):
	'''staments : stament'''
	#p[0] = Node('staments',[#p[1]])

def p_staments_2(p):
	'''staments : staments SEMICOLON stament'''
	##p[1].append(p[3])
	#p[0] = #p[1]

def p_stament_1(p):
	'''stament : WHILE relation DO stament'''
	#p[0] = Node('beg_end',[p[2]])

def p_stament_2(p):
	'''stament : IF relation THEN stament else'''
	#p[0] = Node('skip',[],[#p[1]])

def p_stament_3(p):
	'''stament : location_read COLONEQUAL expression'''
	#p[0] = #p[1]

def p_stament_4(p):
	'''stament : PRINT LPAREN TEXT RPAREN'''
	#p[0] = #p[1]

def p_stament_5(p):
	'''stament : WRITE LPAREN expression RPAREN'''
	#p[0] = #p[1]

def p_stament_6(p):
	'''stament : READ LPAREN location_read RPAREN'''
	#p[0] = #p[1]

def p_stament_7(p):
	'''stament : RETURN expression'''
	#p[0] = #p[1]

def p_stament_8(p):
	'''stament : ID LPAREN expression_list RPAREN'''
	#p[0] = #p[1]

def p_stament_9(p):
	'''stament : SKIP'''
	#p[0] = #p[1]

def p_stament_10(p):
	'''stament : BREAK'''
	##a = Node('name',[],[#p[1]])
	#p[0] = Node('expr_list',[a,p[3]])

def p_stament_11(p):
	'''stament : BEGIN staments END'''
	#a = Node('name',[],[#p[1]])
	#p[0] = Node('expr_list',[a,p[3]])

def p_else_1(p):
	'''else : ELSE stament'''
	#p[0] = Node('read',[p[3]])

def p_else_2(p):
	'''else : empty'''
	
def p_location_read_1(p):
	'''location_read : ID'''
	#p[0] = Node('id',[],[#p[1]])

def p_location_read_2(p):
	'''location_read : ID LBRACKET expression RBRACKET'''
	##a = Node('id',[],[#p[1]])
	#b = Node('expr',[],[p[3]])
	#p[0] = Node('vec',[a,b])

def p_expression_1(p):
	'''expression : expression PLUS expression'''
	#p[0] = Node('fnum',[],[#p[1]])

def p_expression_2(p):
	'''expression : expression DIVIDE expression'''
	#a = Node('id',[],[#p[1]])
	b = Node('expr',[],[p[3]])
	#p[0] = Node('vec',[a,b])

def p_expression_3(p):
	'''expression : expression MULT expression'''
	#p[0] = Node('id',[],[#p[1]])

def p_expression_4(p):
	'''expression : expression MINUS expression'''
	#p[0] = Node('num',[],[#p[1]])

def p_expression_5(p):
	'''expression : UMINUS expression'''
	#p[0] = Node('plus',[#p[1],p[3]])

def p_expression_6(p):
	'''expression : LPAREN expression RPAREN'''
	#p[0] = Node('divide',[#p[1],p[3]])

def p_expression_7(p):
	'''expression : ID LPAREN expression_list RPAREN'''
	#p[0] = Node('mult',[#p[1],p[3]])

def p_expression_8(p):
	'''expression : ID'''
	#p[0] = Node('minus',[#p[1],p[3]])

def p_expression_9(p):
	'''expression : ID LBRACKET expression RBRACKET'''
	#p[0] = Node('uminus', [p[2]], [#p[1]])

def p_expression_10(p):
	'''expression : INUMBER'''
	#p[0] = p[2]

def p_expression_11(p):
	'''expression : FNUMBER'''
	##a = Node('name',[],[#p[1]])
	#p[0] = Node('expr_list',[p[3]])

def p_expression_12(p):
	'''expression : INT LPAREN expression RPAREN'''
	##a = Node('name',[],[#p[1]])
	#p[0] = Node('expr_list',[p[3]])

def p_expression_13(p):
	'''expression : FLOAT LPAREN expression RPAREN'''
	##a = Node('name',[],[#p[1]])
	#p[0] = Node('expr_list',[p[3]])

def p_expression_list_1(p):
	'''expression_list : expression'''
	#p[0] = #p[1]

def p_expression_list_2(p):
	'''expression_list : expression_list COMMA expression'''
	##p[1].append(p[3])
	#p[0] = #p[1]

def p_expression_list_3(p):
	'''expression_list : empty'''
	#p[1].append(p[3])

def p_relation_1(p):
	'''relation :  expression GREATER expression'''
	#p[0] = p[2]

def p_relation_2(p):
	'''relation :  expression DEQUAL expression'''
	#p[0] = p[2]

def p_relation_3(p):
	'''relation : expression LESS expression'''
	#a = Node('ope',[],[p[2]])
	#p[0] = Node('relation',[#p[1],a,p[3]])

def p_relation_4(p):
	'''relation : expression GREATEREQUAL expression'''
	#a = Node('ope',[],[p[2]])
	#p[0] = Node('relation',[#p[1],a,p[3]])

def p_relation_5(p):
	'''relation : expression LESSEQUAL expression'''
	#a = Node('ope',[],[p[2]])
	#p[0] = Node('relation',[#p[1],a,p[3]])

def p_relation_6(p):
	'''relation : expression DISTINT expression'''
	#a = Node('ope',[],[p[2]])
	#p[0] = Node('relation',[#p[1],a,p[3]])

def p_relation_7(p):
	'''relation : expression NOT expression'''
	#a = Node('ope',[],[p[2]])
	#p[0] = Node('relation',[#p[1],a,p[3]])

def p_relation_8(p):
	'''relation : expression OR expression'''
	#a = Node('ope',[],[p[2]])
	#p[0] = Node('relation',[#p[1],a,p[3]])

def p_relation_9(p):
	'''relation : expression AND expression'''
	#a = Node('ope',[],[p[2]])
	#p[0] = Node('relation',[#p[1],a,p[3]])

def p_relation_10(p):
	'''relation : NOT expression'''
	#a = Node('ope',[],[#p[1]])
	#p[0] = Node('relation',[a,p[2]])

def p_relation_11(p):
	'''relation : LPAREN expression RPAREN'''
	#a = Node('ope',[],[#p[1]])
	#p[0] = Node('relation',[a,p[2]])

def p_empty(p):
	"empty :"
	pass

def p_error(p):
	print "Error de sintaxis en o cerca de -> '%s'" % p.value,
	print "linea: %i " % p.lineno

parser = yacc.yacc(debug=1)

#
#Leo el archivo de entrada
#

try:
	f = open(sys.argv[1])
	res = parser.parse(f.read())

	if f: #Muestro el AST
		print "\n[    -----AST-----    ]"
		#dump_tree(res)
		print "[____-----End-----____]"

except IOError:
		print "Error al leer el archivo!"

