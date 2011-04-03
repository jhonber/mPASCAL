
import ply.yacc as yacc

from mpaslex import tokens

def p_program(p):
	'''program : list_functions main'''
	pass

def p_list_functions(p):
	'''list_functions : FUN ID LPAREN arguments RPAREN locals BEGIN staments END
					  | empty'''
	pass

def p_main(p):
	"main : FUN MAIN LPAREN arguments RPAREN locals BEGIN staments END"
	pass

def p_arguments(p):
	''' arguments : declaration_variables
                                | empty'''
	pass

def p_locals(p):
	'''locals : declaration_variables SEMICOLON locals
              | declaration_functions SEMICOLON locals
              | empty'''
	pass

def p_declaration_variables(p):
	'''declaration_variables : ID COLON tipo
                          | ID COLON tipo LBRACKET INUMBER RBRACKET
                          | arguments COMMA ID COLON tipo
                          | arguments COMMA ID COLON tipo LBRACKET INUMBER RBRACKET
		'''
	pass



def p_tipo(p):
	'''tipo : INT
     		| FLOAT'''
	pass

def p_declaration_functions(p):
	'''declaration_functions : FUN ID LPAREN arguments RPAREN locals BEGIN staments END SEMICOLON
                             | declaration_functions FUN ID LPAREN arguments'''
	pass

def p_staments(p):
	'''staments : stament
                | stament SEMICOLON stament'''
	pass

def p_stament(p):
	'''stament : while
               | if
               | if_else
               | assign
               | print
               | write
               | read
               | return
               | ID LPAREN expression RPAREN 
               | SKIP SEMICOLON
               | BREAK SEMICOLON'''
	pass

def p_while(p):
	'''while : WHILE relation DO staments
             | WHILE relation BEGIN staments END'''
	pass

def p_if(p):
	'''if : IF relation THEN staments SEMICOLON
          | IF relation THEN BEGIN staments END SEMICOLON'''
	pass

def p_if_else(p):
	'''if_else : IF ralation THEN staments ELSE staments SEMICOLON'''
	pass

def p_assign(p):
	'''assign : ID COLONEQUAL expression SEMICOLON'''
	pass

def p_print(p):
	'''print : PRINT LPAREN TEXT RPAREN SEMICOLON'''
	pass

def p_write(p):
	'''write : WRITE LPAREN expression RPAREN SEMICOLON'''
	pass

def p_read(p):
	'''read : READ LPAREN location_read RPAREN SEMICOLON'''
	pass

def p_return(p):
	'''return : RETURN expression SEMICOLON'''
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
        	      | MINUS expression
        	      | LPAREN expression RPAREN
        	      | ID LPAREN expression_list RPAREN
        	      | ID
        	      | ID LBRACKET expression RBRACKET
        	      | INUMBER
        	      | FNUMBER'''
	pass

def p_expression_list(p):
	'''expression_list : expression
    	                | expression COMMA expression
                    	| empty'''
	pass	


def p_relation(p):
	'''relation : expression GREATER expression
                | expression LESS expression
                | expression GREATEREQUAL expression
                | expression LESSEQUAL expression
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

def p_error(t):
	print "Error cuiado"
	raise ParseError()

yacc.yacc(debug=1)

