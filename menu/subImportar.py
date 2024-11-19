import tkinter as tk
import ventanas_auxiliares
from . import ventanasEliminar, ventanasImportar
import eventos
import glo

def desplegar_importar(subMenu, root):
    subMenu.add_command(label="Importar Modelos", command="")
    subMenu.add_command(label="Importar Tecnicos", command="")
    subMenu.add_command(label="Importar Vehiculos", command="")
    subMenu.add_command(label="Importar Procesos", command="")
    subMenu.add_command(label="Importar Referencias/Modelos", command=lambda : vent_importar_referencias_modelos(glo.base_datos))
    subMenu.add_separator()
    subMenu.add_command(label="Importar Pedido", command=lambda : vent_importar_pedido(glo.base_datos))
    subMenu.add_command(label="Importar Programa", command="")
    subMenu.add_command(label="Importar Historicos", command="")
    return




def vent_importar_modelos():
    pass
  
def vent_importar_tecnicos():
    pass

def vent_importar_vehiculos():
    pass

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


