import tkinter as tk
import ventanas_auxiliares
from . import ventanasEliminar, ventanasImportar
import eventos
import glo
import BBDD

def desplegar_exportar(subMenu, root):
    
    subMenu.add_command(label="Exportar Procesos",             command = lambda : vent_exportar("PROCESOS", glo.base_datos))
    subMenu.add_command(label="Exportar Tecnicos",             command = lambda : vent_exportar("TECNICOS", glo.base_datos))
    subMenu.add_command(label="Exportar Marcas/Modelos",       command = lambda : vent_exportar("MARCAS_MODELOS", glo.base_datos))
    subMenu.add_command(label="Exportar Tiempos",              command = lambda : vent_exportar("TIEMPOS", glo.base_datos)) 
    subMenu.add_command(label="Exportar Referencias/Modelos ", command = lambda : vent_exportar("REFERENCIAS", glo.base_datos))
    subMenu.add_command(label="Exportar Vehiculos",            command = lambda : vent_exportar("VEHICULOS", glo.base_datos))

    subMenu.add_separator()
    subMenu.add_command(label="Exportar Pedidos",                   command = lambda : vent_exportar("PEDIDOS", glo.base_datos))
    subMenu.add_command(label="Exportar Programa (No funciona)",   command = lambda : vent_exportar("PROGRAMA", glo.base_datos))
    subMenu.add_command(label="Exportar Historicos (No funciona)", command = lambda : vent_exportar("HISTÓRICOS", glo.base_datos))
    return

def vent_exportar(nombreVentana, bbdd):
    if nombreVentana == "PROCESOS":
        dataframe = BBDD.leer_procesos_df(bbdd)

    elif nombreVentana == "TECNICOS":
        dataframe = BBDD.leer_tecnicos_df(bbdd)

    elif nombreVentana == "MARCAS_MODELOS":
        dataframe = BBDD.leer_modelos_marcas_df(bbdd)

    elif nombreVentana == "TIEMPOS":
        dataframe = BBDD.leer_tiempos_modelos_df(bbdd)

    elif nombreVentana == "REFERENCIAS":
        dataframe = BBDD.leer_referencias_modelos_df(bbdd)

    elif nombreVentana == "VEHICULOS":
        dataframe = BBDD.leer_vehiculos_df(bbdd)

    elif nombreVentana == "PEDIDOS":
        dataframe = BBDD.leer_pedidos_df(bbdd)

    elif nombreVentana == "PROGRAMA":
        pass

    elif nombreVentana == "HISTORICOS":
        pass

    ventana = ventanas_auxiliares.VentanaVistaPrevia(nombreVentana, dataframe, bbdd)
    ventana.asignafuncion(funcionAceptar  = lambda : eventos.aceptar_exportar_to_excel(ventana, dataframe, nombreVentana),
                          funcionCancelar = ventana.rootAux.destroy)
