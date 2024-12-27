from . import ventanasImportar
import controller.controller as controller
import controller.glo as glo

def desplegar_importar(subMenu, root):    
    subMenu.add_command(label="Importar Procesos",            command = lambda: vent_importar( "PROCESOS", glo.base_datos))
    subMenu.add_command(label="Importar Tecnicos",            command = lambda: vent_importar( "TECNICOS", glo.base_datos))
    subMenu.add_command(label="Importar Modelos",             command = lambda: vent_importar( "MODELOS", glo.base_datos))
    subMenu.add_command(label="Importar Tiempos",             command = lambda: vent_importar( "TIEMPOS_MODELOS", glo.base_datos))    
    subMenu.add_command(label="Importar Referencias/Modelos", command = lambda : vent_importar("REFERENCIAS", glo.base_datos))
    subMenu.add_separator()
    subMenu.add_command(label="Importar Pedido",     command=lambda : vent_importar("PEDIDO", glo.base_datos))
    subMenu.add_command(label="Importar Historicos", command=lambda :vent_importar("HISTORICOS", glo.base_datos))
    return

def vent_importar(nombreVentana, bbdd):

    if nombreVentana == "HISTORICOS":

        ventana = ventanasImportar.VentanaImportarDatos(nombreVentana, bbdd)
        ventana.asignafuncion(funcionAceptar  = lambda : controller.aceptar_cargar_historicos_excel(ventana, nombreVentana, bbdd),
                            funcionCancelar = ventana.rootAux.destroy)
        return
    ventana = ventanasImportar.VentanaImportarDatos(nombreVentana, bbdd)
    ventana.asignafuncion(funcionAceptar  = lambda : controller.aceptar_cargar_excel(ventana, nombreVentana, bbdd),
                          funcionCancelar = ventana.rootAux.destroy)
    
def vent_importar_referencias_modelos(bbdd):
    ventana = ventanasImportar.VentanaImportarReferencias(bbdd)
    ventana.asignafuncion(funcionAceptar  = lambda : controller.aceptar_cargar_referencias_excel(ventana, bbdd),
                          funcionCancelar = ventana.rootAux.destroy)

def vent_importar_pedido(bbdd):
    ventana = ventanasImportar.VentanaImportarPedido(bbdd)
    ventana.asignafuncion(funcionAceptar  = lambda : controller.aceptar_cargar_pedido_excel(ventana, bbdd),
                          funcionCancelar = ventana.rootAux.destroy)

def vent_importar_historicos():
    pass


