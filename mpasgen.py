def generate(out,top):
    print >>out, "! Creado por mpascal.py"
    print >>out, "! Jhon IS744 (2011-1)"

def emit_program(out,top):
	for i in range (0,len(top.children)):
		func=top.children[i]
		emit_function(out,func)

def emit_function(out,func):
	fname = func.children[0].name
	print >>out,"\n! function: %s (start) " % fname
    
	for i in range (0,len(func.children[-1].children)):
		funcstatements = func.children[-1].children
		emit_statements(out,funcstatements)

	print >>out,"! function: %s (end) " % fname

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
	elif s.name == 'while':
		emit_while(out,s)
	elif hasattr(s,'call'):
		emit_call(out,s)
		
def emit_print(out,s):
	print >>out, "\n! call"

def emit_call(out,s):
	print >>out, "\n! print (start)"
	print >>out, "! print (end)"

'''
def emit_while(out,s):
    print >>out, "\n! while (start)"
    ...
    statement = (get body of while)
    emit_statement(out,statement)
    ...
    print >>out, "! while (end)"
'''
