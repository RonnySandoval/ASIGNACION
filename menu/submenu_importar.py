import tkinter as tk
import ventanas_topLevel
from . import ventanasEliminar, ventanasImportar
import eventos
import glo

def desplegar_importar(subMenu, root):
    
    subMenu.add_command(label="Importar Procesos",                command = lambda: vent_importar( "PROCESOS", glo.base_datos))
    subMenu.add_command(label="Importar Tecnicos",                command = lambda: vent_importar( "TECNICOS", glo.base_datos))
    subMenu.add_command(label="Importar Modelos",                 command = lambda: vent_importar( "MODELOS", glo.base_datos))
    subMenu.add_command(label="Importar Tiempos",                 command = lambda: vent_importar( "TIEMPOS_MODELOS", glo.base_datos))    
    subMenu.add_command(label="Importar Referencias/Modelos",     command = lambda : vent_importar("REFERENCIAS", glo.base_datos))
    subMenu.add_command(label="Importar Vehiculos (No funciona)", command ="")

    subMenu.add_separator()
    subMenu.add_command(label="Importar Pedido", command=lambda : vent_importar("PEDIDO", glo.base_datos))
    subMenu.add_command(label="Importar Programa (No funciona)", command="")
    subMenu.add_command(label="Importar Historicos (No funciona)", command="")
    return


def vent_importar(nombreVentana, bbdd):
    ventana = ventanasImportar.VentanaImportarDatos(nombreVentana, bbdd)
    ventana.asignafuncion(funcionAceptar  = lambda : eventos.aceptar_cargar_excel(ventana, nombreVentana, bbdd),
                          funcionCancelar = ventana.rootAux.destroy)
    

def vent_importar_referencias_modelos(bbdd):
    ventana = ventanasImportar.VentanaImportarReferencias(bbdd)
    ventana.asignafuncion(funcionAceptar  = lambda : eventos.aceptar_cargar_referencias_excel(ventana, bbdd),
                          funcionCancelar = ventana.rootAux.destroy)

def vent_importar_pedido(bbdd):
    ventana = ventanasImportar.VentanaImportarPedido(bbdd)
    ventana.asignafuncion(funcionAceptar  = lambda : eventos.aceptar_cargar_pedido_excel(ventana, bbdd),
                          funcionCancelar = ventana.rootAux.destroy)

def vent_importar_programa():
    pass

def vent_importar_historicos():
    pass


