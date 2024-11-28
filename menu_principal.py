import tkinter as tk
from estilos import grisOscuro, blancoCalido
import menu.submenu_nuevo  as subNuevo
import menu.submenu_editar as subEditar
import menu.subImportar as subImportar


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
    #############################################################################



    ############################## submenu de Editar ###########################
    menuEditar=tk.Menu(barraMenu, tearoff=0)
    barraMenu.add_cascade(label="Editar", menu=menuEditar)
    subEditar.desplegar_editar(subMenu = menuEditar, root=raiz)
    ##########################################################################



    ########################### submenu de Importar ###########################
    menuImportar=tk.Menu(barraMenu, tearoff=0)
    barraMenu.add_cascade(label="Importar", menu=menuImportar)
    subImportar.desplegar_importar(subMenu = menuImportar, root=raiz)

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