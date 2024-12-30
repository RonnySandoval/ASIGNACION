from . import ventanasEliminar
import view.ventanas_topLevel as ventanas_topLevel
import controller.controller as controller
import controller.glo as glo

def desplegar_editar(subMenu, root):
    editarPlanta  = subMenu.add_command(label="Editar Planta",  command =lambda: vent_editar("PLANTA", glo.base_datos))
    editarPlanta  = subMenu.add_command(label="Editar Proceso", command =lambda: vent_editar("PROCESO", glo.base_datos))
    editarPlanta  = subMenu.add_command(label="Editar Técnico", command =lambda: vent_editar("TECNICO", glo.base_datos))
    subMenu.add_separator()
    eliminarPedido  = subMenu.add_command(label="Eliminar Pedido",  command=lambda:vent_eliminar_item("PEDIDO", glo.base_datos)) 
    eliminarModelo  = subMenu.add_command(label="Eliminar Modelo",  command=lambda:vent_eliminar_item("MODELO", glo.base_datos)) 
    eliminarTecnico = subMenu.add_command(label="Eliminar Tecnico", command=lambda:vent_eliminar_item("TECNICO", glo.base_datos))
    eliminarProceso = subMenu.add_command(label="Eliminar Proceso", command=lambda:vent_eliminar_item("PROCESO", glo.base_datos))
    return

############## FUNCIONES PARA EDITAR ######################
def vent_editar(tipo, bbdd):
    if tipo =="PLANTA":
        ventana = ventanas_topLevel.VentanaEditarPlanta("EDITAR", bbdd)
        ventana.asignafuncion(funcionAceptar = lambda : controller.editar_planta_BD(ventana, bbdd),
                              funcionCancelar = ventana.rootAux.destroy)
    
    if tipo =="PROCESO":
        ventana = ventanas_topLevel.VentanaTablaEditar(tipo,
                                                       bbdd,
                                                       funcion=lambda ventana, datos, bbdd: controller.editar_proceso_BD(ventana, datos, bbdd))
    
    if tipo =="TECNICO":
        ventana = ventanas_topLevel.VentanaTablaEditar(tipo,
                                                       bbdd,
                                                       funcion=lambda ventana, datos, bbdd: controller.editar_tecnico_BD(ventana, datos, bbdd))

############## FUNCIONES PARA ELIMINAR ####################
def vent_eliminar_item(tipo, bbdd):
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