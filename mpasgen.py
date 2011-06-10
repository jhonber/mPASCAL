import StringIO
data = StringIO.StringIO()

cont = -1
sp_cont = 64
l_cont = 0
t_cont = 0

def generate(out,top):
	print >>out, "! Creado por mpascal.py"
	print >>out, "! Jhon IS744 (2011-1)"
	print >>out, "   .section     \".text\""

def emit_program(out,top):
	print >>out,"\n! program"
	for i in range (0,len(top.children)):
		func=top.children[i]
		emit_function(out,func)
	print >>out,"\n    .section \".rodata\" \n"

def emit_function(out,func):
	fname = func.children[0].name
	print >>out,"\n! function: %s (start) " % fname
	print >>out,"    .global %s \n" % fname
	print >>out,"%s: \n" % fname
	label = new_label()
	sttms = func.children[2].children
	args = func.children[0].children
	local = func.children[1].children
	#offset_p = allocate_locals(local)
	#calcular_sp(out, args, local)
	funcstatements = func.children[-1].children
	emit_statements(out,funcstatements)
	print >> out, "\n%s:" % label
	if func.leaf =="main":
		print >> out, "     mov 0, %o0"
		print >> out, "     call_exit "
		print >> out, "     nop"
	print >> out, "     ret"
	print >> out, "     restore"
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
	value = s.leaf
	label = new_label()
	print >> data, '%s:      .asciz "%s" ' % (label, value)
	print >> out, '      sethi %%hi(%s), %%o0' % label
	print >> out, '      or    %%0, %%lo(%s), %%o0' %label
	print >> out, '      call  flprint'
	print >> out, '      nop'
	print >> out, "! print (end)"
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
	result = pop(out)
	print >>out, "     st %s, %s                ! %s := pop" % (result ,s.children[0].name,s.children[0].name)
	print >>out, "! asig (end)"

def emit_while(out,s):
	print >>out, "! while (start)"
	test_label= new_label()
	done_label= new_label()
	print >>out, "%s:" % test_label
	relop = s.children[0]
	eval_expression(out,relop)
	print >>out, "!   relop := pop" 
	print >>out, "!   if not relop: goto done"

	for i in range(0,len(s.children[1].children)):
		statement = s.children[1].children[i]
		emit_statement(out,statement)
	print >>out, "! goto %s" % test_label
	print >>out, "%s:" % done_label
	print >>out, "! while (end)\n"

def emit_if(out,s):
	print >>out, "\n! if (start)"
	if_label = new_label()
	relop = s.children[0]
	print >>out, "! relop := pop"
	print >>out, "! if false: goto %s:" % if_label
	if s.children[1].name == "staments":
		for i in range(0,len(s.children[1].children)):
			statement = s.children[1].children[i]
			emit_statement(out,statement)
	else:
		emit_statement(out,s.children[1])
	
	else_label = new_label()
	print >>out, "! goto %s " % else_label
	print >>out, "! else:"
	if s.children[2].name == "else":
		if s.children[2].children[0].name == "staments":
			for i in range(0,len(s.children[2].children[0].children)):
				statement = s.children[2].children[0].children[i]
				emit_statement(out,statement)
		else:
			emit_statement(out,s.children[2].children[0])

	print >>out, "! %s: " % else_label
	print >>out, "! if (end)\n"

#
# Evaluacion de expresiones
#
def eval_expression(out,expr):
	if expr.name == 'number':
		print >> out, '     mov %s, %s               ! push %s' %(expr.value,push(out),expr.value)

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
		print >> out, '     mov %s, %s               ! push %s' %(expr.value,push(out),expr.value)

	elif expr.name == '+':
		left = expr.children[0]
		right = expr.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		r = pop(out)
		l = pop(out)
		print >>out, "     add %s, %s, %s        ! add" %(l,r,push(out))

	elif expr.name == '-':
		left = expr.children[0]
		right = expr.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		r = pop(out)
		l = pop(out)
		print >>out, "     sub %s, %s, %s        ! sub" %(l,r,push(out))

	elif expr.name == '*':
		left = expr.children[0]
		right = expr.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		r = pop(out)
		l = pop(out)
		print >>out, "     mov %s,%%o0" %l
		print >>out, "     call .mul                ! mult"
		print >>out, "     mov %s,%%o1" %r
		print >>out, "     mov %%o0, %s             ! push" % push(out)

	elif expr.name == '/':
		left = expr.children[0]
		right = expr.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		r = pop(out)
		l = pop(out)
		print >>out, "     mov %s,%%o0" %l
		print >>out, "     call .div             ! div"
		print >>out, "     mov %s,%%o1" %r
		print >>out, "     mov %%o0, %s          ! push" % push(out)

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

def new_label():
	global cont
	cont+=1
	return ".L%s" % cont

def calcular_sp(out, args, local):
    global sp_cont
    sp_cont += 4
    for s in local:
        if s.children[0].name == "vec":
            temp = int(s.children[0].children[0].leaf)*4
            sp_cont += temp
        else:
            sp_cont += 4
    for s2 in args:
        if s2.children[0].name == "vec":
            temp = int(s2.children[0].children[0].leaf)*4
            sp_cont += temp
        else:
            sp_cont += 4
    while (sp_cont % 8) != 0:
        sp_cont += 4
    print >> out, '     save %%sp, -%d, %%sp' % sp_cont

def allocate_locals(local):
	offset = 0    
	for s in local:
		if s.children.name == "vec":
			temp = int(s.children[0].children[0].leaf)*4
			offset += temp
		else:
			offset += 4


def push(out):
    global l_cont
    global t_cont
    global sp_cont
    if l_cont < 8 and t_cont != 8:
        l = '%l'+str(l_cont)
        l_cont +=1        
    else:
        if l_cont == 8:
            l_cont = 0
            t_cont = 8
        l = '%l'+str(l_cont)
        print >> out, "     st %s, [%%fp -%d]" % (l, sp_cont)
        sp_cont +=4
        l_cont +=1        
    return l
    
def pop(out):
    global l_cont
    global t_cont
    global sp_cont
    if l_cont >= 0 and t_cont == 0:
        l_cont -=1
        l = '%l'+str(l_cont)
    else:
        l_cont = t_cont
        t_cont = 0
        l_cont -=1
        l = '%l'+str(l_cont)
    return l
