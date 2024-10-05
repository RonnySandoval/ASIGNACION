import tkinter as tk
from . import ventanaNuevaPlanta, ventanaNuevoPedido

def desplegar_nuevo(subMenu):
    nuevaPlanta=subMenu.add_command   (label = "Nueva Planta (vacio)"   , command = vent_nueva_planta)
    subMenu.add_separator()
    nuevoPedido=subMenu.add_command   (label = "Nuevo Pedido (vacio)"   , command = vent_nuevo_pedido)
    nuevoModelo=subMenu.add_command   (label = "Nuevo Modelo (vacio)"   , command = vent_nuevo_modelo)
    nuevoVehiculo=subMenu.add_command (label = "Nuevo Vehículo (vacio)" , command = vent_nuevo_vehiculo)
    nuevoTecnico=subMenu.add_command  (label = "Nuevo Técnico (vacio)"  , command = vent_nuevo_tecnico)
    nuevoProveedor=subMenu.add_command(label = "Nuevo Proveedor (vacio)", command = vent_nuevo_proveedor)
    subMenu.add_separator()
    subMenu.add_command(label="Salir", command="")
    return


def vent_nueva_planta():
    ventanaNuevaPlanta.VentanaNuevaPlanta()
    

def vent_nuevo_pedido():
    ventanaNuevoPedido.VentanaNuevoPedido()


def vent_nuevo_modelo():
    pass

def vent_nuevo_vehiculo():
    pass

def vent_nuevo_tecnico():
    pass

def vent_nuevo_proveedor():
    pass
