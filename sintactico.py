from instancias import controles, propiedades, colocaciones, token, error
from generadorHtml import Generador
# Variables
generador = Generador()
contadorTokens = 0

class Sintactico:
    def __init__(self):
        pass

    # Inicializa el analizador Sintactico
    def Sintactico (self):
        global contadorTokens
        contadorTokens = 0
        if token.listaTokens[contadorTokens].tipo == 'Diagonal':
            contadorTokens += 1
            self.Comentario()
        else:
            self.ListaInstrucciones()

    # Opción por si es un comentario
    def Comentario (self):
        global contadorTokens
        if token.listaTokens[contadorTokens].tipo == 'Diagonal':
            contadorTokens += 1
            if token.listaTokens[contadorTokens].tipo == 'Comentario':
                contadorTokens += 1
        elif token.listaTokens[contadorTokens].tipo == 'Asterisco':
            contadorTokens += 1
            if token.listaTokens[contadorTokens].tipo == 'Comentario':
                contadorTokens += 1
                if token.listaTokens[contadorTokens].tipo == 'Asterisco':
                    contadorTokens += 1
                    if token.listaTokens[contadorTokens].tipo == 'Diagonal':
                        contadorTokens += 1
                    else:
                        self.ErrorSintactico('/')
                        contadorTokens += 1
                else:
                    self.ErrorSintactico('*')
                    contadorTokens += 1
        else:
            self.ErrorSintactico('/ o *')
            contadorTokens += 1

    # Inicia la lista de instrucciones
    def ListaInstrucciones (self):
        if token.listaTokens[contadorTokens] != None:
            if token.listaTokens[contadorTokens].tipo == 'EOF':
                generador.ReporteHTML()
                generador.ReporteCSS()
            else:
                self.Instruccion()
                self.ListaInstrucciones()
        else:
            generador.ReporteHTML()
            generador.ReporteCSS()

    # Ingresa a verificar que entre a controles, propiedades o colocación
    def Instruccion (self):
        global contadorTokens
        if token.listaTokens[contadorTokens].tipo == 'Apertura':
            contadorTokens += 1
            if token.listaTokens[contadorTokens].tipo == 'Admiración':
                contadorTokens += 1
                if token.listaTokens[contadorTokens].tipo == 'Guión':
                    contadorTokens += 1
                    if token.listaTokens[contadorTokens].tipo == 'Guión':
                        contadorTokens += 1
                        if token.listaTokens[contadorTokens].lexema == 'Controles':
                            contadorTokens += 1
                            self.Controles()
                        elif token.listaTokens[contadorTokens].lexema == 'propiedades':
                            contadorTokens += 1
                            self.Propiedades()
                        elif token.listaTokens[contadorTokens].lexema == 'Colocacion':
                            contadorTokens += 1
                            self.Colocacion()
                        else:
                            self.ErrorSintactico('Control')
                            contadorTokens += 1
                    else:
                        self.ErrorSintactico('-')
                        contadorTokens += 1
                else:
                    self.ErrorSintactico('-')
                    contadorTokens += 1
            else:
                self.ErrorSintactico('!')
                contadorTokens += 1
        else:
            self.ErrorSintactico('<')
            contadorTokens += 1
            self.Instruccion()

    # Ingresa a la opción de controles
    def Controles (self):
        global contadorTokens
        if token.listaTokens[contadorTokens].tipo == 'Diagonal':
            contadorTokens += 1
            self.Comentario()
            self.Controles()
        else:
            self.ListaControles()
            if token.listaTokens[contadorTokens].tipo == 'Guión':
                contadorTokens += 1
                if token.listaTokens[contadorTokens].tipo == 'Guión':
                    contadorTokens += 1
                    if token.listaTokens[contadorTokens].tipo == 'Cierre':
                        contadorTokens += 1
                    else:
                        self.ErrorSintactico('>')
                        contadorTokens += 1
                else:
                    self.ErrorSintactico('-')
                    contadorTokens += 1
            else:
                self.ErrorSintactico('-')
                contadorTokens += 1

    # Ingresa a la lista de controles que vendran
    def ListaControles (self):
        global contadorTokens
        if token.listaTokens[contadorTokens].lexema == 'Controles':
            contadorTokens += 1
        elif token.listaTokens[contadorTokens].tipo == 'Diagonal':
            contadorTokens += 1
            self.Comentario()
            self.ListaControles()
        else:
            tmpControl = token.listaTokens[contadorTokens].lexema
            if tmpControl == 'Etiqueta' or tmpControl == 'Boton' or tmpControl == 'Check' or tmpControl == 'RadioBoton' or tmpControl == 'Texto' or tmpControl == 'AreaTexto' or tmpControl == 'Clave' or tmpControl == 'Contenedor':
                contadorTokens += 1
                tmpID = token.listaTokens[contadorTokens].lexema
                if token.listaTokens[contadorTokens].tipo != 'Punto y coma':
                    contadorTokens += 1
                    if token.listaTokens[contadorTokens].tipo == 'Punto y coma':
                        contadorTokens += 1
                        controles.nuevoControl (tmpControl, tmpID, '')
                        self.ListaControles()
                else:
                    self.ErrorSintactico('ID')
                    contadorTokens += 2
                    self.ListaControles()
            else:
                self.ErrorSintactico('Control')
                contadorTokens += 3
                self.ListaControles()

    # Ingresa a la opción de propiedades
    def Propiedades (self):
        global contadorTokens
        if token.listaTokens[contadorTokens].tipo == 'Diagonal':
            contadorTokens += 1
            self.Comentario()
            self.Propiedades()
        else:
            self.ListaPropiedades()
            if token.listaTokens[contadorTokens].tipo == 'Guión':
                contadorTokens += 1
                if token.listaTokens[contadorTokens].tipo == 'Guión':
                    contadorTokens += 1
                    if token.listaTokens[contadorTokens].tipo == 'Cierre':
                        contadorTokens += 1
                    else:
                        self.ErrorSintactico('>')
                        contadorTokens += 1
                else:
                    self.ErrorSintactico('-')
                    contadorTokens += 1
            else:
                self.ErrorSintactico('-')
                contadorTokens += 1

    # Ingresa a la lista de propiedades que vendran
    def ListaPropiedades (self):
        global contadorTokens
        if token.listaTokens[contadorTokens].lexema == 'propiedades':
            contadorTokens += 1
        elif token.listaTokens[contadorTokens].tipo == 'Diagonal':
            contadorTokens += 1
            self.Comentario()
            self.ListaPropiedades()
        else:
            tmpControl = token.listaTokens[contadorTokens].lexema
            tmpTipo = ''
            for encontrar in controles.listaControles:
                if tmpControl == encontrar.id:
                    tmpTipo = encontrar.control
                    break
            if tmpTipo != '':
                contadorTokens += 1
                if token.listaTokens[contadorTokens].lexema == '.':
                    contadorTokens += 1
                    tmpPropiedad = token.listaTokens[contadorTokens].lexema
                    if tmpPropiedad == 'setColorLetra' or tmpPropiedad == 'setTexto' or tmpPropiedad == 'setAlineacion' or tmpPropiedad == 'setColorFondo' or tmpPropiedad == 'setMarcada' or tmpPropiedad == 'setGrupo' or tmpPropiedad == 'setAncho' or tmpPropiedad == 'setAlto':
                        contadorTokens += 1
                        if token.listaTokens[contadorTokens].lexema == '(':
                            contadorTokens += 1
                            propied = self.Valores()
                            if token.listaTokens[contadorTokens].lexema == ';':
                                contadorTokens += 1
                                propiedades.nuevaPropiedad(tmpTipo, tmpControl, tmpPropiedad, propied)
                            else:
                                self.ErrorSintactico(';')
                            self.ListaPropiedades()
                        else:
                            self.ErrorSintactico('\(')
                            while tmpControl != ';':
                                tmpControl = token.listaTokens[contadorTokens].lexema
                                contadorTokens += 1
                            self.ListaPropiedades()
                    else:
                        self.ErrorSintactico('Propiedad')
                        while tmpControl != ';':
                            tmpControl = token.listaTokens[contadorTokens].lexema
                            contadorTokens += 1
                        self.ListaPropiedades()
                else:
                    self.ErrorSintactico('.')
                    while tmpControl != ';':
                        tmpControl = token.listaTokens[contadorTokens].lexema
                        contadorTokens += 1
                    self.ListaPropiedades()
            else:
                self.ErrorSintactico('Control')
                while tmpControl != ';':
                    tmpControl = token.listaTokens[contadorTokens].lexema
                    contadorTokens += 1
                self.ListaPropiedades()

    # Valores que contendran la propiedad
    def Valores (self):
        global contadorTokens
        valor = ''
        while token.listaTokens[contadorTokens].lexema != ')':
            valor += (token.listaTokens[contadorTokens].lexema)
            contadorTokens += 1
        contadorTokens += 1
        return valor

    # Ingresa a la opción de colocacion
    def Colocacion (self):
        global contadorTokens
        if token.listaTokens[contadorTokens].tipo == 'Diagonal':
            contadorTokens += 1
            self.Comentario()
            self.Colocacion()
        else:
            self.ListaColocaciones()
            if token.listaTokens[contadorTokens].tipo == 'Guión':
                contadorTokens += 1
                if token.listaTokens[contadorTokens].tipo == 'Guión':
                    contadorTokens += 1
                    if token.listaTokens[contadorTokens].tipo == 'Cierre':
                        contadorTokens += 1
                    else:
                        self.ErrorSintactico('>')
                        contadorTokens += 1
                else:
                    self.ErrorSintactico('-')
                    contadorTokens += 1
            else:
                self.ErrorSintactico('-')
                contadorTokens += 1

    # Ingresa a la lista de colocaciones que vendran
    def ListaColocaciones (self):
        global contadorTokens
        if token.listaTokens[contadorTokens].lexema == 'Colocacion':
            contadorTokens += 1
        elif token.listaTokens[contadorTokens].tipo == 'Diagonal':
            contadorTokens += 1
            self.Comentario()
            self.ListaColocaciones()
        else:
            tmpControl = token.listaTokens[contadorTokens].lexema
            if tmpControl == 'this':
                contadorTokens += 1
                if token.listaTokens[contadorTokens].lexema == '.':
                    contadorTokens += 1
                    prop = token.listaTokens[contadorTokens].lexema
                    if prop == 'setPosicion' or prop == 'add':
                        contadorTokens += 1
                        if token.listaTokens[contadorTokens].lexema == '(':
                            contadorTokens += 1
                            valores = self.Valores()
                            if prop == 'setPosicion':
                                propiedades.nuevaPropiedad (tmpTipo, tmpControl, prop, valores)
                            else:
                                colocaciones.nuevaColocacion ('Body', tmpControl, prop, valores)
                            if token.listaTokens[contadorTokens].lexema == ';':
                                contadorTokens += 1
                            else:
                                self.ErrorSintactico('.')
                            self.ListaColocaciones()
                    else:
                        self.ErrorSintactico('.')
                        while tmpControl != ';':
                            tmpControl = token.listaTokens[contadorTokens].lexema
                            contadorTokens += 1
                        self.ListaColocaciones()
                else:
                    self.ErrorSintactico('.')
                    while tmpControl != ';':
                        tmpControl = token.listaTokens[contadorTokens].lexema
                        contadorTokens += 1
                    self.ListaColocaciones()
            else:
                tmpTipo = ''
                for encontrar in controles.listaControles:
                    if tmpControl == encontrar.id:
                        tmpTipo = encontrar.control
                        break
                if tmpTipo != '':
                    contadorTokens += 1
                    if token.listaTokens[contadorTokens].lexema == '.':
                        contadorTokens += 1
                        prop = token.listaTokens[contadorTokens].lexema
                        if prop == 'setPosicion' or prop == 'add':
                            contadorTokens += 1
                            if token.listaTokens[contadorTokens].lexema == '(':
                                contadorTokens += 1
                                valores = self.Valores()
                                if prop == 'setPosicion':
                                    propiedades.nuevaPropiedad (tmpTipo, tmpControl, prop, valores)
                                else:
                                    colocaciones.nuevaColocacion (tmpTipo, tmpControl, prop, valores)
                                if token.listaTokens[contadorTokens].lexema == ';':
                                    contadorTokens += 1
                                else:
                                    self.ErrorSintactico('.')
                                self.ListaColocaciones()
                        else:
                            self.ErrorSintactico('.')
                            while tmpControl != ';':
                                tmpControl = token.listaTokens[contadorTokens].lexema
                                contadorTokens += 1
                            self.ListaColocaciones()
                    else:
                        self.ErrorSintactico('.')
                        while tmpControl != ';':
                            tmpControl = token.listaTokens[contadorTokens].lexema
                            contadorTokens += 1
                        self.ListaColocaciones()
                else:
                    self.ErrorSintactico('ID o this')
                    while tmpControl != ';':
                        tmpControl = token.listaTokens[contadorTokens].lexema
                        contadorTokens += 1
                    self.ListaColocaciones()

    # Ingresa un error sintactico 
    def ErrorSintactico (self, esperado):
        lexema = token.listaTokens[contadorTokens].lexema
        columna = token.listaTokens[contadorTokens].columna
        fila = token.listaTokens[contadorTokens].fila
        error.NuevoError(lexema, 'Error Sintáctico', columna, fila, esperado)
