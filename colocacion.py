class Colocaciones:
    def __init__ (self, control, id, propiedad, valores):
        self.control = control
        self.id = id
        self.propiedad = propiedad
        self.valores = valores

class Colocacion:
    def __init__ (self):
        self.listaColocaciones = []

    # Agrega un nuevo Token al listado
    def nuevaColocacion (self, control, id, propiedad, valores):
        nuevo = Colocaciones (control, id, propiedad, valores)
        self.listaColocaciones.append (nuevo)
        #print (f'Control: {nuevo.control} | ID: {nuevo.id}')