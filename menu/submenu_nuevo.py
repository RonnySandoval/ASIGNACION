import view.ventanas_topLevel as ventanas_topLevel
from . import ventanaNuevoPedido, ventanaNuevoTecnico, ventanaNuevoProceso
import controller.controller as controller
import controller.glo as glo

def desplegar_nuevo(subMenu, root):
    nuevaPlanta    = subMenu.add_command(label = "Nueva Planta"   , command = vent_nueva_planta)
    abrirPlanta    = subMenu.add_command(label = "Abrir Planta"   , command = vent_abrir_planta)
    subMenu.add_separator()
    nuevoPedido    = subMenu.add_command(label = "Nuevo Pedido"   , command = vent_nuevo_pedido)
    nuevoModelo    = subMenu.add_command(label = "Nuevo Modelo"   , command = vent_nuevo_modelo)
    nuevoVehiculo  = subMenu.add_command(label = "Nuevo Vehículo" , command = vent_nuevo_vehiculo)
    nuevoTecnico   = subMenu.add_command(label = "Nuevo Técnico"  , command = vent_nuevo_tecnico)
    nuevoProceso   = subMenu.add_command(label = "Nuevo Proceso"  , command = vent_nuevo_proceso)
    subMenu.add_separator()
    subMenu.add_command(label="Salir", command = root.destroy)
    return

def vent_nueva_planta():
    controller.step_crearNuevaPlanta()
      
def vent_abrir_planta():
    controller.abrir_planta()

def vent_nuevo_pedido():
    ventana = ventanaNuevoPedido.VentanaNuevoPedido(bbdd=glo.base_datos)                                           # Llamar al constructor del objeto ventana
    ventana.asignafuncion(funcionGuardar  = lambda:controller.guardar_pedido_nuevo(ventana = ventana, bbdd = glo.base_datos),
                          funcionCancelar = ventana.rootAux.destroy)                            # asignar los botones de guardar y cancelar en la ventana
    
def vent_nuevo_modelo():
    ventana = ventanas_topLevel.VentanaCreaEditaModelo(accion="CREAR", bbdd=glo.base_datos)              #Llamar al constructor del objeto ventana
    ventana.asignafuncion(funcionGuardar  = lambda:controller.guardar_modelo_nuevo(accion = ventana, bbdd = glo.base_datos),
                          funcionCancelar = ventana.rootAux.destroy)                           #asignar los botones de guardar y cancelar en la ventana

def vent_nuevo_vehiculo():
    ventana = ventanas_topLevel.VentanaGestionaVehiculos(accion = "AGREGAR", bbdd = glo.base_datos)      #Llamar al constructor del objeto ventana
    ventana.asignafuncion(funcionAgregar = lambda:controller.aceptar_agregar_vehiculo(ventana, glo.base_datos),
                          funcionCancelar = ventana.rootAux.destroy)                                             #asignar los botones de guardar y cancelar en la ventana

def vent_nuevo_tecnico():
    ventana = ventanaNuevoTecnico.VentanaNuevoTecnico()
    ventana.asignaFuncion(funcionGuardar = lambda: controller.guardar_tecnico_nuevo(ventana, glo.base_datos),
                          funcionCancelar= ventana.rootAux.destroy)

def vent_nuevo_proceso():
    ventana = ventanaNuevoProceso.VentanaNuevoProceso()
    ventana.asignaFuncion(funcionGuardar = lambda: controller.guardar_proceso_nuevo(ventana, glo.base_datos),
                          funcionCancelar= ventana.rootAux.destroy)

    pass
