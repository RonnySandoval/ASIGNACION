import sqlite3
import pandas as pd
import os
import ventanas_emergentes as ventEmerg
import fechahora
#from planta import modelos, marcas, tiempos


###########################################################################
########################### MANEJO DE TABLAS ##############################
###########################################################################
def crear_tabla(bbdd):
    try:
        # Conectarse a la base de datos
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()
        
        # Crear el comando SQL para eliminar la tabla
        drop_table_script = f'''CREATE TABLE IF NOT EXISTS TECNICOS_PROCESOS_PRUEBA (
        TEC_PROC TEXT PRIMARY KEY,
        ID_TECNICO TEXT NOT NULL,
        ID_PROCESO TEXT NOT NULL)'''
        cursor.execute(drop_table_script)
        conn.commit()
        print(f"Tabla creada exitosamente.")
        
    except sqlite3.Error as e:
        print(f"Error al crear la tabla: {e}")
    
    finally:
        conn.close()

def eliminar_tabla(bbdd, nombre_tabla):
    try:
        # Conectarse a la base de datos
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()
        
        # Crear el comando SQL para eliminar la tabla
        drop_table_script = f"DROP TABLE IF EXISTS {nombre_tabla}"
        cursor.execute(drop_table_script)
        conn.commit()
        print(f"Tabla '{nombre_tabla}' eliminada exitosamente.")
        
    except sqlite3.Error as e:
        print(f"Error al eliminar la tabla: {e}")
    
    finally:
        conn.close()

def renombrar_tabla(bbdd, tabla_actual, nueva_tabla):
    # Conectar a la base de datos
    conn = sqlite3.connect(bbdd)
    cursor = conn.cursor()

    try:
        # Renombrar la tabla
        cursor.execute(f"ALTER TABLE {tabla_actual} RENAME TO {nueva_tabla}")
        print(f"Tabla '{tabla_actual}' renombrada a '{nueva_tabla}' correctamente.")
    except sqlite3.Error as e:
        print(f"Error al renombrar la tabla: {e}")
    finally:
        # Cerrar la conexión
        conn.commit()
        conn.close()

###########################################################################
############################# PARA PARA INSERTAR ##########################
###########################################################################

def insertar_info_planta(bbdd, nombre, descripcion):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()          
        insert_data_script = """INSERT INTO INFORMACION
                                    (NOMBRE_PLANTA, DESCRIPCION)
                                    VALUES (?, ?)
                                """
        cursor.execute(insert_data_script, ( nombre, descripcion))
        conn.commit()
        print("Registro de información general de planta añadido")
        request =None
        
    except sqlite3.Error as e:
        print(f"Error al insertar la información genenral de planta: {e}")
        request = False

    except UnboundLocalError as e:
        print(f"No se llenaron todos los campos de la tabla de información general de planta: {e}")
        request = False

    finally:
        conn.close()
        return request

def insertar_proceso(bbdd, id, proceso, descripcion, secuencia):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()          
        insert_data_script = """INSERT INTO PROCESOS 
                                    (ID_PROCESO, NOMBRE, DESCRIPCION, SECUENCIA)
                                    VALUES (?, ?, ?, ?)
                                """
        cursor.execute(insert_data_script, (id, proceso, descripcion, secuencia))
        conn.commit()
        print("Registro añadido")
        
    except sqlite3.Error as e:
        print(f"Error al insertar el proceso: {e}")

    except UnboundLocalError as e:
        print(f"No se llenaron todos los campos: {e}") 

    finally:
        conn.close()

def insertar_procesos_df(bbdd, dataframe):
    try:
        conn = sqlite3.connect(bbdd)

        dataframe.to_sql("PROCESOS", conn, if_exists="append", index=False)
        resultado = pd.read_sql("SELECT * FROM PROCESOS", conn)
        print("dataframe de procesos añadido a la BBDD")
        print(resultado)
        return resultado
    
    except sqlite3.Error as e:
        print(f"Error al insertar el dataframe con los procesos: {e}")
        request = False
    
    except UnboundLocalError as e:
        print(f"No se llenaron los campos obligatorios de la tabla procesos: {e}") 
        request = False
    
    finally:
        conn.close()
        return request


def insertar_modelo(bbdd, id, marca, modelo):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()          
        insert_data_script = """INSERT INTO MODELOS 
                                    (ID_MODELO, MARCA, MODELO)
                                    VALUES (?, ?, ?)
                                """
        cursor.execute(insert_data_script, (id, marca, modelo))
        conn.commit()
        print("Registro añadido")
        
    except sqlite3.Error as e:
        print(f"Error al insertar el modelo: {e}")

    except UnboundLocalError as e:
        print(f"No se llenaron todos los campos: {e}") 

    finally:
        conn.close()

def insertar_modelos_df(bbdd, dataframe):
    try:
        conn = sqlite3.connect(bbdd)

        dataframe.to_sql("MODELOS", conn, if_exists="append", index=False)
        resultado = pd.read_sql("SELECT * FROM MODELOS", conn)
        print("dataframe de modelos añadido a la BBDD")
        print(resultado)

    except sqlite3.Error as e:
        print(f"Error al insertar el dataframe con los modelos: {e}")
        request = False

    except UnboundLocalError as e:
        print(f"No se llenaron los campos obligatorios de la tabla modelos: {e}") 
        request = False

    finally:
        conn.close()
        request = None
        return request

def insertar_tiempo_modelo(bbdd, procmodel, id_proceso, id_modelo, tiempo):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()          
        insert_data_script = """INSERT INTO TIEMPOS_MODELOS 
                                    (PROCESO_MODELO, ID_PROCESO, ID_MODELO, TIEMPO)
                                    VALUES (?, ?, ?, ?)
                                """
        cursor.execute(insert_data_script, (procmodel, id_proceso, id_modelo, tiempo))
        conn.commit()
        print("Registro añadido")
        
    except sqlite3.Error as e:
        print(f"Error al insertar el tiempo: {e}")

    except UnboundLocalError as e:
        print(f"No se llenaron todos los campos: {e}") 

    finally:
        conn.close()

def insertar_tiempos_modelos_df(bbdd, dataframe):
    try:
        conn = sqlite3.connect(bbdd)

        dataframe.to_sql("TIEMPOS_MODELOS", conn, if_exists="append", index=False)
        resultado = pd.read_sql("SELECT * FROM TIEMPOS_MODELOS", conn)                     # Leer los datos para verificar
        print("dataframe de tiempos de modelos añadido a la BBDD")
        print(resultado)
        request = resultado

    except sqlite3.Error as e:
        print(f"Error al insertar el dataframe con los tiempos de modelos: {e}")
        request = False

    except UnboundLocalError as e:
        print(f"No se llenaron los campos obligatorios de la tabla de tiempos de modelos: {e}") 
        request = False

    finally:
        conn.close()
        return request

def insRem_tiempos_modelos_df(bbdd, dataframe):
    try:
        # Usar 'with' para asegurar el cierre de la conexión de forma automática
        with sqlite3.connect(bbdd) as conn:
            cursor = conn.cursor()

            # Crear una lista de tuplas con los valores del dataframe
            data = [(row['PROCESO_MODELO'], row['ID_PROCESO'], row['ID_MODELO'], row['TIEMPO']) for _, row in dataframe.iterrows()]

            # Usar un solo comando INSERT OR REPLACE INTO para todos los registros
            cursor.executemany('''
                INSERT OR REPLACE INTO TIEMPOS_MODELOS (PROCESO_MODELO, ID_PROCESO, ID_MODELO, TIEMPO)
                VALUES (?, ?, ?, ?)
            ''', data)

            conn.commit()  # Hacer commit para guardar los cambios
            print("Registros de tiempos actualizados exitosamente.")
            return None  # Retornar None si no hay errores
    
    except sqlite3.Error as e:
        print(f"Error al actualizar los registros de tiempos: {e}")
        return False  # Retornar False en caso de error


def insertar_tecnico(bbdd, id, nombre, apellido, documento, especialidad):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()          
        insert_data_script = """INSERT INTO TECNICOS 
                                    (ID_TECNICO, NOMBRE, APELLIDO, DOCUMENTO, ESPECIALIDAD)
                                    VALUES (?, ?, ?, ?, ?)
                                """
        cursor.execute(insert_data_script, (id, nombre, apellido, documento, especialidad))
        conn.commit()
        print("Registro añadido")
        
    except sqlite3.Error as e:
        print(f"Error al insertar el registro: {e}")

    except UnboundLocalError as e:
        print(f"No se llenaron todos los campos: {e}") 

    finally:
        conn.close()

def insertar_tecnico_proceso(bbdd, proc_tec, id_tecnico, id_proceso):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()          
        insert_data_script = """INSERT INTO TECNICOS_PROCESOS
                                    (TEC_PROC, ID_TECNICO, ID_PROCESO)
                                    VALUES (?, ?, ?)
                                """
        cursor.execute(insert_data_script, (proc_tec, id_tecnico, id_proceso))
        conn.commit()
        print("Registro de especialidad de técnico añadido")
        
    except sqlite3.Error as e:
        print(f"Error al insertar el registro de especialidad de técnico: {e}")

    except UnboundLocalError as e:
        print(f"No se llenaron todos los campos: {e}") 

    finally:
        conn.close()

def insertar_tecnicos_df(bbdd, dataframe):
    try:
        conn = sqlite3.connect(bbdd)

        dataframe.to_sql("TECNICOS", conn, if_exists="append", index=False)
        resultado = pd.read_sql("SELECT * TECNICOS", conn)
        print("dataframe de tecnicos añadido a la BBDD")
        print(resultado)

    except sqlite3.Error as e:
        print(f"Error al insertar el dataframe con los tecnicos: {e}")
        request = False

    except UnboundLocalError as e:
        print(f"No se llenaron los campos obligatorios de la tabla tecnicos: {e}") 
        request = False

    finally:
        conn.close()
        request = None
        return request

def insertar_tecnicos_procesos_df(bbdd, dataframe):
    try:
        conn = sqlite3.connect(bbdd)

        dataframe.to_sql("TECNICOS_PROCESOS", conn, if_exists="append", index=False)
        resultado = pd.read_sql("SELECT * TECNICOS_PROCESOS", conn)
        print("dataframe de especialidades de tecnicos añadidos a la BBDD")
        print(resultado)

    except sqlite3.Error as e:
        print(f"Error al insertar el dataframe con los tecnicos_procesos: {e}")
        request = False

    except UnboundLocalError as e:
        print(f"No se llenaron los campos obligatorios de la tabla de especialidades de tecnicos: {e}") 
        request = False

    finally:
        conn.close()
        request = None
        return request

def insertar_vehiculo(bbdd, chasis, fecha_ingreso, id_modelo, color, novedades, subcontratar, id_pedido):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()

        if all(item is not None for item in (chasis, id_modelo, color, id_pedido,)):
            
            insert_data_script = """INSERT INTO vehiculos 
                                    (CHASIS, FECHA_INGRESO, ID_MODELO, COLOR, NOVEDADES, SUBCONTRATAR, ID_PEDIDO)
                                    VALUES  (?, ?, ?, ?, ?, ?, ?)
                                """
            
        cursor.execute(insert_data_script, (chasis, fecha_ingreso, id_modelo, color, novedades, subcontratar, id_pedido))
        conn.commit()
        print("Registro añadido")
        
    except sqlite3.Error as e:
        print(f"Error al insertar el vehículo: {e}")

    except UnboundLocalError as e:
        print(f"No se llenaron todos los campos: {e}") 

    finally:
        conn.close()

def insertar_tiempo_vehiculo(bbdd, procvehi, id_proceso, chasis, tiempo):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()          
        insert_data_script = """INSERT INTO TIEMPOS_VEHICULOS
                                    (PROCESO_CHASIS, ID_PROCESO, CHASIS, TIEMPO)
                                    VALUES (?, ?, ?, ?)
                                """
        cursor.execute(insert_data_script, (procvehi, id_proceso, chasis, tiempo))
        conn.commit()
        print("Registro añadido")
        
    except sqlite3.Error as e:
        print(f"Error al insertar el tiempo: {e}")

    except UnboundLocalError as e:
        print(f"No se llenaron todos los campos: {e}") 

    finally:
        conn.close()

def insertar_vehiculos_df(bbdd, df):
    try:
        conn = sqlite3.connect(bbdd)

        df.to_sql("VEHICULOS", conn, if_exists="append", index=False)                # Guardar en SQLite usando to_sql
        resultado = pd.read_sql("SELECT * FROM VEHICULOS", conn)                     # Leer los datos para verificar
        print("dataframe de vehiculos añadido a la BBDD")
        print(resultado)
        request = None

    except sqlite3.Error as e:
        print(f"Error al insertar el dataframe con los vehiculos: {e}")
        request = False

    except UnboundLocalError as e:
        print(f"No se llenaron los campos obligatorios de la tabla de vehiculos: {e}")
        request = False

    except Exception as e:
        print(f"Error desconocido:  {e}")
        request = False

    finally:
        conn.close()
        return request

def insertar_tiempos_vehiculos_df(bbdd, df):
    try:
        conn = sqlite3.connect(bbdd)

        df.to_sql("TIEMPOS_VEHICULOS", conn, if_exists="append", index=False)               # Guardar en SQLite usando to_sql
        resultado = pd.read_sql("SELECT * FROM TIEMPOS_VEHICULOS", conn)                     # Leer los datos para verificar
        print("dataframe de tiempos de vehiculos añadido a la BBDD")
        print(resultado)

    except sqlite3.Error as e:
        print(f"Error al insertar el dataframe con los tiempos de vehiculos: {e}")
        request = False

    except UnboundLocalError as e:
        print(f"No se llenaron los campos obligatorios: {e}") 
        request = False

    except Exception as e:
        print(f"Error desconocido:  {e}")

    finally:
        conn.close()
        request = None
        return request

def insertar_pedido(bbdd, id_pedido, cliente, fecha_recepcion, fecha_ingreso, fecha_estimada, fecha_entrega, consecutivo):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()          
        insert_data_script = """INSERT INTO PEDIDOS
                                    (ID_PEDIDO, CLIENTE, FECHA_RECEPCION, FECHA_INGRESO, ENTREGA_ESTIMADA, FECHA_ENTREGA, CONSECUTIVO)
                                    VALUES (?, ?, ?, ?, ?, ?, ?)
                                """
        cursor.execute(insert_data_script, (id_pedido, cliente, fecha_recepcion, fecha_ingreso, fecha_estimada, fecha_entrega, consecutivo))
        conn.commit()
        print("Registro añadido")
        
    except sqlite3.Error as e:
        print(f"Error al insertar el pedido: {e}")

    except UnboundLocalError as e:
        print(f"No se llenaron todos los campos: {e}") 

    except Exception as e:
        print(f"Error desconocido: {e}") 

    finally:
        conn.close()

def insertar_historico(bbdd, codigo, chasis, tec, proc, observ, start, end, delta, estado):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()

        if all(item is not None for item in (codigo, chasis, tec, proc, start)):
            
            insert_data_script = """INSERT INTO HISTORICOS 
                                    (CODIGO_ASIGNACION, CHASIS, ID_TECNICO, ID_PROCESO, OBSERVACIONES, INICIO, FIN, DURACION, ESTADO)
                                    VALUES  (?, ?, ?, ?, ?, ?, ?, ?, ?)
                                """
            
        cursor.execute(insert_data_script, (codigo, chasis, tec, proc, observ, start, end, delta, estado))
        conn.commit()
        print("Registro de Histórico añadido")
        
    except sqlite3.Error as e:
        print(f"Error al insertar la Asignación: {e}")

    except UnboundLocalError as e:
        print(f"No se llenaron los campos obligatorios: {e}") 

    finally:
        conn.close()

def insertar_referencias_df(bbdd, dataframe):
    try:
        conn = sqlite3.connect(bbdd)

        dataframe.to_sql("MODELOS_REFERENCIAS", conn, if_exists="append", index=False)     # Guardar en SQLite usando to_sql
        resultado = pd.read_sql("SELECT * FROM MODELOS_REFERENCIAS", conn)                     # Leer los datos para verificar
        print("dataframe de referencias de modeslo añadido a la BBDD")
        print(resultado)
    except sqlite3.Error as e:
        print(f"Error al insertar el dataframe con las referencias de modelos: {e}")
        request = False

    except UnboundLocalError as e:
        print(f"No se llenaron los campos obligatorios de la tabla de referencias de modelos: {e}") 
        request = False
        
    finally:
        conn.close()
        return request

def insertar_ordenes_df(bbdd, dataframe):
    try:
        conn = sqlite3.connect(bbdd)

        dataframe.to_sql("ORDENES", conn, if_exists="append", index=False)     # Guardar en SQLite usando to_sql
        resultado = pd.read_sql("SELECT * FROM ORDENES", conn)                     # Leer los datos para verificar
        print("dataframe de órdenes añadido a la BBDD")
        print(resultado)
        request = resultado
    except sqlite3.Error as e:
        print(f"Error al insertar el dataframe con las órdenes: {e}")
        request = False

    except UnboundLocalError as e:
        print(f"No se llenaron los campos obligatorios de la tabla de órdenes: {e}") 
        request = False
        
    finally:
        conn.close()
        return request
    
def insertar_programa(bbdd, nombrePrograma, descripcion, consecutivo):

    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()          
        insert_data_script = """INSERT INTO PROGRAMAS
                                    (ID_PROGRAMA, DESCRIPCION, CONSECUTIVO)
                                    VALUES (?, ?, ?)
                                """
        cursor.execute(insert_data_script, (nombrePrograma, descripcion, consecutivo))
        conn.commit()
        print(f"Registro de programa de producción {nombrePrograma} añadido")
        request = None
        
    except sqlite3.Error as e:
        print(f"Error al insertar el programa de produción {nombrePrograma}: {e}")
        request = False

    except UnboundLocalError as e:
        print(f"No se llenaron todos los campos de la tabla de programas: {e}")
        request = False

    finally:
        conn.close()
        return request

###########################################################################
############################ PARA PARA LEER ###############################
###########################################################################

def leer_historicos(bbdd):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM HISTORICOS')
        registros = cursor.fetchall()
        print(registros)

    except sqlite3.Error as e:
        print(f"Error al leer la Tabla de Históricoss: {e}")

    finally:
        conn.close()

    return registros

def leer_historicos_completo(bbdd):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()

        cursor.execute('''SELECT DISTINCT
                            h.CODIGO_ASIGNACION,
                            h.CHASIS,
                            t.NOMBRE AS NOMBRE_TECNICO,
                            p.NOMBRE AS NOMBRE_PROCESO,
                            v.ID_MODELO,
                            v.COLOR,
                            h.INICIO,
                            h.FIN,
                            h.DURACION,
                            h.ESTADO,
                            v.NOVEDADES,
                            h.OBSERVACIONES,
                            v.SUBCONTRATAR,
                            v.ID_PEDIDO
                        FROM 
                            HISTORICOS AS h
                        JOIN 
                            PROCESOS AS p ON h.ID_PROCESO = p.ID_PROCESO
                        JOIN 
                            TECNICOS AS t ON h.ID_TECNICO = t.ID_TECNICO
                        JOIN 
                            VEHICULOS AS v ON h.CHASIS = v.CHASIS''')
        registros = cursor.fetchall()
        print(registros)

    except sqlite3.Error as e:
        print(f"Error al leer la Tabla de Tiempos_Vehiculos y de Vehiculos: {e}")
        registros = None

    finally:
        conn.close()    # Cierra la conexión
    
    return registros

def leer_historico_chasis(bbdd, chasis):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM HISTORICOS WHERE CHASIS = ?', (chasis,))
        registros = cursor.fetchall()
        print(registros)

    except sqlite3.Error as e:
        print(f"Error al leer la Tabla de Históricos: {e}")
        registros = None
        
    finally:
        conn.close()

    return registros

def leer_historico_completo(bbdd, chasis):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()
        vehiculo = chasis
        cursor.execute('''SELECT 
                            h.CODIGO_ASIGNACION,
                            h.CHASIS,
                            t.NOMBRE || ' ' || t.APELLIDO AS NOMBRE_COMPLETO,
                            h.ID_PROCESO,
                            v.ID_MODELO,
                            v.COLOR,
                            h.INICIO,
                            h.FIN,
                            h.DURACION,
                            h.ESTADO,
                            v.NOVEDADES,
                            h.OBSERVACIONES,
                            v.SUBCONTRATAR,
                            v.ID_PEDIDO
                        FROM 
                            HISTORICOS AS h
                        JOIN 
                            TECNICOS AS t ON h.ID_TECNICO = t.ID_TECNICO
                        JOIN 
                            VEHICULOS AS v ON h.CHASIS = v.CHASIS
                        WHERE h.CHASIS = ?''', (vehiculo,))
        registros = cursor.fetchall()
        print(registros)

    except sqlite3.Error as e:
        print(f"Error al leer la Tabla de Tiempos_Vehiculos y de Vehiculos: {e}")
        registros = None

    finally:
        conn.close()    # Cierra la conexión
    
    return registros

def leer_historico_completo_porId(bbdd, id):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()
        codigo = id
        cursor.execute('''SELECT 
                            h.CODIGO_ASIGNACION,
                            h.CHASIS,
                            t.NOMBRE || ' ' || t.APELLIDO AS NOMBRE_COMPLETO,
                            h.ID_PROCESO,
                            v.ID_MODELO,
                            v.COLOR,
                            h.INICIO,
                            h.FIN,
                            h.DURACION,
                            h.ESTADO,
                            v.NOVEDADES,
                            v.SUBCONTRATAR,
                            h.OBSERVACIONES,
                            v.ID_PEDIDO
                        FROM 
                            HISTORICOS AS h
                        JOIN 
                            TECNICOS AS t ON h.ID_TECNICO = t.ID_TECNICO
                        JOIN 
                            VEHICULOS AS v ON h.CHASIS = v.CHASIS
                        WHERE h.CODIGO_ASIGNACION = ?''', (codigo,))
        registro = cursor.fetchone()
        print(registro)

    except sqlite3.Error as e:
        print(f"Error al leer la Tabla de Tiempos_Vehiculos y de Vehiculos: {e}")
        registro = None

    finally:
        conn.close()    # Cierra la conexión
    
    return registro

def leer_ids_proceso_modelo(bbdd, proc_modelo):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()          
        cursor.execute("""
                        SELECT *
                            FROM TIEMPOS_MODELOS
                            WHERE ID_MODELO=?""",
                            (proc_modelo,))
        datos = cursor.fetchall()
        
    except sqlite3.Error as e:
        print(f"Error al leer el registro: {e}")
        datos = None

    finally:
        conn.close()
        return datos

def leer_modelo(bbdd, id_modelo):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()          
        id = id_modelo
        cursor.execute("SELECT * FROM MODELOS WHERE ID_MODELO=?", (id,))
        datos = cursor.fetchone()
        print(datos)
    except sqlite3.Error as e:
        print(f"Error al leer el registro: {e}")

    finally:
        conn.close()
        return datos

def leer_modelos(bbdd):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()          
        cursor.execute("SELECT * FROM MODELOS")
        datos = cursor.fetchall()
        conn.commit()
        
    except sqlite3.Error as e:
        print(f"Error al leer el registro: {e}")
        datos = None

    finally:
        conn.close()
        return datos

def leer_modelos_marcas(bbdd):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()          
        cursor.execute("SELECT MARCA, MODELO FROM MODELOS")
        datos = cursor.fetchall()
        print(datos)

    except sqlite3.Error as e:
        print(f"Error al leer el registro: {e}")

    finally:
        conn.close()
        return datos

def leer_modelos_marcas_df(bbdd):
    try:
        conn = sqlite3.connect(bbdd)
        query = "SELECT ID_MODELO, MARCA, MODELO FROM MODELOS"
        dataframe = pd.read_sql_query(query, conn)
        print(dataframe)

    except sqlite3.Error as e:
        print(f"Error al leer la tabla de marcas y modelos: {e}")
        dataframe = None
    finally:
        conn.close()
        return dataframe

def leer_modelos_id_modelos(bbdd):
    try:
        conn = sqlite3.connect(bbdd)
        df_datos = pd.read_sql_query("SELECT MODELO, ID_MODELO FROM MODELOS", conn)
        print(df_datos)

    except sqlite3.Error as e:
        print(f"Error al leer el registro: {e}")

    finally:
        conn.close()
    return df_datos

def leer_procesos(bbdd):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()          
        cursor.execute("SELECT NOMBRE FROM PROCESOS ")
        datos = cursor.fetchall()
        registros =[]
        for tupla in datos:             #ciclo para desempaquetar el formato de tuplas que arroja la lectura
            nombreProceso = tupla[0]
            registros.append(nombreProceso)
        conn.commit()
        
    except sqlite3.Error as e:
        print(f"Error al leer el registro: {e}")

    finally:
        conn.close()
        return registros

def leer_procesos_secuencia(bbdd):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()          
        cursor.execute("SELECT NOMBRE FROM PROCESOS ORDER BY SECUENCIA")
        datos = cursor.fetchall()
        registros =[]
        for tupla in datos:             #ciclo para desempaquetar el formato de tuplas que arroja la lectura
            nombreProceso = tupla[0]
            registros.append(nombreProceso)
        conn.commit()
        
    except sqlite3.Error as e:
        print(f"Error al leer el registro: {e}")
        registros =[]

    finally:
        conn.close()
        return registros

def leer_procesos_completo(bbdd):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()          
        cursor.execute("SELECT * FROM PROCESOS")
        datos = cursor.fetchall()
        conn.commit()
        
    except sqlite3.Error as e:
        print(f"Error al leer el registro: {e}")

    finally:
        conn.close()
        return datos

def leer_procesos_df(bbdd):
    try:
        conn = sqlite3.connect(bbdd)
        query = "SELECT * FROM PROCESOS"
        dataframe = pd.read_sql_query(query, conn)
        print(dataframe)

    except sqlite3.Error as e:
        print(f"Error al leer la tabla de procesos: {e}")
        dataframe = None
    finally:
        conn.close()
        return dataframe

def leer_tecnicos(bbdd):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()          
        cursor.execute("SELECT * FROM TECNICOS")
        datos = cursor.fetchall()  # Mantener la consulta original
    except sqlite3.Error as e:
        print(f"Error al leer el registro: {e}")
        datos = []  # Inicializar como lista vacía en caso de error
    finally:
        conn.close()
    
    return datos

def leer_tecnicos_df(bbdd):
    try:
        conn = sqlite3.connect(bbdd)
        query = "SELECT * FROM TECNICOS"
        dataframe = pd.read_sql_query(query, conn)
        print(dataframe)

    except sqlite3.Error as e:
        print(f"Error al leer la tabla de técnicos: {e}")
        dataframe = None

    finally:
        conn.close()
        return dataframe

def leer_tecnicos_modificado(bbdd):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()          
        cursor.execute("SELECT * FROM TECNICOS")
        datos = cursor.fetchall()
        
        # Modificar los datos según lo solicitado
        datos_modificados = [
            (tecnico[0], f"{tecnico[1]} {tecnico[2]}", tecnico[4])
            for tecnico in datos
        ]
        
    except sqlite3.Error as e:
        print(f"Error al leer el registro: {e}")
        datos_modificados = []  # Inicializar como lista vacía en caso de error

    finally:
        conn.close()
    
    return datos_modificados

def leer_tecnicos_procesos_df(bbdd):
    try:
        conn = sqlite3.connect(bbdd)
        query = "SELECT * FROM TECNICOS_PROCESOS"
        dataframe = pd.read_sql_query(query, conn)
        print(dataframe)

    except sqlite3.Error as e:
        print(f"Error al leer la tabla de especialidades de tecnicos: {e}")
        dataframe = None

    except Exception as e:
        print(f"Error al leer la base de datos: {e}")
        datos_modificados = None
    finally:
        conn.close()
        return dataframe

def leer_tecnicos_por_proceso(bbdd, id_proceso):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()          
        cursor.execute("""
                    SELECT
                       *
                    FROM
                       TECNICOS
                    LEFT JOIN
                       TECNICOS_PROCESOS
                    ON
                       TECNICOS_PROCESOS.ID_TECNICO = TECNICOS.ID_TECNICO
                    WHERE
                       TECNICOS_PROCESOS.ID_PROCESO = ?
                       """,
                    (id_proceso))
        datos = cursor.fetchall()
        
        # Modificar los datos según lo solicitado
        datos_modificados = [
            (tecnico[0],
             f"{tecnico[1]} {tecnico[2]}",
             tecnico[4])
            for tecnico in datos
        ]
        
    except sqlite3.Error as e:
        print(f"Error al leer el registro de especialidades de técnicos: {e}")
        datos_modificados = []  # Inicializar como lista vacía en caso de error

    finally:
        conn.close()
    
    return datos_modificados

def leer_vehiculo(bbdd, chasis):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()

        vehiculo = chasis
        cursor.execute('''SELECT 
                            CHASIS,
                            FECHA_INGRESO,
                            ID_MODELO,
                            COLOR,
                            NOVEDADES,
                            SUBCONTRATAR,
                            ID_PEDIDO
                        FROM vehiculos
                        WHERE CHASIS=?''', 
                        (vehiculo,))
        registro = cursor.fetchone()
        print(registro)

    except sqlite3.Error as e:
        print(f"Error al leer el vehiculo: {e}")
        registro = False

    finally:
        conn.close()

    return registro

def leer_tiempos_vehiculo(bbdd, chasis):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()

        vehiculo = chasis
        cursor.execute('SELECT ID_PROCESO, TIEMPO FROM TIEMPOS_VEHICULOS WHERE CHASIS=?', (vehiculo,))
        registro = cursor.fetchall()
        print(registro)

    except sqlite3.Error as e:
        print(f"Error al leer la Tabla de Tiempos_Vehiculos: {e}")

    finally:
        conn.close()

    return registro

def leer_tiempo_vehiculo(bbdd, chasis, id_proceso):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()

        vehiculo = chasis
        id= id_proceso
        cursor.execute('SELECT ID_PROCESO, TIEMPO FROM TIEMPOS_VEHICULOS WHERE CHASIS=? AND ID_PROCESO = ?',
                       (vehiculo, id))
        registro = cursor.fetchall()
        print(registro[0])

    except sqlite3.Error as e:
        print(f"Error al leer la Tabla de Tiempos_Vehiculos: {e}")

    finally:
        conn.close()

    return registro[0][1]

def leer_vehiculo_completo(bbdd, chasis):
    registros = None  # Inicializa registros para manejar el caso de que no se encuentren resultados
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()

        vehiculo = chasis
        cursor.execute('''
                    SELECT
                        VEHICULOS.*,
                        TIEMPOS_VEHICULOS.ID_PROCESO,
                        TIEMPOS_VEHICULOS.TIEMPO
                    FROM
                        VEHICULOS
                    LEFT JOIN
                        TIEMPOS_VEHICULOS
                    ON
                        VEHICULOS.CHASIS = TIEMPOS_VEHICULOS.CHASIS
                    WHERE
                        VEHICULOS.CHASIS = ?
                        ''', (vehiculo,))
        
        registros = cursor.fetchall()  # Esto puede ser None si no hay resultados
        if registros is not None:
            print(registros)
        else:
            print("No se encontraron registros para el chasis proporcionado.")

    except sqlite3.Error as e:
        print(f"Error al leer la Tabla de Tiempos_Vehiculos y de Vehiculos: {e}")

    finally:
        conn.close()    # Cierra la conexión
    
    return registros

def leer_vehiculos(bbdd):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()

        cursor.execute('''SELECT
                            CHASIS,
                            FECHA_INGRESO,
                            ID_MODELO,
                            COLOR, 
                            ESTADO,
                            NOVEDADES,
                            SUBCONTRATAR,
                            ID_PEDIDO
                       FROM VEHICULOS''')
        registros = cursor.fetchall()
        print(registros)

    except sqlite3.Error as e:
        print(f"Error al leer la Tabla de Vehiculos: {e}")

    finally:
        conn.close()

    return registros

def leer_vehiculos_df(bbdd):
    try:
        conn = sqlite3.connect(bbdd)
        query = "SELECT * FROM VEHICULOS"
        dataframe = pd.read_sql_query(query, conn)
        print(dataframe)

    except sqlite3.Error as e:
        print(f"Error al leer la tabla de vehiculos: {e}")
        dataframe = None
    finally:
        conn.close()
        return dataframe

def leer_tiempos_vehiculos(bbdd):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM TIEMPOS_VEHICULOS')
        registros = cursor.fetchall()
        print(registros)

    except sqlite3.Error as e:
        print(f"Error al leer la Tabla de Vehiculos: {e}")

    finally:
        conn.close()

    return registros

def leer_vehiculos_completos(bbdd):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()

        cursor.execute('''
                        SELECT 
                            VEHICULOS.CHASIS,
                            VEHICULOS.FECHA_INGRESO,
                            VEHICULOS.ID_MODELO,
                            VEHICULOS.COLOR,
                            
                            -- Subconsulta para obtener el nombre del proceso o 'ninguno' si es NULL
                            COALESCE(
                                (SELECT PROCESOS.NOMBRE
                                FROM HISTORICOS
                                JOIN PROCESOS ON HISTORICOS.ID_PROCESO = PROCESOS.ID_PROCESO
                                WHERE HISTORICOS.CHASIS = VEHICULOS.CHASIS
                                AND HISTORICOS.ESTADO = 'EN EJECUCION'
                                LIMIT 1),
                                (SELECT PROCESOS.NOMBRE
                                FROM HISTORICOS
                                JOIN PROCESOS ON HISTORICOS.ID_PROCESO = PROCESOS.ID_PROCESO
                                WHERE HISTORICOS.CHASIS = VEHICULOS.CHASIS
                                AND HISTORICOS.ESTADO = 'TERMINADO'
                                AND HISTORICOS.FIN = (
                                    SELECT MAX(FIN)
                                    FROM HISTORICOS AS HIST2
                                    WHERE HIST2.CHASIS = VEHICULOS.CHASIS AND HIST2.ESTADO = 'TERMINADO'
                                )
                                LIMIT 1),
                                'ninguno'
                            ) AS NOMBRE_PROCESO,
                            
                            -- Subconsulta para obtener el estado o 'ninguno' si es NULL
                            COALESCE(
                                (SELECT HISTORICOS.ESTADO
                                FROM HISTORICOS
                                WHERE HISTORICOS.CHASIS = VEHICULOS.CHASIS
                                AND HISTORICOS.ESTADO = 'EN EJECUCION'
                                LIMIT 1),
                                (SELECT HISTORICOS.ESTADO
                                FROM HISTORICOS
                                WHERE HISTORICOS.CHASIS = VEHICULOS.CHASIS
                                AND HISTORICOS.ESTADO = 'TERMINADO'
                                AND HISTORICOS.FIN = (
                                    SELECT MAX(FIN)
                                    FROM HISTORICOS AS HIST2
                                    WHERE HIST2.CHASIS = VEHICULOS.CHASIS AND HIST2.ESTADO = 'TERMINADO'
                                )
                                LIMIT 1),
                                'ninguno'
                            ) AS ESTADO,

                            VEHICULOS.NOVEDADES,
                            VEHICULOS.SUBCONTRATAR,
                            VEHICULOS.ID_PEDIDO
                        FROM
                            VEHICULOS
                        GROUP BY
                            VEHICULOS.CHASIS;
                        ''')
        registros = cursor.fetchall()
        print(registros)

    except sqlite3.Error as e:
        print(f"Error al leer la Tabla de Tiempos_Vehiculos y de Vehiculos: {e}")
        registros = None

    finally:
        conn.close()    # Cierra la conexión
    
    return registros

def leer_vehiculos_por_pedido(bbdd, pedido):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()

        cursor.execute('''
                        SELECT 
                            VEHICULOS.CHASIS,
                            VEHICULOS.ID_MODELO,
                            VEHICULOS.COLOR,
                            
                            -- Subconsulta para obtener el nombre del proceso o 'ninguno' si es NULL
                            COALESCE(
                                (SELECT PROCESOS.NOMBRE
                                FROM HISTORICOS
                                JOIN PROCESOS ON HISTORICOS.ID_PROCESO = PROCESOS.ID_PROCESO
                                WHERE HISTORICOS.CHASIS = VEHICULOS.CHASIS
                                AND HISTORICOS.ESTADO = 'EN EJECUCION'
                                LIMIT 1),
                                (SELECT PROCESOS.NOMBRE
                                FROM HISTORICOS
                                JOIN PROCESOS ON HISTORICOS.ID_PROCESO = PROCESOS.ID_PROCESO
                                WHERE HISTORICOS.CHASIS = VEHICULOS.CHASIS
                                AND HISTORICOS.ESTADO = 'TERMINADO'
                                AND HISTORICOS.FIN = (
                                    SELECT MAX(FIN)
                                    FROM HISTORICOS AS HIST2
                                    WHERE HIST2.CHASIS = VEHICULOS.CHASIS AND HIST2.ESTADO = 'TERMINADO'
                                )
                                LIMIT 1),
                                'ninguno'
                            ) AS NOMBRE_PROCESO,
                            
                            -- Subconsulta para obtener el estado o 'ninguno' si es NULL
                            COALESCE(
                                (SELECT HISTORICOS.ESTADO
                                FROM HISTORICOS
                                WHERE HISTORICOS.CHASIS = VEHICULOS.CHASIS
                                AND HISTORICOS.ESTADO = 'EN EJECUCION'
                                LIMIT 1),
                                (SELECT HISTORICOS.ESTADO
                                FROM HISTORICOS
                                WHERE HISTORICOS.CHASIS = VEHICULOS.CHASIS
                                AND HISTORICOS.ESTADO = 'TERMINADO'
                                AND HISTORICOS.FIN = (
                                    SELECT MAX(FIN)
                                    FROM HISTORICOS AS HIST2
                                    WHERE HIST2.CHASIS = VEHICULOS.CHASIS AND HIST2.ESTADO = 'TERMINADO'
                                )
                                LIMIT 1),
                                'ninguno'
                            ) AS ESTADO
                        FROM
                            VEHICULOS
                        LEFT JOIN 
                            PEDIDOS ON VEHICULOS.ID_PEDIDO = PEDIDOS.ID_PEDIDO
                        WHERE
                            PEDIDOS.ID_PEDIDO = ?
                        GROUP BY
                            VEHICULOS.CHASIS;
                        ''', (pedido,))
        registros = cursor.fetchall()
        print(registros)

    except sqlite3.Error as e:
        print(f"Error al leer la Tabla de Tiempos_Vehiculos y de Vehiculos: {e}")
        registros = None

    finally:
        conn.close()    # Cierra la conexión
    
    return registros

def leer_vehiculos_completos_marcamodelo(bbdd):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()

        cursor.execute('''
                        SELECT 
                            VEHICULOS.CHASIS,
                            VEHICULOS.FECHA_INGRESO,
                            MODELOS.MARCA,
                            MODELOS.MODELO,
                            VEHICULOS.COLOR,
                            
                            -- Subconsulta para obtener el nombre del proceso o 'ninguno' si es NULL
                            COALESCE(
                                (SELECT PROCESOS.ID_PROCESO
                                FROM HISTORICOS
                                JOIN PROCESOS ON HISTORICOS.ID_PROCESO = PROCESOS.ID_PROCESO
                                WHERE HISTORICOS.CHASIS = VEHICULOS.CHASIS
                                AND HISTORICOS.ESTADO = 'EN EJECUCION'
                                LIMIT 1),
                                (SELECT PROCESOS.ID_PROCESO
                                FROM HISTORICOS
                                JOIN PROCESOS ON HISTORICOS.ID_PROCESO = PROCESOS.ID_PROCESO
                                WHERE HISTORICOS.CHASIS = VEHICULOS.CHASIS
                                AND HISTORICOS.ESTADO = 'TERMINADO'
                                AND HISTORICOS.FIN = (
                                    SELECT MAX(FIN)
                                    FROM HISTORICOS AS HIST2
                                    WHERE HIST2.CHASIS = VEHICULOS.CHASIS AND HIST2.ESTADO = 'TERMINADO'
                                )
                                LIMIT 1),
                                'ninguno'
                            ),
                            
                            -- Subconsulta para obtener el estado o 'ninguno' si es NULL
                            COALESCE(
                                (SELECT HISTORICOS.ESTADO
                                FROM HISTORICOS
                                WHERE HISTORICOS.CHASIS = VEHICULOS.CHASIS
                                AND HISTORICOS.ESTADO = 'EN EJECUCION'
                                LIMIT 1),
                                (SELECT HISTORICOS.ESTADO
                                FROM HISTORICOS
                                WHERE HISTORICOS.CHASIS = VEHICULOS.CHASIS
                                AND HISTORICOS.ESTADO = 'TERMINADO'
                                AND HISTORICOS.FIN = (
                                    SELECT MAX(FIN)
                                    FROM HISTORICOS AS HIST2
                                    WHERE HIST2.CHASIS = VEHICULOS.CHASIS AND HIST2.ESTADO = 'TERMINADO'
                                )
                                LIMIT 1),
                                'ninguno'
                            ) AS ESTADO,

                            VEHICULOS.NOVEDADES,
                            VEHICULOS.SUBCONTRATAR,
                            VEHICULOS.ID_PEDIDO,
                            
                            COALESCE(GROUP_CONCAT(TIEMPOS_VEHICULOS.ID_PROCESO || ': ' || TIEMPOS_VEHICULOS.TIEMPO, ' | '), 'Sin procesos') AS PROCESOS_TIEMPOS
                        FROM
                            VEHICULOS
                        LEFT JOIN 
                            TIEMPOS_VEHICULOS ON VEHICULOS.CHASIS = TIEMPOS_VEHICULOS.CHASIS
                        LEFT JOIN 
                            MODELOS ON VEHICULOS.ID_MODELO = MODELOS.ID_MODELO
                        GROUP BY
                            VEHICULOS.CHASIS;
                        ''')
        registros = cursor.fetchall()
        print(registros)

    except sqlite3.Error as e:
        print(f"Error al leer la Tabla de Tiempos_Vehiculos y de Vehiculos: {e}")
        registros = None

    finally:
        conn.close()
    
    return registros

def buscar_vehiculo_por_modelo(bbdd, id_modelo):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()

        id = id_modelo
        cursor.execute('''
                       SELECT *
                            FROM VEHICULOS
                            INNER JOIN MODELOS
                            ON MODELOS.ID_MODELO = VEHICULOS.ID_MODELO
                            WHERE MODELOS.ID_MODELO = ?
                       ''',(id,)
                        )
        registros = cursor.fetchall()
        print(registros)

    except sqlite3.Error as e:
        print(f"Error al leer el vehiculo: {e}")

    finally:
        conn.close()

    return registros

def calcula_tecnicos(bbdd):

    conn = sqlite3.connect(bbdd)
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM TECNICOS;')
    numero_registros = cursor.fetchone()[0]

    conn.close()
    return numero_registros

def calcula_modelos(bbdd):

    conn = sqlite3.connect(bbdd)
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM MODELOS;')
    numero_registros = cursor.fetchone()[0]

    conn.close()
    return numero_registros

def calcula_procesos(bbdd):

    conn = sqlite3.connect(bbdd)
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM PROCESOS;')
    numero_registros = cursor.fetchone()[0]

    conn.close()
    return numero_registros

def obtener_id_modelo(bbdd, modelo):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()
        
        # Obtener el ID_MODELO usando un parámetro
        cursor.execute("SELECT DISTINCT ID_MODELO FROM MODELOS WHERE MODELO=?", (modelo,))
        id_modelo = cursor.fetchone()  # devuelve una tupla o None si no hay resultados
        conn.commit()

    except sqlite3.Error as e:
        print(f"Error al obtener el ID_MODELO: {e}")
        id_modelo = None

    finally:
        conn.close()  # Cerrar la conexión después de usarla

    return id_modelo[0]

def obtener_id_proceso(bbdd, proceso):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()
        
        cursor.execute("SELECT DISTINCT ID_PROCESO FROM TIEMPOS_MODELOS WHERE NOMBRE=?", (proceso,))
        id_proceso = cursor.fetchone()  # Devuelve una tupla o None si no hay resultados
        conn.commit()

    except sqlite3.Error as e:
        print(f"Error al obtener los ID_PROCESO: {e}")
        id_proceso = None

    finally:
        conn.close()

    return id_proceso[0]

def obtener_id_procesos(bbdd):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()
        
        # Obtener todos los ID_PROCESO únicos
        cursor.execute("SELECT DISTINCT ID_PROCESO FROM TIEMPOS_MODELOS")
        id_procesos = [row[0] for row in cursor.fetchall()]  # Lista de procesos
        conn.commit()
        id_procesos.sort()

    except sqlite3.Error as e:
        print(f"Error al obtener los ID_PROCESO: {e}")
        id_procesos = []
    
    finally:
        conn.close()

    return id_procesos

def obtener_id_procesos_secuencia(bbdd):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()
        
        # Obtener todos los ID_PROCESO únicos
        cursor.execute("SELECT ID_PROCESO FROM PROCESOS ORDER BY SECUENCIA")
        id_procesos = [row[0] for row in cursor.fetchall()]  # Lista de procesos
        conn.commit()

    except sqlite3.Error as e:
        print(f"Error al obtener los ID_PROCESO: {e}")
        id_procesos = []
    
    finally:
        conn.close()

    return id_procesos

def generar_consulta_tiempos_modelos(bbdd):
    # Obtener la lista de procesos
    id_procesos = obtener_id_procesos(bbdd)

    if not id_procesos:
        return None

    # Construir dinámicamente la parte del CASE
    case_statements = []
    for proceso in id_procesos:
        case_statements.append(f"MAX(CASE WHEN TIEMPOS_MODELOS.ID_PROCESO = '{proceso}' THEN TIEMPOS_MODELOS.TIEMPO END) AS '{proceso}'")

    # Unir las partes para generar la consulta completa
    consulta_sql = f"""
    SELECT MODELOS.MODELO, {', '.join(case_statements)}
    FROM MODELOS
    LEFT JOIN TIEMPOS_MODELOS ON MODELOS.ID_MODELO = TIEMPOS_MODELOS.ID_MODELO
    GROUP BY MODELOS.MODELO;
    """
    return consulta_sql

def leer_tiempos_modelos_df(bbdd):
    try:
        # Generar consulta SQL
        consulta = generar_consulta_tiempos_modelos(bbdd)

        if consulta is None:
            return None

        # Conectar a la base de datos y ejecutar la consulta
        conn = sqlite3.connect(bbdd)
        df = pd.read_sql_query(consulta, conn)  # Leer los resultados como un DataFrame de pandas
        conn.close()

        return df  # Retornar el DataFrame

    except sqlite3.Error as e:
        print(f"Error en la consulta: {e}")
        return None

def generar_consulta_tiempos_vehiculos(bbdd):
    # Obtener la lista de procesos
    id_procesos = obtener_id_procesos(bbdd)

    if not id_procesos:
        return None

    # Construir dinámicamente la parte del CASE
    case_statements = []
    for proceso in id_procesos:
        case_statements.append(f"MAX(CASE WHEN TIEMPOS_VEHICULOS.ID_PROCESO = '{proceso}' THEN TIEMPOS_VEHICULOS.TIEMPO END) AS '{proceso}'")

    # Unir las partes para generar la consulta completa
    consulta_sql = f"""
    SELECT VEHICULOS.CHASIS, {', '.join(case_statements)}
    FROM VEHICULOS
    LEFT JOIN TIEMPOS_VEHICULOS ON VEHICULOS.CHASIS = TIEMPOS_VEHICULOS.CHASIS
    GROUP BY VEHICULOS.CHASIS;
    """
    return consulta_sql

def leer_tiempos_vehiculos_df(bbdd):
    try:
        # Generar consulta SQL
        consulta = generar_consulta_tiempos_vehiculos(bbdd)

        if consulta is None:
            return None

        # Conectar a la base de datos y ejecutar la consulta
        conn = sqlite3.connect(bbdd)
        df = pd.read_sql_query(consulta, conn)  # Leer los resultados como un DataFrame de pandas
        conn.close()

        return df  # Retornar el DataFrame

    except sqlite3.Error as e:
        print(f"Error en la consulta: {e}")
        return None

def leer_pedido(bbdd, id):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM PEDIDOS WHERE ID_PEDIDO=?", (id,))
        datos = cursor.fetchone()

        print(datos)

    except sqlite3.Error as e:
        print(f"Error al leer el registro: {e}")
        datos = None

    finally:
        conn.close()
        return datos  # Retorna los datos si se encuentran

def leer_pedidos(bbdd):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()          
        cursor.execute("SELECT * FROM PEDIDOS")
        datos = cursor.fetchall()
        conn.commit()
        
    except sqlite3.Error as e:
        print(f"Error al leer los registro de Pedidos: {e}")

    finally:
        conn.close()
        print(datos)
        return datos

def leer_pedidos_df(bbdd):
    try:
        conn = sqlite3.connect(bbdd)
        query = "SELECT * FROM PEDIDOS"
        dataframe = pd.read_sql_query(query, conn)
        print(dataframe)

    except sqlite3.Error as e:
        print(f"Error al leer la tabla de pedidos: {e}")
        dataframe = None
    finally:
        conn.close()
        return dataframe

def leer_referencias_modelos_df(bbdd):
    try:
        conn = sqlite3.connect(bbdd)
        df_datos = pd.read_sql_query("SELECT * FROM MODELOS_REFERENCIAS", conn)
        print(df_datos)

    except sqlite3.Error as e:
        print(f"Error al leer el registro: {e}")

    finally:
        conn.close()
    return df_datos

def leer_programa(bbdd, id):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM PROGRAMAS WHERE ID_PROGRAMA=?", (id,))
        datos = cursor.fetchone()

        print(datos)

    except sqlite3.Error as e:
        print(f"Error al leer el programa {id}: {e}")
        datos = None

    finally:
        conn.close()
        return datos  # Retorna los datos si se encuentran

def leer_programas(bbdd):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()          
        cursor.execute("SELECT * FROM PROGRAMAS")
        datos = cursor.fetchall()
        conn.commit()
        
    except sqlite3.Error as e:
        print(f"Error al leer los registro de Programas: {e}")
        datos = None
    finally:
        conn.close()
        print(datos)
        return datos

def leer_orden(bbdd, codigo):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM PEDIDOS WHERE CODIGO_ORDEN = ?", (codigo,))
        datos = cursor.fetchone()

        print(datos)

    except sqlite3.Error as e:
        print(f"Error al leer la programa {codigo}: {e}")
        datos = None

    finally:
        conn.close()
        return datos  # Retorna los datos si se encuentran
    
def leer_ordenes_completo(bbdd):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()

        cursor.execute('''
                        SELECT
                            ORDENES.CODIGO_ORDEN,
                            ORDENES.CHASIS,
                            ORDENES.INICIO,
                            ORDENES.FIN,
                            ORDENES.DURACION,
                            ORDENES.TIEMPO_PRODUCTIVO,
                            PROCESOS.NOMBRE,
                            ORDENES.OBSERVACIONES,
                            VEHICULOS.ID_MODELO,
                            VEHICULOS.COLOR,
                            TECNICOS.NOMBRE || TECNICOS.APELLIDO AS TECNICO
                        FROM
                            ORDENES
                        LEFT JOIN 
                            VEHICULOS ON VEHICULOS.CHASIS = ORDENES.CHASIS
                        LEFT JOIN
                            TECNICOS ON TECNICOS.ID_TECNICO = ORDENES.ID_TECNICO
                        LEFT JOIN
                            PROGRAMAS ON PROGRAMAS.ID_PROGRAMA = ORDENES.ID_PROGRAMA
                        LEFT JOIN
                            PROCESOS ON PROCESOS.ID_PROCESO = ORDENES.ID_PROCESO
                        ''')
        registros = cursor.fetchall()
        print(registros)

    except sqlite3.Error as e:
        print(f"Error al leer alguna de las Tabla: de Órdenes, de Programas, de Vehículos o de Técnicos: {e}")
        registros = None

    finally:
        conn.close()    # Cierra la conexión
    
    return registros

def leer_ordenes_por_programa(bbdd, programa):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()

        cursor.execute('''
                        SELECT
                            ORDENES.CODIGO_ORDEN,
                            ORDENES.CHASIS,
                            ORDENES.INICIO,
                            ORDENES.FIN,
                            ORDENES.DURACION,
                            ORDENES.TIEMPO_PRODUCTIVO,
                            PROCESOS.NOMBRE,
                            ORDENES.OBSERVACIONES,
                            VEHICULOS.ID_MODELO,
                            VEHICULOS.COLOR,
                            TECNICOS.NOMBRE || TECNICOS.APELLIDO AS TECNICO
                        FROM
                            ORDENES
                        LEFT JOIN 
                            VEHICULOS ON VEHICULOS.CHASIS = ORDENES.CHASIS
                        LEFT JOIN
                            TECNICOS ON TECNICOS.ID_TECNICO = ORDENES.ID_TECNICO
                        LEFT JOIN
                            PROGRAMAS ON PROGRAMAS.ID_PROGRAMA = ORDENES.ID_PROGRAMA
                        LEFT JOIN
                            PROCESOS ON PROCESOS.ID_PROCESO = ORDENES.ID_PROCESO
                        WHERE
                            PROGRAMAS.ID_PROGRAMA = ?
                        ''', (programa,))
        registros = cursor.fetchall()
        print(registros)

    except sqlite3.Error as e:
        print(f"Error al leer alguna de las Tabla: de Órdenes, de Programas, de Vehículos o de Técnicos: {e}")
        registros = None

    finally:
        conn.close()    # Cierra la conexión
    
    return registros

#####################################################################
########################## MODIFICAR REGISTROS ######################
def actualizar_historico_estado(bbdd, id, estado):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()          
        insert_data_script = """
                                UPDATE HISTORICOS
                                    SET ESTADO = ?
                                    WHERE CODIGO_ASIGNACION = ?
                            """
        cursor.execute(insert_data_script, (estado, id))
        conn.commit()
        print(f"El Registro histórico con {id} cambió su estado por {estado}")
        
    except sqlite3.Error as e:
        print(f"Error al insertar el modelo: {e}")

    except UnboundLocalError as e:
        print(f"No se llenaron todos los campos: {e}") 

    finally:
        conn.close()

def actualizar_modelo(bbdd, id_anterior, marca, modelo, id_nuevo):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()          
        insert_data_script = """
                                UPDATE MODELOS 
                                    SET ID_MODELO=?, MARCA=?, MODELO=?
                                    WHERE ID_MODELO=?
                            """
        cursor.execute(insert_data_script, (id_nuevo, marca, modelo, id_anterior))
        conn.commit()
        print(f"Registro {id_anterior} actualizado por {id_nuevo}")
        
    except sqlite3.Error as e:
        print(f"Error al insertar el modelo: {e}")

    except UnboundLocalError as e:
        print(f"No se llenaron todos los campos: {e}") 

    finally:
        conn.close()

def actualizar_orden(bbdd, id_programa_anterior, id_programa_nuevo):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()

        # Asegurar que los valores clave no sean None
        if all(item is not None for item in (id_programa_anterior, id_programa_nuevo)):
            
            update_data_script = """UPDATE ORDENES
                                    SET ID_PROGRAMA = ?
                                    WHERE ID_PROGRAMA = ?
                                """
            
            cursor.execute(update_data_script, (id_programa_nuevo, id_programa_anterior))
            conn.commit()
            print("Registros de órdenes actualizados")

    except sqlite3.Error as e:
        print(f"Error al actualizar la orden: {e}")

    finally:
        conn.close()

def actualizar_tiempo_modelo(bbdd, procmodel, id_proceso, id_modelo, tiempo, procmodelo_anterior):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()          
        insert_data_script = """
                                UPDATE TIEMPOS_MODELOS
                                    SET  PROCESO_MODELO=?, ID_PROCESO=?, ID_MODELO=?, TIEMPO=?
                                    WHERE PROCESO_MODELO=?
                            """
        cursor.execute(insert_data_script, (procmodel, id_proceso, id_modelo, tiempo, procmodelo_anterior))
        conn.commit()
        print(f"Registro {procmodelo_anterior} actualizado por {procmodel}")
        
    except sqlite3.Error as e:
        print(f"Error al actualizar el tiempo {procmodelo_anterior}:{e}")

    except UnboundLocalError as e:
        print(f"No se llenaron todos los campos: {e}") 

    finally:
        conn.close()

def actualizar_tiempo_vehiculo(bbdd, procvehi, id_proceso, chasis, tiempo, procvehi_anterior):
    try:
        # Conectar a la base de datos
        with sqlite3.connect(bbdd) as conn:
            cursor = conn.cursor()

            # Consulta de actualización
            update_data_script = """UPDATE TIEMPOS_VEHICULOS
                                    SET PROCESO_CHASIS = ?,
                                        ID_PROCESO = ?, 
                                        CHASIS = ?,
                                        TIEMPO = ?
                                    WHERE PROCESO_CHASIS = ?
                                """

            # Ejecutar la consulta
            cursor.execute(update_data_script, (procvehi, id_proceso, chasis, tiempo, procvehi_anterior))
            conn.commit()

            print(f"Registro de Tiempo_vehiculo de {procvehi_anterior} actualizado")



    except sqlite3.Error as e:
        print(f"Error al actualizar el tiempo: {e}")
    
    finally:
        conn.close()

def actualizar_vehiculo(bbdd, chasis, fecha_ingreso, id_modelo, color, estado, novedades, subcontratar, id_pedido, chasis_anterior):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()

        # Asegurar que los valores clave no sean None
        if all(item is not None for item in (chasis, id_modelo, color, estado, id_pedido)):
            
            update_data_script = """UPDATE VEHICULOS 
                                    SET CHASIS = ?,
                                        FECHA_INGRESO = ?, 
                                        ID_MODELO = ?, 
                                        COLOR = ?, 
                                        ESTADO = ?, 
                                        NOVEDADES = ?, 
                                        SUBCONTRATAR = ?, 
                                        ID_PEDIDO = ?
                                    WHERE CHASIS = ?
                                """
            
            cursor.execute(update_data_script, (chasis, fecha_ingreso, id_modelo, color, estado, novedades, subcontratar, id_pedido, chasis_anterior))
            conn.commit()
            print("Registro actualizado")

    except sqlite3.Error as e:
        print(f"Error al actualizar el vehículo: {e}")

    finally:
        conn.close()


####################################################################
########################## ELIMINAR REGISTROS ######################

def eliminar_historico(bbdd, id_historico):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM HISTORICOS WHERE CODIGO_ASIGNACION=?", (id_historico,))
        conn.commit()
        print(f"El registro de histórico con{id_historico} se eliminó correctamente de la tabla HISTÓRICOS")

    except sqlite3.Error as e:
        print(f"Error al eliminar el histórico  con id {id_historico}: {e}")

    finally:
        conn.close()  # Cerrar la conexión después de usarla

def eliminar_modelo(bbdd, modelo):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM MODELOS WHERE MODELO=?", (modelo,))
        conn.commit()
        print(f"El modelo {modelo} se eliminó correctamente de la tabla MODELOS")

    except sqlite3.Error as e:
        print(f"Error al eliminar el modelo {modelo}: {e}")

    finally:
        conn.close()

def eliminar_tiempo_modelo(bbdd, modelo):
    id_modelo = obtener_id_modelo(bbdd, modelo)

    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM TIEMPOS_MODELOS WHERE PROCESO_MODELO=?", (modelo,))
        conn.commit()
        print(f"Los registro del modelo {modelo} se eliminaron correctamente de la tabla TIEMPOS_MODELOS")

    except sqlite3.Error as e:
        print(f"Error al eliminar el modelo {modelo}: {e}")

    finally:
        conn.close()  # Cerrar la conexión después de usarla

def eliminar_modelo_completo(bbdd, modelo):
    eliminar_tiempo_modelo(bbdd, modelo)   #eliminar primero el registro con clave foranea
    eliminar_modelo(bbdd, modelo)          #eliminar después el registro con clave primaria


def eliminar_vehiculo(bbdd, chasis):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM VEHICULOS WHERE CHASIS=?", (chasis,))
        conn.commit()
        print(f"El modelo {chasis} se eliminó correctamente de la tabla VEHICULOS")

    except sqlite3.Error as e:
        print(f"Error al eliminar el Vehiculo con chasis {chasis}: {e}")

    finally:
        conn.close()  # Cerrar la conexión después de usarla

def eliminar_tiempo_vehiculo(bbdd, chasis):

    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM TIEMPOS_VEHICULOS WHERE CHASIS=?", (chasis,))
        conn.commit()
        print(f"Los registro del vehiculo {chasis} se eliminó correctamente de la tabla TIEMPOS_VEHICULOS")

    except sqlite3.Error as e:
        print(f"Error al eliminar el vehiculo con chasis {chasis}: {e}")

    finally:
        conn.close()  # Cerrar la conexión después de usarla

def eliminar_vehiculo_completo(bbdd, chasis):
    eliminar_tiempo_vehiculo(bbdd, chasis)   #eliminar primero el registro con clave foranea
    eliminar_vehiculo(bbdd, chasis)          #eliminar después el registro con clave primaria


def eliminar_proceso(bbdd, id):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM PROCESOS WHERE ID_PROCESO=?", (id,))
        conn.commit()
        print(f"El proceso {id} se eliminó correctamente de la tabla PROCESOS")

    except sqlite3.Error as e:
        print(f"Error al eliminar el proceso {id}: {e}")

    finally:
        conn.close()

def eliminar_tecnico(bbdd, id):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM TECNICOS WHERE ID_TECNICO=?", (id,))
        conn.commit()
        print(f"El tecnico {id} se eliminó correctamente de la tabla TECNICOS")

    except sqlite3.Error as e:
        print(f"Error al eliminar el tecnico {id}: {e}")

    finally:
        conn.close()

def eliminar_pedido(bbdd, id):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM PEDIDOS WHERE ID_PEDIDO=?", (id,))
        conn.commit()


    except sqlite3.Error as e:
        print(f"Error al eliminar el pedido {id}: {e}")

    finally:
        conn.close()
        lectura_prueba = leer_pedido(bbdd, id)
        if  lectura_prueba == None:
            print(f"El pedido {id} se eliminó correctamente de la tabla PEDIDOS")

        elif lectura_prueba != None:
            print(f"No se eliminó el pedido {id}")

def eliminar_todos_registros(bbdd):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM TECNICOS_PROCESOS_PRUEBA")
        conn.commit()

    except sqlite3.Error as e:
        print(f"Error al eliminar ")

    finally:
        conn.close()

###### FUNCIONES DE APOYO PARA LAS BBDD ######
def next_consecutivoPedido(bbdd):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()

        # Obtener el valor máximo del contador numérico
        cursor.execute("SELECT MAX(CONSECUTIVO) FROM PEDIDOS")
        max_consec = cursor.fetchone()[0]
        if max_consec is None:
            max_consec = 0
        nuevo_consec = max_consec + 1          # avanzar el consecutivo

    except sqlite3.Error as e:
        print(f"No se pudo leer el maximo consecutivo de la tabla de pedidos: {e}")
        nuevo_consec = None

    finally:
        conn.close()
        return nuevo_consec

def next_consecutivoPrograma(bbdd):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()

        # Obtener el valor máximo del contador numérico
        cursor.execute("SELECT MAX(CONSECUTIVO) FROM PROGRAMAS")
        max_consec = cursor.fetchone()[0]
        if max_consec is None:
            max_consec = 0
        nuevo_consec = max_consec + 1          # avanzar el consecutivo

    except sqlite3.Error as e:
        print(f"No se pudo leer el maximo consecutivo de la tabla de programas: {e}")
        nuevo_consec = None

    finally:
        conn.close()
        return nuevo_consec




"""
df_especialidades = leer_tecnicos_procesos_df('planta_tulcan.db')
df_ids_procesos = leer_procesos_df('planta_tulcan.db')
df_combinado = pd.merge(left=df_especialidades,
                        right=df_ids_procesos,
                        how="left",
                        left_on="ID_PROCESO",
                        right_on="NOMBRE")
df_reducido = df_combinado[["ID_TECNICO", "ID_PROCESO_y"]]
df_reducido.rename(columns={'ID_PROCESO_y': 'ID_PROCESO'}, inplace=True)
print(df_reducido)
df_reducido['TEC_PROC'] = df_reducido['ID_TECNICO'].astype(str) + df_reducido['ID_PROCESO'].astype(str)
df_reducido = df_reducido[['TEC_PROC', 'ID_TECNICO', 'ID_PROCESO']]
print(df_reducido)
"""


"""
# Crear el DataFrame
data = {
    "TEC_PROC": [
        "JuanYane400009LAV", "JoséPére898391PDI", "MiguSánc284815PIN", "DiegPedr756093LAV",
        "JesuFern703446PDI", "RaúlSuar805850PDI", "JorgMora673796LAV", "LuisGarc739041LAV",
        "DaniPeña224970PIN", "JeanPere096862LAV", "GabrLópe764514PDI", "AndrCast889408PIN",
        "RicaHern380721LAV", "JohaAgui862120PDI", "LeniMont601067PIN", "LuisGarz511185TEL",
        "AlexUrib809574TEL", "DannPlin609447TEL"
    ],
    "ID_TECNICO": [
        "JuanYane400009", "JoséPére898391", "MiguSánc284815", "DiegPedr756093",
        "JesuFern703446", "RaúlSuar805850", "JorgMora673796", "LuisGarc739041",
        "DaniPeña224970", "JeanPere096862", "GabrLópe764514", "AndrCast889408",
        "RicaHern380721", "JohaAgui862120", "LeniMont601067", "LuisGarz511185",
        "AlexUrib809574", "DannPlin609447"
    ],
    "ID_PROCESO": [
        "LAV", "PDI", "PIN", "LAV", "PDI", "PDI", "LAV", "LAV", "PIN", "LAV", "PDI",
        "PIN", "LAV", "PDI", "PIN", "TEL", "TEL", "TEL"
    ]
}

df = pd.DataFrame(data)
print(df)

insertar_tecnicos_procesos_df('planta_tulcan.db', df)
"""




"""
def leer_vehiculos_completos(bbdd):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()

        cursor.execute('''
                        SELECT 
                            VEHICULOS.CHASIS,
                            VEHICULOS.FECHA_INGRESO,
                            VEHICULOS.ID_MODELO,
                            VEHICULOS.COLOR,
                            
                            -- Subconsulta para obtener el nombre del proceso o 'ninguno' si es NULL
                            COALESCE(
                                (SELECT PROCESOS.NOMBRE
                                FROM HISTORICOS
                                JOIN PROCESOS ON HISTORICOS.ID_PROCESO = PROCESOS.ID_PROCESO
                                WHERE HISTORICOS.CHASIS = VEHICULOS.CHASIS
                                AND HISTORICOS.ESTADO = 'EN EJECUCION'
                                LIMIT 1),
                                (SELECT PROCESOS.NOMBRE
                                FROM HISTORICOS
                                JOIN PROCESOS ON HISTORICOS.ID_PROCESO = PROCESOS.ID_PROCESO
                                WHERE HISTORICOS.CHASIS = VEHICULOS.CHASIS
                                AND HISTORICOS.ESTADO = 'TERMINADO'
                                AND HISTORICOS.FIN = (
                                    SELECT MAX(FIN)
                                    FROM HISTORICOS AS HIST2
                                    WHERE HIST2.CHASIS = VEHICULOS.CHASIS AND HIST2.ESTADO = 'TERMINADO'
                                )
                                LIMIT 1),
                                'ninguno'
                            ) AS NOMBRE_PROCESO,
                            
                            -- Subconsulta para obtener el estado o 'ninguno' si es NULL
                            COALESCE(
                                (SELECT HISTORICOS.ESTADO
                                FROM HISTORICOS
                                WHERE HISTORICOS.CHASIS = VEHICULOS.CHASIS
                                AND HISTORICOS.ESTADO = 'EN EJECUCION'
                                LIMIT 1),
                                (SELECT HISTORICOS.ESTADO
                                FROM HISTORICOS
                                WHERE HISTORICOS.CHASIS = VEHICULOS.CHASIS
                                AND HISTORICOS.ESTADO = 'TERMINADO'
                                AND HISTORICOS.FIN = (
                                    SELECT MAX(FIN)
                                    FROM HISTORICOS AS HIST2
                                    WHERE HIST2.CHASIS = VEHICULOS.CHASIS AND HIST2.ESTADO = 'TERMINADO'
                                )
                                LIMIT 1),
                                'ninguno'
                            ) AS ESTADO,

                            VEHICULOS.NOVEDADES,
                            VEHICULOS.SUBCONTRATAR,
                            VEHICULOS.ID_PEDIDO,
                            
                            COALESCE(GROUP_CONCAT(TIEMPOS_VEHICULOS.ID_PROCESO || ': ' || TIEMPOS_VEHICULOS.TIEMPO, ' | '), 'Sin procesos') AS PROCESOS_TIEMPOS
                        FROM
                            VEHICULOS
                        LEFT JOIN 
                            TIEMPOS_VEHICULOS ON VEHICULOS.CHASIS = TIEMPOS_VEHICULOS.CHASIS
                        GROUP BY
                            VEHICULOS.CHASIS;
                        ''')
        registros = cursor.fetchall()
        print(registros)

    except sqlite3.Error as e:
        print(f"Error al leer la Tabla de Tiempos_Vehiculos y de Vehiculos: {e}")
        registros = None

    finally:
        conn.close()    # Cierra la conexión
    
    return registros
"""





"""
marcas = {
    "NISSAN":   ["ALTIMA","FRONTIER","KICKS","QASHQAI","LEAFT","VERSA","PATHFINDER","XTRAIL",],
    "RENAULT":  ["CAPTUR","KOLEOS","KWID",],
    "BAIC":     ["BJ20","BJ40","D50","NX55","X35","X55","U5P",],
    "FOTON":    ["AUMARK","AUMAN","TUNLAND","VIEW","TOANO",],
    "GEELY":    ["AZKARRA","COOLRAY",],
    "MG":       ["RX8","RX5","MG5","ZS","ONE"]
}


for marca, modelos in marcas.items():
    for modelo in modelos:
        id_marcamodelo = marca + "-" + modelo
        #print( id_marcamodelo, marca, modelo)
        insertar_modelo('planta_manta.db', id_marcamodelo, marca, modelo)
"""

""""
procesos=[
    ("TEL", "TELEQUINOX", "Instalacion de accesorios Packs y Recubrimientos"),
    ("PDI", "PDI MECANICO", "Revision exterior, interior, habitaculo, cambio aros, scanner"),
    ("LAV", "LAVADO", "Operaciones de lavado y secado"),
    ("PIN", "PINTURA", "Micropulidos, Pulidos, Latoneria y Pintura"),
    ("CAL", "CALIDAD", "Inspeccion de rutina")
]

for proceso in procesos:
    #print(proceso[0], proceso[1], proceso[2])
    insertar_proceso('planta_manta.db', proceso[0], proceso[1], proceso[2])
"""







"""
#Tiempo de los 5 procesos para cada modelo
dictiempos = {
    "ALTIMA":       [0,   60,  60,  30,   15],
    "FRONTIER":     [420, 128, 55,  23,   15],
    "KICKS":        [150, 123, 55,  23,   15],
    "QASHQAI":      [330, 63,  55,  23,   15],
    "LEAFT":        [0,   63,  50,  23,   15],
    "VERSA":        [390, 123, 55,  23,   15],
    "PATHFINDER":   [60,  63,  60,  23,   15],
    "XTRAIL":       [60,  63,  55,  23,   15],
    "CAPTUR":       [60,  60,  60,  30,   15],
    "KOLEOS":       [60,  63,  60,  48,   15],
    "KWID":         [60,  68,  50,  48,   15],
    "BJ20":         [0,   72,  55,  52,   15],
    "BJ40":         [0,   72,  55,  52,   15],
    "D50":          [270, 72,  55,  52,   15],
    "NX55":         [240, 72,  55,  52,   15],
    "X35":          [270, 72,  55,  52,   15],
    "X55":          [0,   72,  55,  52,   15],
    "U5P":          [270, 72,  55,  52,   15],
    "AUMARK":       [0,   365, 120, 300,  15],
    "AUMAN":        [0,   960, 120, 1920, 15],
    "TUNLAND":      [270, 240, 120, 185,  15],
    "VIEW":         [240, 295, 90,  685,  15],
    "TOANO":        [240, 240, 90,  685,  15],
    "AZKARRA":      [0,   72,  55,  22,   15],
    "COOLRAY":      [0,   72,  55,  22,   15],
    "RX8":          [0,   92,  50,  15,   15],
    "RX5":          [0,   210, 50,  15,   15],
    "MG5":          [0,   105, 50,  15,   15],
    "ZS":           [0,   110, 50,  15,   15],
    "ONE":          [0,   200, 50,  15,   15]
}

marcas = {
    "NISSAN":   ["ALTIMA","FRONTIER","KICKS","QASHQAI","LEAFT","VERSA","PATHFINDER","XTRAIL",],
    "RENAULT":  ["CAPTUR","KOLEOS","KWID",],
    "BAIC":     ["BJ20","BJ40","D50","NX55","X35","X55","U5P",],
    "FOTON":    ["AUMARK","AUMAN","TUNLAND","VIEW","TOANO",],
    "GEELY":    ["AZKARRA","COOLRAY",],
    "MG":       ["RX8","RX5","MG5","ZS","ONE"]
}

        
procesos = leer_procesos('planta_manta.db')
modelos = leer_modelos('planta_manta.db')
datosTiemposModelos =[]

print(procesos)
print(modelos)
diccionario={}

for datos in modelos:
    diccionario[datos[2]]= datos[0]

for datos in modelos:
    diccionario[datos[2]]= datos[0]

print(diccionario)

for modelo, tiempos in dictiempos.items():
    for proceso, tiempo in zip(procesos, tiempos):
        proceso_modelo = proceso[0] + "-" + modelo
        datosTiemposModelos.append([proceso_modelo, proceso[0], diccionario[modelo], tiempo])
        insertar_tiempo_modelo('planta_manta.db', proceso_modelo, proceso[0], diccionario[modelo], tiempo)

for dato in datosTiemposModelos:
    print(dato)
"""







"""
lista_de_tecnicos = [
    ("Tel02Osm", "Osman", "Gomez", "TELEQUINOX"),
    ("Tel03Bra", "Jesus","Cetina", "TELEQUINOX"),
    ("Tel04Jer", "Jeremias", "Rodriguez","TELEQUINOX"),
    ("Tel05Lui", "Luis", "Buelvas","TELEQUINOX"),
    ("Tel06Alb", "Alberto", "Barriga","TELEQUINOX"),
    ("Tel07Jos", "Jose", "Peña","TELEQUINOX"),
    ("Tel08JuJ", "JuanJose", "Pita","TELEQUINOX"),
    ("Tel09JuD", "JuanDavid", "Blanco","TELEQUINOX"),
    ("Tel10Wil", "William", "Lopez","TELEQUINOX"),
    ("Tel11Ces", "Cesar", "Gomez","TELEQUINOX"),
    ("Tel12Car", "Carlos", "Rivadeneira","TELEQUINOX"),
    ("Tel13Cha", "Charly", "","TELEQUINOX"),

    ("Pdi01Ang", "Angel", "Lopez","PDI"),
    ("Pdi02Tit", "Tito", "Suarez","PDI"),
    ("Pdi03Dav", "David", "Bonilla","PDI"),
    ("Pdi04Cri", "Cristian", "Quintero","PDI"),
    ("Pdi05Jes", "Jesus", "Sierra","PDI"),
    ("Pdi06Bec", "Backer", "Calderon","PDI"),
    ("Pdi07Gus", "Gustavo", "Ospina","PDI"),

    ("Lav01Lui", "Luis", "Casas","LAVADO"),
    ("Lav02Jes", "Jesus", "Botero","LAVADO"),
    ("Lav03Ala", "Alan", "Leiva","LAVADO"),

    ("Pin01Dan", "Daniel", "Garcia","PINTURA"),
    ("Pin02Vic", "Victor", "Vasquez","PINTURA"),
    ("Pin03Kev", "Kevin", "Jaimes","PINTURA"),

    ("Cal01Dav", "David", "Solarte","CALIDAD"),
 ]

for tecnico in lista_de_tecnicos:
    print(tecnico[0], tecnico[1], tecnico[2], tecnico[3])
    #insertar_tecnico('planta_manta.db', tecnico[0], tecnico[1], tecnico[2], tecnico[3])
"""


























