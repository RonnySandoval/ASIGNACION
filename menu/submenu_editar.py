import tkinter as tk
import ventanas_auxiliares
from . import ventanasEliminar
import eventos
import glo

def desplegar_editar(subMenu, root):
    editarPlanta  = subMenu.add_command(label="Editar Planta", command="")
    subMenu.add_separator()
    editarPedido  = subMenu.add_command(label="Editar Pedido", command="") 
    editarModelo  = subMenu.add_command(label="Editar Modelo", command="") 
    editarTecnico = subMenu.add_command(label="Editar Tecnico", command="")
    editarProceso = subMenu.add_command(label="Editar Proceso", command="")
    subMenu.add_separator()
    eliminarPlanta  = subMenu.add_command(label="Eliminar Planta", command="")
    subMenu.add_separator()
    eliminarPedido  = subMenu.add_command(label="Eliminar Pedido", command="") 
    eliminarModelo  = subMenu.add_command(label="Eliminar Modelo", command="") 
    eliminarTecnico = subMenu.add_command(label="Eliminar Tecnico", command=lambda:vent_eliminar_tecnico(glo.base_datos))
    eliminarProceso = subMenu.add_command(label="Eliminar Proceso", command="")
    return


############## FUNCIONES PARA EDITAR ######################
def vent_editar_planta():
    pass
  
def vent_editar_pedido():
    pass

def vent_editar_modelo():
    pass                          #asignar los botones de guardar y cancelar en la ventana

def vent_editar_vehiculo():
    pass                                            #asignar los botones de guardar y cancelar en la ventana

def vent_editar_tecnico():
    pass

def vent_editar_proceso():
    pass


############## FUNCIONES PARA ELIMINAR ####################
def vent_eliminar_planta():
    pass
  
def vent_eliminar_pedido():
    pass

def vent_eliminar_modelo():
    pass                          #asignar los botones de guardar y cancelar en la ventana

def vent_eliminar_vehiculo():
    pass                                            #asignar los botones de guardar y cancelar en la ventana

def vent_eliminar_tecnico(bbdd):
    ventana = ventanasEliminar.VentanaEliminarTecnico(glo.base_datos)
    ventana.asignafuncion(funcionEliminar = lambda : eventos.eliminar_tecnico_BD(ventana, bbdd),
                          funcionCancelar = ventana.rootAux.destroy)

def vent_eliminar_proceso():
    pass