import view.ventanas_topLevel as ventanas_topLevel
from . import ventanaNuevoPedido, ventanaNuevoTecnico, ventanaNuevoProceso
import controller.controller as controller
import controller.glo as glo

def desplegar_nuevo(subMenu, root):
    nuevaPlanta    = subMenu.add_command(label = "Nueva Planta"   , command = vent_nueva_planta)
    abrirPlanta    = subMenu.add_command(label = "Abrir Planta"   , command = vent_abrir_planta)
    subMenu.add_separator()
    nuevoPedido    = subMenu.add_command(label = "Nuevo Pedido"   , command = lambda:vent_nuevo_item("PEDIDO"))
    nuevoModelo    = subMenu.add_command(label = "Nuevo Modelo"   , command = lambda:vent_nuevo_item("MODELO"))
    nuevoVehiculo  = subMenu.add_command(label = "Nuevo Vehículo" , command = lambda:vent_nuevo_item("VEHICULO"))
    nuevoTecnico   = subMenu.add_command(label = "Nuevo Técnico"  , command = lambda:vent_nuevo_item("TECNICO"))
    nuevoProceso   = subMenu.add_command(label = "Nuevo Proceso"  , command = lambda:vent_nuevo_item("PROCESO"))
    subMenu.add_separator()
    subMenu.add_command(label="Salir", command = root.destroy)
    return

def vent_nueva_planta():
    controller.step_crearNuevaPlanta()
      
def vent_abrir_planta():
    controller.abrir_planta()

def vent_nuevo_item(tipo):
    
    if tipo == "PEDIDO" :
        funcion = lambda:controller.guardar_pedido_nuevo(ventana = ventana, bbdd = glo.base_datos)
        ventana = ventanaNuevoPedido.VentanaNuevoPedido(bbdd=glo.base_datos)                                 # Llamar al constructor del objeto ventana

    elif tipo == "MODELO" :
        funcion = lambda:controller.guardar_modelo_nuevo(accion = ventana, bbdd = glo.base_datos)
        ventana = ventanas_topLevel.VentanaCreaEditaModelo(accion="CREAR", bbdd=glo.base_datos)              #Llamar al constructor del objeto ventana

    elif tipo == "VEHICULO" :
        funcion = lambda:controller.aceptar_agregar_vehiculo(ventana, glo.base_datos)
        ventana = ventanas_topLevel.VentanaGestionaVehiculos(accion = "AGREGAR", bbdd = glo.base_datos)      #Llamar al constructor del objeto ventana

    elif tipo == "PROCESO" :
        funcion = lambda:controller.guardar_proceso_nuevo(ventana, glo.base_datos)
        ventana = ventanaNuevoProceso.VentanaNuevoProceso()

    elif tipo == "TECNICO" :
        funcion = lambda: controller.guardar_tecnico_nuevo(ventana, glo.base_datos)
        ventana = ventanaNuevoTecnico.VentanaNuevoTecnico()

    ventana.asignafuncion(funcion,
                          ventana.rootAux.destroy)   
