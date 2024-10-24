import sqlite3
import pandas as pd
import os
import ventanas_emergentes as ventEmerg
#from planta import modelos, marcas, tiempos

###########################################################################
############################# CREACIÓN DE TABLAS###########################
###########################################################################



###########################################################################
############################# ELIMINAR TABLAS##############################
###########################################################################
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


###########################################################################
############################# PARA PARA INSERTAR ###########################
###########################################################################

def insertar_proceso(bbdd, id, proceso, descripcion):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()          
        insert_data_script = """INSERT INTO PROCESOS 
                                    (ID_PROCESO, NOMBRE, DESCRIPCION)
                                    VALUES (?, ?, ?)
                                """
        cursor.execute(insert_data_script, (id, proceso, descripcion))
        conn.commit()
        print("Registro añadido")
        
    except sqlite3.Error as e:
        print(f"Error al insertar el proceso: {e}")

    except UnboundLocalError as e:
        print(f"No se llenaron todos los campos: {e}") 

    finally:
        conn.close()

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

def insertar_tecnico(bbdd, id, nombre, apellido, especialidad):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()          
        insert_data_script = """INSERT INTO TECNICOS 
                                    (ID_TECNICO, NOMBRE, APELLIDO, ESPECIALIDAD)
                                    VALUES (?, ?, ?, ?)
                                """
        cursor.execute(insert_data_script, (id, nombre, apellido, especialidad))
        conn.commit()
        print("Registro añadido")
        
    except sqlite3.Error as e:
        print(f"Error al insertar el registro: {e}")

    except UnboundLocalError as e:
        print(f"No se llenaron todos los campos: {e}") 

    finally:
        conn.close()

def insertar_vehiculo(bbdd, chasis, fecha_ingreso, id_modelo, color, estado, novedades, subcontratar, id_pedido):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()

        if all(item is not None for item in (chasis, id_modelo, color, estado, id_pedido,)):
            
            insert_data_script = """INSERT INTO vehiculos 
                                    (CHASIS, FECHA_INGRESO, ID_MODELO, COLOR, ESTADO, NOVEDADES, SUBCONTRATAR, ID_PEDIDO)
                                    VALUES  (?, ?, ?, ?, ?, ?, ?, ?)
                                """
            
        cursor.execute(insert_data_script, (chasis, fecha_ingreso, id_modelo, color, estado, novedades, subcontratar, id_pedido))
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

def insertar_pedido(bbdd, id_pedido, cliente, fecha_recepcion, entrega_estimada, fecha_entrega):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()          
        insert_data_script = """INSERT INTO TECNICOS 
                                    (ID_PEDIDO, CLIENTE, FECHA_RECEPCION, ENTREGA_ESTIMADA, FECHA_ENTREGA)
                                    VALUES (?, ?, ?, ?)
                                """
        cursor.execute(insert_data_script, (id, id_pedido, cliente, fecha_recepcion, entrega_estimada, fecha_entrega))
        conn.commit()
        print("Registro añadido")
        
    except sqlite3.Error as e:
        print(f"Error al insertar el pedido: {e}")

    except UnboundLocalError as e:
        print(f"No se llenaron todos los campos: {e}") 

    finally:
        conn.close()



###########################################################################
############################ PARA PARA LEER ###############################
###########################################################################

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

def leer_modelos(bbdd):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()          
        cursor.execute("SELECT * FROM MODELOS")
        datos = cursor.fetchall()
        conn.commit()
        
    except sqlite3.Error as e:
        print(f"Error al leer el registro: {e}")

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

def leer_tecnicos_modificado(bbdd):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()          
        cursor.execute("SELECT * FROM TECNICOS")
        datos = cursor.fetchall()
        
        # Modificar los datos según lo solicitado
        datos_modificados = [
            (tecnico[0], f"{tecnico[1]}_{tecnico[2]}", tecnico[4])
            for tecnico in datos
        ]
        
    except sqlite3.Error as e:
        print(f"Error al leer el registro: {e}")
        datos_modificados = []  # Inicializar como lista vacía en caso de error

    finally:
        conn.close()
    
    return datos_modificados

def leer_vehiculo(bbdd, chasis):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()

        vehiculo = chasis
        cursor.execute('SELECT * FROM vehiculos WHERE CHASIS=?', (vehiculo,))
        registro = cursor.fetchone()
        print(registro)

    except sqlite3.Error as e:
        print(f"Error al leer el vehiculo: {e}")

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

def leer_vehiculo_completo(bbdd, chasis):
    registros = None  # Inicializa registros para manejar el caso de que no se encuentren resultados
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()

        vehiculo = chasis
        cursor.execute('''
                        SELECT VEHICULOS.*, TIEMPOS_VEHICULOS.ID_PROCESO, TIEMPOS_VEHICULOS.TIEMPO
                        FROM VEHICULOS LEFT JOIN TIEMPOS_VEHICULOS
                        ON VEHICULOS.CHASIS = TIEMPOS_VEHICULOS.CHASIS
                        WHERE VEHICULOS.CHASIS = ?
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

        cursor.execute('SELECT * FROM VEHICULOS')
        registros = cursor.fetchall()
        print(registros)

    except sqlite3.Error as e:
        print(f"Error al leer la Tabla de Vehiculos: {e}")

    finally:
        conn.close()

    return registros

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
                        SELECT VEHICULOS.*,
                        COALESCE(GROUP_CONCAT(TIEMPOS_VEHICULOS.ID_PROCESO || ': ' || TIEMPOS_VEHICULOS.TIEMPO, '  |  '), 'Sin procesos') AS PROCESOS_TIEMPOS
                        FROM VEHICULOS LEFT JOIN TIEMPOS_VEHICULOS
                        ON VEHICULOS.CHASIS = TIEMPOS_VEHICULOS.CHASIS
                        GROUP BY VEHICULOS.CHASIS;
                        ''')
        registros = cursor.fetchall()
        print(registros)

    except sqlite3.Error as e:
        print(f"Error al leer la Tabla de Tiempos_Vehiculos y de Vehiculos: {e}")
        registros = None

    finally:
        conn.close()    # Cierra la conexión
    
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

def leer_tiempos_modelos_procesos(bbdd):
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

def leer_tiempos_vehiculos_procesos(bbdd):
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


####################################################################
########################## ELIMINAR REGISTROS ######################

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
        conn.close()  # Cerrar la conexión después de usarla

def eliminar_tiempo_modelo(bbdd, modelo):
    id_modelo = obtener_id_modelo(bbdd, modelo)

    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM TIEMPOS_MODELOS WHERE ID_MODELO=?", (id_modelo,))
        conn.commit()
        print(f"Los registro del modelo {modelo} se eliminaron correctamente de la tabla TIEMPOS_MODELOS")

    except sqlite3.Error as e:
        print(f"Error al eliminar el modelo {modelo}: {e}")

    finally:
        conn.close()  # Cerrar la conexión después de usarla

def eliminar_modelo_completo(bbdd, modelo):
    if ventEmerg.msg_eliminar_mod(modelo):
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
    if ventEmerg.msg_eliminar_veh(chasis):
        eliminar_tiempo_vehiculo(bbdd, chasis)   #eliminar primero el registro con clave foranea
        eliminar_vehiculo(bbdd, chasis)          #eliminar después el registro con clave primaria



#####################################################################
########################## MODIFICAR REGISTROS ######################
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


























