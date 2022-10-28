from instancias import controles, propiedades, colocaciones, token, error
import re

class Analizador:
    def __init__(self):
        pass

    def Analizar (self, cadena):
        # Inicializando los atributos
        columna = 1
        fila = 1
        buffer = ''
        bufferTemp = ''
        centinela = '$'
        cadena += centinela
        estado = 0
        estadoTemp = 1
        bandera = False
        
        # Analizando el texto plano
        contador = 0
        for caracter in cadena:
            contador += 1
            # Iniciando a estudiar los estados a la espera de un signo '<'
            #? --------------  Estado 0 --------------------- 
            if estado == 0:
                # Verificamos que no sea itinerada actual
                if bandera == False:
                    # Verificamos que empiece con un signo menor que
                    if caracter == '<':
                        token.NuevoToken (caracter, 'Apertura', columna, fila)
                        columna += 1
                        estado = 3
                        bandera = True
                        buffer = ''
                        bufferTemp = ''
                    elif caracter == centinela:
                        token.NuevoToken (caracter, 'EOF', columna, fila)
                        print ('Cadena analizada')
                        #self.Sintactico()
                        break
                    else:
                        if caracter == '\n':
                            columna = 1
                            fila = fila + 1
                        elif caracter == '\t':
                            columna += 4
                        elif caracter == ' ':
                            columna += 1
                        elif caracter == '\r':
                            pass
                        elif caracter == '/':
                            token.NuevoToken (caracter, 'Diagonal', columna, fila)
                            if buffer == '':
                                buffer += caracter
                                columna += 1
                            elif buffer == '/':
                                buffer = ''
                                columna += 1
                                estadoTemp = 0
                                estado = 1
                                bandera = True
                            else:
                                error.NuevoError (buffer, 'Error léxico', columna, fila, '')
                                columna += 1
                        elif caracter == '*':
                            token.NuevoToken (caracter, 'Asterisco', columna, fila)
                            if buffer == '/':
                                buffer = ''
                                columna += 1
                                estadoTemp = 0
                                estado = 2
                                bandera = True
                            else:
                                error.NuevoError (buffer, 'Error léxico', columna, fila, '')
                                columna += 1
                        else:
                            error.NuevoError (caracter, 'Error léxico', columna, fila, '')
                            columna += 1
                else:
                    bandera = False
            
            # Estado para reconocer texto en comentarios lineales
            #? --------------  Estado 1 ---------------------
            elif estado == 1:
                # Verificamos que no sea itinerada actual
                if bandera == False:
                    if caracter == '\n':
                        token.NuevoToken (buffer, 'Comentario', (columna-1), fila)
                        columna = 1
                        fila += 1
                        estado = estadoTemp
                        if estado > 1:
                            bandera = True
                        buffer = ''
                    elif caracter == '\t':
                        columna += 4
                        buffer += ' '
                    elif caracter == ' ':
                        buffer += caracter
                        columna += 1
                    elif caracter == '\r':
                        pass
                    elif caracter == centinela:
                        if buffer != '' and contador-1 == len(cadena):
                            token.NuevoToken (buffer, 'Comentario', columna, fila)
                            print ('Cadena analizada')
                        else:
                            buffer += caracter
                            columna += 1
                    else:
                        buffer += caracter
                        columna += 1
                else:
                    bandera = False
            
            # Estado para reconocer texto en comentarios con 1 o varias lineas
            #? --------------  Estado 2 ---------------------
            elif estado == 2:
                # Verificamos que no sea itinerada actual
                if bandera == False:
                    if bufferTemp == '':
                        if caracter == '\n':
                            buffer += caracter
                            columna = 1
                            fila += 1
                        elif caracter == '\t':
                            columna += 4
                            buffer += ' '
                        elif caracter == ' ':
                            buffer += caracter
                            columna += 1
                        elif caracter == '\r':
                            pass
                        elif caracter == centinela:
                            if buffer != '' and contador-1 == len(cadena):
                                token.NuevoToken (buffer, 'Comentario', columna, fila)
                                print ('Cadena analizada')
                            else:
                                buffer += caracter
                                columna += 1
                        elif caracter == '*':
                            bufferTemp = caracter
                            columna += 1
                        else:
                            buffer += caracter
                            columna += 1
                    else:
                        if caracter == '/':
                            token.NuevoToken (buffer, 'Comentario', columna, fila)
                            token.NuevoToken ('*', 'Asterisco', (columna - 1), fila)
                            token.NuevoToken (caracter, 'Diagonal', columna, fila)
                            bufferTemp = ''
                            buffer = ''
                            estado = estadoTemp
                            if estado > 1:
                                bandera = True
                            columna += 1
                        else:
                            buffer += bufferTemp
                            bufferTemp = ''
                            if caracter == '\n':
                                buffer += caracter
                                columna = 1
                                fila += 1
                            elif caracter == '\t':
                                columna += 4
                                buffer += ' '
                            elif caracter == ' ':
                                buffer += caracter
                                columna += 1
                            elif caracter == '\r':
                                pass
                            elif caracter == centinela:
                                if buffer != '' and contador-1 == len(cadena):
                                    token.NuevoToken (buffer, 'Comentario', columna, fila)
                                    print ('Cadena analizada')
                                else:
                                    buffer += caracter
                                    columna += 1
                            elif caracter == '*':
                                bufferTemp = caracter
                                columna += 1
                            else:
                                buffer += caracter
                                bufferTemp = ''
                                columna += 1
                else:
                    bandera = False

            # Estado para reconocer las partes de afuera (Controles, Propiedades, Colocación)
            #? --------------  Estado 3 ---------------------
            if estado == 3:
                # Verificamos que no sea itinerada actual
                if bandera == False:
                    # Verificamos que empiece con un signo de admiración
                    if re.search('[A-Za-z]', caracter):
                        buffer += caracter
                        if buffer == 'Controles':
                            token.NuevoToken (buffer, 'Palabra reservada', columna, fila)
                            estado = 4
                            bandera = True
                            buffer = ''
                            bufferTemp = ''
                        elif buffer == 'propiedades' or buffer == 'Colocacion':
                            token.NuevoToken (buffer, 'Palabra reservada', columna, fila)
                            estado = 5
                            bandera = True
                            buffer = ''
                            bufferTemp = ''
                        columna += 1
                    elif caracter == centinela:
                        print ('Cadena analizada')
                    else:
                        if caracter == '!':
                            token.NuevoToken (caracter, 'Admiración', columna, fila)
                            columna += 1
                        elif caracter == '-':
                            token.NuevoToken (caracter, 'Guión', columna, fila)
                            columna += 1
                        elif caracter == '>':
                            token.NuevoToken (caracter, 'Cierre', columna, fila)
                            columna += 1
                            estado = 0
                            buffer = ''
                        else:
                            if caracter == '\n':
                                columna = 1
                                fila = fila + 1
                            elif caracter == '\t':
                                columna += 4
                            elif caracter == ' ':
                                columna += 1
                            elif caracter == '\r':
                                pass
                            elif caracter == '/':
                                token.NuevoToken (caracter, 'Diagonal', columna, fila)
                                if buffer == '':
                                    buffer += caracter
                                    columna += 1
                                elif buffer == '/':
                                    buffer = ''
                                    columna += 1
                                    estadoTemp = 3
                                    estado = 1
                                else:
                                    error.NuevoError (buffer, 'Error léxico', columna, fila, '')
                                    columna += 1
                            elif caracter == '*':
                                token.NuevoToken (caracter, 'Asterisco', columna, fila)
                                if buffer == '/':
                                    buffer = ''
                                    columna += 1
                                    estadoTemp = 3
                                    estado = 2
                                else:
                                    error.NuevoError (buffer, 'Error léxico', columna, fila, '')
                                    columna += 1
                            else:
                                error.NuevoError (caracter, 'Error léxico', columna, fila, '')
                                columna += 1
                else:
                    bandera = False
            
            # Estado para reconocer el texto dentro de controles
            #? --------------  Estado 4 ---------------------
            if estado == 4:
                # Verificamos que no sea itinerada actual
                if bandera == False:
                    if re.search('[A-Za-z]', caracter) or re.search('[0-9]', caracter) or re.search('[_]', caracter):
                        buffer += caracter
                        if bufferTemp == '':
                            if buffer == 'Etiqueta':
                                token.NuevoToken (buffer, 'Control', columna, fila)
                                bufferTemp = buffer
                                buffer = ''
                            elif buffer == 'Boton':
                                token.NuevoToken (buffer, 'Control', columna, fila)
                                bufferTemp = buffer
                                buffer = ''
                            elif buffer == 'Check':
                                token.NuevoToken (buffer, 'Control', columna, fila)
                                bufferTemp = buffer
                                buffer = ''
                            elif buffer == 'RadioBoton':
                                token.NuevoToken (buffer, 'Control', columna, fila)
                                bufferTemp = buffer
                                buffer = ''
                            elif buffer == 'Texto':
                                token.NuevoToken (buffer, 'Control', columna, fila)
                                bufferTemp = buffer
                                buffer = ''
                            elif buffer == 'AreaTexto':
                                token.NuevoToken (buffer, 'Control', columna, fila)
                                bufferTemp = buffer
                                buffer = ''
                            elif buffer == 'Clave':
                                token.NuevoToken (buffer, 'Control', columna, fila)
                                bufferTemp = buffer
                                buffer = ''
                            elif buffer == 'Contenedor':
                                token.NuevoToken (buffer, 'Control', columna, fila)
                                bufferTemp = buffer
                                buffer = ''
                            elif buffer == 'Controles':
                                token.NuevoToken (buffer, 'Control', columna, fila)
                                estado = 3
                                buffer = ''
                                bufferTemp = ''
                        columna += 1
                    elif caracter == centinela:
                        print ('Cadena analizada')
                    else:
                        if caracter == ';':
                            if buffer != '':
                                token.NuevoToken (buffer, 'ID', (columna - 1), fila)
                            token.NuevoToken (caracter, 'Punto y coma', columna, fila)
                            columna += 1
                            buffer = ''
                            bufferTemp = ''
                        else:
                            if caracter == '\n':
                                if buffer != '':
                                    token.NuevoToken (buffer, 'ID', (columna - 1), fila)
                                columna = 1
                                fila = fila + 1
                            elif caracter == '\t':
                                columna += 4
                            elif caracter == ' ':
                                if buffer != '':
                                    token.NuevoToken (buffer, 'ID', columna, fila)
                                    buffer = ''
                                    pass
                                columna += 1
                            elif caracter == '\r':
                                pass
                            elif caracter == '/':
                                token.NuevoToken (caracter, 'Diagonal', columna, fila)
                                if buffer == '':
                                    buffer += caracter
                                    columna += 1
                                elif buffer == '/':
                                    buffer = ''
                                    columna += 1
                                    estadoTemp = 4
                                    estado = 1
                                else:
                                    error.NuevoError (buffer, 'Error léxico', columna, fila, '')
                                    columna += 1
                            elif caracter == '*':
                                token.NuevoToken (caracter, 'Asterisco', columna, fila)
                                if buffer == '/':
                                    buffer = ''
                                    columna += 1
                                    estadoTemp = 4
                                    estado = 2
                                else:
                                    error.NuevoError (buffer, 'Error léxico', columna, fila, '')
                                    columna += 1
                            else:
                                error.NuevoError (caracter, 'Error léxico', columna, fila, '')
                                columna += 1
                else:
                    bandera = False

            # Estado para reconocer el texto dentro de propiedades
            #? --------------  Estado 5 ---------------------
            if estado == 5:
                # Verificamos que no sea itinerada actual
                if bandera == False:
                    if re.search('[A-Za-z]', caracter) or re.search('[0-9]', caracter) or re.search('[_]', caracter):
                        buffer += caracter
                        if buffer == 'propiedades' or buffer == 'Colocacion':
                            token.NuevoToken (buffer, 'Palabra reservada', columna, fila)
                            estado = 3
                            bandera = True
                            buffer = ''
                            bufferTemp = ''
                        columna += 1
                    elif caracter == centinela:
                        print ('Cadena analizada')
                    else:
                        if caracter == '.':
                            if buffer != '':
                                token.NuevoToken (buffer, 'Control', (columna - 1), fila)
                            token.NuevoToken (caracter, 'Punto', columna, fila)
                            columna += 1
                            buffer = ''
                            bufferTemp = ''
                        elif caracter == '(':
                            if buffer != '':
                                token.NuevoToken (buffer, 'Propiedad', (columna - 1), fila)
                            token.NuevoToken (caracter, 'Parentesis Abierto', columna, fila)
                            columna += 1
                            buffer = ''
                            bufferTemp = ''
                            estadoTemp = 5
                            estado = 6
                            bandera = True
                        elif caracter == ';':
                            if buffer != '':
                                token.NuevoToken (buffer, 'Propiedad', (columna - 1), fila)
                            token.NuevoToken (caracter, 'Punto y Coma', columna, fila)
                            columna += 1
                            buffer = ''
                            bufferTemp = ''
                        else:
                            if caracter == '\n':
                                if buffer != '':
                                    token.NuevoToken (buffer, 'ID', (columna - 1), fila)
                                columna = 1
                                fila = fila + 1
                            elif caracter == '\t':
                                columna += 4
                            elif caracter == ' ':
                                if buffer != '':
                                    token.NuevoToken (buffer, 'ID', columna, fila)
                                    buffer = ''
                                    pass
                                columna += 1
                            elif caracter == '\r':
                                pass
                            elif caracter == '/':
                                token.NuevoToken (caracter, 'Diagonal', columna, fila)
                                if buffer == '':
                                    buffer += caracter
                                    columna += 1
                                elif buffer == '/':
                                    buffer = ''
                                    columna += 1
                                    estadoTemp = 5
                                    estado = 1
                                else:
                                    error.NuevoError (buffer, 'Error léxico', columna, fila, '')
                                    columna += 1
                            elif caracter == '*':
                                token.NuevoToken (caracter, 'Asterisco', columna, fila)
                                if buffer == '/':
                                    buffer = ''
                                    columna += 1
                                    estadoTemp = 5
                                    estado = 2
                                else:
                                    error.NuevoError (buffer, 'Error léxico', columna, fila, '')
                                    columna += 1
                            else:
                                error.NuevoError (caracter, 'Error léxico', columna, fila, '')
                                columna += 1
                else:
                    bandera = False
                
            # Estado para reconocer el texto dentro de valores de propiedad
            #? --------------  Estado 6 ---------------------
            if estado == 6:
                # Verificamos que no sea itinerada actual
                if bandera == False:
                    if re.search('[A-Za-z]', caracter) or re.search('[0-9]', caracter) or re.search('[_]', caracter):
                        buffer += caracter
                        columna += 1
                    elif caracter == centinela:
                        print ('Cadena analizada')
                    else:
                        if caracter == ',':
                            if buffer != '':
                                token.NuevoToken (buffer, 'Valor', (columna - 1), fila)
                            token.NuevoToken (caracter, 'Coma', columna, fila)
                            columna += 1
                            buffer = ''
                            bufferTemp = ''
                        elif caracter == ')':
                            if buffer != '':
                                token.NuevoToken (buffer, 'Valor', (columna - 1), fila)
                            token.NuevoToken (caracter, 'Parentesis Cerrado', columna, fila)
                            columna += 1
                            buffer = ''
                            bufferTemp = ''
                            estado = estadoTemp
                        elif caracter == '\"':
                            if buffer != '':
                                token.NuevoToken (buffer, 'Valor', (columna - 1), fila)
                            token.NuevoToken (caracter, 'Comilla', columna, fila)
                            columna += 1
                            buffer = ''
                            bufferTemp = ''
                        else:
                            if caracter == '\n':
                                if buffer != '':
                                    token.NuevoToken (buffer, 'ID', (columna - 1), fila)
                                columna = 1
                                fila = fila + 1
                            elif caracter == '\t':
                                columna += 4
                            elif caracter == ' ':
                                if buffer != '':
                                    token.NuevoToken (buffer, 'ID', columna, fila)
                                    buffer = ''
                                    pass
                                columna += 1
                            elif caracter == '\r':
                                pass
                            elif caracter == '/':
                                token.NuevoToken (caracter, 'Diagonal', columna, fila)
                                if buffer == '':
                                    buffer += caracter
                                    columna += 1
                                elif buffer == '/':
                                    buffer = ''
                                    columna += 1
                                    estadoTemp = 4
                                    estado = 1
                                else:
                                    error.NuevoError (buffer, 'Error léxico', columna, fila, '')
                                    columna += 1
                            elif caracter == '*':
                                token.NuevoToken (caracter, 'Asterisco', columna, fila)
                                if buffer == '/':
                                    buffer = ''
                                    columna += 1
                                    estadoTemp = 4
                                    estado = 2
                                else:
                                    error.NuevoError (buffer, 'Error léxico', columna, fila, '')
                                    columna += 1
                            else:
                                error.NuevoError (caracter, 'Error léxico', columna, fila, '')
                                columna += 1
                else:
                    bandera = False
        
