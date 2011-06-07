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
import symtab
import mpastype

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
	('right', 'ELSE'),
    )

#
#Definicion de la gramatica y contruccion del AST
#

def p_program(p):
	'''program : funclist'''
	p[0] = p[1]

def p_funclist_1(p):
	'''funclist : function'''
	p[0] = Node('program',[p[1]])

def p_funclist_2(p):
	'''funclist : funclist function'''
	p[1].append(p[2])
	p[0] = p[1]

funcstack = [ ] # Pila de funciones

def p_function(p):
	'''function : fun arguments locals BEGIN staments END'''
	p[0] = Node('func', [p[1],p[2],p[3],p[5]])
	#p[0].typ="int"
	
	symtab.pop_scope()
	

def p_fun_scope(p):
	'''fun : FUN ID'''
	p[0] = Node('',[],[p[2]])
	p[0].name = p[2]
	p[0].typ = "int"
	# Miro si el nombre de la funcion ya esta en current
	re=symtab.redeclaration(p[2])
	if re:
		print "#Error# redeclaracion de funcion '%s' en linea %i" % (re.name,re.lineno)
	else: #Sino esta redefinido lo agrega a la tabla
		symtab.baf(p[2],"int")
	
	funcstack.append(p[2])
	
	#Creo un nuevo scope
	symtab.new_scope()


def p_arguments_1(p):
	'''arguments : LPAREN RPAREN'''
	p[0] = Node('arguments ()',[])
	p[0].arg = 0
	funcstack.insert(len(funcstack),0)

def p_argument_2(p):
	'''arguments : LPAREN declaration_variables RPAREN'''
	p[0] = p[2]
	p[0].arg=len(p[2].children)


##	Intengo colocar en la tabla de simbolos inf de los
	#print "\n\nFun: %s\n\n" % p[2].children[0].typ
	for i in p[2].children:
		#print ": i-",i.typ
		symtab.addarg(i.typ)
##

	# Para ponerle los artributos a las funciones el numero de argumentos
	symtab.baf(funcstack[-1],p[2].arg)

def p_declaration_variables_1(p):
	'''declaration_variables : param'''
	p[0] = Node('arguments',[p[1]])
	

def p_declaration_variables_2(p):
	'''declaration_variables : declaration_variables COMMA param'''
	p[1].append(p[3])
	p[0] = p[1]	

def p_param_2(p):
	'''param : ID COLON ID'''
	p[0] = Node('',[],[p[1],p[3]])

def p_param_3(p):
	'''param : ID COLON INT'''

	p[0] = Node('',[],[p[1],p[3]])
	p[0].clase = "ident"
	p[0].typ = p[3]
	p[0].name = p[1]
	p[0].value = p[1]
	
	a=symtab.banf(p[0].name,p[0].typ)
	if a :
		print "#Error# redeclaracion de identificador '%s' en linea %i" % (p[0].name,a.lineno)
	

def p_param_4(p):
	'''param : ID COLON FLOAT'''
	p[0] = Node('',[],[p[1],p[3]])
	p[0] = Node('',[],[p[1],p[3]])
	p[0].clase = "ident"
	p[0].typ = p[3]
	p[0].name = p[1]

	a=symtab.banf(p[0].name,p[0].typ)
	if a :
		print "#Error# redeclaracion de identificador '%s' en linea %i" % (p[0].name,a.lineno)

def p_param_5(p):
	'''param : ID COLON type'''
	p[0] = Node('',[p[3]],p[1])
	p[0].name = p[1]
	p[0].value = p[1]
	p[0].typ=p[3].typ

	a=symtab.banf(p[0].name,p[3].typ)
	if a :
		print "#Error# redeclaracion de identificador '%s' en linea %i" % (p[0].name,a.lineno)

def p_locals_1(p):
	'''locals : dec_list SEMICOLON'''
	p[0] = p[1]
	if hasattr(p[1], "typ"):
		typ = p[1].typ
	else:
		typ=None
	symtab.banf(p[1].name,typ)


def p_locals_2(p):
	'''locals : empty'''
	p[0] = Node('locals ()',[])

def p_dec_list_1(p):
	'''dec_list : var_dec'''
	p[0] = Node('locals',[p[1]])
	p[0].name = p[1].name
	p[0].clase = "ident"
	if hasattr(p[1], "typ"):
		p[0].typ = p[1].typ

def p_dec_list_2(p):
	'''dec_list : dec_list SEMICOLON var_dec'''
	p[1].append(p[3])
	p[0] = p[1]

def p_var_dec_1(p):
	'''var_dec : param'''
	p[0] = p[1]

def p_var_dec_2(p):
	'''var_dec : function'''
	p[0] = p[1]

def p_type_3(p):
	'''type : INT LBRACKET expression RBRACKET'''
	p[0] = Node('type',[p[3]],p[1])
	p[0].typ="int["+str(p[3].value)+"]"

def p_type_4(p):
	'''type : FLOAT LBRACKET expression RBRACKET'''
	p[0] = Node('type',[p[3]],p[1])
	p[0].typ="int["+str(p[3].value)+"]"

def p_staments_1(p):
	'''staments : stament'''
	p[0] = Node('staments',[p[1]])
	
def p_staments_2(p):
	'''staments : staments SEMICOLON stament'''
	p[1].append(p[3])
	p[0] = p[1]

def p_stament_1(p):
	'''stament : WHILE relation DO stament''' #while
	#a = Node('',[p[4]])
	p[0] = Node('while',[p[2],p[4]])

def p_stament_2(p):
	'''stament : IF relation THEN stament else''' #if
	p[0] = Node('if',[p[2],p[4],p[5]])

def p_stament_3(p):
	'''stament : location_read COLONEQUAL expression''' #assign
	p[0] = Node('assign',[p[1],p[3]])
	p[0].assign = 1
	a=symtab.findS(p[1].name)

	if hasattr(p[1], "typ"):
		typ=p[1].typ
	else:
		typ=None

	s=symtab.banf2(p[1].name,typ)
	if not s:
		print "#Error# Assign '%s' error de tipos" % (p[1].name)

	if a:
		print "#Error# variable no declarada '%s' en la linea %i " % (p[1].name,a.lineno)

def p_stament_4(p):
	'''stament : PRINT LPAREN TEXT RPAREN'''
	p[0] = Node('print',[],p[3])

def p_stament_5(p):
	'''stament : WRITE LPAREN expression RPAREN'''
	p[0] = Node('write',[p[3]])
	
def p_stament_6(p):
	'''stament : READ LPAREN location_read RPAREN'''
	p[0] = Node('read',[p[3]])

def p_stament_7(p):
	'''stament : RETURN expression'''
	p[0] = Node('',[p[2]],p[1])

def p_stament_8(p):
	'''stament : ID LPAREN expression_list RPAREN''' #call
	f=symtab.findS2(p[1])

	args = len(p[3].children)
	if 	p[3].leaf:
		args += 1

	if not f:
		print "#Error# Función no declarada '%s' " % (p[1]),
		if hasattr(f,'lineno'):
			print "en la linea",f.lineno
	else:
		##print "ARgs= ",args,"len(f.num)=",len(f.numpar)
		
		if args != len(f.numpar):
			print "#Error# Numero de argumentos erroneo en '%s'" % f.name
		else:
			if 	p[3].leaf:
				#print "adadsdsad: ", p[3].typ , ":::" , f.name,f.numpar
				if p[3].typ != f.numpar[0]:
					print "#Error# Tipos de argumentos erroneo en'%s'" % f.name
				else:
					for i in range(0,len(p[3].children)):
						##print "p[3].children[i]= ",p[3].children[i],p[3].children[i].typ
						##print "f.numpar[i+1]: ",f.numpar[i+1]
						if hasattr(p[3].children[i],'typ'):
							if p[3].children[i].typ != f.numpar[i+1]:
								print "#Error# Tipos de argumentos erroneo en'%s'" % f.name
								break
						
	#print "tiene argumentos arG? ",p[3].typ
	if hasattr(p[3],'typ'):
		p[0] = Node('',[p[3]],p[1])
		p[0].name = p[1]
		p[0].value = p[1]
		p[0].call = 1
		p[0].typ = p[3].typ
	else:
		p[0] = Node('',[p[3]],p[1])
		p[0].call = 1
		p[0].name = p[1]
		p[0].value = p[1]

def p_stament_9(p):
	'''stament : SKIP'''
	p[0] = Node('skip',[p[1]])

def p_stament_10(p):
	'''stament : BREAK'''
	p[0] = Node('',[],p[1])

def p_stament_11(p):
	'''stament : BEGIN staments END'''
	p[0] = p[2]

def p_else_1(p):
	'''else : ELSE stament'''
	p[0] = Node('else',[p[2]])

def p_else_2(p):
	'''else : empty'''
	p[0] = Node('else ()')
	
def p_location_read_1(p):
	'''location_read : ID'''
	p[0] = Node('',[],p[1])
	p[0].name = p[1]
	p[0].value = p[1]
	#p[0] = p[1]

def p_location_read_2(p):
	'''location_read : ID LBRACKET expression RBRACKET'''
	p[0] = Node('',[p[3]],p[1])
	p[0].name = p[1]
	p[0].value = p[1]

	if hasattr(p[3],'typ'):
		if p[3].typ != 'int':
			print "#Error# El indice de un vector debe ser entero '%s'" % f.name
		else:
			p[0].typ = p[3].typ

def p_expression_1(p):
	'''expression : expression PLUS expression'''
	p[0] = Node('+',[p[1],p[3]])

def p_expression_2(p):
	'''expression : expression DIVIDE expression'''
	p[0] = Node('/',[p[1],p[3]])

def p_expression_3(p):
	'''expression : expression MULT expression'''
	p[0] = Node('*',[p[1],p[3]])

def p_expression_4(p):
	'''expression : expression MINUS expression'''
	p[0] = Node('-',[p[1],p[3]])

#def p_expression_5(p):
#	'''expression : UMINUS expression'''
#	p[0] = Node('uminus',[p[2]])


def p_expressionUNO(p):
	'''expression : MINUS expression'''
	p[0] = Node('uminus',[p[2]])
	p[0].typ = 'um'

def p_expressionDOS(p):
	'''expression : PLUS expression'''
	p[0] = Node('uminus',[p[2]])

def p_expression_6(p):
	'''expression : LPAREN expression RPAREN'''
	p[0] = p[2]

def p_expression_7(p):
	'''expression : ID LPAREN expression_list RPAREN'''
	p[0] = Node('call',[p[3]],p[1])
	p[0].value = p[1]
	#print "dir ",dir(p[1]),"name: ",p[1]
	f = symtab.findS2(p[1])
	##print "**dir ",dir(f),"name: ",f.name
	if f:
		p[0].typ = "int"

def p_expression_8(p):
	'''expression : ID'''
	p[0] = Node('id',[],p[1])
	p[0].value = p[1]
	f = symtab.findS2(p[1])
	if f:
		#print "\n* %s *\n" % dir(f)
		p[0].typ = f.typ

def p_expression_9(p):
	'''expression : ID LBRACKET expression RBRACKET'''
	p[0] = Node('vec', [p[3]],p[1])
	p[0].value = p[1]

	if hasattr(p[3],'typ'):
		if p[3].typ != 'int':
			print "#Error# El indice de un vector debe ser entero '%s'" % f.name
		else:
			p[0].typ = p[3].typ

def p_expression_10(p):
	'''expression : INUMBER'''
	p[0] = Node('number',[],p[1])
	p[0].value = p[1]
	p[0].typ = "int"

def p_expression_11(p):
	'''expression : FNUMBER'''
	p[0] = Node('number',[],p[1])
	p[0].value = p[1]
	p[0].typ= "float"

def p_expression_12(p):
	'''expression : INT LPAREN expression RPAREN'''
	p[0] = Node('cast',[p[3]],p[1])
	p[0].typ = "int"

def p_expression_13(p):
	'''expression : FLOAT LPAREN expression RPAREN'''
	p[0] = Node('cast',[p[3]],p[1])
	p[0].typ = "float"

def p_expression_list_1(p):
	'''expression_list : expression'''
	p[0] = p[1]
	#argstack2.insert(len(argstack2),p[1].name)

def p_expression_list_2(p):
	'''expression_list : expression_list COMMA expression'''
	p[1].append(p[3])
	p[0] = p[1]

def p_expression_list_3(p):
	'''expression_list : empty'''
	p[0] = Node('expr_list',[])
	p[0].arg = 0

def p_relation_1(p):
	'''relation : expression GREATER expression'''
	p[0] = Node('>',[p[1],p[3]])

def p_relation_2(p):
	'''relation :  expression DEQUAL expression'''
	p[0] = Node('==',[p[1],p[3]])

def p_relation_3(p):
	'''relation : expression LESS expression'''
	p[0] = Node('<',[p[1],p[3]])

def p_relation_4(p):
	'''relation : expression GREATEREQUAL expression'''
	p[0] = Node('>=',[p[1],p[3]])

def p_relation_5(p):
	'''relation : expression LESSEQUAL expression'''
	p[0] = Node('<=',[p[1],p[3]])

def p_relation_6(p):
	'''relation : expression DISTINT expression'''
	p[0] = Node('!=',[p[1],p[3]])

#def p_relation_7(p):
#	'''relation : expression NOT expression'''
#	p[0] = Node('relation',[p[1],p[3]],p[2])

def p_relation_8(p):
	'''relation : relation OR relation'''
	p[0] = Node('or',[p[1],p[3]])

def p_relation_9(p):
	'''relation : relation AND relation'''
	p[0] = Node('and',[p[1],p[3]])

def p_relation_10(p):
	'''relation : NOT relation'''
	p[0] = Node('not',[p[2]])

def p_relation_11(p):
	'''relation : LPAREN relation RPAREN'''
	p[0] = Node('relation',[p[2]])

def p_empty(p):
	"empty :"
	pass

#Para contar los errores
Error=0

def p_error(p):
	#print dir(p)
	global Error
	Error +=1
	if hasattr(p,'value'):	
		print "#Error# de sintaxis en o cerca de -> '%s'" % p.value,
		print "linea: %i col: %i" % (p.lineno,p.lexpos)
	else:
		print "#Error# léxico"

parser = yacc.yacc(debug=1)

#
#Leo el archivo de entrada
#
'''
try:
	if sys.argv[1] == '-t':
		f = open(sys.argv[2])
	else:
		pass
		f = open(sys.argv[1])

	res = parser.parse(f.read())
	if f and sys.argv[1] == '-t': #Muestro el AST 
		if Error==0:
			print "\n[    -----AST-----    ]"
			dump_tree(res)
			print "[____-----End-----____]"
			pass

except IOError:
		print "Error al leer el archivo!"
'''

