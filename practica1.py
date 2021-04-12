import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import simpledialog, messagebox
import matplotlib.animation as animation

fig = plt.figure(figsize=(5,5))
ax1 = fig.add_subplot()
root = tk.Tk()
root.title("Práctica 1")

def definirMapa():
    f = open("doc.txt","r")
    matriz = f.read()
    lista = []
    col = 0
    row = 0
    for car in matriz:
        if car != ",":
            col += 1
        if car == "\n":
            break
    col = col-1
    for car in matriz:
        if car == "\n":
            row +=1
        if car != "," and car != "\n":
            lista.append(int(car))
    mapa = np.array(lista).reshape(row,col)
    ax1.xaxis.set_ticks_position('top')
    ax1.set_xticks(np.arange(1,col+1))
    ax1.set_yticks(np.arange(1,row+1))
    ax1.imshow(mapa,cmap = ListedColormap(['gray','w']), extent = [1,col+1,row+1,1])
    return mapa

def animate(i):
    definirMapa()
    
ax1.grid(color='k')

def muestraMapa():
    
    root_panel = tk.Frame()
    root_panel.pack()

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()

    canvas.get_tk_widget().pack()
    
    ani = animation.FuncAnimation(fig, animate, interval=1000) 

    btnMC = tk.Button(root_panel,
                     text = "Mostrar valor de Casilla",
                     command= lambda: mostrarCasilla(definirMapa()))    
    btnMC.pack(padx=5, pady=10, side=tk.LEFT)
    
    btnCC = tk.Button(root_panel,
                     text = "Cambiar valor de Casilla",
                     command= lambda: cambiarCasilla(definirMapa()))       
    btnCC.pack(padx=5, pady=10, side=tk.LEFT)

    
    root.mainloop() 

def mostrarCasilla(mapa):
    valorCol = simpledialog.askinteger("Columna","Ingrese el valor de la columna deseada", parent=root) 
    valorFila = simpledialog.askinteger("Fila","Ingrese el valor de la fila deseada",parent=root) 
    if (valorCol and valorFila) is not None:
        if mapa[valorFila-1,valorCol-1] == 0:
            valor = "Valor de casilla: Muro"
        elif mapa[valorFila-1,valorCol-1] == 1:
            valor = "Valor de casilla: Pasillo"
        else: 
            valor = "Valor de casilla: No definido"
        messagebox.showinfo("Valor",valor)    
    else:
        messagebox.showerror("Error","Ingrese datos validos")

def cambiarCasilla(mapa):
    valorCol = simpledialog.askinteger("Columna","Ingrese el valor de la columna deseada", parent=root) 
    valorFila = simpledialog.askinteger("Fila","Ingrese el valor de la fila deseada",parent=root) 
    nuevoValor = simpledialog.askinteger("Nuevo valor","Ingrese el nuevo valor",parent=root) 
    if (valorCol and valorFila) is not None:
        mapa[valorFila-1,valorCol-1] = nuevoValor
    else:
        messagebox.showerror("Error","Ingrese datos validos")
    
    f = open("doc.txt","w")
    for fila in mapa:
        for i in range(len(fila)):
            f.write(str(fila[i]))
        f.write("\n")    
    f.close
    #muestraMapa()

muestraMapa()