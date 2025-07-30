import tkinter as tk

from view.estilos import grisOscuro, blancoCalido
import menu.submenu_nuevo  as subNuevo
import menu.submenu_editar as subEditar
import menu.submenu_importar as subImportar
import menu.submenu_exportar as subExportar

def crearMenuPrincipal(raiz):
    #Barra de menú
    barraMenu = tk.Menu(raiz, bg=grisOscuro, fg=blancoCalido)
    raiz.config(menu=barraMenu)

    ######################### submenu de Nuevo######################################
    menuNuevo=tk.Menu(barraMenu, tearoff=0)
    barraMenu.add_cascade(label="Nuevo", menu=menuNuevo)
    subNuevo.desplegar_nuevo(subMenu = menuNuevo, root=raiz)
    ###############################################################################

    ########################### submenu de Editar ##############################
    menuEditar=tk.Menu(barraMenu, tearoff=0)
    barraMenu.add_cascade(label="Editar", menu=menuEditar)
    subEditar.desplegar_editar(subMenu = menuEditar, root=raiz)
    ##########################################################################

    ########################### submenu de Importar ###########################
    menuImportar=tk.Menu(barraMenu, tearoff=0)
    barraMenu.add_cascade(label="Importar", menu=menuImportar)
    subImportar.desplegar_importar(subMenu = menuImportar, root=raiz)

    #########################################################################
    #################### submenu de Exportar #################################
    menuExportar=tk.Menu(barraMenu, tearoff=0)
    barraMenu.add_cascade(label="Exportar", menu=menuExportar)
    subExportar.desplegar_exportar(subMenu = menuExportar, root=raiz)

    ##########################################################################
    ######################### submenu de Ayuda ###############################
    menuAyuda=tk.Menu(barraMenu, tearoff=0)
    barraMenu.add_cascade(label="Acerca de", menu=menuAyuda)
    menuAyuda.add_command(label="Planta (No funciona)", command="")
    menuAyuda.add_command(label="Instrucciones (No funciona)", command="")
    ##########################################################################