import tkinter as Tk
from estilos import grisOscuro, blancoCalido
import menu.submenu_nuevo as subNuevo


def crearMenuPrincipal(raiz):
    #Barra de menú
    barraMenu=Tk.Menu(raiz,bg=grisOscuro, fg=blancoCalido)
    raiz.config(menu=barraMenu)


    ###########submenu de Nuevo
    menuNuevo=Tk.Menu(barraMenu, tearoff=0)
    barraMenu.add_cascade(label="Nuevo", menu=menuNuevo)
    subNuevo.desplegar_nuevo(menuNuevo)
    ###########################


    ###########submenu de Abrir
    menuAbrir=Tk.Menu(barraMenu, tearoff=0)
    barraMenu.add_cascade(label="Abrir", menu=menuAbrir)
    menuAbrir.add_command(label="Abrir Planta", command="")
    menuAbrir.add_command(label="Abrir Pedido", command="")
    ###########################


    #submenu de Editar
    menuEditar=Tk.Menu(barraMenu, tearoff=0)
    barraMenu.add_cascade(label="Editar", menu=menuEditar)
    menuEditar.add_command(label="Editar Planta", command="")
    menuEditar.add_separator()
    menuEditar.add_command(label="Editar Pedido", command="") 
    menuEditar.add_command(label="Editar Modelo", command="") 
    menuEditar.add_command(label="Editar Tecnico", command="")


    #submenu de Importar
    menuImportar=Tk.Menu(barraMenu, tearoff=0)
    barraMenu.add_cascade(label="Importar", menu=menuImportar)
    menuImportar.add_command(label="Importar Modelos", command="")
    menuImportar.add_command(label="Importar Tecnicos", command="")
    menuImportar.add_command(label="Importar Vehiculos", command="")
    menuImportar.add_separator()
    menuImportar.add_command(label="Importar Pedido", command="")
    menuImportar.add_command(label="Importar Programa", command="")

    #submenu de Exportar
    menuExportar=Tk.Menu(barraMenu, tearoff=0)
    barraMenu.add_cascade(label="Exportar", menu=menuExportar)
    menuExportar.add_command(label="Exportar Modelos", command="")
    menuExportar.add_command(label="Exportar Tecnicos", command="")
    menuExportar.add_command(label="Exportar Vehiculos", command="")
    menuExportar.add_separator()
    menuExportar.add_command(label="Exportar Pedido", command="")
    menuExportar.add_command(label="Exportar Programa", command="")

    #submenu de Ayuda
    menuAyuda=Tk.Menu(barraMenu, tearoff=0)
    barraMenu.add_cascade(label="Ayuda", menu=menuAyuda)
    menuAyuda.add_command(label="Acerca de", command="")
    menuAyuda.add_command(label="Instrucciones", command="")