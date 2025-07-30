import re
import pandas as pd
import tkinter as tk
import os
import datetime
from tkinter.filedialog import askopenfilename

import database.BDcreate as BDcreate
import database.BDqueries as BDqueries
import controller.glo as glo
import controller.exception_manejar as e
import menu.stepsNuevaPlanta as steps_nueva_planta
import menu.ventanaNuevaPlanta as ventanaNuevaPlanta
import model.model_classPlant    as model_classPlant
import model.model_instancePlant as model_instancePlant
import model.model_callGantt     as model_callGantt
import model.model_datetime      as model_datetime
import model.model_gantt         as model_gantt
import view.ventanas_topLevel as ventanas_topLevel
import view.ventanas_emergentes as ventanas_emergentes
from view.estilos import *

#################################################################################################################################
######################### EVENTOS PARA PLANTA #############################################################################
#################################################################################################################################
@e.manejar_errores("---Abrir planta. Seleccionando de archivo.db de planta a abrir---")
def abrir_planta():
    ruta = askopenfilename(title="Seleccionar la Planta",
                            filetypes=[("Archivos Base de datos sqlite", "*.db")])
    print(ruta)
    glo.base_datos = os.path.basename(ruta)
    glo.turnos.set_times()
    glo.actualizar_todo()

@e.manejar_errores("---Crear planta. En el Paso que abre la ventana para ingresar los campos---")
def step_crearNuevaPlanta():
    
    ventana = ventanaNuevaPlanta.VentanaNuevaPlanta()
    ventana.asignafuncion(funcionCancelar   = ventana.rootAux.destroy,
                          funcionVistaPrevia= lambda: step_CargarTodo(ventana))

@e.manejar_errores("---Crear planta, Cargando todo. Recogiendo el archivo de Excel y muestra en una ventana con la vista previa---")
def step_CargarTodo(ventana):
    ruta = ventana.ruta
    nombre= ventana.varNombre.get()
    descripcion = ventana.varDescripcion.get()
    iniciaAM    = ventana.varInicio_AM.get()
    terminaAM   = ventana.varTermino_AM.get()
    iniciaPM    = ventana.varInicio_PM.get()
    terminaPM   = ventana.varTermino_PM.get()

    ventana.rootAux.destroy()
    hojas = pd.read_excel(ruta, sheet_name=None)
    dataframes = {}                                 # Crear un diccionario para guardar los DataFrames con nombres de hojas
    for nombre_hoja, dataframe in hojas.items():    # Iterar sobre cada hoja
        # Limpiar filas o columnas vacías
        dataframe = dataframe.dropna(how='all')  # Elimina filas completamente vacías
        dataframe = dataframe.loc[:, dataframe.columns.notna()]  # Elimina columnas vacías
        
        # Guardar en el diccionario
        dataframes[nombre_hoja] = dataframe
        
        print(f"Hoja: {nombre_hoja}")
        print(f"Encabezados: {list(dataframe.columns)}")
        print(dataframe, "\n")
    
    ventVistaPrevia = steps_nueva_planta.VentanaPreviewLoad(dataframes)
    ventVistaPrevia.asignafuncion(funcionAceptar = lambda : crear_plantaBD( dataframes  = dataframes,
                                                                            name        = nombre,
                                                                            description = descripcion,
                                                                            iniciaAM    = iniciaAM,
                                                                            terminaAM   = terminaAM,
                                                                            iniciaPM    = iniciaPM,
                                                                            terminaPM   = terminaPM,
                                                                            ventana     = ventVistaPrevia),
                                  funcionCancelar=ventVistaPrevia.rootAux.destroy)

@e.manejar_errores("---Crear planta. Generando los dataframe necesarios para nueva planta y/o cargando en base de datos---")
def crear_plantaBD(dataframes, name, description, iniciaAM, terminaAM, iniciaPM, terminaPM,ventana):
    df_procesos     = dataframes["PROCESOS"]
    df_tecnicos     = dataframes["TECNICOS"]
    #df_modelos      = dataframes["MARCAS_MODELOS"]
    df_referencias  = dataframes["MODELOS_REFERENCIAS"]
    df_tiempos_modelos = dataframes["TIEMPOS_MODELOS"]
    ventana.rootAux.destroy()

    #df_tiempos_modelos = genera_tiempos_modelos_default(df_modelos, df_procesos)

    df_tecnicos["ID_TECNICO"] = df_tecnicos.apply(lambda row:genera_idTecnico(row["NOMBRE"], row["APELLIDO"], row["DOCUMENTO"]), axis=1)
    df_tiempos_modelos["ID_MODELO"] = df_tiempos_modelos.apply(lambda row:genera_idModelo(row["MARCA"], row["MODELO"]), axis=1)
    df_modelos = df_tiempos_modelos[["ID_MODELO", "MARCA", "MODELO"]]

    df_procesos = elimina_Duplicados_df(df_procesos, "ID_PROCESO")[0]
    df_tecnicos = elimina_Duplicados_df(df_tecnicos, "ID_TECNICO")[0]
    df_modelos = elimina_Duplicados_df(df_modelos, "ID_MODELO")[0]
    df_referencias = elimina_Duplicados_df(df_referencias, "REFERENCIA")[0]

    df_merged = pd.merge(df_referencias, df_tiempos_modelos, on='MODELO', how='left')       # Realiza el merge entre df_referencias y df_modelos
    df_referencias = df_merged [['REFERENCIA', 'ID_MODELO']]                            # Reasigna el dataframe

    df_tecnicos, df_tecnicos_procesos = genera_df_tecnicos_proceso(df_tec = df_tecnicos, df_proc=df_procesos)
    df_tiempos_modelos = transformar_dataframe_tiempos(df_tiempos_modelos, "MODELO")
    df_tiempos_modelos = elimina_Duplicados_df(df_tiempos_modelos, "PROCESO_MODELO")[0]

    print(df_procesos)
    print(df_tecnicos)
    print(df_tecnicos_procesos)
    print(df_modelos)
    print(df_referencias)
    print(df_tiempos_modelos)
    base_datos = BDcreate.crea_BBDD(nombre = name)
    if base_datos == "existe":
        return
    
    BDqueries.insertar_info_planta(bbdd = base_datos,
                              nombre = name,
                              descripcion = description,
                              iniciaAM = iniciaAM,
                              terminaAM = terminaAM,
                              iniciaPM = iniciaPM,
                              terminaPM = terminaPM)
    ins_proce  = BDqueries.insertar_procesos_df(bbdd = base_datos, dataframe=df_procesos)
    ins_tecni  = BDqueries.insertar_tecnicos_df(bbdd = base_datos, dataframe=df_tecnicos)
    ins_tecpr  = BDqueries.insertar_tecnicos_procesos_df(bbdd = base_datos, dataframe=df_tecnicos_procesos)
    ins_model  = BDqueries.insertar_modelos_df(bbdd = base_datos, dataframe=df_modelos)  
    ins_refer  = BDqueries.insertar_referencias_df(bbdd = base_datos, dataframe=df_referencias)
    ins_timod  = BDqueries.insertar_tiempos_modelos_df(bbdd = base_datos, dataframe=df_tiempos_modelos)

    no_insertados = []
    if ins_proce is False:
        no_insertados.append("procesos")
        print("No se insertaron los registros de procesos")
    if ins_tecni is False:
        no_insertados.append("tecnicos")
        print("No se insertaron los registros de tecnicos")
    if ins_tecpr is False:
        no_insertados.append("especialidades")
        print("No se insertaron los registros de especialidad de tecnicos")
    if ins_model is False:
        no_insertados.append("modelos")
        print("No se insertaron los registros de procesos")
    if ins_refer is False:
        no_insertados.append("referencias")
        print("No se insertaron los registros de referencias de modelos")
    if ins_timod is False:
        no_insertados.append("tiempos_modelos")
        print("No se insertaron los registros de tiempos de modelos")

    if no_insertados != []:
        ventanas_emergentes.messagebox.showinfo("Registros NO añadidos",
                                            f"""No se añadieron los registros de {no_insertados}.
                                            Revisar en la entrada de datos de Excel,que coincidan las tablas de modelos y de referencias, así como la de técnicos con la de procesos""")
        return
    
    ventanas_emergentes.messagebox.showinfo("Registros añadidos",
                                            """Se añadieron con éxito todos los registros de procesos, técnicos, modelos, referencias y tiempos.""")
    

    glo.turnos.set_times()
    glo.actualizar_todo()

@e.manejar_errores("---Crear planta. Transformando el df de tecnicos y procesos en los que recibe la base de datos---")
def genera_df_tecnicos_proceso(df_tec, df_proc): 
    especialidad_cols = df_tec.filter(like='ESPECIALIDAD').columns                             # Filtrar columnas que contienen 'ESPECIALIDAD'
    df_tecnicos = df_tec.loc[:, ~df_tec.columns.str.contains('ESPECIALIDAD')]                  # Eliminar las columnas que contienen la cadena 'ESPECIALIDAD'
    df_tecnicos = df_tecnicos[["ID_TECNICO", "NOMBRE", "APELLIDO","DOCUMENTO"]]                # Reordenamos las columnas
    df_tecnicos["ESPECIALIDAD"] = df_tec[especialidad_cols].apply(lambda row:
                                                               ", ".join(row.dropna().
                                                                         astype(str)), axis=1) # Crear listas con valores de 'ESPECIALIDAD'
    especialidades_columns = df_tec.columns[df_tec.columns.str.contains('ESPECIALIDAD')]        # Obtenemos las columnas 'ESPECIALIDAD', 'ESPECIALIDAD.1', etc.
    
    df_tecnicos_procesos = pd.DataFrame(columns=['TEC_PROC', 'ID_TECNICO', 'ID_PROCESO'])      # Ahora creamos un DataFrame donde concatenamos ID_TECNICO con las especialidades
    ids_procesos = df_proc.set_index('NOMBRE')['ID_PROCESO'].to_dict()


    for col in especialidades_columns:                                                         # Iteramos sobre las columnas de especialidades para generar el nuevo DataFrame
        temp_df = df_tec[['ID_TECNICO', col]].dropna(subset=[col])                             # Eliminamos filas con valores nulos en esa especialidad
        temp_df['ID_PROCESO']=temp_df[col].map(ids_procesos)                                   # Asignamos el valor del id para la especialidad a ID_PROCESO
        temp_df['TEC_PROC'] = temp_df['ID_TECNICO'] + temp_df['ID_PROCESO']                    # Concatenamos ID_TECNICO y el valor de la especialidad
        temp_df = temp_df[['TEC_PROC', 'ID_TECNICO', 'ID_PROCESO']]                            # Reordenamos las columnas
        df_tecnicos_procesos = pd.concat([df_tecnicos_procesos, temp_df], ignore_index=True)   # Concatenamos al DataFrame final

    # Mostrar los resultados
    print("\nDataFrame Limpio (sin las columnas 'ESPECIALIDAD'):")
    print(df_tecnicos)
    print("\nNuevo DataFrame 'df_tecnicos_procesos':")
    print(df_tecnicos_procesos)

    return df_tecnicos, df_tecnicos_procesos

@e.manejar_errores("---Crear planta. Generando un df con tiempos_proceso en 0")
def genera_tiempos_modelos_default(df_modelos, df_procesos):
    df_combinaciones = pd.merge(df_modelos[['ID_MODELO']],    # Crear el DataFrame con las combinaciones deseadas
                                df_procesos[['ID_PROCESO']],
                                how='cross')
    df_combinaciones['PROCESO_MODELO'] = df_combinaciones['ID_MODELO']+ '-' + df_combinaciones['ID_PROCESO']    # Crear la columna 'PROCESO_MODELO'
    df_combinaciones = df_combinaciones[['PROCESO_MODELO',    # Resultado final
                                         'ID_PROCESO',
                                         'ID_MODELO']]
    df_combinaciones['TIEMPO'] = 0                            # Añadir tiempos por defecto
    print(df_combinaciones)                                   # Mostrar el resultado
    return df_combinaciones

def editar_planta_BD(ventana, bbdd):
    nombre      = ventana.varNombre.get()
    descripcion = ventana.entryDescripcion.get(index1="1.0")
    iniciaAM    = ventana.varInicia_AM.get()
    terminaAM   = ventana.varTermina_AM.get()
    iniciaPM    = ventana.varInicia_PM.get()
    terminaPM   = ventana.varTermina_PM.get()
    ventana.rootAux.destroy()

    BDqueries.actualizar_planta_info(bbdd, nombre, descripcion , iniciaAM, terminaAM , iniciaPM, terminaPM)
    ventanas_emergentes.messagebox.showinfo("Planta Actualizada", "Se ha actualizado la información básica de la Planta")
    glo.actualizar_todo()

#####################################################################################################################
################EVENTOS PARA SECCION DE MODELOS######################################################################
#####################################################################################################################
@e.manejar_errores("---Crear Modelo. Abriendo ventana para nuevo modelo---")
def crear_modelo(bbdd):
    print("pusó el botón crear modelo")
    ventana = ventanas_topLevel.VentanaCreaEditaModelo("CREAR", bbdd)              #Llamar al constructor del objeto ventana
    ventana.asignafuncion(funcionGuardar  = lambda:guardar_modelo_nuevo(ventana, bbdd),
                               funcionCancelar = lambda:cancelar(ventana))    #asignar los botones de guardar y cancelar en la ventana

@e.manejar_errores("---Crear (Guardar) Modelo. Tomando datos de ventana y almacenando de Base de datos---")
def guardar_modelo_nuevo(ventana, bbdd):
    print(ventana)
    datos = (ventana.varMarca.get(),
            ventana.varModelo.get())        #NOMBRES DE MARCA Y MODELO
    
    tiempos =[]             #SE CREA Y LLENA UNA LISTA CON LOS TIEMPOS DE PROCESO
    for clave, valor in glo.strVar_nuevosTiemposMod.items():    
        tiempos.append(valor.get())
    
    #OBTENEMOS ID DE MODELOS Y PROCESOS
    id_modelo = f"{datos[0]}-{datos[1]}"
    id_procesos = BDqueries.obtener_id_procesos(bbdd)
    id_procesos.sort()
    #Insertamos en la tabla de modelos
    BDqueries.insertar_modelo(bbdd, id_modelo, datos[0], datos[1])

    #insertamos en la tabla de timepos modelos
    for id_proceso, tiempo in zip(id_procesos, tiempos):
        proc_model = f"{id_proceso}-{datos[0]}-{datos[1]}"
        BDqueries.insertar_tiempo_modelo(bbdd,
                                    proc_model, 
                                    id_proceso,
                                    id_modelo,
                                    tiempo)

    ventana.rootAux.destroy()   #cerramos la ventana auxiliar
    
    #actualizamos el frame de modelos en la ventana
    glo.stateFrame.contenidoDeModelos.actualizar_contenido(bbdd)

@e.manejar_errores("---Crear Modelo. Recogiendo datos del modelo del panel---")
def recoger_datos_modelo(filaBoton, bbdd):
    print(filaBoton)
    fila = re.search(r'(\d+)$', filaBoton).group(1)                             #extraer el numero de la fila
    marca_modelo = glo.lbl_Modelos[f"labelVehiculo{fila}"].cget("text")         #obtener la marca y el modelo apartir del numero de la fila
    marca = re.search(r'^(.*?)\s*-\s*(.*?)$', marca_modelo).group(1).strip()    #expresion regular para truncar solo la marca
    modelo = re.search(r'^(.*?)\s*-\s*(.*?)$', marca_modelo).group(2).strip()   #expresion regular para truncar solo el modelo
    print(f"marca={marca} modelo={modelo}")         
    
    tiempos={}
    nombresProcesos = BDqueries.leer_procesos_nombres(bbdd)                                               #lee los noombres de los procesos
    infoProcesos = BDqueries.leer_procesos_completo(bbdd)                                         #lee toda la información de los procesos
    idsProcesos = [proceso[0] for proceso in infoProcesos]         #crea unalista con ids de acuerdo al primer elemento de la lista infoProcesos
    nombresProcesos = [proceso[1] for proceso in infoProcesos]  #crea una lista solo con los nombres de los procesos cuyos ids aparecen en el dataframe
    nombresProcesos.sort()
    columna = 1
    for proceso in nombresProcesos:
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

@e.manejar_errores("---Editar Modelo. Abriendo una ventana para modificar datos de modelo---")
def editar_modelo(botonPulsado, bbdd):
    print(recoger_datos_modelo(botonPulsado, bbdd))
    datos = recoger_datos_modelo(botonPulsado, bbdd)                         # llamar a la función que recoge los datos de los entry en el panel de modelos
    ventana = ventanas_topLevel.VentanaCreaEditaModelo("EDITAR", bbdd)       # Llamar al constructor del objeto ventana para editar el modelo
    ventana.set_values(datos)                                                # llamar al metodo del objeto ventana creada, que llena los campos de modelo y tiempos
    ventana.asignafuncion(lambda:guardar_modelo_actualizado(ventana, datos, bbdd), lambda:cancelar(ventana))    #asignar los botones de guardar y cancelar en la ventana

@e.manejar_errores("---Editar Modelo. Actualizando en la base de datos los datos modificados del modelo y sus tiempos---")
def guardar_modelo_actualizado(ventana, datos_iniciales, bbdd):

    id_modelo_actual = datos_iniciales["marca"]+ "-" + datos_iniciales["modelo"]
    datos = list((ventana.varMarca.get(),
                  ventana.varModelo.get()))
    
    tiempos =[]             #SE CREA Y LLENA UNA LISTA CON LOS TIEMPOS DE PROCESO
    for clave, valor in glo.strVar_nuevosTiemposMod.items():    
        tiempos.append(valor.get())
    print("Diccionario de tiempos que sobreescribirán: ", glo.strVar_nuevosTiemposMod)



    idModelo = f"{datos[0]}-{datos[1]}"                     # OBTENEMOS ID DE MODELOS Y PROCESOS
    id_procesos = BDqueries.obtener_id_procesos(bbdd)            # leemos en la base de datos los IDS de los procesos
    id_procesos.sort()                                      # ordenamos la lista de id's procesos

    BDqueries.actualizar_modelo(bbdd         = bbdd,             # Insertamos en la tabla de modelos
                           id_anterior  = id_modelo_actual, 
                           marca        = datos[0],
                           modelo       = datos[1],
                           id_nuevo     = idModelo)


    registroTiemposProcesos = BDqueries.leer_ids_proceso_modelo(bbdd, id_modelo_actual)      # leemos los registros de tiempos para el modelo (una lista de tuplas con los ids de procesos y modelos)
    idProcesosConTiempo = [registro[1] for registro in registroTiemposProcesos]         # recolectamos solo los id's de procesos que tienen registro de tiempo en la BBDD
    idProcesosConTiempo.sort()                                                          # ordenamos la lista de id's de procesos con tiempos
    ids_proceso_modelo  = [registro[0] for registro in registroTiemposProcesos]         # recolectamos los los id's proceso_modelo que tienen registro de tiempo
    ids_proceso_modelo.sort()                                                           # ordenamos la lista de id's de proceso_modelo con registro de tiempos

    ids_procesos_sinTiempos = [ids for ids in id_procesos + idProcesosConTiempo
                              if (ids not in id_procesos or ids not in idProcesosConTiempo)]    # creamos una lista con los id's de procesos que NO tienen registros de tiempos de BBDD

    print("registroTiemposProcesos: ", registroTiemposProcesos)
    print("idProcesosConTiempo: ", idProcesosConTiempo)
    print("ids_procesos_sinTiempos: ", ids_procesos_sinTiempos)
    print("ids_proceso_modelo: ", ids_proceso_modelo)
    print("id_procesos: ", id_procesos)
    


    for idProceso in ids_procesos_sinTiempos:                                         #insertamos un tiempo = 0 para aquel proceso sin registor de tiempos del modelo
        procModelo = f"{idProceso}-{datos[1]}"
        BDqueries.insertar_tiempo_modelo(bbdd        = bbdd,
                                    procmodel   = procModelo, 
                                    id_proceso  = idProceso,
                                    id_modelo   = idModelo,
                                    tiempo      = 0)

    # actualizamos enla tabla de tiempos_modelos
    for idProceso, time, proceso_modelo in zip(id_procesos, tiempos, ids_proceso_modelo):
        procModelo = f"{idProceso}-{datos[1]}"
        BDqueries.actualizar_tiempo_modelo(bbdd       =   bbdd,
                                      procmodel  =   procModelo, 
                                      id_proceso =   idProceso,
                                      id_modelo  =   idModelo,
                                      tiempo     =   time,
                                      procmodelo_anterior=proceso_modelo)
    
    ventana.rootAux.destroy()
    glo.stateFrame.contenidoDeModelos.actualizar_contenido(bbdd)    #actualizamos el frame de modelos en la ventana

@e.manejar_errores("---Agregar Modelo. Abriendo una toplevel para agregar un vehiculo en base al modelo---")
def agregar_vehiculo(botonPulsado, bbdd):
    datos = recoger_datos_modelo(botonPulsado, bbdd)
    print(datos)
    ventana = ventanas_topLevel.VentanaGestionaVehiculos("AGREGAR", bbdd)
    ventana.set_values(datos, None, "AGREGAR")
    ventana.asignafuncion(lambda:aceptar_agregar_vehiculo(ventana, bbdd), lambda:cancelar(ventana))

@e.manejar_errores("---Agregar Vehiculo. Recogiendo datos datos de vehiculo y sus tiempos y almacenando en la base de datos---")
def aceptar_agregar_vehiculo(ventana, bbdd):
    #Se recogen los datos de la fila
    datos = [ventana.varChasis.get(),
            ventana.varFecha.get()]
        
    tiempos =[]
    for clave, valor in glo.strVar_nuevosTiemposVeh.items():    
        tiempos.append(valor.get())
    
    id_modelo=BDqueries.obtener_id_modelo(bbdd, ventana.varModelo.get())

    datos.extend([id_modelo,
                ventana.varColor.get(),
                ventana.varNoved.get(),
                ventana.varSubcon.get(),
                ventana.varPedido.get()]
                )

    for dato in datos:
        print (dato)
    BDqueries.insertar_vehiculo(bbdd,*datos)

    id_procesos = BDqueries.obtener_id_procesos(bbdd)
    id_procesos.sort()
    #insertamos en la tabla de tiempos_vehiculoss
    for id_proceso, tiempo in zip(id_procesos, tiempos):
        proc_chasis = f"{id_proceso}-{datos[0]}"
        BDqueries.insertar_tiempo_vehiculo(bbdd,
                                    proc_chasis, 
                                    id_proceso,
                                    datos[0],
                                    tiempo)

    ventana.rootAux.destroy()   #cerramos la ventana auxiliar
    
    #actualizamos el frame de vehiculos en la ventana
    for frame in (glo.stateFrame.contenidoDeVehiculos, glo.stateFrame.contenidoDeDetalles):
        frame.actualizar_tabla(bbdd)

@e.manejar_errores("---Eliminar Modelo. Abriendo una ventana para eliminar un modelo y sus tiempos y guardar cambios en base de datos---")
def eliminar_modelo_BD(ventana, bbdd):
    modeloDelete = ventana.varItem.get()
    vehiCoinciden = BDqueries.leer_vehiculo_por_modelo(bbdd, modeloDelete)
    if ventanas_emergentes.msg_eliminar_mod(modelo = modeloDelete, vehiculos = vehiCoinciden) == "Aceptar":
        BDqueries.eliminar_modelo_completo(bbdd, modelo = modeloDelete)          # usar el método de la BD para eliminar
        for vehiculo in vehiCoinciden:
            BDqueries.eliminar_vehiculo_completo(bbdd, chasis = vehiculo[0])
        ventana.rootAux.destroy()                                         # cerrar la ventana toplevel

#####################################################################################################################
################## EVENTOS PARA SECCION REFERENCIAS #################################################################
#####################################################################################################################

@e.manejar_errores("---Crear Referencia. Abriendo una ventana para crear una nueva referencia---")
def crear_referencia(bbdd):
    print("pusó el botón crear referencia")
    ventana = ventanas_topLevel.VentanaCreaEditaReferencia("CREAR", bbdd)              #Llamar al constructor del objeto ventana
    ventana.asignafuncion(funcionGuardar  = lambda:guardar_referencia_nueva(ventana, bbdd),
                               funcionCancelar = lambda:cancelar(ventana))            # asignar los botones de guardar y cancelar en la ventana

@e.manejar_errores("---Crear Referencia. Recogiendo datos de la nueva referencia y guardandolos en la base de datos---")
def guardar_referencia_nueva(ventana, bbdd):
    print(ventana)
    datos = (ventana.varReferencia.get(),       #recogemos los datos de la ventana
             ventana.varMarcaModelo.get())
    
    BDqueries.insertar_referencia(bbdd, *datos)
    ventana.rootAux.destroy()   #cerramos la ventana auxiliar
    
    #actualizamos el frame de modelos en la ventana
    glo.stateFrame.contenidoDeReferencias.actualizar_contenido(bbdd)

@e.manejar_errores("---Editar Referencia. Recogiendo datos de la referencia del panel---")
def recoger_datos_referencia(filaBoton, bbdd):
    print(filaBoton)
    fila = re.search(r'(\d+)$', filaBoton).group(1)                           #extraer el numero de la fila
    marca_modelo = glo.lbl_IdModelos[f"labelIdModelo{fila}"].cget("text")     #obtener la marca y el modelo apartir del numero de la fila
    referencia = glo.lbl_Referencias[f"labelReferencia{fila}"].cget("text")   #obtener la marca y el modelo apartir del numero de la fila
     
    diccDatos = {"marca_modelo": marca_modelo, "referencia": referencia}
    print(diccDatos)
    return diccDatos

@e.manejar_errores("---Editar Referencia. Abriendo una ventana para modificar datos de referencia---")
def editar_referencia(botonPulsado, bbdd):
    datos = recoger_datos_referencia(botonPulsado, bbdd)                         # llamar a la función que recoge los datos de los entry en el panel de modelos
    ref_anterior = datos["referencia"]
    print(datos)
    ventana = ventanas_topLevel.VentanaCreaEditaReferencia("EDITAR", bbdd)       # Llamar al constructor del objeto ventana para editar el modelo
    ventana.set_values(datos)                                                    # llamar al metodo del objeto ventana creada, que llena los campos de modelo y tiempos
    ventana.asignafuncion(lambda:guardar_referencia_actualizada(ventana, ref_anterior, bbdd),
                          lambda:cancelar(ventana))    #asignar los botones de guardar y cancelar en la ventana

@e.manejar_errores("---Editar Referencia. Actualizando en la base de datos los datos modificados de la referencia---")
def guardar_referencia_actualizada(ventana, ref_inicial, bbdd):

    print(ref_inicial)
    datos = (ventana.varReferencia.get(),       #recogemos los datos de la ventana
             ventana.varMarcaModelo.get())
    print(datos, ref_inicial)

    BDqueries.actualizar_referencia(bbdd, *datos, ref_inicial)
    ventana.rootAux.destroy()   #cerramos la ventana auxiliar
    
    #actualizamos el frame de modelos en la ventana
    glo.stateFrame.contenidoDeReferencias.actualizar_contenido(bbdd)

def eliminar_referencia_BBDD(botonPulsado, bbdd):

    datos = recoger_datos_referencia(botonPulsado, bbdd)                         # llamar a la función que recoge los datos de los entry en el panel de modelos
    print(datos)
    referencia = datos["referencia"]
    modelo     = datos["marca_modelo"]
     
    if ventanas_emergentes.msg_eliminar_ref(referencia, modelo) == "Aceptar":
        BDqueries.eliminar_referencia(bbdd, referencia)          # usar el método de la BD para eliminar
#####################################################################################################################
################### EVENTOS PARA SECCION TÉCNICOS ###################################################################
#####################################################################################################################

@e.manejar_errores("---Actualizar Técnico. Abriendo una ventana para modificar un técnico---")
def editar_tecnico_BD(ventana, datos, bbdd):
    ventana.rootAux.destroy()
    ventEditar = ventanas_topLevel.VentanaEditaTecnico("EDITAR", "TECNICO")
    ventEditar.set_values(datos)
    id_anterior = datos[0]
    ventEditar.asignafuncion(funcionGuardar  = lambda:guardar_tecnico_actualizado(id_anterior, ventEditar, bbdd),
                             funcionCancelar = lambda:ventEditar.rootAux.destroy)

@e.manejar_errores("---Actualizar Técnico. Recogiendo datos y efectuando actualizacion de técnico en base de datos---")
def guardar_tecnico_actualizado(id_anterior, ventana, bbdd):
    
    nombre = ventana.varNombre.get()
    apellido = ventana.varApellido.get()
    documento = ventana.varDocumento.get()
    especialidad = ventana.varEspecialidad.get()
    ventana.rootAux.destroy()

    id_tecnico_nuevo = genera_idTecnico(nombre, apellido, documento)
    BDqueries.actualizar_tecnico(bbdd, id_tecnico_nuevo, nombre, apellido, documento, especialidad, id_anterior)
    
    df_tecnProc = BDqueries.leer_tecnicos_procesos_df(bbdd)

    df_tecnProc_anterior = df_tecnProc[df_tecnProc['ID_PROCESO'] == id_anterior]

    ids_tecnProc_anterior, ids_procesos = df_tecnProc_anterior["TEC_PROC"], df_tecnProc_anterior["ID_PROCESO"]
    
    ids_tecnProc_nuevo = []
    for id_proceso in ids_procesos:
        nuevo_id_tecnProc = f"{id_tecnico_nuevo}{id_proceso}"
        ids_tecnProc_nuevo.append(nuevo_id_tecnProc)

    BDqueries.actualizar_tecnicos_proceso_many(bbdd, ids_tecnProc_anterior, ids_tecnProc_nuevo, id_tecnico_nuevo)

    ventanas_emergentes.messagebox.showinfo("Tecnico actualizado",
                                            f"Tecnico {id_anterior} actualizado con éxito.")


@e.manejar_errores("---Check Tecnicos. Recogiendo checkbox para verificar los técnicos a incluir en el programa---")
def recoge_check_tecnicos():
    checktecnicos = {}     # Crear un nuevo diccionario temporal para almacenar las claves modificadas
    print(glo.intVar_tecnicos.items())
    for clave, var in glo.intVar_tecnicos.items():
        nueva_clave = re.sub(r'.*?-', '', clave)   # Expresión regular para eliminar desde el guión hacia atrás
        checktecnicos[nueva_clave] = var.get()     # Actualizar el valor en el diccionario temporal con la nueva clave y el valor actual de IntVar

    print(checktecnicos)
    return checktecnicos

@e.manejar_errores("---Crear Tecnico. Recogiendo datos de técnico nuevo(y especialidad) y guardando en base de datos---")
def guardar_tecnico_nuevo(ventana, bbdd):
    #Recoger los datos agregados del nuevo tecnico
    datos = (ventana.varNombre.get(),
             ventana.varApellido.get(),
             ventana.varDocumento.get(),
             ventana.varEspecialidad.get())
    ventana.rootAux.destroy()

    ids_procesos = BDqueries.leer_procesos_completo(bbdd)
    ids_procesos = {nombre:id for id, nombre, desc, secue in ids_procesos}
    ParteDoc = datos[2][-6:] if len(datos[3]) >= 6 else datos[2]                    # extraer las ultimos 4 numeros del documento
    id_proc = ids_procesos[datos[3]]                                              # extramos el id del proceso
    idTecnico = datos[0][:4] + datos[1][:4] + ParteDoc                              # construir un id com el nombre, elapellido y el documento
    proc_espec = idTecnico + id_proc                                               # construimos el id del tecnico_proceso
    print(datos)
    print(proc_espec, idTecnico, id_proc)

    BDqueries.insertar_tecnico(bbdd, idTecnico, *datos)                                  # insertar el registro del técnico en BD
    BDqueries.insertar_tecnico_proceso(bbdd, proc_espec, idTecnico, id_proc)             # insertar el registro del técnico_proceso en BD

@e.manejar_errores("---Eliminar Tecnico. Recogiendo datos de técnico a eliminar y actualizando en base de datos---")
def eliminar_tecnico_BD(ventana, bbdd):
    nombreTecnico = ventana.varItem.get()        # obtener el técnico seleccionado
    idTecnico = ventana.ids_items.get(nombreTecnico) # obtiene la clave con el id de acuerdo al valor con nombre completo de técnico
    if ventanas_emergentes.msg_eliminar_tec(id_tecnico = idTecnico, nombre = nombreTecnico) == "Aceptar":
        BDqueries.eliminar_tecnico_completo(bbdd, idTecnico)          # usar el método de la BD para eliminar
        ventana.rootAux.destroy()                                # cerrar la ventana toplevel

#####################################################################################################################
################### EVENTOS PARA SECCION PROCESOS ###################################################################
#####################################################################################################################
@e.manejar_errores("---Actualizar Proceso. Abriendo una ventana para modificar un proceso---")
def editar_proceso_BD(ventana, datos, bbdd):
    ventana.rootAux.destroy()
    ventEditar = ventanas_topLevel.VentanaEditaProceso("EDITAR", "PROCESO")
    ventEditar.set_values(datos)
    id_anterior = datos[0]
    ventEditar.asignafuncion(funcionGuardar  = lambda:guardar_proceso_actualizado(id_anterior, ventEditar, bbdd),
                             funcionCancelar = lambda:ventEditar.rootAux.destroy)
    
@e.manejar_errores("---Actualizar Proceso. Recogiendo datos y efectuando actualizacion de proceso en base de datos---")
def guardar_proceso_actualizado(id_anterior, ventana, bbdd):
    nombre = ventana.varNombre.get()
    id_proceso_nuevo = ventana.varIdProceso.get()
    descripcion = ventana.varDescripcion.get()
    secuencia = ventana.varSecuencia.get()
    ventana.rootAux.destroy()

    BDqueries.actualizar_proceso(bbdd, id_proceso_nuevo, nombre, descripcion, secuencia, id_anterior)
    
    df_timeMode = BDqueries.leer_procesos_modelos_df(bbdd)
    df_tecnProc = BDqueries.leer_tecnicos_procesos_df(bbdd)

    df_timeMode_anterior = df_timeMode[df_timeMode['ID_PROCESO'] == id_anterior]
    df_tecnProc_anterior = df_tecnProc[df_tecnProc['ID_PROCESO'] == id_anterior]

    ids_timeMode_anterior, ids_modelos = df_timeMode_anterior["PROCESO_MODELO"], df_timeMode_anterior["ID_MODELO"]
    ids_tecnProc_anterior, ids_tecnicos = df_tecnProc_anterior["TEC_PROC"], df_tecnProc_anterior["ID_TECNICO"]

    ids_timeMode_nuevo = []
    for id_modelo in ids_modelos:
        nuevo_id_timeMode = f"{id_proceso_nuevo}-{id_modelo}"
        ids_timeMode_nuevo.append(nuevo_id_timeMode)
    
    ids_tecnProc_nuevo = []
    for id_tecnico in ids_tecnicos:
        nuevo_id_tecnProc = f"{id_tecnico}{id_proceso_nuevo}"
        ids_tecnProc_nuevo.append(nuevo_id_tecnProc)

    BDqueries.actualizar_proceso_modelos_many(bbdd, ids_timeMode_anterior, ids_timeMode_nuevo, id_proceso_nuevo)
    BDqueries.actualizar_tecnicos_proceso_many(bbdd, ids_tecnProc_anterior, ids_tecnProc_nuevo, id_proceso_nuevo)

    ventanas_emergentes.messagebox.showinfo("Proceso actualiado",
                                            f"Proceso {id_anterior} actualizado con éxito.")

@e.manejar_errores("---Crear Proceso. Recogiendo datos de proceso nuevo y almacenando en base de datos---")
def guardar_proceso_nuevo(ventana, bbdd):
    id_proceso, nombre_proceso, descripcion, secuencia = (ventana.varIdProceso.get(),
                                                          ventana.varNombre.get(),
                                                          ventana.varDescripcion.get(),
                                                          ventana.varSecuencia.get())


    #PREPARAR DATAFRAME DE TIEMPOS MODELOS
    ids_modelos = [modelo[0] for modelo in BDqueries.leer_modelos(bbdd)]
    df_procesos_modelos = pd.DataFrame([{'PROCESO_MODELO': f"{id_proceso}-{id_modelo}",
                                         'ID_PROCESO': id_proceso,
                                         'ID_MODELO': id_modelo,
                                         'TIEMPO': 0}  for id_modelo in ids_modelos])
    #PREPARAR DATAFRAME DE TIEMPOS VEHICULOS
    chasises = [vehiculo[0] for vehiculo in BDqueries.leer_vehiculos(bbdd)]
    df_procesos_chasises = pd.DataFrame([{'PROCESO_CHASIS': f"{id_proceso}-{chasis}",
                                         'ID_PROCESO': id_proceso,
                                         'CHASIS': chasis,
                                         'TIEMPO': 0}  for chasis in chasises])

    #PREPARAR DATAFRAME DE TECNICOS PROCESOS
    ids_tecnicos = [tecnico[0] for tecnico in BDqueries.leer_tecnicos(bbdd)]
    df_tecnicos_procesos = pd.DataFrame([{'TEC_PROC': f"{id_tecnico}{id_proceso}",
                                         'ID_PROCESO': id_proceso,
                                         'ID_TECNICO': id_tecnico}  for id_tecnico in ids_tecnicos])

    print(id_proceso, nombre_proceso, descripcion, secuencia)
    print(df_procesos_modelos)
    print(df_procesos_chasises)
    print(df_tecnicos_procesos)

    BDqueries.insertar_proceso(bbdd, id_proceso, nombre_proceso, descripcion, secuencia)
    BDqueries.insertar_tiempos_modelos_df(bbdd, df_procesos_modelos)
    BDqueries.insertar_tiempos_vehiculos_df(bbdd, df_procesos_chasises)
    BDqueries.insertar_tecnicos_procesos_df(bbdd, df_tecnicos_procesos)

    ventana.rootAux.destroy()
    ventanas_emergentes.messagebox.showinfo("Proceso creado",
                                            f"Proceso {id_proceso} creado con éxito."
                                            "Se actualizaron las tablas de tiempos de modelos, tiempos de vehiculos y tecnicos procesos.")  

@e.manejar_errores("---Eliminar Proceso. Recogiendo datos de proceso a eliminar y actualizando en base de datos---")
def eliminar_proceso_BD(ventana, bbdd):
    nombreProceso = ventana.varItem.get()        # obtener el técnico seleccionado
    idProceso = ventana.ids_items.get(nombreProceso) # obtiene la clave con el id de acuerdo al valor con nombre completo de técnico
    if ventanas_emergentes.msg_eliminar_proc(nombre = nombreProceso) == "Aceptar":
        BDqueries.eliminar_proceso_completo(bbdd, idProceso)          # usar el método de la BD para eliminar
        ventana.rootAux.destroy()                                # cerrar la ventana toplevel


#####################################################################################################################
################EVENTOS PARA SECCION DE VEHICULOS####################################################################
#####################################################################################################################
@e.manejar_errores("---Leer datos Vehiculo. Recogiendo datos de vehiculo  en base de datos---")
def recoger_datos_vehiculo(chasis, bbdd):
    return BDqueries.leer_vehiculo(bbdd, chasis)

@e.manejar_errores("---Modificar Vehiculo. Recogiendo datos de tiempos e histórico de vehiculo y abriendo ventana para modificarlos---")
def modificar_datos_vehiculo(chasis_anterior, bbdd):

    datos = list(recoger_datos_vehiculo(chasis_anterior, bbdd))                     #LEER DE LA BASE DATOS EL VEHICULO
    print(datos)
    marcamodelo = list(BDqueries.leer_modelo(bbdd, datos[2]))
    datos.pop(2)
    datos.insert(2, marcamodelo[1])
    datos.insert(2, marcamodelo[2])
    tiempos    = BDqueries.leer_tiempos_vehiculo(bbdd, chasis_anterior)                     #LEER LOS TIEMPOS DEL VEHICULO
    historicos = BDqueries.leer_historico_chasis(bbdd, chasis_anterior)
    print("Los datos en el modulo eventos son: ", datos)
    print("Los tiempos en el modulo eventos son: ", tiempos)
    ventana = ventanas_topLevel.VentanaGestionaVehiculos("MODIFICAR", bbdd)       #CREAR LA VENTANA EMERGENTE PARA EDITAR EL VEHICULO
    ventana.set_values(datos, tiempos, "MODIFICAR")                                        #AGREGAR LOS DATOS DE LA BBDD A LA VENTANA
    ventana.asignafuncion(lambda:modificarVH_en_BBDD(ventana, chasis_anterior, bbdd), lambda:cancelar(ventana))  #ASIGNAR BOTONES

@e.manejar_errores("---Modificar Vehiculo. Actualizando en la base de datos los datos modificados del vehiculo y sus tiempos---")
def modificarVH_en_BBDD(ventana, chasis_anterior, bbdd):
    #Se recogen los datos de la fila
    tiempos = []
    for clave in glo.strVar_nuevosTiemposVeh:
        tiempos.append(glo.strVar_nuevosTiemposVeh[clave].get())
    

    id_modelo = BDqueries.leer_vehiculo(bbdd, chasis_anterior)[2]
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
    BDqueries.actualizar_vehiculo(bbdd, *datos, chasis_anterior)

    id_procesos = BDqueries.obtener_id_procesos(bbdd)
    id_procesos.sort()
    #insertamos en la tabla de tiempos_vehiculoss
    for id_proceso, tiempo in zip(id_procesos, tiempos):
        proc_chasis_anterior = f"{id_proceso}-{chasis_anterior}"
        proc_chasis = f"{id_proceso}-{datos[0]}"
        BDqueries.actualizar_tiempo_vehiculo(bbdd,
                                        proc_chasis, 
                                        id_proceso,
                                        datos[0],
                                        tiempo,
                                        proc_chasis_anterior)

    ventana.rootAux.destroy()   #cerramos la ventana auxiliar

@e.manejar_errores("---Eliminar Vehiculo. Actualizando cambios en base de datos---")
def eliminar_VH_pedido(chasis):
    if ventanas_emergentes.msg_eliminar_veh(chasis) == "Aceptar":
        BDqueries.eliminar_vehiculo(chasis)

@e.manejar_errores("---Mostrar info de Vehiculo. Recogiendo datos de vehiculo en base de datos, tiempos e sus históricos y abriendo ventana para mostrarlos---")
def ventana_infoVehiculo(chasisVh, bbdd):
    lecturaRegistros = BDqueries.leer_historico_chasis(bbdd, chasisVh)
    datosVehiculo = BDqueries.leer_vehiculo(bbdd, chasisVh)

    nombresTecnicos = {}
    for tecnico in  BDqueries.leer_tecnicos_modificado(bbdd):
        nombresTecnicos[tecnico[0]] = tecnico[1]            # Adicionar solo id y nombre al diccionario de tecnicos en base a la lectura de BBDD

    registros_modificados = []

    for registro in lecturaRegistros:
        id_tecnico = registro[2]                            # Tomar el tercer elemento de la tupla
        
        if id_tecnico in nombresTecnicos:                                       # Si el tercer elemento coincide con una clave en NombresTecnicos
            registro_modificado = list(registro)                                # Convertir la tupla en una lista para poder modificarla
            registro_modificado[2] = nombresTecnicos[id_tecnico]                # Reemplazar el tercer elemento con el valor correspondiente en NombresTecnicos
            registros_modificados.append(tuple(registro_modificado))            # Volver a convertir la lista a tupla y agregarla a la lista de resultados
       
        else:
            registros_modificados.append(registro)                              # Si no hay coincidencia, agregar el registro original

    for registro in lecturaRegistros:
        print("lectura", registro)

    if len(registros_modificados)==0:           #Si no hay registros
        ventanas_emergentes.messagebox.showinfo(
            title="Información de Vehículo",
            message="No hay registros históricos del vehiculo con chasis "+ chasisVh)
        
    else:
        ventana = ventanas_topLevel.VentanaMuestraInfoVH(bbdd, registros_modificados, datosVehiculo)
        ventana.asignafuncionBoton(lambda:cancelar(ventana))

@e.manejar_errores("---Asignar Vehiculo. Abriendo ventana para asignar un vehiculo a un técnico en un proceso con fecha y hora---")
def ventana_AsignarUnVehiculo(chasis, bbdd):
    ventana = ventanas_topLevel.VentanaAsignaVehiculo(chasis, bbdd)
    ventana.asignaFuncion(funcionAceptar = lambda:aceptar_AsignarUnVehiculo(ventana, chasis, bbdd),
                          funcionCancelar = lambda:cancelar(ventana))

@e.manejar_errores("---Asignar Vehiculo. Recogiendo datos de asignación de vehiculo y guardando en históricos de base de datos---")
def aceptar_AsignarUnVehiculo(ventana, chasisVh, bbdd):
    datos = [ventana.varTecnico.get(),
             ventana.varProceso.get(),
             chasisVh]
    concatenado = ''.join([re.match(r'(.{3})', dato).group(1) for dato in datos if len(dato) >= 3])
    id_asig = model_classPlant.reemplazar_caracteres(concatenado + fecha + hora)
    fecha = ventana.varFecha.get()
    hora = ventana.varHora.get()
    observaciones = ventana.varObser.get()
    id_tec = ventana.ids_tecnicos.get(datos[0])    
    id_proc = ventana.ids_procesos.get(datos[1])
    print(id_asig, id_proc, id_tec)

    inicio = model_datetime.parseDT(fecha, hora) 
    tiempo = BDqueries.leer_tiempo_vehiculo(bbdd, chasisVh, id_proc)
    fin    = model_datetime.calcular_hora_finalDT(inicio, tiempo)
    estado = ventana.varEstado.get()

    print(id_asig, id_proc, id_tec, inicio, fin, tiempo)

    BDqueries.insertar_historico(bbdd,
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
    ventanas_emergentes.messagebox.showinfo("Vehículo asignado", f"Se asignó el vehículo {chasisVh} al técnico {id_tec} en el proceso {id_proc}")

#####################################################################################################################
################## EVENTOS PARA SECCION DE PEDIDOS ##################################################################
#####################################################################################################################
@e.manejar_errores("---Crear Pedido. <recogiendo datos de nuevo pedido y guardando en base de datos---")
def guardar_pedido_nuevo(ventana, bbdd):
    datos = (ventana.varNombre.get(),
             ventana.varDependCliente.get(),
             ventana.varFechaRecepcion.get(),
             ventana.varFechaIngreso.get(),
             ventana.varFechaEstimada.get(),
             ventana.varFechaEntrega.get())
    print(datos)
    ventana.rootAux.destroy()

    consecutivo = BDqueries.next_consecutivoPedido(bbdd)
    id_pedido = datos[0] + "_" + str(consecutivo)
    datos_completos = tuple(list(datos) + consecutivo)
    print(datos_completos)
    BDqueries.insertar_pedido(bbdd, *datos_completos)

@e.manejar_errores("---Recoger datos Pedido. Recogiendo datos de pedido, programas e históricos en base de datos y abriendo ventana para mostrarlos---")
def ventana_infoPedido(id_pedido, bbdd):
    datosPedido = BDqueries.leer_pedido(bbdd, id_pedido)
    datosProgramas = BDqueries.leer_programas_por_pedido(bbdd, id_pedido)
    df_vehiculos = BDqueries.leer_historicos_estados_pedido_df(bbdd, id_pedido)
    ventana = ventanas_topLevel.VentanaMuestraInfoPedi(bbdd, datosPedido, datosProgramas, df_vehiculos)
    ventana.asignafuncionBoton(funcionCerrar=ventana.rootAux.destroy)

@e.manejar_errores("---Modificar Pedido. Abriendo ventana para modificar datos de pedido---")
def modificar_datos_pedido(id_anterior, bbdd):

    ventana = ventanas_topLevel.VentanaModificarPedido(geometry      = "450x400",       #CREAR LA VENTANA EMERGENTE PARA EDITAR EL PEDIDO
                                                       nombreVentana = "MODIFICAR PEDIDO",
                                                       id_pedido     = id_anterior,
                                                       bbdd          = bbdd)
    ventana.botones.asignarfunciones(funcionOk      = lambda : modificarPedido_en_BBDD(ventana, id_anterior, bbdd),
                                     funcionCancel  = lambda : cancelar(ventana))

@e.manejar_errores("---Mostrar Info Programa. Abriendo ventana para mostrar info del programa---")
def ventana_infoPrograma(id_programa, bbdd):
    ventana = ventanas_topLevel.VentanaMuestraInfoProg(id_programa, bbdd)
    ventana.asignafuncionBoton(funcionCerrar=ventana.rootAux.destroy)

@e.manejar_errores("---Modificar Pedido. Recogiendo datos de pedido y actualizando en la base de datos de pedidos, vehiculosy programas---")
def modificarPedido_en_BBDD(ventana, id_anterior, bbdd):

    datos = (
        ventana.varCliente.get(),
        ventana.labelEntryFechaRecepcion.varFecha.get(),
        ventana.labelEntryFechaIngreso.varFecha.get(),
        ventana.labelEntryFechaEstimada.varFecha.get(),
        ventana.labelEntryFechaEntrega.varFecha.get(),
    )
    print(datos)
    ventana.rootAux.destroy()   #cerramos la ventana auxiliar

    consecutivo = BDqueries.next_consecutivoPedido(bbdd)
    id_bruto = re.sub(r'_[^_]*$', '', id_anterior)
    id_pedido = id_bruto + "_" + str(consecutivo) 
    datos_completos = (id_pedido,) + tuple(map(str, datos)) + (consecutivo,)
    print(datos_completos)
    BDqueries.actualizar_pedido(bbdd, *datos_completos, id_anterior)    # Actualizamos pedido
    BDqueries.actualizar_vehiculos_pedido(bbdd, id_anterior, id_pedido)     # Actualizamos vehiculos de pedido
    BDqueries.actualizar_programas_pedido(bbdd, id_anterior, id_pedido)     # Actualizamos programas de pedido

    ventanas_emergentes.messagebox.showinfo("Registros actualizados", f"Se actualizaron los registros de programas y vehículos del pedido {id_anterior}")

@e.manejar_errores("---Eliminar Pedido. Actualizando cambios en base de datos---")
def eliminar_pedido_BD(id_pedido, bbdd):
    if ventanas_emergentes.msg_eliminar_ped(id_pedido) == "Aceptar":
        request, incorrecta = BDqueries.eliminar_pedido_cascada(bbdd, id_pedido)
        if  incorrecta == None:
            ventanas_emergentes.messagebox.showerror("ERROR EN LA ELIMINACIÓN DE REGISTROS", f"No se eliminó ningún registros:\nError: {request}")
        elif incorrecta ==True:
            ventanas_emergentes.messagebox.showerror("TRANSACCIÓN NO EXISTOSA", f"No se eliminó ningún registros.\nDetalles de eliminación:\n\n{request}")
        elif incorrecta ==False:
            ventanas_emergentes.messagebox.showinfo("TRANSACCIÓN EXISTOSA", f"Se afectaron los siguientes registros en base de datos:\n{request}")
        
#####################################################################################################################
################## EVENTOS PARA SECCION DE PROGRAMAS##################################################################
#####################################################################################################################
@e.manejar_errores("---Mostrar Gantt de programa. Recogiendo datos de programa y turnos en base de datos y abriendo ventana para Gantt---")
def mostrar_gantt_programa(id_programa, bbdd):
    df = BDqueries.leer_ordenes_graficar_programa(bbdd, id_programa)

    # Convertir las columnas de fechas de string a datetime
    df["INICIO"] = pd.to_datetime(df["INICIO"])
    df["FIN"]    = pd.to_datetime(df["FIN"])
    inicio_horizonte = df["INICIO"].min()    # Encontrar el valor mínimo de cada columna
    fin_horizonte    = df["FIN"].max()       # Encontrar el valor máximo de cada columna

    startAM, endAM, startPM, endPM = BDqueries.leer_turnos_programa(bbdd, id_programa)
    df_con_bloques = incluir_bloques_horarios(df, startAM, endAM, startPM, endPM)
    gantt_tecnicos, gantt_vehiculos = model_gantt.generar_gantt(df_con_bloques, inicio_horizonte, fin_horizonte)

    diagramas = {"diagramaTecnicos" : gantt_tecnicos,
                 "diagramaVehiculos": gantt_vehiculos}
    
    ventana = ventanas_topLevel.ventanaGraficos("1000x700", id_programa, diagramas, df)
    ventana.botones.asignarfunciones(funcionCancel= ventana.rootAux.destroy,
                                     funcionOk= lambda: exportar_tabla(ventana, id_programa, "programa", bbdd))

@e.manejar_errores("---Mostrar info de Programa. Abriendo ventana para mostrar datos de las órdenes---")
def ventana_infoOrdenes(id_orden, bbdd):
    ventana = ventanas_topLevel.VentanaMuestraInfoOrde(id_orden, bbdd)
    ventana.asignafuncionBoton(funcionCerrar = ventana.rootAux.destroy)

@e.manejar_errores("---Eliminar Programa. Eliminado programa y sus órdenes en base de datos---")
def eliminar_programa_BD(id_programa, bbdd):
    if ventanas_emergentes.msg_eliminar_prog(id_programa) == "Aceptar":
        delPrograma = BDqueries.eliminar_programa(bbdd, id_programa)
        delOrdenes  = BDqueries.eliminar_ordenes_por_programa(bbdd, id_programa)
        print("Programa: ", delPrograma, "\n.Órdenes: ", delOrdenes)
        if delPrograma is False:
            if delOrdenes is False:
                ventanas_emergentes.messagebox.showerror("Programa No eliminado", f"Hubo un error al eliminar el programa {id_programa} y sus registros de órdenes")
            ventanas_emergentes.messagebox.showerror("Órdenes No eliminadas", f"Se eliminó el programa {id_programa}, pero no las órdenes del mismo") 
        
        ventanas_emergentes.messagebox.showinfo("Programa Eliminado",
                                                f"""Registros de programa {id_programa} eliminados correctamente:
                                                {delPrograma} programas eliminados
                                                {delOrdenes} órdenes eliminadas""")

@e.manejar_errores("---Eliminar. Eliminando una orden de un programa en base de datos---")
def ventana_eliminarOrden(id_orden, bbdd):
    if BDqueries.ventEmerg.msg_eliminar_ord(id_orden) == "Aceptar":
        BDqueries.eliminar_orden(bbdd, id_orden)
#####################################################################################################################
################ EVENTOS PARA SECCION DE HISTÓRICOS #################################################################
#####################################################################################################################
@e.manejar_errores("---Mostrar info de Histórico. Abriendo una ventana para mostrar histórico---")
def ventanaResumenHistorico(id_historico, bbdd):
    ventana = ventanas_topLevel.VentanaMuestraInfoHis(id_historico, bbdd)
    ventana.asignafuncionBoton(funcionCerrar = ventana.rootAux.destroy)

@e.manejar_errores("---Cambiar Estado de Histórico. Abriendo ventana para cambiar estado de histórico---")
def ventanaCambiarEstado(id, est_anterior, bbdd):
    ventana = ventanas_topLevel.VentanaCambiarEstadoHist(id, bbdd)
    ventana.asignafuncion(funcionAceptar  = lambda: aceptarCambiarEstado(ventana, id, est_anterior, bbdd),
                          funcionCancelar = ventana.rootAux.destroy)

@e.manejar_errores("---Cambiar Estado de Histórico. Actualizando en la base de datos el estado de un histórico---")
def aceptarCambiarEstado(ventana, id, est_anterior, bbdd):
    nuevo_estado = ventana.varEstado.get()
    BDqueries.actualizar_historico_estado(bbdd, id, nuevo_estado)
    ventana.rootAux.destroy()
    ventanas_emergentes.messagebox.showinfo("Registro Actualizado",
                                            f"El histórico con código {id} cambió su estado de {est_anterior} a {nuevo_estado}")

@e.manejar_errores("---Modificar Histórico. Abriendo ventana para modificar histórico---")
def ventana_modificarHistorico(id_anterior, bbdd):
    ventana = ventanas_topLevel.VentanaModificarHistorico("600x600", "MODIFICAR HISTÓRICO", id_anterior, bbdd)
    ventana.botones.asignarfunciones(funcionOk     = lambda : print("pulsó en aceptar"),
                                     funcionCancel = ventana.rootAux.destroy)

@e.manejar_errores("---Modificar Histórico. Abriendo ventana para añadir novedad y/observación---")
def ventana_ObserNoved(valores):
    pass

@e.manejar_errores("---Eliminar Histórico. Eliminando histórico en base de datos---")
def ventana_eliminarHistorico(id_historico, bbdd):
    if BDqueries.ventEmerg.msg_eliminar_his(id_historico) == "Aceptar":
        BDqueries.eliminar_historico(bbdd, id_historico)

#####################################################################################################################
############ EVENTOS PARA SECCION DE GANTT HISTORICOS ################################################################
#####################################################################################################################
@e.manejar_errores("---Generar Gantt de Históricos. Preparando datos para diagramas de Gantt de históricos---")
def generar_df_gantt(bbdd):
    df = BDqueries.leer_historicos_graficar(bbdd)

    # Convertir las columnas de fechas de string a datetime
    df["INICIO"] = pd.to_datetime(df["INICIO"])
    df["FIN"]    = pd.to_datetime(df["FIN"])

    # Encontrar el valor máximo y mínimo de cada columna
    inicio_horizonte = df["INICIO"].min()
    fin_horizonte    = df["FIN"].max()
    if pd.isna(inicio_horizonte):
        inicio_horizonte = datetime.datetime.now().replace(microsecond=0)
    if pd.isna(fin_horizonte):
        fin_horizonte = datetime.datetime.now().replace(hour=23, minute=59, second=0, microsecond=0)
        
    gantt_tecnicos, gantt_vehiculos = model_gantt.generar_gantt(df, inicio_horizonte, fin_horizonte)

    diagramas = {"diagramaTecnicos" : gantt_tecnicos,
                 "diagramaVehiculos": gantt_vehiculos}
    
    return df, diagramas

###########################################################################################################################
#################### MANEJO DE IMPORTACIÓN DESDE EXCEL ####################################################################
###########################################################################################################################

@e.manejar_errores("---Cargar Excel. Recogiendo datos de ventana, cargando archivo Excel y limpiandolo---")
def aceptar_cargar_excel(ventana, nombreVentana, bbdd):
    ruta = ventana.ruta
    columns = ventana.varColumnas.get()
    encabezados = ventana.varEncabezadoFila.get()
    dataframe = pd.read_excel(ruta, usecols=columns, header=int(encabezados)-1).dropna(how="all")
    dataframe = dataframe.map(lambda x: x.strip() if isinstance(x, str) else x)
    print("XLSX-->datosExcel: \n", dataframe)
    dataframe_limpio = limpiar_espacios_df(df = dataframe)

    
    if nombreVentana == "HISTORICOS":
        funcion = lambda : guardar_HistoricosExcel_BBDD(ventVistaPrevia, dataframe_limpio, bbdd)

    if nombreVentana == "MODELOS":
        funcion = lambda : guardar_ModelosExcel_BBDD(ventVistaPrevia, dataframe_limpio, bbdd)

    if nombreVentana == "PEDIDO":
        ventana.rootAux.destroy()
        funcion = lambda : guardar_PedidoExcel_BBDD(ventVistaPrevia, dataframe_limpio, bbdd)
        ventVistaPrevia = ventanas_topLevel.VentanaVistaPreviaPedido(dataframe_limpio, bbdd)
        ventVistaPrevia.asignafuncion(funcionAceptar  = lambda : guardar_PedidoExcel_BBDD(ventVistaPrevia, dataframe_limpio, bbdd), 
                                      funcionCancelar = ventVistaPrevia.rootAux.destroy)
        return

    if nombreVentana == "PROCESOS":
        funcion = lambda : guardar_ProcesosExcel_BBDD(ventVistaPrevia, dataframe_limpio, bbdd)

    if nombreVentana == "REFERENCIAS":
        funcion = lambda : guardar_ReferenciasExcel_BBDD(ventVistaPrevia, dataframe_limpio, bbdd)

    if nombreVentana == "TECNICOS":
        funcion = lambda : guardar_TecnicosExcel_BBDD(ventVistaPrevia, dataframe_limpio, bbdd)
    
    if nombreVentana == "TIEMPOS_MODELOS":
        funcion = lambda : guardar_TiemposModelosExcel_BBDD(ventVistaPrevia, dataframe_limpio, bbdd)

    ventana.rootAux.destroy()
    ventVistaPrevia = ventanas_topLevel.VentanaVistaPrevia(nombreVentana, dataframe, bbdd)
    ventVistaPrevia.asignafuncion(funcionAceptar  = funcion,
                                  funcionCancelar = ventVistaPrevia.rootAux.destroy)

@e.manejar_errores("---Cargar históricos de Excel. Recogiendo datos de ventana, cargando archivo Excel, limpiandolo y abriendo ventana para vista previa---")
def aceptar_cargar_historicos_excel(ventana, nombreVentana, bbdd):
    ruta = ventana.ruta
    ventana.rootAux.destroy()
    hojas = pd.read_excel(ruta, sheet_name=None)
    dataframes = {}                                 # Crear un diccionario para guardar los DataFrames con nombres de hojas
    for nombre_hoja, dataframe in hojas.items():    # Iterar sobre cada hoja
        # Limpiar filas o columnas vacías
        dataframe = dataframe.dropna(how='all')  # Elimina filas completamente vacías
        dataframe = dataframe.loc[:, dataframe.columns.notna()]  # Elimina columnas vacías
        
        # Guardar en el diccionario
        dataframes[nombre_hoja] = dataframe
        
        print(f"Hoja: {nombre_hoja}")
        print(f"Encabezados: {list(dataframe.columns)}")
        print(dataframe, "\n")
    
    ventVistaPrevia = ventanas_topLevel.VentanaPreviewLoad(dataframes)
    ventVistaPrevia.asignafuncion(funcionAceptar = lambda : guardar_HistoricosExcel_BBDD(ventana    = ventVistaPrevia,
                                                                                         dataframes = dataframes,
                                                                                         bbdd       = bbdd),
                                  funcionCancelar=ventVistaPrevia.rootAux.destroy)

@e.manejar_errores("---Cargar pedido de Excel. Recogiendo datos de ventana, cargando archivo Excel y abriendo ventana para vista previa---")
def aceptar_cargar_pedido_excel(ventana, bbdd):
    ruta = ventana.ruta
    columns = ventana.varColumnas.get()
    rowSkips = ventana.varSaltarFila.get()
    dataframe = pd.read_excel(ruta,
                            usecols=columns,
                            header=None,
                            skiprows=int(rowSkips)-1).dropna(how="all")
    dataframe.columns = ['CHASIS', 'REFERENCIA', 'COLOR']
    dataframe = dataframe.map(lambda x: x.strip() if isinstance(x, str) else x)
    print("XLSX-->datosExcel: \n", dataframe)
    
    ventana.rootAux.destroy()
    ventVistaPrevia = ventanas_topLevel.VentanaVistaPreviaPedido(dataframe, bbdd)
    ventVistaPrevia.asignafuncion(funcionAceptar  = lambda : guardar_PedidoExcel_BBDD(ventVistaPrevia, dataframe, bbdd), 
                                  funcionCancelar = ventVistaPrevia.rootAux.destroy)

@e.manejar_errores("---Cargar referencias de Excel. Recogiendo datos de ventana, cargando archivo Excel y abriendo ventana para vista previa---")
def aceptar_cargar_referencias_excel(ventana, bbdd):
    ruta = ventana.ruta
    columns = ventana.varColumnas.get()
    rowSkips = ventana.varSaltarFila.get()
    dataframe = pd.read_excel(ruta,
                            usecols=columns,
                            header=0,
                            skiprows=int(rowSkips)).dropna(how="all")
    print("XLSX-->datosExcel: \n", dataframe)
    
    ventana.rootAux.destroy()
    ventVistaPrevia = ventanas_topLevel.VentanaVistaPreviaReferencias(dataframe, bbdd)
    ventVistaPrevia.asignafuncion(funcionAceptar  = lambda: guardar_ReferenciasExcel_BBDD(ventVistaPrevia, dataframe, bbdd), 
                                  funcionCancelar = ventVistaPrevia.rootAux.destroy)
    return dataframe

@e.manejar_errores("---Guardar referencia. Guardando referencia en Base de datos---")
def aceptar_agregar_referencias(ventana, bbdd):
    ventana.rootAux.destroy()
    print("PRESIONÓ AGREGAR REFERENCIAS")
    print("Aun no se almacenan, ni se cargan los modelos en el pedido")

@e.manejar_errores("---Cargar(Guardar) Históricos. Preparando dataframe para guardar en base de datos---")
def guardar_HistoricosExcel_BBDD(ventana, dataframes, bbdd):
    ventana.rootAux.destroy()
    try:
        df_con_id_tecnico = {}
        df_con_id_tecnico = {tecnico: historicos.assign(ID_TECNICO=tecnico).copy()
                            for tecnico, historicos in dataframes.items()}
    
        df_agrupado = pd.concat(df_con_id_tecnico.values(), ignore_index=True)
        print(df_agrupado)

        # Asegurarse de que la columna de hora esté en el formato correcto
        df_agrupado ['HORA_INICIO'] = pd.to_datetime(df_agrupado ['HORA_INICIO'], format='%H:%M:%S').dt.time
        df_agrupado ['HORA_FIN']    = pd.to_datetime(df_agrupado ['HORA_FIN'], format='%H:%M:%S').dt.time

        df_agrupado ['INICIO'] = pd.to_datetime(df_agrupado ['FECHA_INICIO'].astype(str) + ' ' + df_agrupado ['HORA_INICIO'].astype(str))    # Fusionar las columnas de fecha y hora en una sola columna
        df_agrupado ['FIN']    = pd.to_datetime(df_agrupado ['FECHA_FIN'].astype(str) + ' ' + df_agrupado ['HORA_FIN'].astype(str))          # Fusionar las columnas de fecha y hora en una sola columna
        df_agrupado.drop(columns=['FECHA_INICIO', 'HORA_INICIO', 'FECHA_FIN', 'HORA_FIN'], inplace=True)
        df_agrupado['DURACION'] = (df_agrupado['FIN'] - df_agrupado['INICIO']).apply(lambda t: int(t.total_seconds() // 60)) # Concatenar las columnas ID_TECNICO, ID_PROCESO y CHASIS
        df_agrupado['CODIGO_ASIGNACION'] = df_agrupado.apply(
                                                        func = lambda row: model_classPlant.reemplazar_caracteres(
                                                                                                    concatenar_id_historico(row)),
                                                        axis = 1)

        df_procesos = BDqueries.leer_procesos_df(bbdd)
        df_agrupado = pd.merge(df_agrupado, df_procesos, how='left', left_on='PROCESO', right_on='NOMBRE')
        df_agrupado.drop(columns=['PROCESO', 'NOMBRE', 'DESCRIPCION', 'SECUENCIA'], inplace=True)

        print(df_agrupado)
        total = df_agrupado.shape[0]

    except Exception as e:
        print(e)
        ventanas_emergentes.messagebox.showerror("Error al agregar históricos", f"Ocurrió un error al agregar la tabla de históricos cargada: {e}")
        return
    
    registrosNuevos = BDqueries.insertar_historicos_df(bbdd, df_agrupado)
    if registrosNuevos > 0:
        ventanas_emergentes.messagebox.showinfo("Históricos agregados", f"Se agregaron correctamente los históricos cargados: total {total} registros")

e.manejar_errores("---Cargar(Guardar) Modelos de excel. Guardando en base de datos el dataframe de modelos---")
def guardar_ModelosExcel_BBDD(ventana, df, bbdd):
    print(df)
    ventana.rootAux.destroy()
    try:
        if BDqueries.insertar_modelos_df(bbdd, df) is False:
            ventanas_emergentes.messagebox.showinfo("Error al agregar Modelos", f"Ocurrió un error al agregar la tabla de Modelos cargada") 
    
        else:
            ventanas_emergentes.messagebox.showinfo("Técnicos Agregado", f"Se agregó correctamente la tabla de Modelos cargada")

    except:
        ventanas_emergentes.messagebox.showinfo("Error al agregar Modelos", f"Ocurrió un error al agregar la tabla de Modelos cargada") 

@e.manejar_errores("---Cargar(Guardar) Pedidos de excel. Recogiendo datos, preparando dataframe y guardando pedido, vehiculos y tiempos en base de datos---")
def guardar_PedidoExcel_BBDD(ventana, df, bbdd):
    nombre = glo.strVar_newPedido['nombre'].get()
    cliente = glo.strVar_newPedido['cliente'].get()  
    fecha_recepcion = glo.strVar_newPedido['fecha_recepcion'].get()
    fecha_ingreso = glo.strVar_newPedido['fecha_ingreso'].get()
    fecha_estimada = glo.strVar_newPedido['fecha_estimada'].get()
    fecha_entrega = glo.strVar_newPedido['fecha_entrega'].get()
    consecutivo = BDqueries.next_consecutivoPedido(bbdd)

    ventana.rootAux.destroy()
    id_pedido = nombre + "_" + str(consecutivo)
    print(id_pedido, cliente,fecha_recepcion, fecha_ingreso, fecha_estimada, fecha_entrega, consecutivo)

    df_para_BBDDVehiculos, df_para_BBDDtiemposVehiculos = transformar_vehiculos_pedido_cargado(df, id_pedido, fecha_ingreso, bbdd)

    #Persistimos en BBDD solo si no hay registros nulos
    existe, coincidencias = verificar_pedidos_vehiculos(bbdd, id_pedido, df_para_BBDDVehiculos, df_para_BBDDtiemposVehiculos)
    if existe == True:
        pedido_coincide = coincidencias["pedido"]                                           # SACAMOS EL ID DEL PEDIDO SI YA EXISTE
        lista_vh_coinciden = [fila for fila in coincidencias["vehiculos"]["CHASIS"]]        #  SACAMOS EL df DE LOS VEHICULOS CON CHASIS SI YA EXISTEN
        lista_times_coinciden = [fila for fila in coincidencias["tiempos"]["CHASIS"]]       #  SACAMOS EL df DE LOS TIEMPOS_VEHICULOS CON CHASIS SI YA EXISTEN
        ventanas_emergentes.messagebox.showerror(f"""Pedido NO AGREGADO""",
            f"""No se agregó el Pedido {id_pedido} ni los vehículos cargados.
            Puede que ya exista el pedido {pedido_coincide}.
            O puede que ya existan registros de los vehiculos {lista_vh_coinciden}
            o registros de tiempos de los vehiculos {lista_times_coinciden}""")
        return

    try:
        BDqueries.insertar_pedido(bbdd = bbdd,                                       # Guardamos pedido en BBDD
                             id_pedido       = id_pedido,
                             cliente         = cliente,
                             fecha_recepcion = fecha_recepcion,
                             fecha_ingreso   = fecha_ingreso,
                             fecha_estimada  = fecha_estimada,
                             fecha_entrega   = fecha_entrega,
                             consecutivo     = consecutivo)
        BDqueries.insertar_vehiculos_df(bbdd,
                                   df_para_BBDDVehiculos)                 # Guardamos los vehiculos
        BDqueries.insertar_tiempos_vehiculos_df(bbdd,
                                           df_para_BBDDtiemposVehiculos)  # Guardamos los tiempos_vehiculos
        
        ventanas_emergentes.messagebox.showinfo("Pedido Agregado", f"Se agregó correctamente el Pedido {id_pedido} y los vehículos cargados")

    except Exception as e:
        ventanas_emergentes.messagebox.showinfo("Error al agregado el pedido", f"Ocurrió un error al egregar el Pedido {id_pedido} y/o los vehículos cargados. Error: {e}") 

@e.manejar_errores("---Cargar(Guardar) Procesos de excel. Guardando en base de datos el dataframe de procesos---")
def guardar_ProcesosExcel_BBDD(ventana, df, bbdd):
    print(df)
    ventana.rootAux.destroy()
    try:
        if BDqueries.insertar_procesos_df(bbdd, df) is False:
            ventanas_emergentes.messagebox.showinfo("Error al agregar procesos", f"Ocurrió un error al agregar la tabla de procesos cargada") 
    
        else:
            ventanas_emergentes.messagebox.showinfo("Procesos Agregado", f"Se agregó correctamente la tabla de procesos cargada")

    except:
        ventanas_emergentes.messagebox.showinfo("Error al agregar procesos", f"Ocurrió un error al agregar la tabla de procesos cargada") 

@e.manejar_errores("---Cargar(Guardar) Referencias de excel. Preparando dataframe y Guardando en base de datos el dataframe de referencias---")
def guardar_ReferenciasExcel_BBDD(ventana, df, bbdd):
    df_tabla_modelos = BDqueries.leer_modelos_id_modelos_df(bbdd)
    print(df_tabla_modelos)
    df_final = pd.merge(df, df_tabla_modelos, on="MODELO", how="left")   # Hacer un merge entre el DataFrame original y la tabla obtenida de la base de datos
    print(df_final)
    df_final = df_final[["REFERENCIA", "ID_MODELO"]]                     # Seleccionar solo las columnas requeridas
    print(df_final)
    ventana.rootAux.destroy()
    BDqueries.insertar_referencias_df(bbdd, df_final)

@e.manejar_errores("---Cargar(Guardar) Técnicos de excel. Guardando en base de datos el dataframe de técnicos---")
def guardar_TecnicosExcel_BBDD(ventana, df, bbdd):
    print(df)
    ventana.rootAux.destroy()
    try:
        if BDqueries.insertar_tecnicos_df(bbdd, df) is False:
            ventanas_emergentes.messagebox.showinfo("Error al agregar técnicos", f"Ocurrió un error al agregar la tabla de técnicos cargada") 
    
        else:
            ventanas_emergentes.messagebox.showinfo("Técnicos Agregado", f"Se agregó correctamente la tabla de técnicos cargada")

    except:
        ventanas_emergentes.messagebox.showinfo("Error al agregar técnicos", f"Ocurrió un error al agregar la tabla de técnicos cargada") 

@e.manejar_errores("---Cargar(Guardar) Tiempos Modelos de excel. Preparando dataframe y Guardando en base de datos el dataframe de tiempos---")
def guardar_TiemposModelosExcel_BBDD(ventana, df, bbdd):
    df_marcasModelos = BDqueries.leer_modelos_marcas_df(bbdd).drop(columns=["MARCA"]) # leemos los id de modelos en base de datos
    print(df_marcasModelos)
    df_combinado = pd.merge(df, df_marcasModelos, on="MODELO", how="left")       # combinamos el dataframe de tiempos con el de id modelos
    print(df_combinado)
    df_idModelos_tiempos = df_combinado.drop(columns=["MODELO", "MARCA"])        # eliminamos las columnas de marca y modelo
    df_idModelos_tiempos =df_idModelos_tiempos[["ID_MODELO"] +          # ubicamos de primera la columna de id_modelo
                                               [colum for colum in df_idModelos_tiempos
                                                if colum !="ID_MODELO"]]
    df_tiempos_modelos = transformar_dataframe_tiempos(df_idModelos_tiempos, "MODELO")   # convertimos el dataframe a uno con la estructura de la tabla TIEMPOS_MODELOS en la BD
    print(df_tiempos_modelos)
    ventana.rootAux.destroy()
    try:
        if BDqueries.insRem_tiempos_modelos_df(bbdd, df_tiempos_modelos) is False:
            ventanas_emergentes.messagebox.showinfo("Error al agregado el pedido", f"Ocurrió un error al agregar la tabla de tiempos de modelos cargada") 
    
        else:
            ventanas_emergentes.messagebox.showinfo("Pedido Agregado", f"Se agregó correctamente la tabla de tiempos de modelos cargada")

    except:
        ventanas_emergentes.messagebox.showinfo("Error al agregado el pedido", f"Ocurrió un error al agregar la tabla de tiempos de modelos cargada") 


@e.manejar_errores("---Concatenar id. Generando un id de histórico")
def concatenar_id_historico(row):
    datos = [row['CHASIS'], row['ID_TECNICO'], row['PROCESO']]
    concatenado = ''.join([re.match(r'(.{3})', str(dato)).group(1) for dato in datos if len(str(dato)) >= 3])
    return model_classPlant.reemplazar_caracteres(concatenado+str(row['INICIO']))

@e.manejar_errores("---Limpiar espacios. Eliminar espacios en blanco al principai y al final de dataframe")
def limpiar_espacios_df(df):
    """
    Limpia los espacios en blanco al final de las cadenas y reduce múltiples espacios
    a uno solo en todas las columnas de un DataFrame.

    :param df: DataFrame de pandas.
    :return: DataFrame con todas las columnas limpiadas.
    """
    for columna in df.columns:
        df[columna] = df[columna].astype(str).apply(lambda x: ' '.join(x.split()))
    return df

@e.manejar_errores("---Verificar existencia pedido. Buscando en base de datos si ya existe pedido, vehiculos o tiempos---")
def verificar_pedidos_vehiculos(bbdd, pedidoNuevo, df_vehiculos, df_tiempos):
    consulta_pedido    = BDqueries.leer_pedido(bbdd, pedidoNuevo)
    consulta_vehiculos = BDqueries.leer_vehiculos_df(bbdd)
    consulta_tiempos   = BDqueries.leer_tiempos_vehiculos_df(bbdd)

    existe = False
    coincidencias = {"pedido":"",
                     "vehiculos":"",
                     "tiempos":""}
    if consulta_pedido is not None:
        print(f"Ya existe el pedido: {consulta_pedido}")
        existe = True

    if consulta_vehiculos is not None and not consulta_vehiculos[consulta_vehiculos["CHASIS"].isin(df_vehiculos["CHASIS"])].empty:
        print(f"Ya existe vehiculos del pedido {pedidoNuevo}")
        coincidencias["vehiculos"] = consulta_vehiculos[consulta_vehiculos["CHASIS"].isin(df_vehiculos["CHASIS"])]
        print(f"COINCIDENCIAS:  {coincidencias["vehiculos"]["CHASIS"]}")
        existe = True

    if consulta_tiempos is not None and not consulta_tiempos[consulta_tiempos["CHASIS"].isin(df_tiempos["CHASIS"])].empty:
        print(f"Ya existe registros de tiempos para los siguientes vehiculos:")
        coincidencias["tiempos"] = consulta_tiempos[consulta_tiempos["CHASIS"].isin(df_tiempos["CHASIS"])]
        print(f"COINCIDENCIAS:  {coincidencias["tiempos"]["CHASIS"]}")
        existe = True

    return existe, coincidencias

@e.manejar_errores("---Destruyendo ventana auxiliar---")
def cancelar(ventana):
    ventana.rootAux.destroy()
###########################################################################################################################
###################### MANEJO DE EXPORTACIÓN A EXCEL ######################################################################
###########################################################################################################################
@e.manejar_errores("---Exportar a Excel. Seleccionando ruta y abriendo ventana para exportar---")
def aceptar_exportar_to_excel(ventana, df, nombreVentana):
    ruta = nombraArchivoExcel(nombreVentana)
    ventana.rootAux.destroy()
    ventanas_emergentes.desea_exportar(nombreExcel = ruta,
                                       nombreVentana = nombreVentana,
                                       df = df)

@e.manejar_errores("---Exportar a Excel. Seleccionando ruta y abriendo ventana para exportar tabla---")
def exportar_tabla(ventana, id, tipo, bbdd):
    if tipo == "programa":
        df = BDqueries.leer_ordenes_graficar_programa(bbdd, id)
    if tipo == "pedido":
        df = BDqueries.leer_vehiculos_por_pedido_df(bbdd, id)

    ruta = nombraArchivoExcel(id)
    ventana.rootAux.destroy()
    ventanas_emergentes.desea_exportar(nombreExcel = ruta,
                                       nombreVentana = id,
                                       df = df)

@e.manejar_errores("---Exportar Plantilla a Excel. Exportando tabla a Excel---")
def generar_formatoExcel_historicos(bbdd):
    try:
        # Agregar un sufijo de tiempo al nombre del archivo para hacerlo único
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nombreArchivo = nombraArchivoExcel(re.sub(r'\..*', '', bbdd) + "_" + timestamp)
        nombreArchivo = 'plantillahistoricos_' + nombreArchivo

        df = BDqueries.leer_tecnicos_df(bbdd)
        if df is None or df.empty:
            print("No se encontraron datos.")
            ventanas_emergentes.messagebox.showerror("Error al generar el archivo de Excel",
                                                     "No se encontraron datos para generar el archivo de Excel.")
            return

        with pd.ExcelWriter(nombreArchivo, engine='openpyxl') as writer:  # Crear un archivo de Excel con múltiples hojas
            for _, row in df.iterrows():
                tecnico = row['ID_TECNICO']
                # Crear un DataFrame con los encabezados requeridos
                df_tecnico = pd.DataFrame(columns=[
                    'CHASIS', 'PROCESO', 'FECHA_INICIO', 'HORA_INICIO', 
                    'FECHA_FIN', 'HORA_FIN', 'ESTADO', 'OBSERVACION'
                ])
                
                # Escribir el DataFrame en una hoja con el nombre del técnico
                df_tecnico.to_excel(writer, sheet_name=str(tecnico), index=False)

        print(f"Archivo de Excel generado: {nombreArchivo}")
        ventanas_emergentes.messagebox.showinfo("Archivo de Excel generado",
                                                f"Se generó con éxito la plantilla de Excel {nombreArchivo}")
    except Exception as e:
        print(f"Error al generar el archivo de Excel: {e}")
        ventanas_emergentes.messagebox.showerror("Error al generar el archivo de Excel",
                                                 f"No se pudo generar la plantilla de Excel. Error: {e}")

@e.manejar_errores("---Nombrando archivo excel---")
def nombraArchivoExcel(nombre):
    return nombre + '_' + '.xlsx'
###############################################################################################################################
######################### EVENTOS PARA EL SCHEDULING ##########################################################################
###############################################################################################################################

@e.manejar_errores("---Programar pedido. Abriendo ventana para programar pedido---")
def abrirFechayHoraProg(tipoPrograma, pedido, bbdd):
    ventana = ventanas_topLevel.EstableceFechaHora(pedido)
    ventana.asignaFuncion(lambda:aceptarFechayHoraProg(ventana, tipoPrograma, bbdd), lambda:cancelar(ventana))

@e.manejar_errores("---Programar pedido. Aceptando fecha y hora para programar pedido---")
def aceptarFechayHoraProg(ventana, tipoPrograma, bbdd):
    #RECOGER LOS DATOS DE LA VENTANA DE FECHA Y HORA
    fecha = ventana.varFecha.get()
    hora = ventana.varHora.get()
    print(f"Fecha: {fecha}, Hora: {hora}")
    ventana.rootAux.destroy()

    #RECOGER DE LA BASE DE DATOS TODA LA INFORMACIÓN DE LA PLANTA Y GENERAR LOS OBJETOS PARA EL PROGRAMADOR
    model_classPlant.obtiene_datos_iniciales()
    procesos, objeModelos, objeVehiculos, objeTecnicos, objePedidos, tiempos = model_instancePlant.obtiene_datos_iniciales()

    #SELECCIONAR SOLO LOS TECNICOS INCLUIDOS A PROGRAMAR  
    tecnicos_a_programar = [tecnico for id, tecnico in objeTecnicos.items()
                            if glo.check_tecnicos.get(id).get() == 1]

    pedido_a_programar   = [pedido for id, pedido in objePedidos.items()
                                if pedido.id_pedido == glo.pedido_seleccionado][0]
    
    print("______________OBJEPEDIDOS________________\n", objePedidos)
    print("______________GLOBAL PEDIDO______________\n",glo.pedido_seleccionado)
    print("______________OBJETECNICOS________________\n", objeTecnicos)
    print("______________GLOBAL TECNICOS______________\n",glo.check_tecnicos)
    print("______________GLOBAL PROCESOS______________\n",glo.check_procesos)

    if tipoPrograma == "completo":
        diccPrograma = model_classPlant.programa_completo(pedido     = pedido_a_programar,
                                                       tecnicos   = tecnicos_a_programar,
                                                       horizonte  = 4000,
                                                       fechaStart = fecha,
                                                       horaStart  = hora)
        horizonte_calculado = model_classPlant.calcular_horizonte(pedido_a_programar)
        print(f"el horizonte es {horizonte_calculado}")

    if tipoPrograma == "inmediato":
        diccPrograma = model_classPlant.programa_inmediato(pedido     = pedido_a_programar,
                                                        tecnicos   = tecnicos_a_programar,
                                                        horizonte  = 4000,
                                                        fechaStart = fecha,
                                                        horaStart  = hora)
        horizonte_calculado = model_classPlant.calcular_horizonte(pedido_a_programar)
        print(f"el horizonte es {horizonte_calculado}")

    if tipoPrograma == "por procesos":
        
        procesos_a_programar = [id_proceso for id_proceso, seleccionado in glo.check_procesos.items()
                                if seleccionado.get() == 1]
        
        print(pedido_a_programar)
        print(tecnicos_a_programar)
        print(procesos_a_programar)

        diccPrograma = model_classPlant.programar_procesos(pedido = pedido_a_programar,
                                           tecnicos   = tecnicos_a_programar,
                                           procesos   = procesos_a_programar,
                                           horizonte  = 4000,
                                           fechaStart = fecha,
                                           horaStart  = hora,
                                           bbdd       = glo.base_datos)
        horizonte_calculado = model_classPlant.calcular_horizonte(pedido_a_programar)
        print(f"el horizonte es {horizonte_calculado}")
    
    ########## GRAFICAR PROGRAMACIÓN EN GANTT ##########
    inicio = datetime.datetime.strptime(fecha + " " + hora, "%Y-%m-%d %H:%M:%S")
    df_con_bloques = incluir_bloques_horarios(diccPrograma["programa"],
                                              glo.turnos.startAM.get(),
                                              glo.turnos.endAM.get(),
                                              glo.turnos.startPM.get(),
                                              glo.turnos.endPM.get())
    
    gantt_tecnicos, gantt_vehiculos = model_gantt.generar_gantt(df_con_bloques,
                                                                inicio,
                                                                horizonte_calculado)

    diagramas = {"diagramaTecnicos" : gantt_tecnicos,
                 "diagramaVehiculos": gantt_vehiculos}
    
    ########## PREPARAR INFORMACIÓN PARA BASE DE DATOS ############
    id_programa = diccPrograma["id"]
    id_programa_new = id_programa + "_" + str(BDqueries.next_consecutivoPrograma(bbdd))
    df_previo   = diccPrograma["programa"]
    df_programa = transformar_dataframe_ordenes(df_ordenes  = df_previo,
                                                id_programa = id_programa_new,
                                                bbdd        = bbdd)
    print(id_programa_new)
    print(df_programa)

    abrirVistaPrevia_programa(pedido    = pedido_a_programar,
                              diagramas = diagramas,
                              programa  = id_programa,
                              df_to_BD  = df_programa,
                              df_previo = df_previo,
                              bbdd      = bbdd)

@e.manejar_errores("---Programar pedido. Abriendo ventana para vista previa de programa---")
def abrirVistaPrevia_programa(pedido, diagramas, programa, df_to_BD, df_previo, bbdd):
    ventana = ventanas_topLevel.ventanaGraficos("1000x700", programa, diagramas, df_previo)
    ventana.botones.asignarfunciones(funcionOk     = lambda : aceptar_guardar_programa(ventana, programa, pedido.id_pedido, df_to_BD, bbdd),
                                     funcionCancel = ventana.rootAux.destroy)

@e.manejar_errores("---Programar pedido. Aceptando y guardando programa en base de datos---")
def aceptar_guardar_programa(ventana, programa, pedido, df_programa, bbdd):
    id_inicial  = programa
    consecutivo = BDqueries.next_consecutivoPrograma(bbdd)
    id_programa = id_inicial + "_" + str(consecutivo)
    ventana.rootAux.destroy()
    print(programa)
    print(df_programa)
    print(pedido)
    startAM = glo.turnos.startAM.get()
    endAM   = glo.turnos.endAM.get()
    startPM = glo.turnos.startPM.get()
    endPM   = glo.turnos.endPM.get()

    cargaOrdenes  = BDqueries.insertar_ordenes_df(bbdd, df_programa)
    cargaPrograma = BDqueries.insertar_programa(bbdd, id_programa, None, consecutivo, pedido,
                                           startAM=startAM, endAM=endAM, startPM=startPM, endPM=endPM)

    if cargaOrdenes is False:
        if cargaPrograma is False:
            ventanas_emergentes.messagebox.showinfo("Error al agregar programa y órdenes", f"Ocurrió un error al añadir las órdenes y el programa a la base de datos")
        ventanas_emergentes.messagebox.showinfo("Error al agregar las órdenes", f"Ocurrió un error al añadir las órdenes a la base de datos") 

    elif cargaPrograma is False:
        ventanas_emergentes.messagebox.showinfo("Error al agregar programa", f"Ocurrió un error al añadir el programa a la base de datos")
    
    else:
        ventanas_emergentes.messagebox.showinfo("Programa Agregado", f"Se agregaron correctamente las órdenes y el  programa de producción a la base de datos")

def incluir_bloques_horarios(df, startAM, endAM, startPM, endPM):
    """
    Incluir bloques de tiempo vacías en programa o históricos,
    de acuerdode horarios en el DataFrame de órdenes de producción.

    :param df: DataFrame de órdenes de producción.
    :param startAM: Hora de inicio del turno de la mañana.
    :param endAM: Hora de fin del turno de la mañana.
    :param startPM: Hora de inicio del turno de la tarde.
    :param endPM: Hora de fin del turno de la tarde.

    :return: DataFrame de órdenes de producción con lo horarios incluidos.
    """
    iniciaAM, terminaAM, iniciaPM, terminaPM = (
                                                hora if isinstance(hora, datetime.time)
                                                else datetime.datetime.strptime(hora, '%H:%M').time()
                                                for hora in (startAM, endAM, startPM, endPM)
                                                )
    nuevas_filas = []               # Lista para almacenar las nuevas filas
    for row in df.itertuples(index=True, name='Pandas'):    # Iterar sobre las filas usando itertuples()
        id_orden    = row.CODIGO_ORDEN
        inicioTarea = row.INICIO.to_pydatetime().replace(microsecond=0)
        finTarea    = row.FIN.to_pydatetime().replace(microsecond=0)
        
        bloques     = model_datetime.definir_bloques(iniciaAM, terminaAM, iniciaPM, terminaPM, inicioTarea, finTarea)
        if bloques == None:
            continue
    
        # Replicar la fila tantas veces como elementos tenga la lista "bloques"
        for inicio, fin in bloques:
            nueva_fila = row._asdict()
            nueva_fila['INICIO'] = inicio
            nueva_fila['FIN'] = fin
            nuevas_filas.append(nueva_fila)

    df_nuevas_filas = pd.DataFrame(nuevas_filas)                           # Crear un nuevo DataFrame con las nuevas filas
    df_con_bloques = df[~df['CODIGO_ORDEN'].isin(df_nuevas_filas['CODIGO_ORDEN'])]    # Eliminar las filas originales que cumplen la condición
    df_con_bloques = pd.concat([df_con_bloques, df_nuevas_filas], ignore_index=True)               # Añadir las nuevas filas al DataFrame original

    return df_con_bloques

      
###############################################################################################################################
####################### FUNCIONES GENERADORAS DE ID ###########################################################################
###############################################################################################################################
@e.manejar_errores("---Generar id. Concatenando datos para id de técnico---")
def genera_idTecnico(nombre, apellido, documento):
    return nombre[:4] + apellido[:4] + str(documento)[-6:]

@e.manejar_errores("---Generar id. Concatenando datos para id de modelo---")
def genera_idModelo(marca, modelo):
    return marca + "-" + modelo

@e.manejar_errores("---Eliminar duplicador. Limpiando el dataframe con datos duplicados---")
def elimina_Duplicados_df(df, columna):
    duplicados = df[df.duplicated(subset=[columna], keep=False)]
    sin_duplicados = df.drop_duplicates(subset=[columna], keep='first')
    return sin_duplicados, duplicados

###############################################################################################################################
####################### FUNCIONES PARA TRANSFORMAR DF #########################################################################
###############################################################################################################################
@e.manejar_errores("---Transformar dataframe. Preparando dataframe de tiempos de modelos o vehiculos para base de datos---")
def transformar_dataframe_tiempos(df, ids):

    # Nombre de la primera columna
    if ids == "MODELO":
        columna_principal = "ID_MODELO"
    if ids == "CHASIS":
        columna_principal = ids

    # Inicializar listas para las nuevas columnas
    combinacion_columna = []
    valores_principal = []
    encabezado = []
    valor = []
    combinacion_ids = 'PROCESO_'+ids

    # Iterar sobre las columnas restantes (excluyendo la primera columna)
    for col in df.columns[2:]:
        for i in range(len(df)):
            combinacion_columna.append(f"{col}-{df.at[i, columna_principal]}")  # Combinar valor de la primera columna con el encabezado
            valores_principal.append(df.at[i, columna_principal])               # Valores de la primera columna
            encabezado.append(col)          # Encabezado actual
            valor.append(df.iloc[i][col])   # Valor del cuerpo del DataFrame
    
    # Crear el nuevo DataFrame con las 4 columnas
    nuevo_df = pd.DataFrame({
        combinacion_ids  : combinacion_columna,
        "ID_PROCESO"     : encabezado,
        columna_principal: valores_principal,
        "TIEMPO"         : valor
    })
    
    return nuevo_df

@e.manejar_errores("---Transformar dataframe. Preparando dataframe de pedidos para base de datos---")
def transformar_vehiculos_pedido_cargado(df, id_pedido, fecha_ingreso, bbdd):

    print("___________________EJECUTANDO TRANSFORMACION___________________")
    df_ref_idModelos = BDqueries.leer_referencias_modelos_df(bbdd)           # lee las referencias en la BBDD    
    print(df)                       
    print(df_ref_idModelos.to_string())
    df_combinado1 = pd.merge(df, df_ref_idModelos, on="REFERENCIA", how="left")                 # Incluye la columna referencias con sus valores en el DF
    print(df_combinado1.to_string())

    registros_nulos = df_combinado1[df_combinado1['ID_MODELO'].isna()]                            # Filtrar registros donde 'ID_MODELO' sea None o NaN
    for index, row in registros_nulos.iterrows():                                                 # Obtener los valores de las columnas 'CHASIS', 'REFERENCIA' y 'COLOR' de todos los registros
        chasis = row['CHASIS']
        referencia = row['REFERENCIA']
        color = row['COLOR']
        print(f"Chasis: {chasis}, Referencia NO encontrada: {referencia}, Color: {color}")
    df_combinado1  = df_combinado1.drop(registros_nulos.index)                                   # Eliminar los registros del DataFrame 
    #registros_nulos.drop('ID_MODELO', axis=1, inplace=True)

    #EVALUAMOS SI HAY REGISTROS SIN REFERENCIA
    if registros_nulos.empty == False:
        respuesta = ventanas_emergentes.msg_registro_nulo(registros_nulos)
        if respuesta == "yes":
            print(registros_nulos)
            ventAgregaRef = ventanas_topLevel.VentanaAgregarReferencias(registros_nulos, bbdd)
            ventAgregaRef.asignaFuncion(funcionAgregar = lambda : aceptar_agregar_referencias(ventAgregaRef, bbdd),
                                        funcionCancelar = ventAgregaRef.rootAux.destroy)
        if respuesta == "No":
            return

    #EVALUAMOS SI HAY DUPLICADOS DE CHASIS
    registros_duplicados = df_combinado1[df_combinado1['CHASIS'].duplicated(keep=False)]          # keep=False incluye todos los registros duplicados
    if registros_duplicados.empty == False:
        ventanas_emergentes.msg_registro_duplicado(registros_nulos)
        return

    df_mod_idModelos = BDqueries.leer_modelos_id_modelos_df(bbdd)                                       # Incluimos los id_modelos    
    df_combinado2 = pd.merge(df_combinado1, df_mod_idModelos, on="ID_MODELO", how="left")
    print(df_combinado2)

    tiempos_modelos = BDqueries.leer_tiempos_modelos_df(bbdd)                                  # INcluimos los tiempos
    df_combinado3 = pd.merge(df_combinado2, tiempos_modelos, on="MODELO", how="left")
    print(df_combinado3)

    df_para_BBDDVehiculos = df_combinado2[["CHASIS", "ID_MODELO", "COLOR", "REFERENCIA"]]       # Seleccionar solo las columnas requeridas
    df_para_BBDDVehiculos['FECHA_INGRESO'] = fecha_ingreso
    df_para_BBDDVehiculos = df_para_BBDDVehiculos.assign(FECHA_INGRESO  =  fecha_ingreso,
                                                         NOVEDADES      =  'NO', 
                                                         SUBCONTRATAR   =  'NO', 
                                                         ID_PEDIDO      =  id_pedido)
    print(df_para_BBDDVehiculos)

    df_para_BBDDtiemposVehiculos = pd.DataFrame(columns=['PROCESO_CHASIS',
                                                         'ID_PROCESO',
                                                         'CHASIS',
                                                         'TIEMPO'])

    lista_para_dataFrame = []
    columnas_deseadas = list(df_combinado3.columns[5:])          # Seleccionar las columnas deseadas: la primera y desde la sexta en adelante
    print(df_combinado3[df_combinado3.columns[0]])
    print(columnas_deseadas)

    for col in columnas_deseadas:
        for row_value in df_combinado3[df_combinado3.columns[0]]:
            proceso_chasis = f"{col}-{row_value}"  # Concatenar encabezados de fila y columna
            fila = {
                'PROCESO_CHASIS': proceso_chasis,  # Columna 1: PROCESO_CHASIS
                'ID_PROCESO': col,                # Columna 2: ID_PROCESO
                'CHASIS': row_value,               # Columna 3: CHASIS
                'TIEMPO': df_combinado3.loc[df_combinado3[df_combinado3.columns[0]] == row_value, col].values[0]  # Columna 4: TIEMPO
            }
            lista_para_dataFrame.append(fila)

    df_para_BBDDtiemposVehiculos = pd.DataFrame(lista_para_dataFrame)    # Crear el nuevo DataFrame con los nombres personalizados de las columnas
    print(df_para_BBDDtiemposVehiculos)                                  # Mostrar el nuevo DataFrame
    print("___________________TRANSFORMACION TERMINADA___________________")
    return df_para_BBDDVehiculos, df_para_BBDDtiemposVehiculos

def transformar_dataframe_ordenes(df_ordenes, id_programa, bbdd):
    """
    Prepara un DataFrame para cargar a la base de datos.

    Args:
        df_ordenes (pd.DataFrame): DataFrame con la orden como la retorna el programador.
        id_programa (str): Código de orden generado por el programador.
        bbdd (str): Nombre de la base de datos.

    Returns:
        pd.DataFrame: DataFrame reducido con las columnas exactas para cargar a la base de datos.

    Procedure:
        1. Elimina del DataFrame de órdenes las columnas que no van en la base de datos.
        2. Cambia el nombre de la columna "procesos" a "id_proceso".
        3. Agrega una columna "id_programa" al DataFrame.
    """

    df_reducido = df_ordenes.drop(["MARCA",                           #RETIRAR LAS COLUMNAS QUE NO VAN EN LA BBDD
                                    "MODELO",
                                    "COLOR",
                                    "NOVEDADES",
                                    "PEDIDO",
                                    "TECNICO",
                                    "PLAZO"],
                       axis=1)
    df_reducido["id_programa"] = id_programa                           # AÑADIR EL MISMO PROGRAMA A TODAS LAS ÓRDENES
    df_reducido = df_reducido.rename(columns={"PROCESO":"ID_PROCESO"}) # CAMBIAR EL NOMBRE DE LA COLUMNA DE PROCESO
    print(df_reducido.to_string())
    return df_reducido

def transformar_dataframe_bloques_programa(df_ordenes, horarios):
    pass
###############################################################################################################################
####################### EVENTO MOSTRAR CUADRO DE TEXTO ########################################################################
###############################################################################################################################
class Tooltip:
    def __init__(self, widget, text_func):
        self.widget = widget
        self.text_func = text_func
        self.tooltip_window = None
        self.widget.bind("<Motion>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        if self.tooltip_window:
            self.tooltip_window.destroy()
        row_id = self.widget.identify_row(event.y)
        if not row_id:
            return
        bbox = self.widget.bbox(row_id)
        if not bbox:
            return
        x, y, width, height = bbox
        x = event.x_root + 20
        y = event.y_root + 10
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        text = self.text_func(row_id)
        label = tk.Label(tw, text=text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         font=numerosPequeños)
        label.pack(ipadx=1)

    def hide_tooltip(self, event):
        if self.tooltip_window:
            self.tooltip_window.destroy()
        self.tooltip_window = None