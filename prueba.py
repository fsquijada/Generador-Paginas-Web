import tkinter as tk
import tkinter.ttk as ttk

def actualizar_posicion():
    cursor.configure(text='cursor: {}'.format(texto.index("insert")))
    puntero.configure(text='puntero: {}'.format(texto.index('current')))
    final.configure(text='final: {}'.format(texto.index("end")))

v_principal = tk.Tk()

texto = tk.Text(v_principal)
texto.pack(fill=tk.Y)

cursor = tk.Label(v_principal, text='cursor: {}'.format(texto.index("insert")))
cursor.pack()
puntero = tk.Label(v_principal, text='puntero: {}'.format(texto.index("current")))
puntero.pack()
final = tk.Label(v_principal, text='final: {}'.format(texto.index("end")))
final.pack()

ttk.Button(v_principal, text='Actualizar posición', command=actualizar_posicion).pack()

v_principal.mainloop()