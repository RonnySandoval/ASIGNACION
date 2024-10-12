import tkinter as tk
import re
import CRUD
import dicc_variables
import ventanas_auxiliares
import ventanas_emergentes
import Mod_clases, Mod_objetos
import graficaGantt

def crear_modelo():
    print("pusó el botón crear modelo")
    ventana = ventanas_auxiliares.VentanaCreaEdita("CREAR")
    ventana.asignafuncionBoton(lambda:guardar_modelo(ventana), lambda:cancelar(ventana))

def guardar_modelo(ventana):
    print(ventana)
    datos = (ventana.varMarca.get(),
            ventana.varModelo.get(),
            ventana.varTel.get(),
            ventana.varPdi.get(),
            ventana.varLav.get(),
            ventana.varPin.get(),
            ventana.varCal.get()
    )
    CRUD.insertar_modelo(*datos)
    ventana.rootAux.destroy()

    #leer BBDD y rellenar los label con la BBDD actualizada

def agregarVH_pedido(ventana):
    #Se recogen los datos de la fila
    datos = (ventana.varChasis.get(),
             ventana.varFecha.get(),
            ventana.varMarca.get(),
            ventana.varModelo.get(),
            ventana.varColor.get(),
            ventana.varEstado.get(),
            ventana.varTel.get(),
            ventana.varPdi.get(),
            ventana.varLav.get(),
            ventana.varPin.get(),
            ventana.varCal.get(),
            ventana.varNoved.get(),
            ventana.varSubcon.get(),
    )
    for dato in datos:
        print (dato)
    CRUD.insertar_vehiculo(*datos)
    ventana.rootAux.destroy()

def modificarVH_en_BBDD(ventana, chasis_anterior):
    #Se recogen los datos de la fila
    datos = (ventana.varChasis.get(),
            ventana.varFecha.get(),
            ventana.varMarca.get(),
            ventana.varModelo.get(),
            ventana.varColor.get(),
            ventana.varEstado.get(),
            ventana.varTel.get(),
            ventana.varPdi.get(),
            ventana.varLav.get(),
            ventana.varPin.get(),
            ventana.varCal.get(),
            ventana.varNoved.get(),
            ventana.varSubcon.get(),
    )
    print(chasis_anterior)

    for dato in datos:
        print (dato)
    #Modifica el registro en la base de datos
    CRUD.modificar_vehiculo(datos, chasis_anterior)
    ventana.rootAux.destroy()

def recoger_datos_modelo(filaBoton):
    #extraer el numero dela fila
    fila = re.search(r'(\d+)$', filaBoton).group(1)
    #obtener la marca y el modelo apartir del numero de la fila
    marca_modelo = dicc_variables.label_variables_vehiculos[f"labelVehiculo{fila}"].cget("text")
    marca = re.search(r'^(.*?)\s*-\s*(.*?)$', marca_modelo).group(1).strip()            #expresion regular para truncar solo la marca
    modelo = re.search(r'^(.*?)\s*-\s*(.*?)$', marca_modelo).group(2).strip()           #expresion regular para truncar solo el modelo
    print(f"marca={marca} modelo={modelo}")
    tiempos=[]
    for columna in range(1,6):
        tiempos.append(dicc_variables.entry_variables[f"ExtryTime{fila}_{columna}"].get())  #obtiene el tiempo de proceso y lo agrega a la lista
    print(tiempos)
    return [marca, modelo] + tiempos

def recoger_datos_vehiculo(id_chasis):
    return CRUD.leer_vehiculo(id_chasis)

def editar_modelo(botonPulsado):
    print(recoger_datos_modelo(botonPulsado))
    datos = recoger_datos_modelo(botonPulsado)
    ventana = ventanas_auxiliares.VentanaCreaEdita("EDITAR")
    ventana.set_values(datos)
    ventana.asignafuncionBoton(lambda:guardar_modelo(ventana), lambda:cancelar(ventana))

def modificar_vehiculo_pedido(chasis_anterior):
    ventana = ventanas_auxiliares.VentanaGestionaPedido("MODIFICAR")
    valores = recoger_datos_vehiculo(chasis_anterior)
    print(valores)
    ventana.set_values(valores, 'MODIFICAR')
    ventana.asignafuncionBoton(lambda:modificarVH_en_BBDD(ventana, chasis_anterior), lambda:cancelar(ventana))
    ventana.rootAux.destroy()

def eliminar_VH_pedido(chasis):
    if ventanas_emergentes.msg_eliminar_vh(chasis) == "Aceptar":
        CRUD.eliminar_vehiculo(chasis)

def agregar_a_pedido(botonPulsado):
    print(recoger_datos_modelo(botonPulsado))
    datos = recoger_datos_modelo(botonPulsado)
    ventana = ventanas_auxiliares.VentanaGestionaPedido("AGREGAR")
    ventana.set_values(datos, "AGREGAR")
    ventana.asignafuncionBoton(lambda:agregarVH_pedido(ventana), lambda:cancelar(ventana))
    ventana.rootAux.destroy()

def cancelar(ventana):
    ventana.rootAux.destroy()

def leepedidoBBDD():
    return CRUD.leer_vehiculos()




def abrirFechayHora(tipoPrograma):
    ventana = ventanas_auxiliares.EstableceFechaHora()
    ventana.asignaFuncion(lambda:aceptarFechayHora(ventana, tipoPrograma), lambda:cancelar(ventana))
    
def aceptarFechayHora(ventana, tipoPrograma):
    fecha = ventana.varFecha.get()
    hora = ventana.varHora.get()
    print(f"Fecha: {fecha}, Hora: {hora}")
    ventana.rootAux.destroy()
    
    if tipoPrograma == "completo":
        Mod_clases.programa_completo(Mod_objetos.pedido_quito06, Mod_clases.personal, 4000, fecha, hora)
        horizonte_calculado = Mod_clases.calcular_horizonte(Mod_objetos.pedido_quito06)
        print(f"el horizonte es {horizonte_calculado}")

        #GRAFICAR PROGRAMACIÓN EN GANTT##########
        graficaGantt.generar_gantt_tecnicos(Mod_clases.personal, fecha, hora, horizonte_calculado=horizonte_calculado)
        graficaGantt.generar_gantt_vehiculos(Mod_objetos.pedido_quito06, fecha, hora, horizonte_calculado=horizonte_calculado)
    
    if tipoPrograma == "inmediato":
        Mod_clases.programa_inmediato(Mod_objetos.pedido_quito06, Mod_clases.personal, 4000, fecha, hora)
        horizonte_calculado = Mod_clases.calcular_horizonte(Mod_objetos.pedido_quito06)
        print(f"el horizonte es {horizonte_calculado}")

        #GRAFICAR PROGRAMACIÓN EN GANTT##########
        graficaGantt.generar_gantt_tecnicos(Mod_clases.personal, fecha, hora, horizonte_calculado=horizonte_calculado)
        graficaGantt.generar_gantt_vehiculos(Mod_objetos.pedido_quito06, fecha, hora, horizonte_calculado=horizonte_calculado)

def nombraArchivoExcel(programa):
    return programa + 'Numero__' + '.xlsx'




