def generate(out,top):
    print >>out, "! Creado por mpascal.py"
    print >>out, "! Jhon IS744 (2011-1)"

def emit_program(out,top):
	print >>out,"\n! program"
	for i in range (0,len(top.children)):
		func=top.children[i]
		emit_function(out,func)

def emit_function(out,func):
	fname = func.children[0].name
	print >>out,"\n! function: %s (start) " % fname
	#for i in range (0,len(func.children[-1].children)):
	funcstatements = func.children[-1].children
	emit_statements(out,funcstatements)
	print >>out,"\n! function: %s (end) " % fname

def emit_statements(out,statements):
	for s in statements:
		emit_statement(out,s)

def emit_statement(out,s):
	if s.name == 'print':
		emit_print(out,s)
	elif s.name == 'read':
		emit_read(out,s)
	elif s.name == 'write':
		emit_write(out,s)
	elif s.name == 'if':
		emit_if(out,s)
	elif s.name == 'while':
		emit_while(out,s)
	elif s.name == 'skip':
		emit_skip(out,s)
	elif hasattr(s,'call'):
		emit_call(out,s)
	elif hasattr(s,'assign'):
		emit_assign(out,s)
		
def emit_print(out,s):
	print >>out, "\n! print (start)"
	print >>out, "! print (end)"

def emit_call(out,s):
	print >>out,"\n! push %s() " % s.name

def emit_read(out,s):
	print >>out, "\n! read (start)"
	print >>out, "! read (end)"

def emit_write(out,s):
	print >>out, "\n! write (start)"
	expr = s.children[0]
	eval_expression(out,expr)
	print >>out, "! expr := pop"
	print >>out, "! write(expr)"
	print >>out, "! write (end)"

def emit_skip(out,s):
	print >>out, "\n! skip (start)"
	print >>out, "! skip (end)"

def emit_assign(out,s):
	print >>out, "\n! assign (start)"
	expr = s.children[1]
	eval_expression(out,expr)
	print >>out, "!   %s := pop" % s.children[0].name
	print >>out, "! assign (end)\n"

def emit_while(out,s):
	print >>out, "! while (start)"
	print >>out, "! test:"
	relop = s.children[0]
	eval_expression(out,relop)
	print >>out, "!   relop := pop" 
	print >>out, "!   if not relop: goto done"

	for i in range(0,len(s.children[1].children)):
		statement = s.children[1].children[i]
		emit_statement(out,statement)
	print >>out, "! goto test"
	print >>out, "! done:"
	print >>out, "! while (end)\n"

def emit_if(out,s):
	print >>out, "\n! if (start)"
	relop = s.children[0]
	print >>out, "!   if false: goto else"
	if s.children[1].name == "staments":
		for i in range(0,len(s.children[1].children)):
			statement = s.children[1].children[i]
			emit_statement(out,statement)
	else:
		emit_statement(out,s.children[1])
	
	print >>out, "! goto next "
	print >>out, "! else:"
	if s.children[2].name == "else":
		if s.children[2].children[0].name == "staments":
			for i in range(0,len(s.children[2].children[0].children)):
				statement = s.children[2].children[0].children[i]
				emit_statement(out,statement)
		else:
			emit_statement(out,s.children[2].children[0])

	print >>out, "! next: "
	print >>out, "! if (end)\n"

#
# Evaluacion de expresiones
#
def eval_expression(out,expr):
	if expr.name == 'number':
		print >>out, "!   push", expr.value

	if expr.name == 'call':
		if not expr.children[0].children:
			eval_expression(out,expr.children[0])
			print >>out,"! arg1 := pop"
			print >>out,"! push %s(arg1) \n" % expr.value

		else:
			eval_expression(out,expr.children[0])
			print >>out,"!   arg1 := pop"
			args="arg1"
			cont=2
			for i in expr.children[0].children:
				eval_expression(out,i)
				print >>out,"!   arg%i := pop" % cont
				args +=",arg"+str(cont)
				cont +=1
			print >>out,"!   push %s(%s)" % (expr.value,args)
		
	elif expr.name == 'vec':
		eval_expression(out,expr.children[0])
		print >>out, "!   index := pop"
		print >>out, "!   push %s[index]" % expr.value

	elif expr.name == 'id':
		print >>out, "!   push", expr.value

	elif expr.name == '+':
		left = expr.children[0]
		right = expr.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>out, "!   add"

	elif expr.name == '-':
		left = expr.children[0]
		right = expr.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>out, "!   sub"

	elif expr.name == '*':
		left = expr.children[0]
		right = expr.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>out, "!   mul"

	elif expr.name == '/':
		left = expr.children[0]
		right = expr.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>out, "!   div"

	elif expr.name == '>':
		left = expr.children[0]
		right = expr.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>out, "!   gt"

	elif expr.name == '==':
		left = expr.children[0]
		right = expr.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>out, "!   eq"

	elif expr.name == '<':
		left = expr.children[0]
		right = expr.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>out, "!   ls"

	elif expr.name == '>=':
		left = expr.children[0]
		right = expr.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>out, "!   ge"

	elif expr.name == '<=':
		left = expr.children[0]
		right = expr.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>out, "!   le"

	elif expr.name == '!=':
		left = expr.children[0]
		right = expr.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>out, "!   dt"

	elif expr.name == 'or':
		left = expr.children[0]
		right = expr.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>out, "!   or"

	elif expr.name == 'and':
		left = expr.children[0]
		right = expr.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>out, "!   and"

	elif expr.name == 'not':
		left = expr.children[0]
		right = expr.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>out, "!   not"
