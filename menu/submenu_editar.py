from . import ventanasEliminar
import view.ventanas_topLevel as ventanas_topLevel
import controller.controller as controller
import controller.glo as glo

def desplegar_editar(subMenu, root):
    editarPlanta  = subMenu.add_command(label="Editar Planta", command =lambda: vent_editar("PLANTA",
                                                                                             glo.base_datos))
    editarPlanta  = subMenu.add_command(label="Editar Proceso (No funciona)", command="")
    editarPlanta  = subMenu.add_command(label="Editar Técnico (No funciona)", command="")
    subMenu.add_separator()
    eliminarPedido  = subMenu.add_command(label="Eliminar Pedido",  command=lambda:vent_eliminar_item(glo.base_datos, "PEDIDO")) 
    eliminarModelo  = subMenu.add_command(label="Eliminar Modelo",  command=lambda:vent_eliminar_item(glo.base_datos, "MODELO")) 
    eliminarTecnico = subMenu.add_command(label="Eliminar Tecnico", command=lambda:vent_eliminar_item(glo.base_datos, "TECNICO"))
    eliminarProceso = subMenu.add_command(label="Eliminar Proceso", command=lambda:vent_eliminar_item(glo.base_datos, "PROCESO"))
    return

############## FUNCIONES PARA EDITAR ######################
def vent_editar(tipo, bbdd):
    if tipo =="PLANTA":
        ventana = ventanas_topLevel.VentanaCreaEditarPlanta("EDITAR", bbdd)
        ventana.asignafuncion(funcionAceptar = lambda : controller.editar_planta_BD(ventana, bbdd),
                              funcionCancelar = ventana.rootAux.destroy)

def vent_editar_proceso():
    pass

def vent_editar_tecnico():
    pass

############## FUNCIONES PARA ELIMINAR ####################
def vent_eliminar_item(bbdd, tipo):
    ventana = ventanasEliminar.VentanaEliminar(tipo, bbdd)

    if   tipo == "MODELO":
        funcion = lambda : controller.eliminar_modelo_BD(ventana, bbdd)

    elif tipo == "PEDIDO":
        funcion = lambda : controller.eliminar_pedido_BD(ventana, bbdd)

    elif tipo == "PROCESO":
        funcion = lambda : controller.eliminar_proceso_BD(ventana, bbdd)

    elif tipo == "TECNICO":
        funcion = lambda : controller.eliminar_tecnico_BD(ventana, bbdd)


    ventana.asignafuncion(funcionEliminar = funcion,
                          funcionCancelar = ventana.rootAux.destroy)