# -----------------------------------------------------------------------------
# Modulo para la tabla de simbolos de miniPASCAL
# -----------------------------------------------------------------------------

# Lista de ambito current

last=[]
scopes = []
current = None

class Symbol:
	def __init__(self,name):
		self.name=name

	def __repr__(self):
		a= self.name
		return a

	def __str__(self):
		return self.name
	


def new_scope():
	global current
	current = []
	scopes.append(current)
	return current

def pop_scope():
	global current
	r = scopes.pop()
	current = scopes[-1]
	return r

# Crea un objeto 's' con el atributo 'name' y lo agrega a current
def add_symbol(name):
	s = Symbol(name)
	current.append(s)
	return s

# Instala un simbol en el ambito current
def set_symbol(s):
	current[s.name] = s
	
# Adjunta entrada tabla de simbolos a token
def attach_symbol(t):
	#print "****"
	#print '** c: ',current
	#print "****"	
	s=is_symbol(t.value) 		# Mira si un token ya esta en la TS
	if not s:					# Si no esta!!
		s = add_symbol(t.value) # Agrega un simbolo a la TS
		s.lineno = t.lineno		# 's' es un objeto y le agrego el att lineno 
		last.append(s)			# Agrego el objeto 's' a last
	else:						# Si esta!!
		s.name=t.value			# le pone el att name
		s.lineno=t.lineno		# y linea
		last.append(s)			# agrega a last

	#print "----"
	#print '-- last: ',last
	#print "----"
	
	#print "\n => ",dir(last[0])

# Mira si un simbolo esta en la tabla de simbolos
def is_symbol(name):
	for s in current:
		if s.name==name:
			return s
	return None


#def bas(name,type,dim):
#	for s in current:
#		if s.name==name:
#			s.type=type
#			s.dim=dim

# Para ponerle el atributo 'clase' a cada funcion 
def baf(name,numpar=None):
	for s in current:
		#print dir(s)
		if s.name == name:
			s.clase = 'funcion'
			if numpar:
				s.numpar=numpar

# Funcion para que chequea si una funcion ya ha sido declarada
def redeclaration(name):
	for s in current:
		#print dir(s)
		if hasattr(s,'clase'):
			if s.name==name:
				return s
	return False

#def redeclaration(name):
#	if current[-1].name==name and not hasattr(current[-1],'type'):
#		return None
#	return last[-1]

def findS(name):
	for n in range(len(scopes)-1,-1,-1):
		for s in scopes[n]:
			if s.name==name and (hasattr(s,'type') or hasattr(s,'clase')):
				return None
	return last[-1]

def buscarSv(name):
	for n in range(len(scopes)-1,-1,-1):
		for s in scopes[n]:
			if s.name==name and hasattr(s,'type'):
				if s.dim>0:
					return None
	return last[-1]


