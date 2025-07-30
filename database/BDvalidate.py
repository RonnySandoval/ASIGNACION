import sqlite3
import controller.glo as glo
import pandas as pd

def gestion_sqlite(bbdd):
    def decorador(func):
        def wrapper(*args, **kwargs):
            try:
                conn = sqlite3.connect(bbdd)                    # Conexión a la base de datos
                cursor = conn.cursor()                          # Abrir el cursor
                resultado = func(cursor, *args, **kwargs)       # Ejecución de la función decorada
                conn.commit()                                   # Guardar los cambios (si corresponde)
                return resultado

            except sqlite3.Error as e:
                print(f"Error de SQLite: {e}")
                return None

            except Exception as e:
                print(f"Error en la función decorada: {e}")
                return None

            except UnboundLocalError as e:
                print(f"Error con la conexion de la Base de Datos: {e}")
                return None
            
            finally:
                conn.close()

        return wrapper
    return decorador

@gestion_sqlite(glo.base_datos)
def lectura_huerfanos(cursor, tabla1, tabla2, campo1, campo2):
    consulta  = f"""
                   SELECT *
                   FROM {tabla1}
                   WHERE {campo1} NOT IN
                   (SELECT {campo2} FROM {tabla2})
                    """
    cursor.execute(consulta)
    return cursor.fetchall()

@gestion_sqlite(glo.base_datos)
def lecturaJoin_huerfanos(cursor, tabla1, tablaJoin, tablaCompare, campo1, campoJoin, campoCompare, join):
    consulta = f"""
                   SELECT *
                   FROM {tabla1}
                   {join} JOIN {tablaJoin}
                   ON {tabla1}.{campo1} = {tablaJoin}.{campoJoin}
                   WHERE {tablaJoin}.{campoCompare} NOT IN
                   (SELECT {campoCompare} FROM {tablaCompare})
                    """
    cursor.execute(consulta)
    return cursor.fetchall()

class Huerfanos:
    def __init__(self):
        self.programas_ordenes = None
        self.vehiculos_tiemposVehiculos = None
        self.tiemposVehiculos_vehiculos = None
        self.vehiculos_pedidos = None
        self.tecnicos_tecnicosProcesos = None
        self.tecnicosProcesos_tecnicos = None
        self.modelos_tiemposModelos = None
        self.tiemposModelos_modelos = None
        self.vehiculos_historicos = None
        self.historicos_vehiculos = None
        self.modelos_referencias = None
        self.referencias_modelos = None
        self.vehiculos_referencias = None
        self.referencias_vehiculos = None
        self.ordenes_programas_pedidos = None
        self.tiemposVehiculos_vehiculos_pedidos = None
        self.tecnicos_tecnicosProcesos_procesos = None
        self.historicos_vehiculos_pedidos = None

    def evaluar_integridad(self):
        """Actualiza las propiedades con los resultados de lectura_huerfanos y lecturaJoin_huerfanos."""
        self.programas_ordenes = lectura_huerfanos("ORDENES", "PROGRAMAS", "ID_PROGRAMA", "ID_PROGRAMA")
        self.vehiculos_tiemposVehiculos = lectura_huerfanos("VEHICULOS", "TIEMPOS_VEHICULOS", "CHASIS", "CHASIS")
        self.tiemposVehiculos_vehiculos = lectura_huerfanos("TIEMPOS_VEHICULOS", "VEHICULOS", "CHASIS", "CHASIS")
        self.vehiculos_pedidos = lectura_huerfanos("VEHICULOS", "PEDIDOS", "ID_PEDIDO", "ID_PEDIDO")
        self.tecnicos_tecnicosProcesos = lectura_huerfanos("TECNICOS", "TECNICOS_PROCESOS", "ID_TECNICO", "ID_TECNICO")
        self.tecnicosProcesos_tecnicos = lectura_huerfanos("TECNICOS_PROCESOS", "TECNICOS", "ID_TECNICO", "ID_TECNICO")
        self.modelos_tiemposModelos = lectura_huerfanos("MODELOS", "TIEMPOS_MODELOS", "ID_MODELO", "ID_MODELO")
        self.tiemposModelos_modelos = lectura_huerfanos("TIEMPOS_MODELOS", "MODELOS", "ID_MODELO", "ID_MODELO")
        self.vehiculos_historicos = lectura_huerfanos("VEHICULOS", "HISTORICOS", "CHASIS", "CHASIS")
        self.historicos_vehiculos = lectura_huerfanos("HISTORICOS", "VEHICULOS", "CHASIS", "CHASIS")
        self.modelos_referencias = lectura_huerfanos("MODELOS", "MODELOS_REFERENCIAS", "ID_MODELO", "ID_MODELO")
        self.referencias_modelos = lectura_huerfanos("MODELOS_REFERENCIAS", "MODELOS", "ID_MODELO", "ID_MODELO")
        self.vehiculos_referencias = lectura_huerfanos("VEHICULOS", "MODELOS_REFERENCIAS", "REFERENCIA", "REFERENCIA")
        self.referencias_vehiculos = lectura_huerfanos("MODELOS_REFERENCIAS", "VEHICULOS", "REFERENCIA", "REFERENCIA")
        self.ordenes_programas_pedidos = lecturaJoin_huerfanos("ORDENES", "PROGRAMAS", "PEDIDOS",
                                                               "ID_PROGRAMA", "ID_PROGRAMA", "ID_PEDIDO", "INNER")
        self.tiemposVehiculos_vehiculos_pedidos = lecturaJoin_huerfanos("TIEMPOS_VEHICULOS", "VEHICULOS", "PEDIDOS",
                                                                        "CHASIS", "CHASIS", "ID_PEDIDO", "INNER")
        self.tecnicos_tecnicosProcesos_procesos = lecturaJoin_huerfanos("TECNICOS", "TECNICOS_PROCESOS", "PROCESOS",
                                                                        "ID_TECNICO", "ID_TECNICO", "ID_PROCESO", "INNER")
        self.historicos_vehiculos_pedidos = lecturaJoin_huerfanos("HISTORICOS", "VEHICULOS", "PEDIDOS",
                                                                  "CHASIS", "CHASIS", "ID_PEDIDO", "INNER")

    def convertir_a_dataframe(self, lista):
        """Convierte una lista de tuplas en un DataFrame sin encabezado."""
        if isinstance(lista, list) and all(isinstance(i, tuple) for i in lista):
            return pd.DataFrame(lista)
        return lista  # Si no es una lista de tuplas, se retorna tal cual.

    def __getattribute__(self, name):
        """Sobrescribe el acceso a todas las propiedades."""
        print(f"Accediendo al atributo: {name}")
        value = super().__getattribute__(name)                      # Llama al método original para obtener el atributo
        if isinstance(value, list) and all(isinstance(i, tuple) for i in value):# Si es una lista de tuplas, convierte a DataFrame
            return pd.DataFrame(value)
        return value

    def __str__(self):
        """Genera una representación por defecto como DataFrame."""
        df = self.generar_dataframe()
        return df.to_string(index=False, header=False)

    def generar_dataframe(self):
        """Genera un DataFrame con las propiedades, sin nombres de columna."""
        data = [[key, len(value) if isinstance(value, list) else 0] for key, value in vars(self).items()]
        return pd.DataFrame(data, columns=["RELACION", "CANTIDAD"])  # Sin nombres de columna

glo.huerfanos = Huerfanos()















"""
--Seleccionar las ordenes cuyos programas tengan pedido que no aparezcan en pedidos.................................
-- SELECT *
-- FROM ORDENES
-- INNER JOIN PROGRAMAS
-- ON PROGRAMAS.ID_PROGRAMA = ORDENES.ID_PROGRAMA 
-- WHERE PROGRAMAS.ID_PEDIDO NOT IN
-- (SELECT ID_PEDIDO FROM PEDIDOS)
"""
"""
--Seleccionar las ordenes cuyos id_programa no aparezcan en programas.....................................
-- SELECT *
-- FROM ORDENES
-- WHERE ORDENES.ID_PROGRAMA NOT IN
-- (SELECT PROGRAMAS.ID_PROGRAMA FROM PROGRAMAS)
"""
"""
--Seleccionar los vehiculos que no aparezcan en la tabla de tiempos........................................
-- SELECT *
-- FROM VEHICULOS
-- WHERE CHASIS NOT IN
-- (SELECT CHASIS FROM TIEMPOS_VEHICULOS)
"""
"""
--Seleccionar los vehiculos que tengas tiempos pero no estén en la tabla de vehiculos........................
-- SELECT *
-- FROM TIEMPOS_VEHICULOS
-- WHERE CHASIS NOT IN
-- (SELECT CHASIS FROM VEHICULOS)
"""
"""
--Seleccionar los tiempos de vehiculos cuyos registros en tabla vehiculos tengan pedido no existente en pedidos........................
-- SELECT *
-- FROM TIEMPOS_VEHICULOS
-- INNER JOIN VEHICULOS
-- ON VEHICULOS.CHASIS = TIEMPOS_VEHICULOS.CHASIS
-- WHERE VEHICULOS.ID_PEDIDO NOT IN
-- (SELECT ID_PEDIDO FROM PEDIDOS)
"""
"""
--Seleccionar los vehiculos cuyos_pedido no existe en pedidos..................................
-- SELECT *
-- FROM VEHICULOS
-- WHERE ID_PEDIDO NOT IN
-- (SELECT ID_PEDIDO FROM PEDIDOS)
"""
"""
--Seleccionar los técnicos cuya especialidad no aparezca en la tabla de procesos..................................
-- SELECT *
-- FROM TECNICOS
-- LEFT JOIN TECNICOS_PROCESOS
-- ON TECNICOS.ID_TECNICO = TECNICOS_PROCESOS.ID_TECNICO
-- WHERE TECNICOS_PROCESOS.ID_PROCESO NOT IN 
-- (SELECT ID_PROCESO FROM PROCESOS)
"""
"""
--Seleccionar los técnicos cuyo id no aparezca en la tabla de tecnicos_procesos..............................
-- SELECT *
-- FROM TECNICOS
-- WHERE ID_TECNICO NOT IN
-- (SELECT ID_TECNICO FROM TECNICOS_PROCESOS)
"""
"""
--Seleccionar los técnicos en la tabla de tecnicos_procesos cuyo id no aparezca en la tabla de tecnicos.....................
-- SELECT *
-- FROM TECNICOS_PROCESOS
-- WHERE ID_TECNICO IN
-- (SELECT ID_TECNICO FROM PROCESOS)
"""
"""
--Seleccionar los vehiculos que no tengan históricos (no es incorrecto)..................................
-- SELECT *
-- FROM VEHICULOS AS V
-- LEFT JOIN HISTORICOS AS H
-- ON H.CHASIS = V.CHASIS
-- WHERE V.CHASIS NOT IN
-- (SELECT CHASIS FROM HISTORICOS)
"""
"""
--Seleccionar los históricos cuyo chasis no aparezca en la tabla de vehiculos.......................................
-- SELECT *
-- FROM HISTORICOS AS H
-- LEFT JOIN VEHICULOS AS V
-- ON H.CHASIS = V.CHASIS
-- WHERE H.CHASIS NOT IN
-- (SELECT CHASIS FROM VEHICULOS)
"""
"""
--Seleccionar los históricos de los vehiculos cuyo id_pedido no aparezca en la tabla de pedidos......................
-- SELECT *
-- FROM HISTORICOS AS H
-- LEFT JOIN VEHICULOS AS V
-- ON H.CHASIS = V.CHASIS
-- WHERE V.ID_PEDIDO NOT IN
-- (SELECT ID_PEDIDO FROM PEDIDOS)

--Seleccionar los pedidos que tengan vehiculos cuyo chasis no aparece en la tabla históricos (no es incorrecto)
-- SELECT *
-- FROM PEDIDOS AS P
-- LEFT JOIN VEHICULOS AS V
-- ON P.ID_PEDIDO = V.ID_PEDIDO
-- WHERE V.CHASIS NOT IN
-- (SELECT CHASIS FROM HISTORICOS)

-- Seleccionar los vehiculos  cuyo chasis no aparece en la tabla históricos (no es incorrecto)
-- SELECT *
-- FROM PEDIDOS AS P
-- LEFT JOIN VEHICULOS AS V
-- ON P.ID_PEDIDO = V.ID_PEDIDO
-- WHERE V.CHASIS NOT IN
-- (SELECT CHASIS FROM HISTORICOS)
"""
"""
--Seleccionar los modelos que no tengan registro en la tabla de tiempos...................................
-- SELECT *
-- FROM MODELOS
-- WHERE ID_MODELO IN
-- (SELECT ID_MODELO FROM TIEMPOS_MODELOS)
"""
"""
--Seleccionar los modelos que tengan tiempos pero no estén en la tabla de modelos..............................
-- SELECT *
-- FROM TIEMPOS_MODELOS
-- WHERE ID_MODELO NOT IN
-- (SELECT ID_MODELO FROM MODELOS)
"""
"""
--Seleccionar las referencias cuyo id_modelo aparezca en la tabla de referencias pero no aparezca en la tabla de modelos...................
-- SELECT *
-- FROM MODELOS_REFERENCIAS
-- WHERE ID_MODELO NOT IN
-- (SELECT ID_MODELO FROM MODELOS)
"""
"""
--Seleccionar los modelos cuyo id_modelo aparezca en la tabla de modelos pero no en la de referencias (no es incorrecto).........................
-- SELECT *
-- FROM MODELOS
-- WHERE ID_MODELO NOT IN
-- (SELECT ID_MODELO FROM MODELOS_REFERENCIAS)
"""
"""
--Seleccionar los vehiculos cuya referencia no aparezca en la tabla de referencias.......................................
-- SELECT *
-- FROM VEHICULOS
-- WHERE REFERENCIA NOT IN
-- (SELECT REFERENCIA FROM MODELOS_REFERENCIAS)
"""
"""
--Seleccionar las referencia de modelos que no tengan registros en la tabla de vehiculos (no es incorrecto)....................
-- SELECT *
-- FROM MODELOS_REFERENCIAS
-- WHERE REFERENCIA NOT IN
-- (SELECT REFERENCIA FROM VEHICULOS)
"""
"""
--Seleccionar los vehiculos cuya referencia no coincida con la referencia que debería tener según el modelo
-- SELECT *
-- FROM VEHICULOS 
-- WHERE REFERENCIA NOT IN	
-- 	(SELECT REFERENCIA 
-- 	FROM MODELOS_REFERENCIAS
-- 	WHERE MODELOS_REFERENCIAS.ID_MODELO = VEHICULOS.ID_MODELO)


----------------------------------------------------------------------------------------------------
---OJO, LOS CAMPOS PRIMARIOS Y LOS DE INTERSECCION (O "FORANEOS") NUNCA DEBERÍAN TENER VALOR NULL---
----------------------------------------------------------------------------------------------------

-----------------------------------------------------------------------------------------------------
-- SELECT NOMBRE_PLANTA
-- FROM INFORMACION
-- WHERE NOMBRE_PLANTA IS NULL
-----------------------------------------------------------------------------------------------------


-----------------------------------------------------------------------------------------------------
-- SELECT CODIGO_ASIGNACION
-- FROM HISTORICOS
-- WHERE CODIGO_ASIGNACION IS NULL

-- SELECT CODIGO_ASIGNACION
-- FROM HISTORICOS
-- WHERE ID_TECNICO IS NULL

-- SELECT CODIGO_ASIGNACION
-- FROM HISTORICOS
-- WHERE CHASIS IS NULL

-- SELECT CODIGO_ASIGNACION
-- FROM HISTORICOS
-- WHERE ID_PROCESO IS NULL
-----------------------------------------------------------------------------------------------------


-----------------------------------------------------------------------------------------------------
-- SELECT ID_MODELO
-- FROM MODELOS
-- WHERE ID_MODELO IS NULL
-----------------------------------------------------------------------------------------------------


-----------------------------------------------------------------------------------------------------
-- SELECT REFERENCIA
-- FROM MODELOS_REFERENCIAS
-- WHERE REFERENCIAS IS NULL


-- SELECT REFERENCIAS
-- FROM MODELOS_REFERENCIAS
-- WHERE ID_MODELO IS NULL
-----------------------------------------------------------------------------------------------------


-----------------------------------------------------------------------------------------------------
-- SELECT CODIGO_ORDEN
-- FROM ORDENES
-- WHERE CODIGO_ASIGNACION IS NULL

-- SELECT CODIGO_ORDEN
-- FROM ORDENES
-- WHERE ID_TECNICO IS NULL

-- SELECT CODIGO_ORDEN
-- FROM ORDENES
-- WHERE CHASIS IS NULL

-- SELECT CODIGO_ORDEN
-- FROM ORDENES
-- WHERE ID_PROCESO IS NULL

-- SELECT CODIGO_ORDEN
-- FROM ORDENES
-- WHERE ID_PROGRAMA IS NULL
-----------------------------------------------------------------------------------------------------


-----------------------------------------------------------------------------------------------------
-- SELECT ID_PEDIDO
-- FROM PEDIDOS
-- WHERE ID_PEDIDO IS NULL
-----------------------------------------------------------------------------------------------------


-----------------------------------------------------------------------------------------------------
-- SELECT ID_PROCESO
-- FROM PROCESOS
-- WHERE ID_PROCESO IS NULL
-----------------------------------------------------------------------------------------------------


-----------------------------------------------------------------------------------------------------
-- SELECT ID_PROGRAMA
-- FROM PROGRAMAS
-- WHERE ID_PROGRAMA IS NULL


-- SELECT ID_PROGRAMA
-- FROM PROGRAMAS
-- WHERE ID_PEDIDO IS NULL
-----------------------------------------------------------------------------------------------------

-----------------------------------------------------------------------------------------------------
-- SELECT ID_TECNICO
-- FROM TECNICOS
-- WHERE ID_TECNICO IS NULL
-----------------------------------------------------------------------------------------------------


-----------------------------------------------------------------------------------------------------
-- SELECT TEC_PROC
-- FROM TECNICOS_PROCESOS
-- WHERE TEC_PROC IS NULL

-- SELECT TEC_PROC
-- FROM TECNICOS_PROCESOS
-- WHERE ID_TECNICO IS NULL

-- SELECT TEC_PROC
-- FROM TECNICOS_PROCESOS
-- WHERE ID_PROCESO IS NULL
-----------------------------------------------------------------------------------------------------


-----------------------------------------------------------------------------------------------------
-- SELECT PROCESO_MODELO
-- FROM TIEMPOS_MODELOS
-- WHERE PROCESO_MODELO IS NULL

-- SELECT PROCESO_MODELO
-- FROM TIEMPOS_MODELOS
-- WHERE ID_MODELO IS NULL

-- SELECT PROCESO_MODELO
-- FROM TIEMPOS_MODELOS
-- WHERE ID_PROCESO IS NULL
-----------------------------------------------------------------------------------------------------


-----------------------------------------------------------------------------------------------------
-- SELECT PROCESO_CHASIS
-- FROM TIEMPOS_VEHICULOS
-- WHERE PROCESO_CHASIS IS NULL

-- SELECT PROCESO_CHASIS
-- FROM TIEMPOS_VEHICULOS
-- WHERE CHASIS IS NULL

-- SELECT PROCESO_CHASIS
-- FROM TIEMPOS_VEHICULOS
-- WHERE ID_PROCESO IS NULL
-----------------------------------------------------------------------------------------------------


-----------------------------------------------------------------------------------------------------
-- SELECT CHASIS
-- FROM VEHICULOS
-- WHERE CHASIS IS NULL

-- SELECT CHASIS
-- FROM VEHICULOS
-- WHERE ID_MODELO IS NULL

-- SELECT CHASIS
-- FROM VEHICULOS
-- WHERE REFERENCIA IS NULL
-----------------------------------------------------------------------------------------------------

"""