import sqlite3
import pandas as pd
#from planta import modelos, marcas, tiempos

###########################################################################
############################# CREACIÓN DE TABLAS###########################
###########################################################################
#Crear la tabla para modelos
def crear_tabla_modelos():

    conn = sqlite3.connect('produccion.db')
    cursor = conn.cursor()

    create_table_script = """
    CREATE TABLE modelos_vehiculos (
        MARCA VARCHAR NOT  NULL,
        MODELO VARCHAR PRIMARY KEY,
        time_telequinox INTEGER NOT NULL,
        time_PDI INTEGER NOT NULL,
        time_LAVADO INTEGER NOT NULL,
        time_PINTURA INTEGER NOT NULL,
        time_CALIDAD INTEGER NOT NULL
    )
    """

    cursor.execute(create_table_script)
    conn.commit()
    conn.close()

    print("Tabla 'modelos_vehiculos' creada exitosamente.")

#Crear la tabla para vehiculos de pedido
def crear_tabla_vehiculos():
    # Conectar a la base de datos (o crearla si no existe)
    conn = sqlite3.connect('produccion.db')
    cursor = conn.cursor()

    create_table_script = """
    CREATE TABLE vehiculos (
        CHASIS VARCHAR PRIMARY KEY,
        FECHA VARCHAR NOT NULL,        
        MARCA VARCHAR NOT NULL,
        MODELO VARCHAR,
        COLOR VARCHAR NOT NULL,
        ESTADO VARCHAR NOT NULL,
        TIME_TEL VARCHAR NOT NULL,
        TIME_PDI VARCHAR NOT NULL,
        TIME_LAV VARCHAR NOT NULL,
        TIME_PIN VARCHAR NOT NULL,
        TIME_CAL VARCHAR NOT NULL,
        NOVEDADES VARCHAR NOT NULL,
        SUBCONTRATAR VARCHAR NOT NULL,
        FOREIGN KEY (MODELO) REFERENCES modelos_vehiculos(MODELO)
    )
    """
    cursor.execute(create_table_script)
    conn.commit()
    conn.close()

    print("Tabla 'Vehiculos' creada exitosamente.")

#Crear la tabla para tecnicos
def crear_tabla_tecnicos():
    # Conectar a la base de datos (o crearla si no existe)
    conn = sqlite3.connect('produccion.db')
    cursor = conn.cursor()

    create_table_script = """
    CREATE TABLE tecnicos (
        ID_TECNICO VARCHAR PRIMARY KEY,
        NOMBRE VARCHAR NOT NULL,        
        ESPECIALIDAD VARCHAR NOT NULL
    )
    """

    cursor.execute(create_table_script)
    conn.commit()
    conn.close()    

    print("Tabla 'tecnicos' creada exitosamente.")

#Crear la tabla para ordenes de pedido
def crear_tabla_ordenes():
    # Conectar a la base de datos (o crearla si no existe)
    conn = sqlite3.connect('produccion.db')
    cursor = conn.cursor()

    create_table_script = """
    CREATE TABLE ordenes (
        CODIGO_ORDEN VARCHAR PRIMARY KEY,
        CHASIS VARCHAR NOT NULL,
        MARCA VARCHAR NOT NULL,
        MODELO VARCHAR NOT NULL,
        COLOR VARCHAR NOT NULL,
        NOVEDADES VARCHAR NOT NULL,
        PEDIDO VARCHAR NOT NULL,
        ID_PEDIDO VARCHAR NOT NULL,
        PROCESO VARCHAR NOT NULL,
        ID_TECNICO VARCHAR NOT NULL,
        NOMBRE_TECNICO VARCHAR NOT NULL,
        ESPECIALIDAD VARCHAR NOT NULL,
        INICIO VARCHAR NOT NULL,
        FIN VARCHAR NOT NULL,
        DURACION VARCHAR NOT NULL,
        PLAZO VARCHAR NOT NULL,
        FOREIGN KEY (CHASIS) REFERENCES modelos_vehiculos(CHASIS)
        FOREIGN KEY (MODELO) REFERENCES modelos(MODELOS)
        FOREIGN KEY (ID_TECNICO) REFERENCES tecnicos(ID_TECNICO)
        )
    """

    cursor.execute(create_table_script)
    conn.commit()
    conn.close()

    print("Tabla 'Ordenes' creada exitosamente.")



###########################################################################
############################# ELIMINAR TABLAS##############################
###########################################################################
def eliminar_tabla(nombre_tabla):
    try:
        # Conectarse a la base de datos
        conn = sqlite3.connect('produccion.db')
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
############################# CRUD PARA MODELOS ###########################
###########################################################################

def leer_procesos():
    # Conectar a la base de datos
    conn = sqlite3.connect('produccion.db')
    cursor = conn.cursor()

    cursor.execute('PRAGMA table_info(modelos_vehiculos)')
    campos = cursor.fetchall()
    # Filtrar las columnas que contienen la cadena "time" en su nombre
    campos_times = [campo[1] for campo in campos if 'time' in campo[1].lower()]
    lista_procesos = list(map(lambda nombre: nombre.replace('time_', ''), campos_times))
    conn.close()
    return lista_procesos


#Inserta un nuevo registro en la tabla de modelos
def insertar_modelo(marca, modelo, ttel, tpdi, tlav, tpin, tcal):
    try:
        conn = sqlite3.connect('produccion.db')
        cursor = conn.cursor()

        if all(item is not None for item in (marca, modelo, ttel, tpdi, tlav, tpin, tcal)):
           
            insert_data_script = """INSERT INTO modelos_vehiculos 
                                    (MARCA, MODELO, time_telequinox, time_PDI, time_LAVADO, time_PINTURA, time_CALIDAD)
                                    VALUES (?, ?, ?, ?, ?, ?, ?)
                                """
            
        cursor.execute(insert_data_script, (marca, modelo, ttel, tpdi, tlav, tpin, tcal))
        conn.commit()
        print("Registro añadido")
        
    except sqlite3.Error as e:
        print(f"Error al insertar el registro: {e}")

    except UnboundLocalError as e:
        print(f"No se llenaron todos los campos: {e}") 

    finally:
        conn.close()


#Borra un registro en la tabla de modelos basandose en el nombre de modelo
def eliminar_modelo(modelo):
    try:
        conn = sqlite3.connect('produccion.db')
        cursor = conn.cursor()
        
        # Sentencia SQL para eliminar el registro
        delete_data_script = """DELETE FROM modelos_vehiculos
                                WHERE MODELO = ?
                             """
        
        cursor.execute(delete_data_script, (modelo,))
        conn.commit()
        
        # Verificar cuántas filas fueron afectadas
        if cursor.rowcount > 0:
            print("Registro eliminado")
        else:
            print("No se encontró el registro para eliminar")
    
    except sqlite3.Error as e:
        print(f"Error al eliminar el registro: {e}")
    
    finally:
        conn.close()


#Cuenta la cantidad de registros en la tabla de modelos
def calcula_modelos():

    conn = sqlite3.connect('produccion.db')
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM modelos_vehiculos;')
    numero_registros = cursor.fetchone()[0]

    conn.close()
    return numero_registros


#Lee las marcas y los modelos y los empaqueta en una lista de tuplas
def leer_modelos():

    conn = sqlite3.connect('produccion.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM modelos_vehiculos;')
    todosRegistros = cursor.fetchall()
    los_modelos = [(registro[0], registro[1]) for registro in todosRegistros]
    print(los_modelos)

    conn.close()
    return los_modelos


#Lee un registro de la tabla modelos basandose en el nombre de modelos
def leer_modelo(modeloVehiculo):

    conn = sqlite3.connect('produccion.db')
    cursor = conn.cursor()
    el_modelo = modeloVehiculo
    cursor.execute('SELECT * FROM modelos_vehiculos WHERE modelo=?',(el_modelo,))
    registro = cursor.fetchone()
    print(registro)

    conn.close()
    return registro


#Buscar el tiempo de un proceso de un modelo en la tabla modelos
def leer_tiempo(modeloVehiculo,indiceColumna):
    # 3 = telequinox, 4 = PDI, 5 = LAVADO, 6 = PINTURA, 7 = CALIDAD

    conn = sqlite3.connect('produccion.db')
    cursor = conn.cursor()
    el_modelo = modeloVehiculo
    cursor.execute('SELECT * FROM modelos_vehiculos WHERE modelo=?',(el_modelo,))
    registro = cursor.fetchone()
    print(registro)
    tiemposIndiv = registro[indiceColumna]
    print(tiemposIndiv)

    conn.close()
    return tiemposIndiv


def leer_tiempos():
    # 3 = telequinox, 4 = PDI, 5 = LAVADO, 6 = PINTURA, 7 = CALIDAD

    conn = sqlite3.connect('produccion.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM modelos_vehiculos')
    registros = list(cursor.fetchall())
    print(registros)

    conn.close()
    return registros


###########################################################################
############################# CRUD PARA PEDIDOS############################
###########################################################################

#Inserta un nuevo registro en la tabla de pedidos
def insertar_vehiculo(chasis, fecha, marca, modelo, color, estado, ttel, tpdi, tlav, tpin, tcal, novedades, subcontratar):
    try:
        conn = sqlite3.connect('produccion.db')
        cursor = conn.cursor()

        if all(item is not None for item in (chasis, fecha, marca, modelo, color, estado, ttel, tpdi, tlav, tpin, tcal, novedades, subcontratar,)):
            
            insert_data_script = """INSERT INTO vehiculos 
                                    (CHASIS, FECHA, MARCA, MODELO, COLOR, ESTADO, TIME_TEL, TIME_PDI, TIME_LAV, TIME_PIN, TIME_CAL, NOVEDADES, SUBCONTRATAR)
                                    VALUES  (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                """
            
        cursor.execute(insert_data_script, (chasis, fecha, marca, modelo, color, estado, ttel, tpdi, tlav, tpin, tcal, novedades, subcontratar))
        conn.commit()
        print("Registro añadido")
        
    except sqlite3.Error as e:
        print(f"Error al insertar el registro: {e}")

    except UnboundLocalError as e:
        print(f"No se llenaron todos los campos: {e}") 

    finally:
        conn.close()



def leer_vehiculos():

    conn = sqlite3.connect('produccion.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM vehiculos')
    registros = cursor.fetchall()
    print(registros)

    conn.close()
    return registros


def leer_vehiculo(chasis):
    conn = sqlite3.connect('produccion.db')
    cursor = conn.cursor()

    vehiculo = chasis
    cursor.execute('SELECT * FROM vehiculos WHERE CHASIS=?', (vehiculo,))
    registros = cursor.fetchone()
    print(registros)

    conn.close()
    return registros


def modificar_vehiculo( nuevo_registro, chasis_actual):
    conn = sqlite3.connect('produccion.db')
    cursor = conn.cursor()
    print(chasis_actual)
    cursor.execute('''UPDATE vehiculos SET
                    CHASIS=?, FECHA=?, MARCA=?, MODELO=?, COLOR=?, ESTADO=?, TIME_TEL=?, TIME_PDI=?, TIME_LAV=?, TIME_PIN=?, TIME_CAL=?, NOVEDADES=?, SUBCONTRATAR=?
                    WHERE CHASIS=?''',
                    (*nuevo_registro, chasis_actual))
    conn.commit()
    conn.close()




def eliminar_vehiculo(chasis):
    try:
        conn = sqlite3.connect('produccion.db')
        cursor = conn.cursor()
        
        # Sentencia SQL para eliminar el registro
        delete_data_script = """DELETE FROM vehiculos
                                WHERE CHASIS = ?
                             """
        
        cursor.execute(delete_data_script, (chasis,))
        conn.commit()
        
        # Verificar cuántas filas fueron afectadas
        if cursor.rowcount > 0:
            print("Registro eliminado")
        else:
            print("No se encontró el registro para eliminar")
    
    except sqlite3.Error as e:
        print(f"Error al eliminar el registro: {e}")
    
    finally:
        conn.close()


###########################################################################
############################# CRUD PARA TECNICOS ##########################
###########################################################################

def insertar_tecnico(id_tec,nombre,especialidad):
    try:
        conn = sqlite3.connect('produccion.db')
        cursor = conn.cursor()

        if all(item is not None for item in (id_tec,nombre,especialidad)):
            
            insert_data_script = """INSERT INTO tecnicos 
                                    (ID_TECNICO, NOMBRE, ESPECIALIDAD)
                                    VALUES  (?, ?, ?)
                                """
            
        cursor.execute(insert_data_script, (id_tec,nombre,especialidad))
        conn.commit()
        print("Registro de tecnico añadido")
        
    except sqlite3.Error as e:
        print(f"Error al insertar el registro: {e}")

    except UnboundLocalError as e:
        print(f"No se llenaron todos los campos: {e}") 

    finally:
        conn.close()


#Lee las datos de todos los tecnicos de la BD y los empaqueta en una lista de tuplas
def leer_tecnicos():

    conn = sqlite3.connect('produccion.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM tecnicos;')
    todosRegistros = cursor.fetchall()
    los_tecnicos = [(registro[0], registro[1], registro[2]) for registro in todosRegistros]
    print(los_tecnicos)

    conn.close()
    return los_tecnicos

#Cuenta la cantidad de registros en la tabla de modelos
def calcula_tecnicos():

    conn = sqlite3.connect('produccion.db')
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM tecnicos;')
    numero_registros = cursor.fetchone()[0]

    conn.close()
    return numero_registros



##################################################################################
######################### CRUD PARA ORDENES ######################################
##################################################################################
#CODIGO_ORDEN, CHASIS, MARCA, MODELO, COLOR, NOVEDADES, PEDIDO, ID_PEDIDO, PROCESO, ID_TECNICO, NOMBRE_TECNICO, ESPECIALIDAD, INICIO, FIN, DURACION, PLAZO

def insertar_orden(codigo_orden, chasis, marca, modelo, color, novedades, pedido, id_pedido, proceso, id_tecnico, nombre_tecnico, especialidad, inicio, fin, duracion, plazo):
    try:
        conn = sqlite3.connect('produccion.db')
        cursor = conn.cursor()

          
        insert_data_script = """INSERT INTO ordenes
                                    (CODIGO_ORDEN, CHASIS, MARCA, MODELO, COLOR, NOVEDADES, PEDIDO, ID_PEDIDO, PROCESO, ID_TECNICO, NOMBRE_TECNICO, ESPECIALIDAD, INICIO, FIN, DURACION, PLAZO)
                                    VALUES  (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                """

        datos = (codigo_orden, chasis, marca, modelo, color, novedades, pedido, id_pedido, proceso, id_tecnico, nombre_tecnico, especialidad, inicio, fin, duracion, plazo)

        cursor.execute(insert_data_script, datos)
        conn.commit()
        print("Orden añadida")
        
    except sqlite3.Error as e:
        print(f"Error al insertar el Orden: {e}")

    except UnboundLocalError as e:
        print(f"No se llenaron todos los campos: {e}") 

    finally:
        conn.close()    

def leer_ordenes_todas():
    conn = sqlite3.connect('produccion.db')         # Conectar a la base de datos
    registros = "SELECT * FROM ordenes"                 # Definir la consulta SQL
    df = pd.read_sql_query(registros, conn)             # Leer la tabla completa y crear un DataFrame
    conn.close()                                    # Cerrar la conexión
    return df




def eliminar_ordenes_todas():

    conn = sqlite3.connect('produccion.db')
    cursor = conn.cursor()            
    cursor.execute("DELETE FROM ordenes")
    conn.commit()
    conn.close()
    
    print("Registro eliminado")





















###################### CONSULTAS Y PRUEBAS ##################################
#crear_tabla_ordenes()
#eliminar_tabla("sqlite_sequence")

#insertar_vehiculo(1,2,3,4,5,6,7,8,9)
#eliminar_vehiculo("123")
#eliminar_vehiculo("BAI")
#eliminar_vehiculo("RENKOL")

#print(leer_ordenes_todas())

#eliminar_ordenes_todas()


"""
#Ejemplos de técnicos
eliminar_tabla('tecnicos')
lista_de_tecnicos = [
    ("Tel02Osm", "Osman", "TELEQUINOX"),
    ("Tel03Bra", "Jesus", "TELEQUINOX"),
    ("Tel04Jer", "Jeremias", "TELEQUINOX"),
    ("Tel05Lui", "Luis", "TELEQUINOX"),
    ("Tel06Alb", "Alberto", "TELEQUINOX"),
    ("Tel07Jos", "Jose", "TELEQUINOX"),
    ("Tel08JuJ", "JuanJose", "TELEQUINOX"),
    ("Tel09JuD", "JuanDavid", "TELEQUINOX"),
    ("Tel10Wil", "William", "TELEQUINOX"),
    ("Tel11Ces", "Cesar", "TELEQUINOX"),
    ("Tel12Car", "Carlos", "TELEQUINOX"),
    ("Tel13Cha", "Charly", "TELEQUINOX"),

    ("Pdi01Ang", "Angel", "PDI"),
    ("Pdi02Tit", "Tito", "PDI"),
    ("Pdi03Dav", "David", "PDI"),
    ("Pdi04Cri", "Cristian", "PDI"),
    ("Pdi05Jes", "Jesus", "PDI"),
    ("Pdi06Bec", "Backer", "PDI"),
    ("Pdi07Gus", "Gustavo", "PDI"),

    ("Lav01Lui", "Luis", "LAVADO"),
    ("Lav02Jes", "Jesus", "LAVADO"),
    ("Lav03Ala", "Alan", "LAVADO"),

    ("Pin01Dan", "Daniel", "PINTURA"),
    ("Pin02Vic", "Victor", "PINTURA"),
    ("Pin03Kev", "Kevin", "PINTURA"),

    ("Cal01Dav", "David", "CALIDAD"),
 ]

crear_tabla_tecnicos()
for operario in lista_de_tecnicos:
    insertar_tecnico(*operario)

"""


# ITERAR SOBRE MODELOS Y MARCAS PARA ALIMENTAR LA BASE DE DATOS
"""
for marca, lista_modelos in marcas.items():
    for modelo in lista_modelos:
        # Aquí 'modelo' es la clave del diccionario tiempos
        if modelo in tiempos:
            tiempos_modelo = tiempos[modelo]
            
            # Imprimir la marca, el modelo y los tiempos correspondientes
            print(f'Marca: {marca}, Modelo: {modelo}, Tiempos: {tiempos_modelo}')
            
            # Ejemplo de cómo podrías usar los tiempos
            for indice, tiempo in enumerate(tiempos_modelo):
                print(f'  Índice: {indice}, Tiempo: {tiempo}')
                
            insertar_modelo(marca, modelo, tiempos_modelo[0], tiempos_modelo[1], tiempos_modelo[2], tiempos_modelo[3], tiempos_modelo[4])
"""