import re
import pandas as pd
from tkinter.filedialog import askopenfilename
import CRUD
import creadorBD
import BBDD
import glo
import menu.stepsNuevaPlanta as steps_nueva_planta
import menu.ventanaNuevaPlanta as ventanaNuevaPlanta
import ventanas_topLevel
import ventanas_emergentes
import modelo_clases, modelo_instancias
import modelo_llamarGantt
import fechahora


#################################################################################
######################### EVENTOS PARA CREAR PLANTA #############################
#################################################################################

def step_crearNuevaPlanta():
    ventana = ventanaNuevaPlanta.VentanaNuevaPlanta()
    ventana.asignafuncion(funcionCancelar   = ventana.rootAux.destroy,
                          funcionVistaPrevia= lambda: step_CargarTodo(ventana))

def step_CargarTodo(ventana):
    ruta = ventana.ruta
    nombre= ventana.varNombre.get()
    descripcion = ventana.varDescripcion.get()

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
    ventVistaPrevia.asignafuncion(funcionAceptar = lambda : crear_plantaBD(dataframes = dataframes,
                                                                           name = nombre,
                                                                           description = descripcion,
                                                                           ventana = ventVistaPrevia),
                                  funcionCancelar=ventVistaPrevia.rootAux.destroy)

def crear_plantaBD(dataframes, name, description, ventana):
    df_procesos     = dataframes["PROCESOS"]
    df_tecnicos     = dataframes["TECNICOS"]
    df_modelos      = dataframes["MARCAS_MODELOS"]
    df_referencias  = dataframes["MODELOS_REFERENCIAS"]
    ventana.rootAux.destroy()

    df_tecnicos["ID_TECNICO"] = df_tecnicos.apply(lambda row:genera_idTecnico(row["NOMBRE"], row["APELLIDO"], row["DOCUMENTO"]), axis=1)
    df_modelos["ID_MODELO"] = df_modelos.apply(lambda row:genera_idModelo(row["MARCA"], row["MODELO"]), axis=1)
    
    df_procesos = elimina_Duplicados_df(df_procesos, "ID_PROCESO")[0]
    df_tecnicos = elimina_Duplicados_df(df_tecnicos, "ID_TECNICO")[0]
    df_modelos = elimina_Duplicados_df(df_modelos, "ID_MODELO")[0]
    df_referencias = elimina_Duplicados_df(df_referencias, "REFERENCIA")[0]

    df_merged = pd.merge(df_referencias, df_modelos, on='MODELO', how='left')       # Realiza el merge entre df_referencias y df_modelos
    df_referencias = df_merged [['REFERENCIA', 'ID_MODELO']]                            # Reasigna el dataframe

    df_tecnicos, df_tecnicos_procesos = genera_df_tecnicos_proceso(df = df_tecnicos)
    df_tiempos_modelos = genera_tiempos_modelos_default(df_modelos, df_procesos)
    print(df_procesos)
    print(df_tecnicos)
    print(df_tecnicos_procesos)
    print(df_modelos)
    print(df_referencias)
    print(df_tiempos_modelos)
    base_datos = creadorBD.crea_BBDD(nombre = name)
    if base_datos == "existe":
        return
    
    BBDD.insertar_info_planta(bbdd = base_datos, nombre = name, descripcion = description)
    ins_proce  = BBDD.insertar_procesos_df(bbdd = base_datos, dataframe=df_procesos)
    ins_tecni  = BBDD.insertar_tecnicos_df(bbdd = base_datos, dataframe=df_tecnicos)
    ins_tecpr  = BBDD.insertar_tecnicos_procesos_df(bbdd = base_datos, dataframe=df_tecnicos_procesos)
    ins_model  = BBDD.insertar_modelos_df(bbdd = base_datos, dataframe=df_modelos)  
    ins_refer  = BBDD.insertar_referencias_df(bbdd = base_datos, dataframe=df_referencias)
    ins_timod  = BBDD.insertar_tiempos_modelos_df(bbdd = base_datos, dataframe=df_tiempos_modelos)

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
                                            """Se añadieron  con éxito todos los registros de procesos, técnicos, modelos y referencias.
                                            Dirígase a la sección IMPORTAR TIEMPOS, para agregar los tiempos de proceso a los modelos""")
    
    recarga_root(bbdd = base_datos)

def genera_df_tecnicos_proceso(df): 
    especialidad_cols = df.filter(like='ESPECIALIDAD').columns                                 # Filtrar columnas que contienen 'ESPECIALIDAD'
    df_tecnicos = df.loc[:, ~df.columns.str.contains('ESPECIALIDAD')]                          # Eliminar las columnas que contienen la cadena 'ESPECIALIDAD'
    df_tecnicos = df_tecnicos[["ID_TECNICO", "NOMBRE", "APELLIDO","DOCUMENTO"]]                # Reordenamos las columnas
    df_tecnicos["ESPECIALIDAD"] = df[especialidad_cols].apply(lambda row:
                                                               ", ".join(row.dropna().
                                                                         astype(str)), axis=1) # Crear listas con valores de 'ESPECIALIDAD'


    especialidades_columns = df.columns[df.columns.str.contains('ESPECIALIDAD')]               # Obtenemos las columnas 'ESPECIALIDAD', 'ESPECIALIDAD.1', etc.
    df_tecnicos_procesos = pd.DataFrame(columns=['TEC_PROC', 'ID_TECNICO', 'ID_PROCESO'])      # Ahora creamos un DataFrame donde concatenamos ID_TECNICO con las especialidades

    for col in especialidades_columns:                                                         # Iteramos sobre las columnas de especialidades para generar el nuevo DataFrame
        temp_df = df[['ID_TECNICO', col]].dropna(subset=[col])                                 # Eliminamos filas con valores nulos en esa especialidad
        temp_df['TEC_PROC'] = temp_df['ID_TECNICO'] + temp_df[col]                             # Concatenamos ID_TECNICO y el valor de la especialidad
        temp_df['ID_PROCESO'] = temp_df[col]                                                   # Asignamos el valor de la especialidad a ID_PROCESO
        temp_df = temp_df[['TEC_PROC', 'ID_TECNICO', 'ID_PROCESO']]                            # Reordenamos las columnas
        df_tecnicos_procesos = pd.concat([df_tecnicos_procesos, temp_df], ignore_index=True)   # Concatenamos al DataFrame final

    # Mostrar los resultados
    print("\nDataFrame Limpio (sin las columnas 'ESPECIALIDAD'):")
    print(df_tecnicos)
    print("\nNuevo DataFrame 'df_tecnicos_procesos':")
    print(df_tecnicos_procesos)

    return df_tecnicos, df_tecnicos_procesos

def recarga_root(bbdd):
    glo.base_datos = bbdd
    #modelo_clases.obtiene_datos_iniciales()
    #modelo_instancias.obtiene_datos_iniciales()
    glo.root.llena_root()

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


#####################################################################
################EVENTOS PARA SECCION DE MODELOS######################
#####################################################################
def crear_modelo(bbdd):
    print("pusó el botón crear modelo")
    ventana = ventanas_topLevel.VentanaCreaEditaModelo("CREAR", bbdd)              #Llamar al constructor del objeto ventana
    ventana.asignafuncion(funcionGuardar  = lambda:guardar_modelo_nuevo(ventana, bbdd),
                               funcionCancelar = lambda:cancelar(ventana))    #asignar los botones de guardar y cancelar en la ventana

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

    #insertamos en la tabla de timepos modelos
    for id_proceso, tiempo in zip(id_procesos, tiempos):
        proc_model = f"{id_proceso}-{datos[0]}-{datos[1]}"
        BBDD.insertar_tiempo_modelo(bbdd,
                                    proc_model, 
                                    id_proceso,
                                    id_modelo,
                                    tiempo)

    ventana.rootAux.destroy()   #cerramos la ventana auxiliar
    
    #actualizamos el frame de modelos en la ventana
    glo.stateFrame.contenidoDeModelos.actualizar_contenido(bbdd)

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
    ventana = ventanas_topLevel.VentanaCreaEditaModelo("EDITAR", bbdd)     # Llamar al constructor del objeto ventana para editar el modelo
    ventana.set_values(datos)                                                # llamar al metodo del objeto ventana creada, que llena los campos de modelo y tiempos
    ventana.asignafuncion(lambda:guardar_modelo_actualizado(ventana, datos, bbdd), lambda:cancelar(ventana))    #asignar los botones de guardar y cancelar en la ventana

def guardar_modelo_actualizado(ventana, datos_iniciales, bbdd):

    id_modelo_actual = datos_iniciales["marca"]+ "-" + datos_iniciales["modelo"]
    datos = list((ventana.varMarca.get(),
                  ventana.varModelo.get()))
    
    tiempos =[]             #SE CREA Y LLENA UNA LISTA CON LOS TIEMPOS DE PROCESO
    for clave, valor in glo.strVar_nuevosTiemposMod.items():    
        tiempos.append(valor.get())
    print("Diccionario de tiempos que sobreescribirán: ", glo.strVar_nuevosTiemposMod)



    idModelo = f"{datos[0]}-{datos[1]}"                     # OBTENEMOS ID DE MODELOS Y PROCESOS
    id_procesos = BBDD.obtener_id_procesos(bbdd)            # leemos en la base de datos los IDS de los procesos
    id_procesos.sort()                                      # ordenamos la lista de id's procesos

    BBDD.actualizar_modelo(bbdd         = bbdd,             # Insertamos en la tabla de modelos
                           id_anterior  = id_modelo_actual, 
                           marca        = datos[0],
                           modelo       = datos[1],
                           id_nuevo     = idModelo)


    registroTiemposProcesos = BBDD.leer_ids_proceso_modelo(bbdd, id_modelo_actual)      # leemos los registros de tiempos para el modelo (una lista de tuplas con los ids de procesos y modelos)
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
        BBDD.insertar_tiempo_modelo(bbdd        = bbdd,
                                    procmodel   = procModelo, 
                                    id_proceso  = idProceso,
                                    id_modelo   = idModelo,
                                    tiempo      = 0)

    # actualizamos enla tabla de tiempos_modelos
    for idProceso, time, proceso_modelo in zip(id_procesos, tiempos, ids_proceso_modelo):
        procModelo = f"{idProceso}-{datos[1]}"
        BBDD.actualizar_tiempo_modelo(bbdd       =   bbdd,
                                      procmodel  =   procModelo, 
                                      id_proceso =   idProceso,
                                      id_modelo  =   idModelo,
                                      tiempo     =   time,
                                      procmodelo_anterior=proceso_modelo)
    
    ventana.rootAux.destroy()
    glo.stateFrame.contenidoDeModelos.actualizar_contenido(bbdd)    #actualizamos el frame de modelos en la ventana


def agregar_vehiculo(botonPulsado, bbdd):
    datos = recoger_datos_modelo(botonPulsado, bbdd)
    print(datos)
    ventana = ventanas_topLevel.VentanaGestionaVehiculos("AGREGAR", bbdd)
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

def eliminar_modelo_BD(ventana, bbdd):
    modeloDelete = ventana.varModelo.get()
    datosModelo = ventana.dfModelos[ventana.dfModelos['MODELO']== modeloDelete] 
    listaDatos = datosModelo.values.flatten().tolist()
    vehiCoinciden = BBDD.buscar_vehiculo_por_modelo(bbdd, modeloDelete)
    if ventanas_emergentes.msg_eliminar_mod(modelo = modeloDelete, vehiculos = vehiCoinciden) == "Aceptar":
        BBDD.eliminar_modelo_completo(bbdd, modelo = modeloDelete)          # usar el método de la BD para eliminar
        for vehiculo in vehiCoinciden:
            BBDD.eliminar_vehiculo_completo(bbdd, chasis = vehiculo[0])
        ventana.rootAux.destroy()                                         # cerrar la ventana toplevel

#####################################################################
################### EVENTOS PARA SECCION TÉCNICOS ###################
#####################################################################
def recoge_check_tecnicos():

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
    if ventanas_emergentes.msg_eliminar_tec(id_tecnico = idTecnico, nombre = nombreTecnico) == "Aceptar":
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
    print(datos)
    marcamodelo = list(BBDD.leer_modelo(bbdd, datos[2]))
    datos.pop(2)
    datos.insert(2, marcamodelo[1])
    datos.insert(2, marcamodelo[2])
    tiempos = BBDD.leer_tiempos_vehiculo(bbdd, chasis_anterior)                     #LEER LOS TIEMPOS DEL VEHICULO

    print("Los datos en el modulo eventos son: ", datos)
    print("Los tiempos en el modulo eventos son: ", tiempos)
    ventana = ventanas_topLevel.VentanaGestionaVehiculos("MODIFICAR", bbdd)       #CREAR LA VENTANA EMERGENTE PARA EDITAR EL VEHICULO
    ventana.set_values(datos, tiempos, "MODIFICAR")                                        #AGREGAR LOS DATOS DE LA BBDD A LA VENTANA
    ventana.asignafuncion(lambda:modificarVH_en_BBDD(ventana, chasis_anterior, bbdd), lambda:cancelar(ventana))  #ASIGNAR BOTONES


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
    if ventanas_emergentes.msg_eliminar_veh(chasis) == "Aceptar":
        CRUD.eliminar_vehiculo(chasis)

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
        ventana = ventanas_topLevel.VentanaMuestraInfoVH(bbdd, registros_modificados, datosVehiculo)
        ventana.asignafuncionBoton(lambda:cancelar(ventana))

def ventana_AsignarUnVehiculo(chasis, bbdd):
    ventana = ventanas_topLevel.VentanaAsignaVehiculo(chasis, bbdd)
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
    ventanas_emergentes.messagebox.showinfo("Vehículo asignado", f"Se asignó el vehículo {chasisVh} al técnico {id_tec} en el proceso {id_proc}")


#####################################################################
################## EVENTOS PARA SECCION DE PEDIDOS ##################
#####################################################################

def guardar_pedido_nuevo(ventana, bbdd):
    datos = (ventana.varNombre.get(),
             ventana.varDependCliente.get(),
             ventana.varFechaRecepcion.get(),
             ventana.varFechaIngreso.get(),
             ventana.varFechaEstimada.get(),
             ventana.varFechaEntrega.get())
    print(datos)
    ventana.rootAux.destroy()

    consecutivo = BBDD.next_consecutivoPedido(bbdd)
    id_pedido = datos[0] + "_" + str(consecutivo)
    datos_completos = tuple(list(datos) + consecutivo)
    print(datos_completos)
    BBDD.insertar_pedido(bbdd, *datos_completos)

def eliminar_pedido_BD(id, bbdd):
    if ventanas_emergentes.msg_eliminar_ped(id) == "Aceptar":
        BBDD.eliminar_pedido(bbdd, id)
#####################################################################
################ EVENTOS PARA SECCION DE HISTÓRICOS #################
#####################################################################

def ventanaResumenHistorico(id, bbdd):
    ventana = ventanas_topLevel.VentanaMuestraInfoHis(id, bbdd)
    ventana.asignafuncionBoton(funcionCerrar = ventana.rootAux.destroy)

def ventanaCambiarEstado(id, bbdd):
    ventana = ventanas_topLevel.VentanaCambiarEstadoHist(id, bbdd)
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


###########################################################################
#################### MANEJO DE ARCHIVOS DE EXCEL ##########################
###########################################################################
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

def guardar_ReferenciasExcel_BBDD(ventana, df, bbdd):
    df_tabla_modelos = BBDD.leer_modelos_id_modelos(bbdd)
    print(df_tabla_modelos)
    df_final = pd.merge(df, df_tabla_modelos, on="MODELO", how="left")   # Hacer un merge entre el DataFrame original y la tabla obtenida de la base de datos
    print(df_final)
    df_final = df_final[["REFERENCIA", "ID_MODELO"]]                     # Seleccionar solo las columnas requeridas
    print(df_final)
    ventana.rootAux.destroy()
    BBDD.insertar_referencias_df(bbdd, df_final)
    
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

def guardar_PedidoExcel_BBDD(ventana, df, bbdd):
    nombre = glo.strVar_newPedido['nombre'].get()
    cliente = glo.strVar_newPedido['cliente'].get()  
    fecha_recepcion = glo.strVar_newPedido['fecha_recepcion'].get()
    fecha_ingreso = glo.strVar_newPedido['fecha_ingreso'].get()
    fecha_estimada = glo.strVar_newPedido['fecha_estimada'].get()
    fecha_entrega = glo.strVar_newPedido['fecha_entrega'].get()
    consecutivo = BBDD.next_consecutivoPedido(bbdd)

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
        BBDD.insertar_pedido(bbdd = bbdd,                                       # Guardamos pedido en BBDD
                             id_pedido       = id_pedido,
                             cliente         = cliente,
                             fecha_recepcion = fecha_recepcion,
                             fecha_ingreso   = fecha_ingreso,
                             fecha_estimada  = fecha_estimada,
                             fecha_entrega   = fecha_entrega,
                             consecutivo     = consecutivo)
        BBDD.insertar_vehiculos_df(bbdd,
                                   df_para_BBDDVehiculos)                 # Guardamos los vehiculos
        BBDD.insertar_tiempos_vehiculos_df(bbdd,
                                           df_para_BBDDtiemposVehiculos)  # Guardamos los tiempos_vehiculos
        
        ventanas_emergentes.messagebox.showinfo("Pedido Agregado", f"Se agregó correctamente el Pedido {id_pedido} y los vehículos cargados")

    except Exception as e:
        ventanas_emergentes.messagebox.showinfo("Error al agregado el pedido", f"Ocurrió un error al egregar el Pedido {id_pedido} y/o los vehículos cargados. Error: {e}") 

def aceptar_cargar_excel(ventana, nombreVentana, bbdd):
    ruta = ventana.ruta
    columns = ventana.varColumnas.get()
    encabezados = ventana.varEncabezadoFila.get()
    dataframe = pd.read_excel(ruta, usecols=columns, header=int(encabezados)-1).dropna(how="all")
    dataframe = dataframe.map(lambda x: x.strip() if isinstance(x, str) else x)
    print("XLSX-->datosExcel: \n", dataframe)
    

    if nombreVentana == "PROCESOS":
        funcion = lambda : guardar_ProcesosExcel_BBDD(ventVistaPrevia, dataframe, bbdd)

    if nombreVentana == "TECNICOS":
        funcion = lambda : guardar_TecnicosExcel_BBDD(ventVistaPrevia, dataframe, bbdd)

    if nombreVentana == "MODELOS":
        funcion = lambda : guardar_ModelosExcel_BBDD(ventVistaPrevia, dataframe, bbdd)

    if nombreVentana == "REFERENCIAS":
        funcion = lambda : guardar_ReferenciasExcel_BBDD(ventVistaPrevia, dataframe, bbdd)

    if nombreVentana == "TIEMPOS_MODELOS":
        funcion = lambda : guardar_TiemposModelosExcel_BBDD(ventVistaPrevia, dataframe, bbdd)

    if nombreVentana == "PEDIDO":
        ventana.rootAux.destroy()
        funcion = lambda : guardar_PedidoExcel_BBDD(ventVistaPrevia, dataframe, bbdd)
        ventVistaPrevia = ventanas_topLevel.VentanaVistaPreviaPedido(dataframe, bbdd)
        ventVistaPrevia.asignafuncion(funcionAceptar  = lambda : guardar_PedidoExcel_BBDD(ventVistaPrevia, dataframe, bbdd), 
                                      funcionCancelar = ventVistaPrevia.rootAux.destroy)
        return
    
    ventana.rootAux.destroy()
    ventVistaPrevia = ventanas_topLevel.VentanaVistaPrevia(nombreVentana, dataframe, bbdd)
    ventVistaPrevia.asignafuncion(funcionAceptar  = funcion,
                                  funcionCancelar = ventVistaPrevia.rootAux.destroy)

def guardar_ProcesosExcel_BBDD(ventana, df, bbdd):
    print(df)
    ventana.rootAux.destroy()
    try:
        if BBDD.insertar_procesos_df(bbdd, df) is False:
            ventanas_emergentes.messagebox.showinfo("Error al agregar procesos", f"Ocurrió un error al agregar la tabla de procesos cargada") 
    
        else:
            ventanas_emergentes.messagebox.showinfo("Procesos Agregado", f"Se agregó correctamente la tabla de procesos cargada")

    except:
        ventanas_emergentes.messagebox.showinfo("Error al agregar procesos", f"Ocurrió un error al agregar la tabla de procesos cargada") 

def guardar_TecnicosExcel_BBDD(ventana, df, bbdd):
    print(df)
    ventana.rootAux.destroy()
    try:
        if BBDD.insertar_tecnicos_df(bbdd, df) is False:
            ventanas_emergentes.messagebox.showinfo("Error al agregar técnicos", f"Ocurrió un error al agregar la tabla de técnicos cargada") 
    
        else:
            ventanas_emergentes.messagebox.showinfo("Técnicos Agregado", f"Se agregó correctamente la tabla de técnicos cargada")

    except:
        ventanas_emergentes.messagebox.showinfo("Error al agregar técnicos", f"Ocurrió un error al agregar la tabla de técnicos cargada") 

def guardar_ModelosExcel_BBDD(ventana, df, bbdd):
    print(df)
    ventana.rootAux.destroy()
    try:
        if BBDD.insertar_tecnicos_df(bbdd, df) is False:
            ventanas_emergentes.messagebox.showinfo("Error al agregar técnicos", f"Ocurrió un error al agregar la tabla de técnicos cargada") 
    
        else:
            ventanas_emergentes.messagebox.showinfo("Técnicos Agregado", f"Se agregó correctamente la tabla de técnicos cargada")

    except:
        ventanas_emergentes.messagebox.showinfo("Error al agregar técnicos", f"Ocurrió un error al agregar la tabla de técnicos cargada") 

def guardar_TiemposModelosExcel_BBDD(ventana, df, bbdd):
    df_marcasModelos = BBDD.leer_modelos_marcas_df(bbdd).drop(columns=["MARCA"]) # leemos los id de modelos en base de datos
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
        if BBDD.insRem_tiempos_modelos_df(bbdd, df_tiempos_modelos) is False:
            ventanas_emergentes.messagebox.showinfo("Error al agregado el pedido", f"Ocurrió un error al agregar la tabla de tiempos de modelos cargada") 
    
        else:
            ventanas_emergentes.messagebox.showinfo("Pedido Agregado", f"Se agregó correctamente la tabla de tiempos de modelos cargada")

    except:
        ventanas_emergentes.messagebox.showinfo("Error al agregado el pedido", f"Ocurrió un error al agregar la tabla de tiempos de modelos cargada") 

def aceptar_agregar_referencias(ventana, bbdd):
    ventana.rootAux.destroy()
    print("PRESIONÓ AGREGAR REFERENCIAS")
    print("Aun no se almacenan, ni se cargan los modelos en el pedido")

def aceptar_exportar_to_excel(ventana, df, nombreVentana):
    ruta = nombraArchivoExcel(nombreVentana)
    ventana.rootAux.destroy()
    ventanas_emergentes.desea_exportar(nombreExcel = ruta,
                                       nombreVentana = nombreVentana,
                                       df = df)
    
def verificar_pedidos_vehiculos(bbdd, pedidoNuevo, df_vehiculos, df_tiempos):
    consulta_pedido    = BBDD.leer_pedido(bbdd, pedidoNuevo)
    consulta_vehiculos = BBDD.leer_vehiculos_df(bbdd)
    consulta_tiempos   = BBDD.leer_tiempos_vehiculos_df(bbdd)

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

def nombraArchivoExcel(nombre):
    return nombre + '__' + '.xlsx'

def cancelar(ventana):
    ventana.rootAux.destroy()

###############################################################################
######################### EVENTOS PARA EL SCHEDULING ##########################
###############################################################################

def abrirFechayHoraProg(tipoPrograma, pedido, bbdd):
    ventana = ventanas_topLevel.EstableceFechaHora(pedido)
    ventana.asignaFuncion(lambda:aceptarFechayHoraProg(ventana, tipoPrograma, bbdd), lambda:cancelar(ventana))
    
def aceptarFechayHoraProg(ventana, tipoPrograma, bbdd):
    #RECOGER LOS DATOS DE LA VENTANA DE FECHA Y HORA
    fecha = ventana.varFecha.get()
    hora = ventana.varHora.get()
    print(f"Fecha: {fecha}, Hora: {hora}")
    ventana.rootAux.destroy()

    #RECOGER DE LA BASE DE DATOS TODA LA INFORMACIÓN DE LA PLANTA Y GENERAR LOS OBJETOS PARA EL PROGRAMADOR
    modelo_clases.obtiene_datos_iniciales()
    procesos, objeModelos, objeVehiculos, objeTecnicos, objePedidos, tiempos = modelo_instancias.obtiene_datos_iniciales()

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
        diccPrograma = modelo_clases.programa_completo(pedido     = pedido_a_programar,
                                                       tecnicos   = tecnicos_a_programar,
                                                       horizonte  = 4000,
                                                       fechaStart = fecha,
                                                       horaStart  = hora)
        horizonte_calculado = modelo_clases.calcular_horizonte(pedido_a_programar)
        print(f"el horizonte es {horizonte_calculado}")

    if tipoPrograma == "inmediato":
        diccPrograma = modelo_clases.programa_inmediato(pedido     = pedido_a_programar,
                                                        tecnicos   = tecnicos_a_programar,
                                                        horizonte  = 4000,
                                                        fechaStart = fecha,
                                                        horaStart  = hora)
        horizonte_calculado = modelo_clases.calcular_horizonte(pedido_a_programar)
        print(f"el horizonte es {horizonte_calculado}")

    if tipoPrograma == "por procesos":
        
        procesos_a_programar = [id_proceso for id_proceso, seleccionado in glo.check_procesos.items()
                                if seleccionado.get() == 1]
        
        print(pedido_a_programar)
        print(tecnicos_a_programar)
        print(procesos_a_programar)

        diccPrograma = modelo_clases.programar_procesos(pedido = pedido_a_programar,
                                           tecnicos   = tecnicos_a_programar,
                                           procesos   = procesos_a_programar,
                                           horizonte  = 4000,
                                           fechaStart = fecha,
                                           horaStart  = hora,
                                           bbdd       = glo.base_datos)
        horizonte_calculado = modelo_clases.calcular_horizonte(pedido_a_programar)
        print(f"el horizonte es {horizonte_calculado}")

    ########## GRAFICAR PROGRAMACIÓN EN GANTT ##########
    modelo_llamarGantt.generar_gantt_tecnicos(personal    = tecnicos_a_programar,
                                              fechaStart  = fecha,
                                              horaStart   = hora,
                                              horizonte_calculado = horizonte_calculado)
    modelo_llamarGantt.generar_gantt_vehiculos(pedido     =  pedido_a_programar,
                                              fechaStart  = fecha,
                                              horaStart   = hora,
                                              horizonte_calculado = horizonte_calculado)
    
    ########## PREPARAR INFORMACIÓN PARA BASE DE DATOS ############
    id_programa = diccPrograma["id"]
    df_previo   = diccPrograma["programa"]
    df_programa = transformar_dataframe_ordenes(df_ordenes  = df_previo,
                                                id_programa = id_programa,
                                                bbdd        = bbdd)
    print(id_programa)
    print(df_programa)


    abrirVistaPrevia_programa(pedido    = pedido_a_programar,
                              programa  = id_programa,
                              df_to_BD  = df_programa,
                              df_previo = df_previo,
                              bbdd      = bbdd)


def abrirVistaPrevia_programa(pedido, programa, df_to_BD, df_previo, bbdd):
    titulo =f"Programa de producción\nPedido: {pedido.id_pedido}\nId Programa : {programa}"
    ventana = ventanas_topLevel.VentanaVistaPrevia(nombreVentana = titulo,
                                                   df            = df_previo,
                                                   bbdd          = bbdd)
    ventana.asignafuncion(funcionAceptar  = lambda : aceptar_guardar_programa(ventana, programa, df_to_BD, bbdd),
                          funcionCancelar = ventana.rootAux.destroy)

def aceptar_guardar_programa(ventana, programa, df_programa, bbdd):
    id_inicial  = programa
    consecutivo = BBDD.next_consecutivoPrograma(bbdd)
    id_programa = id_inicial + "_" + str(consecutivo)
    ventana.rootAux.destroy()
    print(programa)
    print(df_programa)

    cargaOrdenes  = BBDD.insertar_ordenes_df(bbdd, df_programa)
    cargaPrograma = BBDD.insertar_programa(bbdd, id_programa, consecutivo)

    if cargaOrdenes is False:
        if cargaPrograma is False:
            ventanas_emergentes.messagebox.showinfo("Error al agregar programa y órdenes", f"Ocurrió un error al añadir las órdenes y el programa a la base de datos")
        ventanas_emergentes.messagebox.showinfo("Error al agregar las órdenes", f"Ocurrió un error al añadir las órdenes a la base de datos") 

    elif cargaPrograma is False:
        ventanas_emergentes.messagebox.showinfo("Error al agregar programa", f"Ocurrió un error al añadir el programa a la base de datos")
    
    else:
        ventanas_emergentes.messagebox.showinfo("Programa Agregado", f"Se agregaron correctamente las órdenes y el  programa de producción a la base de datos")

###############################################################################
###############################################################################
###############################################################################


###############################################################################
####################### FUNCIONES GENERADORAS DE ID ###########################
###############################################################################
def genera_idTecnico(nombre, apellido, documento):
    return nombre[:4] + apellido[:4] + str(documento)[-6:]

def genera_idModelo(marca, modelo):
    return marca + "-" + modelo

def elimina_Duplicados_df(df, columna):
    duplicados = df[df.duplicated(subset=[columna], keep=False)]
    sin_duplicados = df.drop_duplicates(subset=[columna], keep='first')
    return sin_duplicados, duplicados


###############################################################################
####################### FUNCIONES PARA TRANSFORMAR DF #########################
###############################################################################
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
    for col in df.columns[1:]:
        for i in range(len(df)):
            combinacion_columna.append(f"{col}-{df.at[i, columna_principal]}")  # Combinar valor de la primera columna con el encabezado
            valores_principal.append(df.at[i, columna_principal])  # Valores de la primera columna
            encabezado.append(col)  # Encabezado actual
            valor.append(df.iloc[i][col])  # Valor del cuerpo del DataFrame
    
    # Crear el nuevo DataFrame con las 4 columnas
    nuevo_df = pd.DataFrame({
        combinacion_ids  : combinacion_columna,
        "ID_PROCESO"     : encabezado,
        columna_principal: valores_principal,
        "TIEMPO"         : valor
    })
    
    return nuevo_df

def transformar_vehiculos_pedido_cargado(df, id_pedido, fecha_ingreso, bbdd):

    print("___________________EJECUTANDO TRANSFORMACION___________________")
    df_ref_idModelos = BBDD.leer_referencias_modelos_df(bbdd)        
    print(df)                              # lee las referencias en la BBDD
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

    df_mod_idModelos = BBDD.leer_modelos_id_modelos(bbdd)                                       # Incluimos los id_modelos    
    df_combinado2 = pd.merge(df_combinado1, df_mod_idModelos, on="ID_MODELO", how="left")
    print(df_combinado2)

    tiempos_modelos = BBDD.leer_tiempos_modelos_df(bbdd)                                  # INcluimos los tiempos
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

    df_reducido = df_ordenes.drop(["marca",                           #RETIRAR LAS COLUMNAS QUE NO VAN EN LA BBDD
                                    "modelo",
                                    "color",
                                    "novedades",
                                    "pedido",
                                    "nombre_tecnico",
                                    "plazo"],
                       axis=1)
    df_reducido["id_programa"] = id_programa                           # AÑADIR EL MISMO PROGRAMA A TODAS LAS ÓRDENES
    df_reducido = df_reducido.rename(columns={"proceso":"ID_PROCESO"}) # CAMBIAR EL NOMBRE DE LA COLUMNA DE PROCESO
    print(df_reducido.to_string())
    return df_reducido
