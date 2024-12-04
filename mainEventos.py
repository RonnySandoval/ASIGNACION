import re
import os
import pandas as pd
from tkinter.filedialog import askopenfilename
import creadorBD
import BBDD
import glo
import menu.stepsNuevaPlanta as steps_nueva_planta
import menu.ventanaNuevaPlanta as ventanaNuevaPlanta
import ventanas_emergentes
import modelo_clases, modelo_instancias
import root
import menu_principal

def abrir_planta():
    ruta = askopenfilename(title="Seleccionar la Planta",
                            filetypes=[("Archivos Base de datos sqlite", "*.db")])
    print(ruta)
    glo.base_datos = os.path.basename(ruta)

    print(glo.base_datos)
    #modelo_clases.obtiene_datos_iniciales()
    #modelo_instancias.obtiene_datos_iniciales()

    raiz = glo.raiz_principal
    raiz.base_root(glo.base_datos)
    menu_principal.crearMenuPrincipal(raiz)
    root.construye_root(raiz)
    
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
    
    nueva_root(bbdd = base_datos)

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

def nueva_root(bbdd):
    #CREAR VENTANA PRINCIPAL CON SU MENÚ
    glo.base_datos = bbdd
    modelo_clases.obtiene_datos_iniciales()
    modelo_instancias.obtiene_datos_iniciales()

    raiz = glo.raiz_principal
    raiz.base_root(glo.raiz_principal)
    menu_principal.crearMenuPrincipal(raiz)
    root.construye_root(raiz)

def genera_tiempos_modelos_default(df_modelos, df_procesos):
    df_combinaciones = pd.merge(df_modelos[['ID_MODELO']],    # Crear el DataFrame con las combinaciones deseadas
                                df_procesos[['ID_PROCESO']],
                                how='cross')
    df_combinaciones['PROCESO_MODELO'] = df_combinaciones['ID_PROCESO'] + '-' + df_combinaciones['ID_MODELO']    # Crear la columna 'PROCESO_MODELO'
    df_combinaciones = df_combinaciones[['PROCESO_MODELO',    # Resultado final
                                         'ID_PROCESO',
                                         'ID_MODELO']]
    df_combinaciones['TIEMPO'] = 0                            # Añadir tiempos por defecto
    print(df_combinaciones)                                   # Mostrar el resultado
    return df_combinaciones

def genera_idTecnico(nombre, apellido, documento):
    return nombre[:4] + apellido[:4] + str(documento)[-6:]

def genera_idModelo(marca, modelo):
    return marca + "-" + modelo

def elimina_Duplicados_df(df, columna):
    duplicados = df[df.duplicated(subset=[columna], keep=False)]
    sin_duplicados = df.drop_duplicates(subset=[columna], keep='first')
    return sin_duplicados, duplicados
