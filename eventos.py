import tkinter as tk
import re
import CRUD
import BBDD
import glo
import ventanas_auxiliares
import ventanas_emergentes
import Mod_clases, Mod_objetos
import graficaGantt

def crear_modelo(bbdd):
    print("pusó el botón crear modelo")
    ventana = ventanas_auxiliares.VentanaCreaEdita("CREAR", bbdd)              #Llamar al constructor del objeto ventana
    ventana.asignafuncionBoton(lambda:guardar_modelo_nuevo(ventana, bbdd), lambda:cancelar(ventana))    #asignar los botones de guardar y cancelar en la ventana

def recoger_datos_modelo(filaBoton, bbdd):
    print(filaBoton)
    fila = re.search(r'(\d+)$', filaBoton).group(1)                             #extraer el numero de la fila
    marca_modelo = glo.lbl_Modelos[f"labelVehiculo{fila}"].cget("text")        #obtener la marca y el modelo apartir del numero de la fila
    marca = re.search(r'^(.*?)\s*-\s*(.*?)$', marca_modelo).group(1).strip()    #expresion regular para truncar solo la marca
    modelo = re.search(r'^(.*?)\s*-\s*(.*?)$', marca_modelo).group(2).strip()   #expresion regular para truncar solo el modelo
    print(f"marca={marca} modelo={modelo}")         
    tiempos=[]
    for columna in range(1, BBDD.calcula_procesos(bbdd)+1):
        tiempos.append(glo.ent_Tiempos[f"ExtryTime{fila}_{columna}"].get())    #obtiene el tiempo de proceso y lo agrega a la lista
    print(tiempos)
    return [marca, modelo] + tiempos

def editar_modelo(botonPulsado, bbdd):
    print(recoger_datos_modelo(botonPulsado, bbdd))
    datos = recoger_datos_modelo(botonPulsado, bbdd)                   # llamar a la función que recoge los datos de los entry en el panel de modelos
    ventana = ventanas_auxiliares.VentanaCreaEdita("EDITAR", bbdd)     # Llamar al constructor del objeto ventana para editar el modelo
    ventana.set_values(datos)                                          # llamar al metodo del objeto ventana creada, que llena los campos de modelo y tiempos
    ventana.asignafuncionBoton(lambda:guardar_modelo_actualizado(ventana, bbdd), lambda:cancelar(ventana))    #asignar los botones de guardar y cancelar en la ventana

def guardar_modelo_nuevo(ventana, bbdd):
    print(ventana)
    datos = (ventana.varMarca.get(),
            ventana.varModelo.get())        #NOMBRES DE MARCA Y MODELO
    
    tiempos =[]             #SE CREA Y LLENA UNA LISTA CON LOS TIEMPOS DE PROCESO
    for clave, valor in glo.strVar_nuevosTiemposMod.items():    
        tiempos.append(valor.get())
    
    #OBTENEMOS ID DE MODELOS Y PROCESOS
    id_modelo = f"{datos[0]}-{datos[1]}"
    id_procesos = BBDD.obtener_id_procesos(bbdd)
    id_procesos.sort()
    #Insertamos en la tabla de modelos
    BBDD.insertar_modelo(bbdd, id_modelo, datos[0], datos[1])

    #insertamos enla tabla de timepos modelos
    for id_proceso, tiempo in zip(id_procesos, tiempos):
        proc_model = f"{id_proceso}-{datos[1]}"
        BBDD.insertar_tiempo_modelo(bbdd,
                                    proc_model, 
                                    id_proceso,
                                    id_modelo,
                                    tiempo)

    ventana.rootAux.destroy()   #cerramos la ventana auxiliar
    
    #actualizamos el frame de modelos en la ventana
    glo.stateFrame.contenidoDeModelos.actualizar_contenido(bbdd)

def guardar_modelo_actualizado(ventana, bbdd):
    print(ventana)
    datos = (ventana.varMarca.get(),
            ventana.varModelo.get())
    for clave, valor in glo.dicc_variables.strVar_nuevosTiemposMod.items():
        datos.append(valor.get())

    CRUD.insertar_modelo(*datos)
    ventana.rootAux.destroy()





def agregar_a_pedido(botonPulsado, bbdd):
    datos = recoger_datos_modelo(botonPulsado, bbdd)
    print(datos)
    ventana = ventanas_auxiliares.VentanaGestionaVehiculos("AGREGAR", bbdd)
    ventana.set_values(datos)
    ventana.asignafuncionBoton(lambda:agregarVH_pedido(ventana, bbdd), lambda:cancelar(ventana))
    ventana.rootAux.destroy()

def agregarVH_pedido(ventana, bbdd):
    #Se recogen los datos de la fila
    datos = [ventana.varChasis.get(),
            ventana.varFecha.get()]
        
    tiempos =[]
    for clave, valor in glo.strVar_nuevosTiemposVeh.items():    
        tiempos.append(valor.get())
    
    id_modelo=BBDD.obtener_id_modelo(bbdd, ventana.varModelo.get())

    datos.extend([id_modelo,
                ventana.varColor.get(),
                ventana.varEstado.get(),
                ventana.varNoved.get(),
                ventana.varSubcon.get(),
                ventana.varPedido.get()]
                )

    for dato in datos:
        print (dato)
    BBDD.insertar_vehiculo(bbdd,*datos)



    id_procesos = BBDD.obtener_id_procesos(bbdd)
    id_procesos.sort()
    #insertamos en la tabla de tiempos_vehiculoss
    for id_proceso, tiempo in zip(id_procesos, tiempos):
        proc_chasis = f"{id_proceso}-{datos[0]}"
        BBDD.insertar_tiempo_vehiculo(bbdd,
                                    proc_chasis, 
                                    id_proceso,
                                    datos[0],
                                    tiempo)

    ventana.rootAux.destroy()   #cerramos la ventana auxiliar
    
    #actualizamos el frame de modelos en la ventana
    #glo.stateFrame.contenidoDeModelos.actualizar_contenido(bbdd)




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
            ventana.varPedido.get()
    )
    print(chasis_anterior)

    for dato in datos:
        print (dato)
    #Modifica el registro en la base de datos
    CRUD.modificar_vehiculo(datos, chasis_anterior)
    ventana.rootAux.destroy()

def recoger_datos_vehiculo(id_chasis):
    return CRUD.leer_vehiculo(id_chasis)

def modificar_vehiculo_pedido(chasis_anterior):
    ventana = ventanas_auxiliares.VentanaGestionaVehiculos("MODIFICAR")
    valores = recoger_datos_vehiculo(chasis_anterior)
    print(valores)
    ventana.set_values(valores, 'MODIFICAR')
    ventana.asignafuncionBoton(lambda:modificarVH_en_BBDD(ventana, chasis_anterior), lambda:cancelar(ventana))
    ventana.rootAux.destroy()

def eliminar_VH_pedido(chasis):
    if ventanas_emergentes.msg_eliminar_vh(chasis) == "Aceptar":
        CRUD.eliminar_vehiculo(chasis)



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




############################################EVENTOS CON NUEVA BASE DE DATOS####################################


def guardar_modeloCRUD(ventana, bbdd):
    print(ventana)
    datos = (ventana.varMarca.get(),
            ventana.varModelo.get())
    for clave, valor in glo.dicc_variables.strVar_nuevosTiemposMod.items():
        datos.append(valor.get())

    CRUD.insertar_modelo(*datos)
    ventana.rootAux.destroy()