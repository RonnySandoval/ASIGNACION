import tkinter as tk
import re
import CRUD
import BBDD
import glo
import ventanas_auxiliares
import ventanas_emergentes
import Mod_clases, Mod_objetos
import modelo_clases, modelo_instancias
import modelo_llamarGantt
import fechahora

#####################################################################
################EVENTOS PARA SECCION DE MODELOS######################
#####################################################################
def crear_modelo(bbdd):
    print("pusó el botón crear modelo")
    ventana = ventanas_auxiliares.VentanaCreaEditaModelo("CREAR", bbdd)              #Llamar al constructor del objeto ventana
    ventana.asignafuncion(funcionGuardar  = lambda:guardar_modelo_nuevo(ventana, bbdd),
                               funcionCancelar = lambda:cancelar(ventana))    #asignar los botones de guardar y cancelar en la ventana

def recoger_datos_modelo(filaBoton, bbdd):
    print(filaBoton)
    fila = re.search(r'(\d+)$', filaBoton).group(1)                             #extraer el numero de la fila
    marca_modelo = glo.lbl_Modelos[f"labelVehiculo{fila}"].cget("text")         #obtener la marca y el modelo apartir del numero de la fila
    marca = re.search(r'^(.*?)\s*-\s*(.*?)$', marca_modelo).group(1).strip()    #expresion regular para truncar solo la marca
    modelo = re.search(r'^(.*?)\s*-\s*(.*?)$', marca_modelo).group(2).strip()   #expresion regular para truncar solo el modelo
    print(f"marca={marca} modelo={modelo}")         
    
    
    tiempos={}
    procesos = BBDD.leer_procesos(bbdd)
    columna = 1
    for proceso in procesos:
        try:
            tiempos[proceso] = glo.ent_Tiempos[f"ExtryTime{fila}_{columna}_{proceso}"].get() #obtiene el tiempo de proceso y lo agrega al diccionario
            columna += 1
        except Exception as e:
            print(f"La clave ExtryTime{fila}_{columna}_{proceso} no está en el diccionario de tiempos")
            print(e)

    print(tiempos)
    diccDatos = {"marca": marca, "modelo": modelo}
    diccDatos.update(tiempos)
    return diccDatos

def editar_modelo(botonPulsado, bbdd):
    print(recoger_datos_modelo(botonPulsado, bbdd))
    datos = recoger_datos_modelo(botonPulsado, bbdd)                         # llamar a la función que recoge los datos de los entry en el panel de modelos
    ventana = ventanas_auxiliares.VentanaCreaEditaModelo("EDITAR", bbdd)     # Llamar al constructor del objeto ventana para editar el modelo
    ventana.set_values(datos)                                                # llamar al metodo del objeto ventana creada, que llena los campos de modelo y tiempos
    ventana.asignafuncion(lambda:guardar_modelo_actualizado(ventana, bbdd), lambda:cancelar(ventana))    #asignar los botones de guardar y cancelar en la ventana

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

def agregar_vehiculo(botonPulsado, bbdd):
    datos = recoger_datos_modelo(botonPulsado, bbdd)
    print(datos)
    ventana = ventanas_auxiliares.VentanaGestionaVehiculos("AGREGAR", bbdd)
    ventana.set_values(datos, None, "AGREGAR")
    ventana.asignafuncion(lambda:aceptar_agregar_vehiculo(ventana, bbdd), lambda:cancelar(ventana))

def aceptar_agregar_vehiculo(ventana, bbdd):
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

def ventana_infoVehiculo(chasisVh, bbdd):
    lecturaRegistros = BBDD.leer_historico(bbdd, chasisVh)
    datosVehiculo = BBDD.leer_vehiculo(bbdd, chasisVh)

    nombresTecnicos = {}
    for tecnico in  BBDD.leer_tecnicos_modificado(bbdd):
        nombresTecnicos[tecnico[0]] = tecnico[1]            # Adicionar solo id y nombre al diccionario de tecnicos en base a la lectura de BBDD

    registros_modificados = []

    for registro in lecturaRegistros:
        id_tecnico = registro[2]                         # Tomar el tercer elemento de la tupla
        
        if id_tecnico in nombresTecnicos:                                    # Si el tercer elemento coincide con una clave en NombresTecnicos
            registro_modificado = list(registro)                                # Convertir la tupla en una lista para poder modificarla
            registro_modificado[2] = nombresTecnicos[id_tecnico]             # Reemplazar el tercer elemento con el valor correspondiente en NombresTecnicos
            registros_modificados.append(tuple(registro_modificado))     # Volver a convertir la lista a tupla y agregarla a la lista de resultados
       
        else:
            registros_modificados.append(registro)                       # Si no hay coincidencia, agregar el registro original

    for registro in lecturaRegistros:
        print("lectura", registro)

    if len(registros_modificados)==0:           #Si no hay registros
        ventanas_emergentes.messagebox.showinfo(
            title="Información de Vehículo",
            message="No hay registros históricos del vehiculo con chasis "+ chasisVh)
        
    else:
        ventana = ventanas_auxiliares.VentanaMuestraInfoVH(bbdd, registros_modificados, datosVehiculo)
        ventana.asignafuncionBoton(lambda:cancelar(ventana))

#####################################################################
################### EVENTOS PARA SECCION TÉCNICOS ###################
#####################################################################
def recoge_estados_check():

    checktecnicos = {}     # Crear un nuevo diccionario temporal para almacenar las claves modificadas
    print(glo.intVar_tecnicos.items())
    for clave, var in glo.intVar_tecnicos.items():
        nueva_clave = re.sub(r'.*?-', '', clave)   # Expresión regular para eliminar desde el guión hacia atrás
        checktecnicos[nueva_clave] = var.get()     # Actualizar el valor en el diccionario temporal con la nueva clave y el valor actual de IntVar

    print(checktecnicos)
    return checktecnicos

def guardar_tecnico_nuevo(ventana, bbdd):
    #Recoger los datos agregados del nuevo tecnico
    datos = (ventana.varNombre.get(),
             ventana.varApellido.get(),
             ventana.varDocumento.get(),
             ventana.varEspecialidad.get())
    
    ParteEsp = datos[3][:3].lower() if len(datos[2]) >= 3 else datos[2].lower()     # Extraer primeras 3 letras dela especialidad
    ParteDoc = datos[2][-4:] if len(datos[3]) >= 4 else datos[3]                    # extraer las ultimos 4 numeros del documento

    idTecnico = ParteEsp + ParteDoc + datos[0]                                      # construir un id con la especialidad, documento y nombre

    print(datos)
    BBDD.insertar_tecnico(bbdd, idTecnico, *datos)                                  # insertar el registro del técnico en BD

    ventana.rootAux.destroy()

def eliminar_tecnico_BD(ventana, bbdd):
    nombreTecnico = ventana.varTecnico.get()        # obtener el técnico seleccionado
    idTecnico = ventana.ids_tecnicos.get(nombreTecnico) # obtiene la clave con el id de acuerdo al valor con nombre completo de técnico
    if ventanas_emergentes.ms_eliminar_tec(id_tecnico = idTecnico, nombre = nombreTecnico) == "Aceptar":
        BBDD.eliminar_tecnico(bbdd, idTecnico)          # usar el método de la BD para eliminar
        ventana.rootAux.destroy()                       # cerrar la ventana toplevel

#####################################################################
################### EVENTOS PARA SECCION PROCESOS ###################
#####################################################################
def guardar_proceso_nuevo(ventana, bbdd):
    datos = (ventana.varIdProceso.get(),
             ventana.varNombre.get(),
             ventana.varDescripcion.get(),
             ventana.varSecuencia.get())
    print(datos)
    BBDD.insertar_proceso(bbdd, *datos)

    ventana.rootAux.destroy()

#####################################################################
################EVENTOS PARA SECCION DE VEHICULOS####################
#####################################################################
def leeVehiculosBBDD(bbdd):
    return BBDD.leer_vehiculos_completos(bbdd)

def recoger_datos_vehiculo(chasis, bbdd):
    return BBDD.leer_vehiculo(bbdd, chasis)

def modificar_vehiculo_pedido(chasis_anterior, bbdd):

    datos = list(recoger_datos_vehiculo(chasis_anterior, bbdd))                     #LEER DE LA BASE DATOS EL VEHICULO
    marcamodelo = list(BBDD.leer_modelo(bbdd, datos[2]))
    datos.pop(2)
    datos.insert(2, marcamodelo[1])
    datos.insert(2, marcamodelo[2])
    tiempos = BBDD.leer_tiempos_vehiculo(bbdd, chasis_anterior)                     #LEER LOS TIEMPOS DEL VEHICULO

    print("Los datos en el modulo eventos son: ", datos)
    print("Los tiempos en el modulo eventos son: ", tiempos)
    ventana = ventanas_auxiliares.VentanaGestionaVehiculos("MODIFICAR", bbdd)       #CREAR LA VENTANA EMERGENTE PARA EDITAR EL VEHICULO
    ventana.set_values(datos, tiempos, "MODIFICAR")                                        #AGREGAR LOS DATOS DE LA BBDD A LA VENTANA
    ventana.asignafuncion(lambda:modificarVH_en_BBDD(ventana, chasis_anterior, bbdd), lambda:cancelar(ventana))  #ASIGNAR BOTONES
    ventana.rootAux.destroy()

def modificarVH_en_BBDD(ventana, chasis_anterior, bbdd):
    #Se recogen los datos de la fila
    tiempos = []
    for clave in glo.strVar_nuevosTiemposVeh:
        tiempos.append(glo.strVar_nuevosTiemposVeh[clave].get())
    

    id_modelo = BBDD.leer_vehiculo(bbdd, chasis_anterior)[2]
    datos = (
        ventana.varChasis.get(),
        ventana.varFecha.get(),
        id_modelo,
        ventana.varColor.get(),
        ventana.varEstado.get(),
        ventana.varNoved.get(),
        ventana.varSubcon.get(),
        ventana.varPedido.get(),
    )
    print(chasis_anterior)

    for dato in datos:
        print (dato)
    print(tiempos)
    #Modifica el registro en la base de datos
    BBDD.actualizar_vehiculo(bbdd, *datos, chasis_anterior)

    id_procesos = BBDD.obtener_id_procesos(bbdd)
    id_procesos.sort()
    #insertamos en la tabla de tiempos_vehiculoss
    for id_proceso, tiempo in zip(id_procesos, tiempos):
        proc_chasis_anterior = f"{id_proceso}-{chasis_anterior}"
        proc_chasis = f"{id_proceso}-{datos[0]}"
        BBDD.actualizar_tiempo_vehiculo(bbdd,
                                        proc_chasis, 
                                        id_proceso,
                                        datos[0],
                                        tiempo,
                                        proc_chasis_anterior)

    ventana.rootAux.destroy()   #cerramos la ventana auxiliar

    #ventana.rootAux.destroy()

def eliminar_VH_pedido(chasis):
    if ventanas_emergentes.msg_eliminar_vh(chasis) == "Aceptar":
        CRUD.eliminar_vehiculo(chasis)

def ventana_AsignarUnVehiculo(chasis, bbdd):
    ventana = ventanas_auxiliares.VentanaAsignaVehiculo(chasis, bbdd)
    ventana.asignaFuncion(funcionAceptar = lambda:aceptar_AsignarUnVehiculo(ventana, chasis, bbdd),
                          funcionCancelar = lambda:cancelar(ventana))

def aceptar_AsignarUnVehiculo(ventana, chasisVh, bbdd):
    datos = [ventana.varTecnico.get(),
             ventana.varProceso.get(),
             chasisVh]
    concatenado = ''.join([re.match(r'(.{3})', dato).group(1) for dato in datos if len(dato) >= 3])

    fecha = ventana.varFecha.get()
    hora = ventana.varHora.get()
    observaciones = ventana.varObser.get()

    id_asig = concatenado + fecha + hora
    print(id_asig)
    id_tec = ventana.ids_tecnicos.get(datos[0])    
    id_proc = ventana.ids_procesos.get(datos[1])

    print(id_asig, id_proc, id_tec)
    inicio = fechahora.parseDT(fecha, hora) 
    tiempo = BBDD.leer_tiempo_vehiculo(bbdd, chasisVh, id_proc)
    fin    = fechahora.calcular_hora_finalDT(inicio, tiempo)
    estado = ventana.varEstado.get()

    print(id_asig, id_proc, id_tec, inicio, fin, tiempo)

    BBDD.insertar_historico(bbdd,
                            id_asig,
                            chasisVh,
                            id_tec,
                            id_proc,
                            observaciones,
                            inicio,
                            fin,
                            tiempo,
                            estado)

    ventana.rootAux.destroy()

#####################################################################
################ EVENTOS PARA SECCION DE HISTÓRICOS #################
#####################################################################

def ventanaResumenHistorico(id, bbdd):
    ventana = ventanas_auxiliares.VentanaMuestraInfoHis(id, bbdd)
    ventana.asignafuncionBoton(funcionCerrar = ventana.rootAux.destroy)

def ventanaCambiarEstado(id, bbdd):
    ventana = ventanas_auxiliares.VentanaCambiarEstadoHist(id, bbdd)
    ventana.asignafuncion(funcionAgregar  = lambda: aceptarCambiarEstado(),
                          funcionCancelar = ventana.rootAux.destroy)


def aceptarCambiarEstado():
    pass

def ventana_modificarHistorico(id_anterior, bbdd):
    pass

def ventana_ObserNoved(valores):
    pass
            
def ventana_eliminarHistorico(id_historico):
    pass
#####################################################################
#####################################################################
#####################################################################


def abrirFechayHora(tipoPrograma):
    ventana = ventanas_auxiliares.EstableceFechaHora()
    ventana.asignaFuncion(lambda:aceptarFechayHora(ventana, tipoPrograma), lambda:cancelar(ventana))
    
def aceptarFechayHora(ventana, tipoPrograma):
    fecha = ventana.varFecha.get()
    hora = ventana.varHora.get()
    print(f"Fecha: {fecha}, Hora: {hora}")
    ventana.rootAux.destroy()
    
    if tipoPrograma == "completo":
        Mod_clases.programa_completo(Mod_objetos.pedido_quito06,
                                     Mod_clases.personal,
                                     4000,
                                     fecha,
                                     hora)
        horizonte_calculado = Mod_clases.calcular_horizonte(Mod_objetos.pedido_quito06)
        print(f"el horizonte es {horizonte_calculado}")

        #GRAFICAR PROGRAMACIÓN EN GANTT##########
        modelo_llamarGantt.generar_gantt_tecnicos(Mod_clases.personal,
                                                  fecha,
                                                  hora,
                                                  horizonte_calculado=horizonte_calculado)
        modelo_llamarGantt.generar_gantt_vehiculos(Mod_objetos.pedido_quito06,
                                                   fecha,
                                                   hora,
                                                   horizonte_calculado=horizonte_calculado)
    
    if tipoPrograma == "inmediato":
        Mod_clases.programa_inmediato(Mod_objetos.pedido_quito06,
                                      Mod_clases.personal,
                                      4000,
                                      fecha,
                                      hora)
        horizonte_calculado = Mod_clases.calcular_horizonte(Mod_objetos.pedido_quito06)
        print(f"el horizonte es {horizonte_calculado}")

        #GRAFICAR PROGRAMACIÓN EN GANTT##########
        modelo_llamarGantt.generar_gantt_tecnicos(Mod_clases.personal,
                                                  fecha,
                                                  hora,
                                                  horizonte_calculado=horizonte_calculado)
        modelo_llamarGantt.generar_gantt_vehiculos(Mod_objetos.pedido_quito06,
                                                   fecha, hora,
                                                   horizonte_calculado=horizonte_calculado)

    if tipoPrograma == "por procesos":
        modelo_clases.programa_por_proceso(pedido     = modelo_instancias.pedido,
                                           tecnicos   = modelo_clases.personal,
                                           procesos   = "",
                                           horizonte  = 4000,
                                           fechaStart = fecha,
                                           horaStart  = hora,
                                           bbdd       = glo.base_datos)
        horizonte_calculado = modelo_clases.calcular_horizonte(modelo_instancias.pedido)
        print(f"el horizonte es {horizonte_calculado}")

        #GRAFICAR PROGRAMACIÓN EN GANTT##########
        modelo_llamarGantt.generar_gantt_tecnicos(personal   = modelo_clases.personal,
                                                  fechaStart = fecha,
                                                  horaStart  = hora,
                                                  horizonte_calculado=horizonte_calculado)
        modelo_llamarGantt.generar_gantt_vehiculos(pedido     =modelo_instancias.pedido,
                                                   fechaStart =fecha,
                                                   horaStart  =hora,
                                                   horizonte_calculado=horizonte_calculado)

    

def nombraArchivoExcel(programa):
    return programa + 'Numero__' + '.xlsx'

def cancelar(ventana):
    ventana.rootAux.destroy()

############################################EVENTOS CON ANTIGUA BASE DE DATOS####################################
