from instancias import controles, propiedades, colocaciones

class Generador:
    def __init__(self):
        pass

    def ReporteHTML (self):
        file = open ('./Reporte/pagina.html', 'w', encoding='utf-8')
        file.write('<html>\n')
        file.write('<head>\n')
        file.write('\t<link href="estilos.css" rel="stylesheet" type="text/css"/> \n')
        file.write('</head>\n')
        file.write('<body>\n')
        self.ColocacionHtml(file, 'this')
        file.write('</body>\n')
        file.write('</html>')

    def ColocacionHtml (self, file, id):
        lisColocaciones = colocaciones.listaColocaciones
        lisPropiedades = propiedades.listaPropiedades
        marcado = False
        for colocacion in lisColocaciones:
            if colocacion.id == id:
                for control in controles.listaControles:
                    if control.id == colocacion.valores:
                        if control.control == 'Contenedor':
                            file.write(f'\t<div id="{control.id}">\n')
                            self.ColocacionHtml(file, colocacion.valores)
                            file.write(f'\t</div>\n')
                            file.write('\n')
                        elif control.control == 'Etiqueta':
                            texto = ''
                            for propiedad in lisPropiedades:
                                if control.id == propiedad.id and propiedad.propiedad == 'setTexto':
                                    valor = propiedad.valores
                                    valor2 = valor.replace('\"', '')
                                    texto = valor2.replace("\'", '')
                                    break
                            file.write(f'\t<label id="{control.id}">{texto}</label>\n')
                            file.write('\n')
                        elif control.control == 'Boton':
                            texto = ''
                            alineacion = 'left'
                            for propiedad in lisPropiedades:
                                if control.id == propiedad.id and propiedad.propiedad == 'setTexto':
                                    valor = propiedad.valores
                                    valor2 = valor.replace('\"', '')
                                    texto = valor2.replace("\'", '')
                                elif control.id == propiedad.id and propiedad.propiedad == 'setAlineacion':
                                    if propiedad.valores == 'Centro':
                                        alineacion = 'center'
                                    elif propiedad.valores == 'Derecho':
                                        alineacion = 'right'
                            file.write(f'\t<input type="submit" id="{control.id}" value="{texto}" style="text-align:{alineacion}"/>\n')
                            file.write('\n')
                        elif control.control == 'Check':
                            texto = ''
                            marcada = ''
                            grupo = ''
                            for propiedad in lisPropiedades:
                                if control.id == propiedad.id and propiedad.propiedad == 'setTexto':
                                    valor = propiedad.valores
                                    valor2 = valor.replace('\"', '')
                                    texto = valor2.replace("\'", '')
                                elif control.id == propiedad.id and propiedad.propiedad == 'setMarcada':
                                    if propiedad.valores == 'true':
                                        marcada = 'checked'
                                elif control.id == propiedad.id and propiedad.propiedad == 'setGrupo':
                                    grupo = propiedad.valores
                            file.write(f'\t<input type="checkbox" id="{control.id}" name="{grupo}" {marcada}"/>{texto}\n')
                            file.write('\n')
                        elif control.control == 'RadioBoton':
                            texto = ''
                            marcada = ''
                            grupo = ''
                            for propiedad in lisPropiedades:
                                if control.id == propiedad.id and propiedad.propiedad == 'setTexto':
                                    valor = propiedad.valores
                                    valor2 = valor.replace('\"', '')
                                    texto = valor2.replace("\'", '')
                                elif control.id == propiedad.id and propiedad.propiedad == 'setMarcada':
                                    if marcado == False:
                                        if propiedad.valores == 'true':
                                            marcada = 'checked'
                                            marcado = True
                                elif control.id == propiedad.id and propiedad.propiedad == 'setGrupo':
                                    grupo = propiedad.valores
                            file.write(f'\t<input type="radio" id="{control.id}" name="{grupo}" {marcada}"/>{texto}\n')
                            file.write('\n')
                        elif control.control == 'Texto':
                            texto = ''
                            alineacion = 'left'
                            for propiedad in lisPropiedades:
                                if control.id == propiedad.id and propiedad.propiedad == 'setTexto':
                                    valor = propiedad.valores
                                    valor2 = valor.replace('\"', '')
                                    texto = valor2.replace("\'", '')
                                elif control.id == propiedad.id and propiedad.propiedad == 'setAlineacion':
                                    if propiedad.valores == 'Centro':
                                        alineacion = 'center'
                                    elif propiedad.valores == 'Derecho':
                                        alineacion = 'right'
                            file.write(f'\t<input type="text" id="{control.id}" value="{texto}" style="text-align:{alineacion}"/>\n')
                            file.write('\n')
                        elif control.control == 'AreaTexto':
                            texto = ''
                            for propiedad in lisPropiedades:
                                if control.id == propiedad.id and propiedad.propiedad == 'setTexto':
                                    valor = propiedad.valores
                                    valor2 = valor.replace('\"', '')
                                    texto = valor2.replace("\'", '')
                                    break
                            file.write(f'\t<textarea id="{control.id}">\n')
                            file.write(f'\t{texto}\n')
                            file.write('\t</textarea>\n')
                            file.write('\n')
                        elif control.control == 'Clave':
                            texto = ''
                            alineacion = 'left'
                            for propiedad in lisPropiedades:
                                if control.id == propiedad.id and propiedad.propiedad == 'setTexto':
                                    valor = propiedad.valores
                                    valor2 = valor.replace('\"', '')
                                    texto = valor2.replace("\'", '')
                                elif control.id == propiedad.id and propiedad.propiedad == 'setAlineacion':
                                    if propiedad.valores == 'Centro':
                                        alineacion = 'center'
                                    elif propiedad.valores == 'Derecho':
                                        alineacion = 'right'
                            file.write(f'\t<input type="password" id="{control.id}" value="{texto}" style="text-align:{alineacion}"/>\n')
                            file.write('\n')

    def ReporteCSS (self):
        lisControles = controles.listaControles
        lisPropiedades = propiedades.listaPropiedades
        file = open ('./Reporte/estilos.css', 'w', encoding='utf-8')
        for control in lisControles:
            ancho = False
            alto = False
            posicion = False
            colorFondo = False
            colorletra = False
            file.write(f'#{control.id}'+'{\n')
            file.write('position:absolute;\n')
            if control.control == 'Contenedor' or control.control == 'Etiqueta':
                pass
            elif control.control == 'AreaTexto':
                file.write('width:150px;\n')
                file.write('height:150px;\n')
            else:
                file.write('width:100px;\n')
                file.write('height:25px;\n')
            for propiedad in lisPropiedades:
                if control.id == propiedad.id:
                    if control.control == 'Contenedor' or control.control == 'Etiqueta':
                        if propiedad.propiedad == 'setAncho':
                            if ancho == False:
                                file.write(f'width:{propiedad.valores}px;\n')
                                ancho = True
                        elif propiedad.propiedad == 'setAlto':
                            if alto == False:
                                file.write(f'height:{propiedad.valores}px;\n')
                                alto = True
                    if propiedad.propiedad == 'setPosicion':
                        if posicion == False:
                            pos = propiedad.valores.split(',')
                            file.write(f'left:{pos[0]}px;\n')
                            file.write(f'top:{pos[1]}px;\n')
                            posicion = True
                    elif propiedad.propiedad == 'setColorFondo':
                        if colorFondo == False:
                            file.write(f'background-color:rgb({propiedad.valores});\n')
                            colorFondo = True
                    elif propiedad.propiedad == 'setColorLetra':
                        if colorletra == False:
                            file.write(f'color:rgb({propiedad.valores});\n')
                            colorletra = True

            file.write('font-size:12px;\n')
            file.write('}\n')
            file.write('\n')
        file.close

