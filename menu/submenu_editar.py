from . import ventanasEliminar
import controller.controller as controller
import controller.glo as glo

def desplegar_editar(subMenu, root):
    editarPlanta  = subMenu.add_command(label="Editar Planta (No funciona)", command="")
    subMenu.add_separator()
    #editarPedido  = subMenu.add_command(label="Editar Pedido (No funciona)", command="") 
    #editarModelo  = subMenu.add_command(label="Editar Modelo (No funciona)", command="") 
    #editarTecnico = subMenu.add_command(label="Editar Tecnico (No funciona)", command="")
    #editarProceso = subMenu.add_command(label="Editar Proceso (No funciona)", command="")
    subMenu.add_separator()
    eliminarPlanta  = subMenu.add_command(label="Eliminar Planta (No funciona)", command="")
    subMenu.add_separator()
    eliminarPedido  = subMenu.add_command(label="Eliminar Pedido (No funciona)", command="") 
    eliminarModelo  = subMenu.add_command(label="Eliminar Modelo", command=lambda:vent_eliminar_modelo(glo.base_datos)) 
    eliminarTecnico = subMenu.add_command(label="Eliminar Tecnico (No funciona)", command=lambda:vent_eliminar_tecnico(glo.base_datos))
    eliminarProceso = subMenu.add_command(label="Eliminar Proceso (No funciona)", command="")
    return

############## FUNCIONES PARA EDITAR ######################
def vent_editar_planta():
    pass

def vent_editar_proceso():
    pass


############## FUNCIONES PARA ELIMINAR ####################
def vent_eliminar_planta():
    pass
  
def vent_eliminar_pedido():
    pass

def vent_eliminar_modelo(bbdd):
    ventana = ventanasEliminar.VentanaEliminarModelo(bbdd)
    ventana.asignafuncion(funcionEliminar = lambda : controller.eliminar_modelo_BD(ventana, bbdd),
                          funcionCancelar = ventana.rootAux.destroy)

def vent_eliminar_vehiculo():
    pass                                            #asignar los botones de guardar y cancelar en la ventana

def vent_eliminar_tecnico(bbdd):
    ventana = ventanasEliminar.VentanaEliminarTecnico(bbdd)
    ventana.asignafuncion(funcionAceptar = lambda : controller.eliminar_tecnico_BD(ventana, bbdd),
                          funcionCancelar = ventana.rootAux.destroy)

def vent_eliminar_proceso():
    pass