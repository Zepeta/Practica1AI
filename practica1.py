import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import simpledialog, messagebox
import matplotlib.animation as animation
import sys

fig = plt.figure(figsize=(5.5,5.5))
ax1 = fig.add_subplot()
root = tk.Tk()
root.title("Práctica 1")

columna = 0
fila = 0
mapeo = []
bandera_ep = False

doc = open("doc.txt","r").read()
filas = doc.split("\n")
row = len(filas)
col = len(filas[0].split(","))
lista = []
for fila in filas:
    aux = fila.split(",")
    for car in aux:
        lista.append(int(car))
mapa = np.array(lista).reshape(row,col)
print(mapa)
ax1.xaxis.set_ticks_position('top')
ax1.set_xticks(np.arange(1,col+1))
ax1.set_yticks(np.arange(1,row+1))
ax1.grid(color='k')

def definirMapa():
    global mapeo
    global bandera_ep
    global ax1
    if not bandera_ep:
        mapeo = np.full((row,col),2)
        im = ax1.imshow(mapeo,cmap = ListedColormap(['k']), extent = [1,col+1,row+1,1])#'gray','w'
    else:
        im = ax1.imshow(mapeo,cmap = ListedColormap(['gray',"w","k"]), extent = [1,col+1,row+1,1])#'gray','w' }
    im = None
    return mapa

def animate(i):
    mapa = definirMapa()
    mapa = None

def muestraMapa():
    
    root_panel = tk.Frame()
    root_panel.pack()

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

    btn_mc = tk.Button(root, #root_panel
                     text = "Mostrar valor de Casilla",
                     command= lambda: mostrarCasilla(definirMapa()))    
    btn_mc.pack(padx=5, pady=10, side=tk.LEFT)

    btn_cc = tk.Button(root, #root_panel
                     text = "Cambiar valor de Casilla",
                     command= lambda: cambiarCasilla(definirMapa()))       
    btn_cc.pack(padx=5, pady=10, side=tk.LEFT)
    
    root.bind("<Key>",eventoClick)
    
    intervalo = 1000
    ani = animation.FuncAnimation(fig, animate, interval=intervalo,cache_frame_data=False,save_count=0) 

    global columna, fila
    columna, fila = establecerPosiciones()

    root.mainloop() 
        

def eventoClick(event):
    global columna
    global fila
    global ax1
    mapa = definirMapa()    
    
    posicion_inicial = mapa[fila,columna]
    posicion_actual = posicion_inicial
    siguiente_posicion = []
    if event.keysym == "Up":
        fila -= 1
        siguiente_posicion = mapa[fila,columna]
        if  siguiente_posicion == 1:
            posicion_actual = siguiente_posicion
            plt.text(float(columna+1)+0.5,float(fila+1)+0.7,"V")
        else: 
            fila +=1
    elif event.keysym == "Down":
        fila +=1
        siguiente_posicion = mapa[fila,columna]
        if  siguiente_posicion == 1:
            posicion_actual = siguiente_posicion
            plt.text(float(columna+1)+0.5,float(fila+1)+0.7,"V")
        else:
            fila -= 1
    elif event.keysym == "Right":
        columna +=1
        siguiente_posicion = mapa[fila,columna]
        if  siguiente_posicion == 1:
            posicion_actual = siguiente_posicion
            plt.text(float(columna+1)+0.5,float(fila+1)+0.7,"V")
        else:
            columna -= 1
    elif event.keysym == "Left":
        columna -=1
        siguiente_posicion = mapa[fila,columna]
        if  siguiente_posicion == 1:
            posicion_actual = siguiente_posicion
            plt.text(float(columna+1)+0.5,float(fila+1)+0.7,"V")
        else:
            columna += 1
    elif event.keysym == "Escape":
        root.destroy()
        sys.exit()
    print(columna+1,fila+1)
    mapear(fila+1, columna+1)
    mapa = None

def mapear(fila, columna):
    mapa = definirMapa()
    fila = fila-1
    columna = columna-1
    filInic = fila
    colInic = fila
    posicion = mapa[fila,columna] 
    if posicion == 1:
        mapeo[fila,columna] = mapa[fila,columna] #actual
        if fila+1<mapa.shape[0]:
            mapeo[fila+1,columna] = mapa[fila+1,columna] #abajo
        if fila-1 >=0:
            mapeo[fila-1,columna] = mapa[fila-1,columna] #arriba
        if columna+1 < mapa.shape[1]:
            mapeo[fila,columna+1] = mapa[fila,columna+1] #derecha
        if columna-1 >= 0: 
            mapeo[fila,columna-1] = mapa[fila,columna-1] #izquierda
    elif mapa[filInic,colInic] == 0:
        messagebox.showerror("Error","Ingrese datos validos")
        establecerPosiciones()

def establecerPosiciones():
    mapa = definirMapa()
    global mapeo
    global bandera_ep
    valorColInic = simpledialog.askinteger("Columna","Ingrese el valor de la columna inicial", parent=root) 
    valorFilaInic = simpledialog.askinteger("Fila","Ingrese el valor de la fila inicial",parent=root) 
    valorColFin = simpledialog.askinteger("Columna","Ingrese el valor de la columna final", parent=root) 
    valorFilaFin = simpledialog.askinteger("Fila","Ingrese el valor de la fila final",parent=root)  
    plt.text(float(valorColInic)+.2,float(valorFilaInic)+.7,"I")
    plt.text(float(valorColInic)+.3,float(valorFilaInic)+.7,"V")
    
    plt.text(float(valorColFin)+.3,float(valorFilaFin)+.7,"F")
    mapear(valorFilaInic,valorColInic)
    bandera_ep = True
    return valorColInic-1, valorFilaInic-1

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

muestraMapa()