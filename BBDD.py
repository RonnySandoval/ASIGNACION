import sqlite3
import pandas as pd
import os
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
############################# CRUD PARA MODELOS ###########################
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
        print(f"Error al insertar el registro: {e}")

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
        print(f"Error al insertar el registro: {e}")

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
        print(f"Error al insertar el registro: {e}")

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



def leer_procesos(bbdd):
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

print(calcula_procesos('planta_manta.db'))






######### CONSULTAS PARA LEER Y ORGANIZAR TIEMPOS ########
def obtener_id_procesos(bbdd):
    try:
        conn = sqlite3.connect(bbdd)
        cursor = conn.cursor()
        
        # Obtener todos los ID_PROCESO únicos
        cursor.execute("SELECT DISTINCT ID_PROCESO FROM TIEMPOS_MODELOS")
        id_procesos = [row[0] for row in cursor.fetchall()]  # Lista de procesos
        conn.commit()

    except sqlite3.Error as e:
        print(f"Error al obtener los ID_PROCESO: {e}")
        id_procesos = []
    
    finally:
        conn.close()

    return id_procesos

def generar_consulta_dinamica(bbdd):
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

def leer_tiempos_procesos(bbdd):
    try:
        # Generar consulta SQL
        consulta = generar_consulta_dinamica(bbdd)

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

# Ejemplo de uso:
df = leer_tiempos_procesos(bbdd = 'planta_manta.db')
#print(df)









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















































"""
procesos=[
    ("TEL", "TELEQUINOX", "Instalacion de accesorios Packs y Recubrimientos"),
    ("PDI", "PDI MECANICO", "Revision exterior, interior, habitaculo"),
    ("LAV", "LAVADO", "Operaciones de lavado y secado"),
    ("PIN", "PINTURA", "Micropulidos Pulidos Latoneria y Pintura"),
    ("CAL", "CALIDAD", "Inspeccion de rutina")
]

for proceso in procesos:
    insertar_procesos('planta_manta.db', proceso[0], proceso[1], proceso[2])





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
        insertar_modelo('planta_manta.db', id_marcamodelo, marca, modelo)


        
procesos = leer_procesos('planta_manta.db')
modelos = leer_modelos('planta_manta.db')
datosTiemposModelos =[]

print(procesos)
print(modelos)
diccionario={}

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
    

    

marcas = {
    "NISSAN":   ["ALTIMA","FRONTIER","KICKS","QASHQAI","LEAFT","VERSA","PATHFINDER","XTRAIL",],
    "RENAULT":  ["CAPTUR","KOLEOS","KWID",],
    "BAIC":     ["BJ20","BJ40","D50","NX55","X35","X55","U5P",],
    "FOTON":    ["AUMARK","AUMAN","TUNLAND","VIEW","TOANO",],
    "GEELY":    ["AZKARRA","COOLRAY",],
    "MG":       ["RX8","RX5","MG5","ZS","ONE"]
}


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


"""

