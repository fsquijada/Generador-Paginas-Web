class Controles:
    def __init__ (self, control, id, propiedades):
        self.control = control
        self.id = id
        self.propiedades = propiedades

class Control:
    def __init__ (self):
        self.listaControles = []

    # Agrega un nuevo Token al listado
    def nuevoControl (self, control, id, propiedades):
        nuevo = Controles (control, id, propiedades)
        self.listaControles.append (nuevo)
        #print (f'Control: {nuevo.control} | ID: {nuevo.id}')