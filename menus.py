from instancias import token, error, controles, propiedades, colocaciones
from analizador import Analizador
from sintactico import Sintactico
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import *
import subprocess
import re
# Variables
root = Tk()
analizadorLexico = Analizador ()
analizadorSintactico = Sintactico ()

class Menus:
    #!::::::::::::::::::::::::::::::::VENTANAS::::::::::::::::::::::::::::::::::::::::::::::
    def __init__(self):
        self.ruta = ''
        # Evento al hacer doble click en la tabla
        def Click (event):
            fila, columna = cuadroTexto.index('insert').split('.')
            posFila.configure(text='Fila: {}'.format(fila))
            posColumna.configure(text='Columna: {}'.format(columna))
        # MENÚ PRINCIPAL
        root.geometry(self.EditorVentana(root, 800, 500))
        root.title('INGENIERIA USAC - Proyecto 2')
        root.iconbitmap('Archivos/books.ico')
        root.config(background='lightblue')
        root.resizable(0,0) # Para que no se pueda modificar tamaño de ventana
        # Frames
        frameTitulo = Frame (root)
        frameTitulo.config(width='800', height='70', bg='lightblue')
        frameTitulo.pack()
        frame = Frame (root)
        frame.config(width='800', height='350', bg='lightblue')
        frame.pack()
        frame2 = Frame (root)
        frame2.config(width='600', height='250', bg='lightblue')
        frame2.pack()
        # Barra de herramientas
        menu = Menu (root)
        root.config (menu=menu)
        # Sección de archivo en barra de herramientas
        barraArchivo = Menu(menu, tearoff=0)
        menu.add_cascade(label='Archivo', menu=barraArchivo)
        barraArchivo.add_command(label='Abrir', command=lambda: self.AbrirArchivo(cuadroTexto, botonGuardar))
        barraArchivo.add_command(label='Nuevo', command=lambda: self.Nuevo(cuadroTexto, botonGuardar, botonTokens, botonErrores))
        barraArchivo.add_command(label='Guardar como', command=lambda: self.GuardarComo(cuadroTexto, botonGuardar))
        barraArchivo.add_separator()
        barraArchivo.add_command(label='Salir', command=lambda: self.EliminarVentana(root))
        # Sección de ayuda en barra de herramientas
        barraAyuda = Menu(menu, tearoff=0)
        menu.add_cascade(label='Ayuda', menu=barraAyuda)
        barraAyuda.add_command(label='Manual de usuario', command=lambda: self.AbrirManual('Manuales\Manual de Usuario.pdf'))
        barraAyuda.add_command(label='Manual Técnico', command=lambda: self.AbrirManual('Manuales\Manual Técnico.pdf'))
        barraAyuda.add_command(label='Temas de ayuda', command=lambda: self.Informacion())
        # Label de información
        tituloSuperior = Label (frameTitulo, text='Generador de HTML')
        tituloSuperior.config(background='lightblue', font=('Arial', 16, 'bold'), justify='center')
        tituloSuperior.grid(column=0, row=0, padx=0, pady=10, columnspan=1)
        tituloSuperior.place()
        # Cuadro de texto
        cuadroTexto = Text (frame, width='70', height='10')
        cuadroTexto.bind('<Button-1>', Click)
        cuadroTexto.grid(column=0, row=1, ipadx=10, ipady=45, padx=10, pady=20)
        # Labels Superiores
        posFila = Label (frame, text='Fila: x')# {cursos.CreditosAprobados()}')
        posFila.config(background='lightblue', font=('Arial', 10, 'italic'), justify='left')
        posFila.place(x='460', y='275')
        # Labels Superiores
        posColumna = Label (frame, text='Columna: y')# {cursos.CreditosAprobados()}')
        posColumna.config(background='lightblue', font=('Arial', 10, 'italic'), justify='left')
        posColumna.place(x='520', y='275')
        # Botones
        botonGuardar = ttk.Button (frame2, text='Guardar', command=lambda: self.Guardar(cuadroTexto))
        botonGuardar.grid(column=1, row=1, ipadx=55, ipady=5, padx=10, pady=10)
        botonGuardar['state'] = 'disabled'
        botonGuardarComo = ttk.Button (frame2, text='Guardar Como', command=lambda: self.GuardarComo(cuadroTexto, botonGuardar))
        botonGuardarComo.grid(column=2, row=1, ipadx=55, ipady=5, padx=10, pady=10)
        botonAnalizar = ttk.Button (frame2, text='Analizar texto', command=lambda: self.AnalizarTexto(cuadroTexto, botonTokens, botonErrores))
        botonAnalizar.grid(column=3, row=1, ipadx=55, ipady=5, padx=10, pady=10)
        botonTokens = ttk.Button (frame2, text='Listado Tokens', command=lambda: self.VentanaTokens())
        botonTokens.grid(column=1, row=2, ipadx=50, ipady=5, padx=10, pady=10)
        botonTokens['state'] = 'disabled'
        botonErrores = ttk.Button (frame2, text='Listado Errores', command=lambda: self.VentanaErrores())
        botonErrores.grid(column=2, row=2, ipadx=60, ipady=5, padx=10, pady=10)
        botonErrores['state'] = 'disabled'
        botonSalir = ttk.Button (frame2, text='Salir', command=lambda: self.EliminarVentana(root))
        botonSalir.grid(column=3, row=2, ipadx=60, ipady=5, padx=10, pady=10)
        # Para que la ventana principal se inicie automáticamente
        root.mainloop()
    
    # Crear Ventana para la tabla de errores
    def VentanaErrores (self):
        # Ocultar ventana principal
        self.OcultarVentana(root)
        # Ventana de Errores
        ventanaErrores = Toplevel ()
        ventanaErrores.geometry(self.EditorVentana(root, 800, 500))
        ventanaErrores.title('INGENIERIA USAC - Tabla de errores')
        ventanaErrores.iconbitmap('archivos/books.ico')
        ventanaErrores.config(background='lightblue')
        ventanaErrores.resizable(0,0) # Para que no se pueda modificar tamaño de ventana
        ventanaErrores.protocol('WM_DELETE_WINDOW', root.quit)
        # Frame
        frameTitulo = Frame (ventanaErrores)
        frameTitulo.config(width='800', height='70', bg='lightblue')
        frameTitulo.pack()
        frame = Frame (ventanaErrores)
        frame.config(width='600', height='200', bg='lightblue')
        frame.pack()
        frame2 = Frame (ventanaErrores)
        frame2.config(width='600', height='250', bg='lightblue')
        frame2.pack()
        # Label de información
        tituloSuperior = Label (frameTitulo, text=' TABLA DE ERRORES')
        tituloSuperior.config(background='lightblue', font=('Arial', 16, 'bold'), justify='center')
        tituloSuperior.grid(column=0, row=0, padx=0, pady=10, columnspan=1)
        tituloSuperior.place()
        # Tabla
        tabla = ttk.Treeview(frame, columns=('#1', '#2', '#3', '#4', '#5'), height='8')
        tabla.grid(row='10', column='0', columnspan='2', pady=100)
        tabla.column('#0', width=50)
        tabla.column('#1', width=140, anchor=CENTER)
        tabla.column('#2', width=105, anchor=CENTER)
        tabla.column('#3', width=80, anchor=CENTER)
        tabla.column('#4', width=70, anchor=CENTER)
        tabla.column('#5', width=170, anchor=CENTER)
        # Títulos de la tabla
        tabla.heading('#0', text='NO.', anchor=CENTER)
        tabla.heading('#1', text='LEXEMA', anchor=CENTER)
        tabla.heading('#2', text='TIPO', anchor=CENTER)
        tabla.heading('#3', text='COLUMNA', anchor=CENTER)
        tabla.heading('#4', text='FILA', anchor=CENTER)
        tabla.heading('#5', text='ESPERADO', anchor=CENTER)
        # Carga de datos para la tabla
        self.InsertarErrores(tabla)
        # Botones
        botonRegresar = ttk.Button (frame2, text='Regresar', command=lambda: self.MostrarEliminarVentana(root, ventanaErrores))
        botonRegresar.grid(column=3, row=2, ipadx=60, ipady=5, padx=10, pady=10)

    # Crear Ventana para la tabla de tokens
    def VentanaTokens (self):
        # Ocultar ventana principal
        self.OcultarVentana(root)
        # Ventana de Tokens
        ventanaTokens = Toplevel ()
        ventanaTokens.geometry(self.EditorVentana(root, 800, 500))
        ventanaTokens.title('INGENIERIA USAC - Tabla de tokens')
        ventanaTokens.iconbitmap('archivos/books.ico')
        ventanaTokens.config(background='lightblue')
        ventanaTokens.resizable(0,0) # Para que no se pueda modificar tamaño de ventana
        ventanaTokens.protocol('WM_DELETE_WINDOW', root.quit)
        # Frame
        frameTitulo = Frame (ventanaTokens)
        frameTitulo.config(width='800', height='70', bg='lightblue')
        frameTitulo.pack()
        frame = Frame (ventanaTokens)
        frame.config(width='600', height='200', bg='lightblue')
        frame.pack()
        frame2 = Frame (ventanaTokens)
        frame2.config(width='600', height='250', bg='lightblue')
        frame2.pack()
        # Label de información
        tituloSuperior = Label (frameTitulo, text=' TABLA DE TOKENS')
        tituloSuperior.config(background='lightblue', font=('Arial', 16, 'bold'), justify='center')
        tituloSuperior.grid(column=0, row=0, padx=0, pady=10, columnspan=1)
        tituloSuperior.place()
        # Tabla
        tabla = ttk.Treeview(frame, columns=('#1', '#2', '#3', '#4'), height='8')
        tabla.grid(row='10', column='0', columnspan='2', pady=100)
        tabla.column('#0', width=50)
        tabla.column('#1', width=240, anchor=CENTER)
        tabla.column('#2', width=105, anchor=CENTER)
        tabla.column('#3', width=80, anchor=CENTER)
        tabla.column('#4', width=70, anchor=CENTER)
        # Títulos de la tabla
        tabla.heading('#0', text='NO.', anchor=CENTER)
        tabla.heading('#1', text='LEXEMA', anchor=CENTER)
        tabla.heading('#2', text='TIPO', anchor=CENTER)
        tabla.heading('#3', text='COLUMNA', anchor=CENTER)
        tabla.heading('#4', text='FILA', anchor=CENTER)
        # Carga de datos para la tabla
        self.InsertarTokens(tabla)
        # Botones
        botonRegresar = ttk.Button (frame2, text='Regresar', command=lambda: self.MostrarEliminarVentana(root, ventanaTokens))
        botonRegresar.grid(column=3, row=2, ipadx=60, ipady=5, padx=10, pady=10)

    #!:::::::::::::::::::::::::::MÉTODOS DE VENTANAS::::::::::::::::::::::::::::::::::::::::
    # Función para definir el tamaño de la ventana y centrarlo en la pantalla
    def EditorVentana (self, ventana, ancho, alto):
        x = ventana.winfo_screenwidth() // 2 - ancho // 2
        y = ventana.winfo_screenheight() // 2 - alto // 2
        posicion = f'{str(ancho)}x{str(alto)}+{str(x)}+{str(y)}'
        return posicion

    # Método para eliminar la pantalla actual y mostrar en pantalla la ventana oculta
    def MostrarEliminarVentana (self, ventanaMostrar, ventanaEliminar):
        ventanaEliminar.destroy()
        ventanaMostrar.deiconify()

    # Método para ocultar la ventana actual
    def OcultarVentana (self, ventana):
        ventana.withdraw()

    # Método para eliminar la ventana actual
    def EliminarVentana (self, ventana):
        ventana.destroy()

    #!::::::::::::::::::::::::::::MÉTODOS GENERALES:::::::::::::::::::::::::::::::::::::::::
    # Método para abrir y cargar archivos
    def AbrirArchivo (self, texto, boton):
        if self.ruta != '':
            respuesta = askyesno('INGENIERIA USAC - Abrir archivo', '¿Deseas guardar el texto actual antes de abrir otro archivo?')
            if respuesta == True:
                self.Guardar(texto)
        else:
            cuadroTexto = texto.get(1.0, 'end-1c')
            if cuadroTexto != '':
                respuesta = askyesno('INGENIERIA USAC - Abrir archivo', '¿Deseas guardar el texto actual antes de abrir otro archivo?')
                if respuesta == True:
                    self.GuardarComo(texto, boton)
        ruta = filedialog.askopenfilename(title='INGENIERIA USAC - Abrir', filetypes=(('Archivos GPW (*.gpw)','*.gpw'),))
        if (ruta != ''):
            cuadroTexto = texto.get(1.0, 'end-1c')
            archivo = open (ruta, 'r', 1, 'utf-8')
            textoPlano = archivo.read ()
            archivo.close ()
            texto.delete(1.0, 'end-1c')
            texto.insert(1.0, textoPlano)
            boton['state'] = 'normal'
            self.ruta = ruta
            showinfo('INGENIERIA USAC - Carga de cursos', 'Los datos se han cargado correctamente')
    
    # Abre un manual en formato pdf
    def AbrirManual (self, ruta):
        rutaAbierta = ruta
        subprocess.Popen([rutaAbierta], shell=True)

    # Analiza el texto en el programa
    def AnalizarTexto (self, texto, botonToken, botonError):
        # Reiniciando los datos
        token.listaTokens = []
        error.listaErrores = []
        controles.listaControles = []
        propiedades.listaPropiedades = []
        colocaciones.listaColocaciones = []
        documento = texto.get(1.0, 'end-1c')
        analizadorLexico.Analizar(documento)
        analizadorSintactico.Sintactico()
        botonToken['state'] = 'normal'
        botonError['state'] = 'normal'
        showinfo('INGENIERIA USAC - Analizador', 'El texto se ha analizado correctamente')
        subprocess.Popen('Reporte\pagina.html', shell=True)

    # Guarda el texto que se encuentra en el cuadro de texto
    def Nuevo (self, texto, botonG, botonT, botonE):
        cuadroTexto = texto.get(1.0, 'end-1c')
        if self.ruta == '':
            if cuadroTexto != '':
                respuesta = askyesnocancel('INGENIERIA USAC - Nuevo archivo', '¿Deseas guardar el texto actual antes de abrir otro archivo?')
                if respuesta == True:
                    self.GuardarComo(texto, botonG)
                    texto.delete(1.0, 'end-1c')
                    botonG['state'] = 'disabled'
                elif respuesta == False:
                    texto.delete(1.0, 'end-1c')
        else:
            respuesta = askyesnocancel('INGENIERIA USAC - Nuevo archivo', '¿Deseas guardar el texto actual antes de iniciar otro archivo?')
            if respuesta == True:
                self.Guardar(texto)
                self.ruta = ''
                botonG['state'] = 'disabled'
                botonT['state'] = 'disabled'
                botonE['state'] = 'disabled'
                texto.delete(1.0, 'end-1c')
            elif respuesta == False:
                self.ruta = ''
                botonG['state'] = 'disabled'
                botonT['state'] = 'disabled'
                botonE['state'] = 'disabled'
                texto.delete(1.0, 'end-1c')

    # Guarda el texto que se encuentra en el cuadro de texto
    def Guardar (self, texto):
        cuadroTexto = texto.get(1.0, 'end-1c')
        if cuadroTexto != '':
            documento = open (self.ruta, 'w', encoding='utf-8')
            documento.write(cuadroTexto)
            documento.close()
            showinfo('INGENIERIA USAC - Guardar', 'El texto se ha guardado correctamente')
        else:
            showerror('INGENIERIA USAC - Guardar', 'No existe nada en el cuadro de texto para guardar')

    # Guarda con un nuevo nombre el texto que se encuentra en el cuadro de texto
    def GuardarComo (self, texto, boton):
        cuadroTexto = texto.get(1.0, 'end-1c')
        if cuadroTexto != '':
            nombreArchivo = filedialog.asksaveasfilename(title='INGENIERIA USAC - Guardar como..', filetypes= (('GPW files', '*.gpw'),))#('Todos los archivos','*.*')))
            if nombreArchivo != '':
                busqueda = re.findall('\.gpw', nombreArchivo)
                if busqueda != []:
                    documento = open (nombreArchivo, 'w', encoding='utf-8')
                    self.ruta = nombreArchivo
                else:
                    documento = open (f'{nombreArchivo}.gpw', 'w', encoding='utf-8')
                    self.ruta = f'{nombreArchivo}.gpw'
                documento.write(cuadroTexto)
                documento.close()
                boton['state'] = 'normal'
                showinfo('INGENIERIA USAC - Guardar como', 'El texto se ha guardado correctamente')
        else:
            showerror('INGENIERIA USAC - Guardar como', 'No existe nada en el cuadro de texto para guardar')

    # Método para agregar datos de error en la tabla
    def InsertarErrores (self, tabla):
        contador = 1
        for dato in error.listaErrores:
            tabla.insert('', END, text=contador, values=(dato.lexema, dato.tipo, dato.columna, dato.fila, dato.esperado))
            contador += 1
    
    # Método para agregar datos de tokens en la tabla
    def InsertarTokens (self, tabla):
        contador = 1
        for dato in token.listaTokens:
            tabla.insert('', END, text=contador, values=(dato.lexema, dato.tipo, dato.columna, dato.fila))
            contador += 1

    # Muestra la información del estudiante que realizó el proyecto.
    def Informacion (self):
        showinfo ('INGENIERIA USAC - Estudiante', 'Fredy Samuel Quijada Ceballos\nCarne: 202004812\nGit: fsquijada')
