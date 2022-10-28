class Propiedades:
    def __init__ (self, control, id, propiedad, valores):
        self.control = control
        self.id = id
        self.propiedad = propiedad
        self.valores = valores

class Propiedad:
    def __init__ (self):
        self.listaPropiedades = []

    # Agrega un nuevo Token al listado
    def nuevaPropiedad (self, control, id, propiedad, valores):
        nuevo = Propiedades (control, id, propiedad, valores)
        self.listaPropiedades.append (nuevo)
        # nuevo = Controles (control, id, propiedades)
        # self.listaControles.append (nuevo)
        # print (f'Control: {nuevo.control} | ID: {nuevo.id}')