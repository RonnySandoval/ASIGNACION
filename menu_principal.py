import tkinter as tk
from estilos import grisOscuro, blancoCalido
import menu.submenu_nuevo  as subNuevo
import menu.submenu_editar as subEditar


def crearMenuPrincipal(raiz):
    #Barra de menú
    barraMenu = tk.Menu(raiz, bg=grisOscuro, fg=blancoCalido)
    raiz.config(menu=barraMenu)


    ###################### submenu de Nuevo######################################
    menuNuevo=tk.Menu(barraMenu, tearoff=0)
    barraMenu.add_cascade(label="Nuevo", menu=menuNuevo)
    subNuevo.desplegar_nuevo(subMenu = menuNuevo, root=raiz)
    #############################################################################



    ########################## submenu de Abrir #################################
    menuAbrir=tk.Menu(barraMenu, tearoff=0)
    barraMenu.add_cascade(label="Abrir", menu=menuAbrir)
    menuAbrir.add_command(label="Abrir Planta", command="")
    menuAbrir.add_command(label="Abrir Pedido", command="")
    #############################################################################



    ############################## submenu de Editar ###########################
    menuEditar=tk.Menu(barraMenu, tearoff=0)
    barraMenu.add_cascade(label="Editar", menu=menuEditar)
    subEditar.desplegar_editar(subMenu = menuEditar, root=raiz)
    ##########################################################################



    ########################### submenu de Importar ###########################
    menuImportar=tk.Menu(barraMenu, tearoff=0)
    barraMenu.add_cascade(label="Importar", menu=menuImportar)
    menuImportar.add_command(label="Importar Modelos", command="")
    menuImportar.add_command(label="Importar Tecnicos", command="")
    menuImportar.add_command(label="Importar Vehiculos", command="")
    menuImportar.add_command(label="Importar Procesos", command="")
    menuImportar.add_separator()
    menuImportar.add_command(label="Importar Pedido", command="")
    menuImportar.add_command(label="Importar Programa", command="")
    menuImportar.add_command(label="Importar Historicos", command="")
    ##########################################################################



    #################### submenu de Exportar #################################
    menuExportar=tk.Menu(barraMenu, tearoff=0)
    barraMenu.add_cascade(label="Exportar", menu=menuExportar)
    menuExportar.add_command(label="Exportar Modelos", command="")
    menuExportar.add_command(label="Exportar Tecnicos", command="")
    menuExportar.add_command(label="Exportar Vehiculos", command="")
    menuExportar.add_command(label="Exportar Procesos", command="")
    menuExportar.add_separator()
    menuExportar.add_command(label="Exportar Pedido", command="")
    menuExportar.add_command(label="Exportar Programa", command="")
    menuExportar.add_command(label="Exportar Historicos", command="")
    ##########################################################################



    ######################### submenu de Ayuda ###############################
    menuAyuda=tk.Menu(barraMenu, tearoff=0)
    barraMenu.add_cascade(label="Ayuda", menu=menuAyuda)
    menuAyuda.add_command(label="Acerca de", command="")
    menuAyuda.add_command(label="Instrucciones", command="")
    ##########################################################################