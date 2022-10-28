class ConstructorError:
    def __init__ (self, lexema, tipo, columna, fila, esperado):
        self.lexema = lexema
        self.tipo = tipo
        self.columna = columna 
        self.fila = fila
        self.esperado = esperado

class Error:
    def __init__ (self):
        self.listaErrores = []
    
    # Agrega un nuevo error a la lista de errores
    def NuevoError (self, lexema, tipo, columna, fila, esperado):
        nuevo = ConstructorError (lexema, tipo, columna, fila, esperado)
        self.listaErrores.append (nuevo)