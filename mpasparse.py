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
	p[0] = Node('program',[p[1],p[2]])


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
	b = Node('staments',[p[8]])
	p[0] = Node('func',[a,p[4],p[6],b])

def p_main(p):
	"main : FUN MAIN LPAREN RPAREN locals BEGIN staments END"
	a = Node('f_name',[],['main'])
	#b = Node('locals',[p[5]])
	#c = Node('staments',[p[7]])
	p[0] = Node('main',[a,p[5],p[7]])

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
	a = Node('f_name',[],[p[2]])
	p[0] = Node('func',[a,p[4],p[6],p[8]])	


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

def p_staments_1(p):
	'''staments : stament'''
	p[0] = Node('staments',[p[1]])


def p_staments_2(p):
	'''staments : staments SEMICOLON stament'''
	p[1].append(p[3])
	p[0] = p[1]

def p_stament_1(p):
	'''stament : BEGIN staments END'''
	p[0] = Node('beg_end',[p[2]])

def p_stament_2(p):
	'''stament : SKIP'''
	p[0] = Node('skip',[],[p[1]])

def p_stament_3(p):
	'''stament : while'''
	p[0] = p[1]

def p_stament_4(p):
	'''stament : if'''
	p[0] = p[1]

def p_stament_5(p):
	'''stament : assign'''
	p[0] = p[1]

def p_stament_6(p):
	'''stament : print'''
	p[0] = p[1]

def p_stament_7(p):
	'''stament : write'''
	p[0] = p[1]

def p_stament_8(p):
	'''stament : read'''
	p[0] = p[1]

def p_stament_9(p):
	'''stament : return'''
	p[0] = p[1]

def p_stament_10(p):
	'''stament : ID LPAREN expression_list RPAREN '''
	a = Node('name',[],[p[1]])
	p[0] = Node('expr_list',[a,p[3]])

def p_stament_11(p):
	'''stament : BREAK'''
	p[0] = Node('break',[],[p[1]])

def p_while(p):
	'''while : WHILE relation DO stament'''
	p[0] = Node('while',[p[2],p[4]])

def p_if_(p):
	'''if : IF relation THEN stament else'''
	p[0] = Node('if',[p[2],p[4],p[5]])

def p_else_1(p):
	'''else : ELSE stament'''
	p[0] = Node('else',[p[2]])

def p_else_2(p):
	'''else : empty'''
	p[0] = Node('else []',[])

def p_assign_1(p):
	'''assign : ID COLONEQUAL expression'''
	a = Node('id',[],[p[1]])
	p[0] = Node('assign',[a,p[3]])

def p_assign_2(p):
	'''assign : ID LBRACKET expression RBRACKET COLONEQUAL expression'''
	a = Node('id',[],[p[1]])
	b = Node('expr',[],[p[3]])
	c = Node('vec',[a,b])
	p[0] = Node('assign',[c,p[6]])

def p_print(p):
	'''print : PRINT LPAREN TEXT RPAREN'''
	p[0] = Node('print',[],[p[1],p[3]])

def p_write(p):
	'''write : WRITE LPAREN expression RPAREN'''
	p[0] = Node('write',[p[3]])

def p_read(p):
	'''read : READ LPAREN location_read RPAREN'''
	p[0] = Node('read',[p[3]])

def p_return(p):
	'''return : RETURN expression'''
	p[0] = Node('return',[p[2]])

def p_location_read_1(p):
	''' location_read : ID'''
	p[0] = Node('id',[],[p[1]])

def p_location_read_2(p):
	'''location_read : ID LBRACKET expression RBRACKET'''
	a = Node('id',[],[p[1]])
	b = Node('expr',[],[p[3]])
	p[0] = Node('vec',[a,b])

def p_expression_1(p):
	'''expression : FNUMBER'''
	p[0] = Node('fnum',[],[p[1]])

def p_expression_2(p):
	'''expression : ID LBRACKET expression RBRACKET'''
	a = Node('id',[],[p[1]])
	b = Node('expr',[],[p[3]])
	p[0] = Node('vec',[a,b])

def p_expression_3(p):
	'''expression : ID'''
	p[0] = Node('id',[],[p[1]])

def p_expression_4(p):
	'''expression : INUMBER'''
	p[0] = Node('num',[],[p[1]])

def p_expression_5(p):
	'''expression : expression PLUS expression'''
	p[0] = Node('plus',[p[1],p[3]])

def p_expression_6(p):
	'''expression : expression DIVIDE expression'''
	p[0] = Node('divide',[p[1],p[3]])

def p_expression_7(p):
	'''expression : expression MULT expression'''
	p[0] = Node('mult',[p[1],p[3]])

def p_expression_8(p):
	'''expression : expression MINUS expression'''
	p[0] = Node('minus',[p[1],p[3]])

def p_expression_9(p):
	'''expression : MINUS expression %prec UMINUS'''
	p[0] = Node('uminus', [p[2]], [p[1]])

def p_expression_10(p):
	'''expression : LPAREN expression RPAREN'''
	p[0] = p[2]

def p_expression_11(p):
	'''expression : ID LPAREN expression_list RPAREN'''
	a = Node('name',[],[p[1]])
	p[0] = Node('expr_list',[p[3]])

def p_expression_list_1(p):
	'''expression_list : expression'''
	p[0] = p[1]

def p_expression_list_2(p):
	'''expression_list : expression_list COMMA expression'''
	p[1].append(p[3])
	p[0] = p[1]

def p_relation_1(p):
	'''relation :  LPAREN expression RPAREN'''
	p[0] = p[2]

def p_relation_2(p):
	'''relation : expression LESS expression'''
	a = Node('ope',[],[p[2]])
	p[0] = Node('relation',[p[1],a,p[3]])

def p_relation_3(p):
	'''relation : expression GREATER expression'''
	a = Node('ope',[],[p[2]])
	p[0] = Node('relation',[p[1],a,p[3]])

def p_relation_4(p):
	'''relation : expression GREATEREQUAL expression'''
	a = Node('ope',[],[p[2]])
	p[0] = Node('relation',[p[1],a,p[3]])

def p_relation_5(p):
	'''relation : expression LESSEQUAL expression'''
	a = Node('ope',[],[p[2]])
	p[0] = Node('relation',[p[1],a,p[3]])

def p_relation_6(p):
	'''relation : expression DEQUAL expression'''
	a = Node('ope',[],[p[2]])
	p[0] = Node('relation',[p[1],a,p[3]])

def p_relation_7(p):
	'''relation : expression DISTINT expression'''
	a = Node('ope',[],[p[2]])
	p[0] = Node('relation',[p[1],a,p[3]])

def p_relation_8(p):
	'''relation : expression NOT expression'''
	a = Node('ope',[],[p[2]])
	p[0] = Node('relation',[p[1],a,p[3]])

def p_relation_9(p):
	'''relation : expression OR expression'''
	a = Node('ope',[],[p[2]])
	p[0] = Node('relation',[p[1],a,p[3]])

def p_relation_10(p):
	'''relation : expression AND expression'''
	a = Node('ope',[],[p[2]])
	p[0] = Node('relation',[p[1],a,p[3]])

def p_relation_11(p):
	'''relation : NOT expression'''
	a = Node('ope',[],[p[1]])
	p[0] = Node('relation',[a,p[2]])

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
