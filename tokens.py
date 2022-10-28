class ConstructorToken:
    def __init__ (self, lexema, tipo, columna, fila):
        self.lexema = lexema
        self.tipo = tipo
        self.columna = columna 
        self.fila = fila

class Token:
    def __init__ (self):
        self.listaTokens = []
    
    # Agrega un nuevo Token al listado
    def NuevoToken (self, lexema, tipo, columna, fila):
        nuevo = ConstructorToken (lexema, tipo, columna, fila)
        self.listaTokens.append (nuevo)