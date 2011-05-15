# -----------------------------------------------------
# mpastype - Sistema de Tipos de Datos
# -----------------------------------------------------

_unknown_num  = 1
_unknown_list = [ ]

class DataType:
    def __init__(self, typename = None):
        global _unknown_num
        if not typename:
            typename = "#%d" % _unknown_num
            _unknown_num += 1
            _unknown_list.append(self)
        self.type = typename
        self.depends = []   # Lista de tipos dependientes de este tipo

    def __cmp__(self, other):
        if self.type == other.type:
            return 0
        return 1

    def __str__(self):
        return self.type

    def __repr__(self):
        return self.type

    def is_array(self):
        return False

    def is_basic(self):
        if self.type != 'error':
            return True
        return False

    def is_unknown(self):
        if self.type[0] == '#':
            return True
        return False

    def is_int(self):
        if self.type == 'int':
            return True
        return False

    def is_float(self):
        if self.type == 'float':
            return True
        return False

    def is_error(self):
        if self.type == 'error':
            return True
        return False

    def typename(self):
        return self.type

    # Fija type a typename
    def unify(self, typename, node = None):
        if self.type == tapename: return
        self.type = typename
        if node: self.node = node
        for t in self.depends:
            t.unify(typename, node)

    # Marca dos tipos desconocidos como lo mismo
    def sametype(self, other):
        if self.type[0] == '#' and other.type[0] == '#':
            self.depends.append(other)
            other.depends.append(self)

    # Chequea dos tipospara ver ellos pueden ser combinados (en operacion binaria)
    # Esta funcion devuelve un error de tipo o posiblemente ejecuta un
    # paso de unificacion
    def combine(self, other, node = None):
        if self.type[0] == '#' and other.type[0] == '#':
            # Ambos son desconocidos. Se debe unificar y regresar
            self.sametype(other)
            return self
        if self.type[0] == '#':
            # Hacerla del mismo tipo de other
            self.unify(other.type, node)
            return self
        if other.type[0] == '#':
            other.unify(self.type, node)
            return self
        if self.type == other.type:
            return self
        # Error de tipo
        return None

class Array(DataType):
    def __init__(self, size, typename):
        self.size = size
        self.type = typename

    def __cmp__(self, other):
        if not other.is_array():
            return 1
        if self.size != other.size:
            return 1
        return cmp(self.type, other.type)

    def __str__(self):
        return '%s[%d]' % (self.type, self.size)

    def __repr__(self):
        return self.__str__()

    def is_basic(self):
        return False

    def is_array(self):
        return True

    def is_unknown(self):
        return self.type.is_unknown()

    def child_type(self):
        return self.type

    def array_size(self):
        return self.size

_types = { }

# Retorna un objeto type para el tipo typename. Primero chequea un cache
# para ver si realmente existe.

def newtype(typename = None):
    if typename:
        t = _types.get(typename)
        if not t:
            t = DataType(typename)
            _types[typename] = t
        return t
    return DataType()

def check_unknown():
    for t in _unknown_list:
        if t.is_unknown():
            sym = t.func
            print "Linea %d. Ningung tipo retornado pudo determinar la %s" % (sym.lineno, sym.name)

