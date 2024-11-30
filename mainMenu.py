import tkinter as tk
from estilos import grisOscuro, blancoCalido
import mainEventos

def crearMenuPrincipal(raiz):
    #Barra de menú
    barraMenu = tk.Menu(raiz, bg=grisOscuro, fg=blancoCalido)
    raiz.config(menu=barraMenu)


    ###################### submenu de Nuevo######################################
    menuNuevo=tk.Menu(barraMenu, tearoff=0)
    barraMenu.add_cascade(label="Nuevo", menu=menuNuevo)
    desplegar_nuevo(subMenu = menuNuevo, root=raiz)
    #############################################################################

    ########################## submenu de Abrir #################################
    menuAbrir=tk.Menu(barraMenu, tearoff=0)
    barraMenu.add_cascade(label="Abrir", menu=menuAbrir)
    desplegar_abrir(subMenu = menuAbrir, root=raiz)
    #############################################################################

def desplegar_nuevo(subMenu, root):
    subMenu.add_command(label = "Nueva Planta"   , command = vent_nueva_planta)
    subMenu.add_separator()
    subMenu.add_command(label="Salir", command= root.destroy)

def desplegar_abrir(subMenu, root):
    subMenu.add_command(label = "Abrir Planta", command = vent_abrir_planta)


def vent_nueva_planta():
    mainEventos.step_crearNuevaPlanta()
    
def vent_abrir_planta():
    mainEventos.abrir_planta()