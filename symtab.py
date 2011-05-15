# -----------------------------------------------------------------------------
# Modulo para la tabla de simbolos de miniPASCAL
# -----------------------------------------------------------------------------

# Lista de ambito actual

_scopes = [ ]
current = None

class Symbol: pass

def new_scope():
    global current
    current = { }
    _scopes.append(current)
    return current

def pop_scope():
    global current
    r = _scopes.pop()
    current = _scopes[-1]
    return r

def get_symbol(name,level=0,attr=None):
    for i in range(len(_scopes)-(level+1),-1,-1):
        s = _scopes[i]
        try:
            sym = s[name]
            if attr:
                if hasattr(sym,attr): return sym
            else:
                return sym
        except KeyError:
            pass
    return None

def add_symbol(name):
    s = Symbol()
    s.name = name
    s.scope = current
    s.level = len(_scopes) - 1
    current[name] = s
    return s

# Instala un simbol en el ambito actual
def set_symbol(s):
    current[s.name] = s
    
# Adjunta entrada tabla de simbolos a token t
def attach_symbol(t):
    s = current.get(t.value)
    if not s:
        s = add_symbol(t.value)
        s.lineno = t.lineno
    t.symtab = s

