import  tkinter as tk
from    tkinter import ttk
from    estilos import *
import  menu_principal
import root_frame_vehiculos as frameVh
import root_frame_tecnicos as frameTec
import root_frame_pedidos as framePed

class ventanaRoot():

    root = tk.Tk()
    root.title("Programación de Planta")
    root.config(bg=grisAzuladoOscuro)
    root.iconbitmap("logo8.ico")
    root.geometry("800x700")
    root.state('zoomed')

    menu_principal.crearMenuPrincipal(root)

    # Creación de los frames principales
    frameVHyTEC = tk.Frame(root, bg=grisAzuladoMedio)
    frameVehiculos = tk.Frame(frameVHyTEC, bg=grisAzuladoMedio)
    frameTecnicos = tk.Frame(frameVHyTEC, bg=grisAzuladoMedio)
    framePedido = tk.Frame(root, bg=grisAzuladoMedio)

    # Posicionar los frames 
    frameVHyTEC.pack(expand=True, side="left", fill="both", padx = 3, pady= 3)
    frameVehiculos.pack(expand=True, side="top", fill="both", padx = 3, pady= 3)
    frameTecnicos.pack(expand=True, side="bottom", fill="both", padx = 3, pady= 3)
    framePedido.pack(expand=True, side="right", fill="both", padx = 3, pady= 3)


    #AÑADIR CONTENIDOS A LOS FRAME
    frameVh.ContenidoVehiculos(frameVehiculos)
    frameTec.ContenidoTecnicos(frameTecnicos)
    contenidoDelPedido=framePed.ContenidoPedidos(framePedido)    
    pedido=framePed.TablaPedido(contenidoDelPedido, framePedido, root)
    filtro=framePed.FiltrosPedido(pedido, contenidoDelPedido)


    root.mainloop()
