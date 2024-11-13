import tkinter as tk
import ventanas_auxiliares
from . import ventanaNuevaPlanta, ventanaNuevoPedido, ventanaNuevoModelo, ventanaNuevoVehiculo, ventanaNuevoTecnico, ventanaNuevoProceso
import eventos
import glo

def desplegar_nuevo(subMenu, root):
    nuevaPlanta    = subMenu.add_command   (label = "Nueva Planta (no funciona)"   , command = vent_nueva_planta)
    subMenu.add_separator()
    nuevoPedido    = subMenu.add_command   (label = "Nuevo Pedido (no funciona)"   , command = vent_nuevo_pedido)
    nuevoModelo    = subMenu.add_command   (label = "Nuevo Modelo"   , command = vent_nuevo_modelo)
    nuevoVehiculo  = subMenu.add_command (label = "Nuevo Vehículo" , command = vent_nuevo_vehiculo)
    nuevoTecnico   = subMenu.add_command  (label = "Nuevo Técnico"  , command = vent_nuevo_tecnico)
    nuevoProceso   = subMenu.add_command  (label = "Nuevo Proceso"  , command = vent_nuevo_proceso)
    nuevoProveedor = subMenu.add_command(label = "Nuevo Proveedor (vacio)", command = vent_nuevo_proveedor)
    subMenu.add_separator()
    subMenu.add_command(label="Salir", command=lambda: root.destroy)
    return

def vent_nueva_planta():
    ventanaNuevaPlanta.VentanaNuevaPlanta()
  
def vent_nuevo_pedido():
    ventanaNuevoPedido.VentanaNuevoPedido()

def vent_nuevo_modelo():
    print("pusó el botón crear modelo")
    ventana = ventanas_auxiliares.VentanaCreaEditaModelo(accion="CREAR", bbdd=glo.base_datos)              #Llamar al constructor del objeto ventana
    ventana.asignafuncion(funcionGuardar  = lambda:eventos.guardar_modelo_nuevo(accion = ventana, bbdd = glo.base_datos),
                          funcionCancelar = ventana.rootAux.destroy)                           #asignar los botones de guardar y cancelar en la ventana

def vent_nuevo_vehiculo():
    ventana = ventanas_auxiliares.VentanaGestionaVehiculos(accion = "AGREGAR", bbdd = glo.base_datos)      #Llamar al constructor del objeto ventana
    ventana.asignafuncion(funcionAgregar = lambda:eventos.aceptar_agregar_vehiculo(ventana, glo.base_datos),
                          funcionCancelar = ventana.rootAux.destroy)                                             #asignar los botones de guardar y cancelar en la ventana

def vent_nuevo_tecnico():
    ventana = ventanaNuevoTecnico.VentanaNuevoTecnico()
    ventana.asignaFuncion(funcionGuardar = lambda: eventos.guardar_tecnico_nuevo(ventana, glo.base_datos),
                          funcionCancelar= ventana.rootAux.destroy)

def vent_nuevo_proceso():
    ventana = ventanaNuevoProceso.VentanaNuevoProceso()
    ventana.asignaFuncion(funcionGuardar = lambda: eventos.guardar_proceso_nuevo(ventana, glo.base_datos),
                          funcionCancelar= ventana.rootAux.destroy)

def vent_nuevo_proveedor():
    pass
