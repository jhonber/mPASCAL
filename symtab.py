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
		self.numpar=[]

	def __repr__(self):
		a= self.name
		return a

	def __str__(self):
		return self.name

	def appd(self,num):
		self.numpar.append(num)


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
	s=is_symbol(t.value) 		# Mira si un token ya esta en la TS
	if not s:					# Si no esta!!
		s = add_symbol(t.value) # Agrega un simbolo a la TS
		s.lineno = t.lineno		# 's' es un objeto y le agrego el att lineno 
		last.append(s)			# Agrego el objeto 's' a last
	else:						# Si esta!!
		s.name=t.value			# le pone el att name
		s.lineno=t.lineno		# y linea
		last.append(s)			# agrega a last

	#print "\n => ",dir(last[0])

# Mira si un simbolo esta en la tabla de simbolos
def is_symbol(name):
	for s in current:
		if s.name==name:
			return s
	return None

# Para ponerle el atributo 'clase'=funcion a cada funcion y tambien el #  de argumentos
def baf(name,arg=None):
	for s in current:
		if s.name == name:
			s.clase = 'funcion'
			s.arg=arg

# Para ponerle el atributo 'class'=ident y 'typ' a cada identificador que no sea una funcion
def banf(name,typ=None):
	for s in current:
		if s.name == name:
			if not (hasattr(s,'clase') or hasattr(s,'typ')):
				s.clase = 'ident'
				s.typ=typ
				return None
			else:
				#print "#REDECLARADO# %s" % s.name
				return s

def banf2(name,typ=None):
	for s in current:
		if s.name == name:
			if not (hasattr(s,'clase') or hasattr(s,'typ')):
				s.clase = 'ident'
				s.typ=typ
			if hasattr(s,'typ'):
				if s.typ != typ:
					return None
			return s

# Funcion para que chequea si una funcion ya ha sido declarada
def redeclaration(name):
	for s in current:
		if hasattr(s,'clase'):
			if s.name==name:
				return s
	return False

# Funcion que chequea si se ha redeclarado una variable
def rdeclaration(name):
	for s in current:
		if hasattr(s,'clase'):
			if s.name==name:
				return s
	return False

# Temporal
def arguments(name,arg):
	for s in current:
		##print "==>", dir(s)
		if s.name==name:
			pass
	return False

# Para agregar inf de los arguments
def addarg(num):
	scopes[-2][-1].appd(num)
	##print "\n#_____#",scopes,"\n"


# Busca identificador en la tabla de simbolos
def findS(name):
	##print ":::::___findS__::::"
	##print "scopes: ",scopes
	for n in range(len(scopes)-1,-1,-1):
		for s in scopes[n]:
			##print "scopes[%i]: %s" % (n,scopes[n])
			##print "s: ",s
			##print "dir(s) ", dir(s)
			##print ":::::__EndFindS___::::"
			if s.name==name and (hasattr(s,'typ') or hasattr(s,'clase')):
				return None
	return last[-1]

# Busca identificador en la tabla de simbolos
def findS2(name):
	##print ":::::___findS__::::"
	##print "scopes: ",scopes
	for n in range(len(scopes)-1,-1,-1):
		for s in scopes[n]:
			##print "scopes[%i]: %s" % (n,scopes[n])
			##print "s: ",s
			##print "dir(s) ", dir(s)
			##print ":::::__EndFindS___::::"
			if s.name==name and (hasattr(s,'typ') or hasattr(s,'clase')):
				return s
	return None

def buscarSv(name):
	for n in range(len(scopes)-1,-1,-1):
		for s in scopes[n]:
			if s.name==name and hasattr(s,'type'):
				if s.dim>0:
					return None
	return last[-1]


