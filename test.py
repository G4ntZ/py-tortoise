import tkinter as tk
from tkinter import ttk
import random
import string

def generar_numeros():
    treeview.delete(*treeview.get_children())
    numeros = []
    caracteres = []
    
    while len(numeros) < 10:
        numero = random.randint(1, 100)
        if numero not in numeros:
            numeros.append(numero)
            caracter = random.choice(string.ascii_letters)
            caracteres.append(caracter)
    
    for numero, caracter in zip(numeros, caracteres):
        treeview.insert('', tk.END, values=(numero, caracter))

def imprimir_mayor_menor():
    elementos_seleccionados = treeview.selection()
    for elemento in elementos_seleccionados:
        valores = treeview.item(elemento)['values']
        numero = int(valores[0])
        caracter = valores[1]
        print("Número:", numero)
        print("Carácter:", caracter)
        print("-----------")

def restablecer_valores():
    treeview.delete(*treeview.get_children())

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Generador de números aleatorios")
ventana.geometry("600x350")

# Crear el cuadro de entrada (input box)
cuadro_entrada = ttk.Entry(ventana)
cuadro_entrada.pack(pady=10)

# Crear el botón "Generar"
boton_generar = ttk.Button(ventana, text="Generar", command=generar_numeros)
boton_generar.pack()

# Crear el treeview (tabla de dos columnas)
treeview = ttk.Treeview(ventana, columns=("Número", "Carácter"), show="headings")
treeview.heading("Número", text="Número")
treeview.heading("Carácter", text="Carácter")
treeview.pack(pady=10)

# Crear el botón "Imprimir mayor y menor"
boton_imprimir = ttk.Button(ventana, text="Imprimir mayor y menor", command=imprimir_mayor_menor)
boton_imprimir.pack()

# Crear el botón "Restablecer valores"
boton_restablecer = ttk.Button(ventana, text="Restablecer valores", command=restablecer_valores)
boton_restablecer.pack()

# Ejecutar el bucle de la aplicación
ventana.mainloop()
