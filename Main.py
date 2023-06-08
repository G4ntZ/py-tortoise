import configparser
import sys
from Svn import Svn
import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle
import subprocess
import json
import re 

config = configparser.ConfigParser()
config.read('pytortoise.properties')
usersvn = config['svn']['user']
passsvn = config['svn']['pass']
rutavscode = config['vscode']['ruta']

svn = Svn(usersvn, passsvn)
#svn.log_path(sys.argv[1])

  
def generar_numeros():
    treeview.delete(*treeview.get_children())
    versiones = []
    acciones = []
    autores = []
    fechas = []
    mensajes = []
    if(cuadro_entrada.get() != ''):
        logs = json.loads(svn.log_path(cuadro_entrada.get()))
        for key in logs:
            versiones.append(key['number'])
            acciones.append(key['action'])
            autores.append(key['author'])
            fechas.append(key['date'])
            mensajes.append(key['message'])

    for version, accion, autor, fecha, mensaje in zip(versiones, acciones, autores, fechas, mensajes):
        treeview.insert('', tk.END, values=(version, accion, autor, fecha, mensaje))
def validate_len(elem,val):
    i=0
    for x in elem:
        i = i + 1
    if(i == val):
        return True
    else:
        return False
    
def save_file(path, version):
    plsql = svn.get_version(path, version)['body']
    #plsql = re.sub('^\n', '\t', plsql_mod)
    #print(plsql)
    text_file = open(f"compares/{version}.sql", "w", encoding="utf-8")
    text_file.write(plsql)
    text_file.close()


def comparar():
    elementos_seleccionados = treeview.selection()
    if(elementos_seleccionados != ()):
        if(validate_len(elementos_seleccionados,2)):
            versiones = []
            versiones.append(rutavscode)
            versiones.append("--diff")
            for elemento in reversed(elementos_seleccionados):
                valores = treeview.item(elemento)['values']
                numero = int(valores[0])
                versiones.append("compares/"+str(numero)+ ".sql")
                save_file(cuadro_entrada.get(),numero)
                #print("Número:", numero)
            #print(str(versiones[0]))
            #print(str(versiones[1]))
            #c1 = "compares/" + str(versiones[0]) + ".sql"
            #c2 = "compares/" + str(versiones[1]) + ".sql"
            subprocess.call(versiones)
            
        else:
            messagebox.showinfo("Alerta", "Debe seleccionar solo dos versiones a comparar")

def abrir():
    elementos_seleccionados = treeview.selection()
    if(elementos_seleccionados != ()):
        if(validate_len(elementos_seleccionados,1)):
            versiones = []
            versiones.append(rutavscode)
            for elemento in elementos_seleccionados:
                valores = treeview.item(elemento)['values']
                numero = int(valores[0])
                print(str(numero))
                versiones.append("compares/"+str(numero)+ ".sql")
                save_file(cuadro_entrada.get().replace(' ','%20'),numero)
            subprocess.call(versiones)
        else:
            messagebox.showinfo("Alerta", "Debe seleccionar solo una version para abrir")

def restablecer_valores():
    treeview.delete(*treeview.get_children())
    cuadro_entrada.delete(0, tk.END)

# Función para comenzar el arrastre de la ventana
def iniciar_arrastre(event):
    global ventana_x, ventana_y
    ventana_x = event.x
    ventana_y = event.y

# Función para arrastrar la ventana
def arrastrar_ventana(event):
    x = ventana.winfo_x() - ventana_x + event.x
    y = ventana.winfo_y() - ventana_y + event.y
    ventana.geometry("+{}+{}".format(x, y))

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Compare SVN PL/SQL by G4ntZ")
#ventana.overrideredirect(True)
ventana.geometry("1200x430")
ventana.iconbitmap("icon/icon.ico")

#ventana.overrideredirect(True)

# Crear el frame para el título personalizado
#frame_titulo = tk.Frame(ventana, bg="gray", relief=tk.RAISED, bd=0)
#frame_titulo.pack(fill=tk.X)

# Crear el botón para cerrar la aplicación
#boton_cerrar = tk.Button(frame_titulo, text="X", bg="gray", fg="white", font=("Helvetica", 10, "bold"), relief=tk.FLAT, command=ventana.quit)
#boton_cerrar.pack(side=tk.RIGHT, padx=5)

# Crear el label del título personalizado
#label_titulo = tk.Label(frame_titulo, text="Compare SVN PL/SQL by G4ntZ", bg="gray", fg="white", font=("Helvetica", 14, "bold"))
#label_titulo.pack(side=tk.LEFT, padx=10, pady=5)

# Asociar los eventos de arrastre a la ventana y al frame_titulo
#frame_titulo.bind("<ButtonPress-1>", iniciar_arrastre)
#frame_titulo.bind("<B1-Motion>", arrastrar_ventana)

style = ThemedStyle(ventana)
style.set_theme("black")  # Puedes elegir otros temas de ttkthemes si lo deseas

#style.configure("TLabel", background=style.lookup("TFrame", "background"))
#style.configure("TLabel.Title", font=("Helvetica", 14, "bold"))
#style.set_theme("elegance")

ancho_cuadro = int(ventana.winfo_width() * 0.8)

# Crear el cuadro de entrada (input box)
cuadro_entrada = ttk.Entry(ventana, width=1000)
cuadro_entrada.place(relx=0.5, rely=0.1, relwidth=0.8, anchor=tk.CENTER)
cuadro_entrada.pack(pady=10)

# Crear el botón "Generar"
boton_generar = ttk.Button(ventana, text="Log", command=generar_numeros)
boton_generar.pack()

# Crear el treeview (tabla de dos columnas)
treeview = ttk.Treeview(ventana, columns=("Version", "Accion", "Autor", "Fecha", "Mensaje"), show="headings")
treeview.heading("Version", text="Version")
treeview.heading("Accion", text="Accion")
treeview.heading("Autor", text="Autor")
treeview.heading("Fecha", text="Fecha")
treeview.heading("Mensaje", text="Mensaje")
treeview.pack(pady=10)

# Crear el botón "Imprimir mayor y menor"
boton_imprimir = ttk.Button(ventana, text="Comparar", command=comparar)
boton_imprimir.pack()

boton_abrir = ttk.Button(ventana, text="Abrir", command=abrir)
boton_abrir.pack()

# Crear el botón "Restablecer valores"
boton_restablecer = ttk.Button(ventana, text="Restablecer valores", command=restablecer_valores)
boton_restablecer.pack()

# Ejecutar el bucle de la aplicación
ventana.mainloop()