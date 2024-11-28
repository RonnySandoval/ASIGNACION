import customtkinter as ctk  # Usar customtkinter en lugar de tkinter
from   estilos import *
import root_frame_modelos       as frameMode
import root_frame_tecnicos      as frameTecn
import root_frame_vehiculos     as frameVehi
import root_frame_procesos      as frameProc
import root_frame_pedidos       as framePedi
import root_frame_detallePedido as frameDeta
import root_frame_historicos    as frameHist
import root_frame_referencias   as frameRefe
import glo

# Configuración global del estilo de customtkinter
ctk.set_appearance_mode("dark")  # Modo oscuro por defecto
ctk.set_default_color_theme("dark-blue")  # Colores por defecto con tonos azulados

def construye_root(root):
    ################################################################################################################################################
    ################################################### Añadir contenidos al frame de PLANTA #######################################################
    ################################################################################################################################################
    glo.stateFrame.contenidoDeModelos   = frameMode.ContenidoModelos(root.creaframeModelos(),   bbdd=glo.base_datos)
    glo.stateFrame.contenidoDeTecnicos  = frameTecn.ContenidoTecnicos(root.creaframeTecnicos(), bbdd=glo.base_datos)
    glo.stateFrame.contenidoDeProcesos  = frameProc.ContenidoProcesos(root.creaframeProcesos(), bbdd=glo.base_datos)   


    ################################################################################################################################################
    ################################################### Añadir contenidos al frame de VEHÍCULOS ####################################################
    ################################################################################################################################################
    glo.stateFrame.contenidoDeVehiculos = frameVehi.ContenidoVehiculos(root.frameVehiculos)
    glo.stateFrame.tablaVehiculos       = frameVehi.TablaVehiculos(glo.stateFrame.contenidoDeVehiculos,  root.frameVehiculos, root, bbdd=glo.base_datos)
    glo.stateFrame.filtroVehiculos      = frameVehi.FiltrosVehiculos(glo.stateFrame.tablaVehiculos, glo.stateFrame.contenidoDeVehiculos,  bbdd=glo.base_datos)


    ################################################################################################################################################
    ################################################### Añadir contenidos al frame de PEDIDOS ######################################################
    ################################################################################################################################################
    glo.stateFrame.contenidoDePedidos = framePedi.ContenidoPedidos(root.framePedidos)
    glo.stateFrame.tablaPedidos       = framePedi.TablaPedidos(glo.stateFrame.contenidoDePedidos, root.framePedidos, root, bbdd=glo.base_datos)
    glo.stateFrame.filtroPedidos      = framePedi.FiltrosPedidos(glo.stateFrame.tablaPedidos, glo.stateFrame.contenidoDePedidos, bbdd=glo.base_datos)

    glo.stateFrame.contenidoDeDetalles = frameDeta.ContenidoDetallePedido(root.framePedidos)
    glo.stateFrame.tablaDetalles       = frameDeta.TablaDetallePedido(glo.stateFrame.contenidoDeDetalles, root.framePedidos, root, bbdd=glo.base_datos)
    glo.stateFrame.filtroDetalles     = frameDeta.FiltrosDetallePedido(glo.stateFrame.tablaDetalles, glo.stateFrame.contenidoDeDetalles, bbdd=glo.base_datos)


    ################################################################################################################################################
    ################################################### Añadir contenidos al frame de HISTÓRICOS ###################################################
    ################################################################################################################################################
    glo.stateFrame.contenidoDeHistoricos= frameHist.ContenidoHistoricos(root.frameHistoricos)
    glo.stateFrame.tablaHistoricos      = frameHist.TablaHistoricos( glo.stateFrame.contenidoDeHistoricos, root.frameHistoricos, root, bbdd=glo.base_datos)
    glo.stateFrame.filtroHistoricos     = frameHist.FiltrosHistoricos(glo.stateFrame.tablaHistoricos, glo.stateFrame.contenidoDeHistoricos, bbdd=glo.base_datos)


    ################################################################################################################################################
    ################################################### Añadir contenidos al frame de REFERENCIAS ##################################################
    ################################################################################################################################################
    glo.stateFrame.contenidoDeReferencias   = frameRefe.ContenidoReferencias(root.frameReferencias, bbdd='planta_manta.db')


    root.mainloop()

"""
#CREAR VENTANA PRINCIPAL CON SU MENÚ
root = ventanaRoot(bbdd=glo.base_datos)
menu_principal.crearMenuPrincipal(root)
construye_root(root)
"""
