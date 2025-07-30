import sqlite3
import pandas as pd

class Query:
    """Ejecuta y Almacena información sobre la consulta"""
    def __init__(self, query_string, params=None, fetch='all', as_dict=True):
        """
        :param query_string: Consulta SQL.
        :param params: Parámetros para ejecutar la consulta (tupla o lista).
        :param fetch: 'one', 'all' o 'none' dependiendo del tipo de resultado esperado.
        """
        self.query_string = query_string
        self.params = params or ()
        self.fetch = fetch
        self.as_dict = as_dict
        self.affected_rows = None

    def execute_query(self, db, type_query, table):
        cursor = db.connection.cursor()
        
        try:
            if type_query == 'INSERT_OR REPLACE':
                cursor.executemany(self.query_string, self.params)
            else:
                cursor.execute(self.query_string, self.params)
                
            #print(self.query_string, self.params)
            print(f"Consulta {type_query} exitosa en la tabla {table}")
            
        except Exception as e:
            print(f"❌ Error al ejecutar la consulta:\n{self.query_string},\n({self.params})\n→ {e}")
            raise
        
        else:
            if self.fetch == 'one':
                row = cursor.fetchone()
                result = dict(row) if row and self.as_dict else row
            elif self.fetch == 'all':
                rows = cursor.fetchall()
                result = [dict(row) for row in rows] if self.as_dict else rows
            else:
                result = None
                try:
                    self.affected_rows = cursor.rowcount
                    if type_query != 'DELETE CASCADE':
                        db.commit_query(self.affected_rows)
                except Exception as e:
                    raise
            return result
        
        finally:
            cursor.close()

    def __str__(self):
        return f"Query: {self.query_string},Affected Rows: {self.affected_rows or 'N/A'}"

class Database:
    """Conecta con base de datos y confirma consultas"""
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self._rows_affected = 0
        
    def __enter__(self):
        return self

    def commit_query(self, rows):
        try:
            self.connection.commit()
            print(f"[Se confirmaron cambios en la base de datos]. Filas afectadas {rows}")
            if  rows is not None:
                self._rows_affected += rows
            
        except sqlite3.Error as e:
            self.connection.rollback()
            print(f"[ERROR al confirmar la consulta] {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
    
    @property
    def track_affected(self):
        return self._rows_affected

class Crud:
    """Construye el código SQL y llama los métodos que lo ejecutan"""
    def __init__(self, db: Database, table_name: str):
        self.db = db
        self.table = table_name

    def __execute_changes__(self, sql, params, type_query) -> int:
        
        query = Query(query_string = sql, params = params, fetch="none")
        query.execute_query(self.db, type_query, self.table)
        return query.affected_rows


    def select(self,
                fields: list[str] = "*",
                joins: dict = None, 
                cases: str = None,
                type_join: str = 'LEFT',
                where: dict = None,
                group_by: str = None,
                order_by: str = None,
                distinct: bool = False,
                fetch: str = "all",
                as_dataframe: bool = False,
                as_list: bool = True) -> list[tuple]:
        """
        Ejecuta una consulta SELECT con cláusulas JOIN.

        Parámetros:
            - fields: list[str]
                Lista de campos a seleccionar, por ejemplo: ['vehiculos.id', 'modelos.nombre']
            - joins: dict
                Diccionario de JOINs, de la forma ->{ 'table': 'table_base.field = table_second.field'}
            - where: dict
                Diccionario de condiciones WHERE. Ej: {'modelos.nombre': 'TOANO', 'vehiculos.estado': 'ACTIVO'}
            - order_by: str
                Campo por el cual ordenar (opcional).
            - distinct: bool
                Booleano para incluir la clausila DISTINCT
            - fetch: str
                String con 'one' o 'all', dependiendo de la cantidad de registros deseados
            - as_dataframe: bool
                Boleano para retornar el resultado en forma de dataframe
            - as_list: bool
                Boleano para retornar el resultado en forma de lista de tuplas
            
        Retorna:
            Lista de tuplas o dataframe con los resultados de la consulta.
        """

        # SELECT, CAMPOS, DISTINCT, CASES
        select_clause = "SELECT "
        select_clause += "DISTINCT "     if distinct else ""
        select_clause += ", ".join(self.format_coalesce(f) for f in fields)
        select_clause += f", {cases} "   if cases else ""
               
        # FROM
        from_clause = f"FROM {self.table}"

        # JOINS        
        join_clauses = "".join(f" {type_join} JOIN {table} ON {condition}" for table, condition in joins.items()) if joins else ""

        # WHERE
        where_clause = " WHERE " + " AND ".join([f"{col} = ?" for col in where]) if where else ""
        vals = tuple(where.values()) if where else ()
        
        # GROUP BY, ORDER BY  
        group_clause = f" GROUP BY {group_by}" if group_by else ""
        order_clause = f" ORDER BY {order_by}" if order_by else ""

        # CONSTRUCCIÓN DE CONSULTA SQL COMPLETA
        query_str = f"{select_clause} {from_clause} {join_clauses} {where_clause} {group_clause} {order_clause}"
        print(query_str,', ' ,vals)
    
        # CREACIÓN DE OBJETO QUERY
        query = Query(query_string=query_str, params=vals, fetch=fetch)
        
        #EJECUCIÓN DE CONSULTA
        results = query.execute_query(self.db, 'SELECT', self.table)
        
        # CONVERTIR A DATAFRAME
        if as_dataframe:
            as_list = False
            
            if not results:
                print(f"No se encontraron registros en la tabla {self.table}")
                return pd.DataFrame(columns=fields.split(", ") if fields != "*" else [])
            
            columns = results[0].keys()
            return pd.DataFrame(results, columns=columns)
        
        # CONVERTIR A LISTA DE TUPLAS
        if as_list:
            if not results:
                print(f"No se encontraron registros en la tabla {self.table}")
                return []
            
            if isinstance(results, dict):  # caso de fetch='one' y as_dict=True
                return tuple(results.values())

            first_row = results[0]
            values = [tuple(row.values()) for row in results]

            if len(first_row.keys()) == 1:
                return [val[0] for val in values]

            return values

        return results

    def insert(self,
               columns: list,
               vals: list) -> int:
        cols_str = ", ".join(columns)
        placeholders = ", ".join(["?"] * len(columns))
        sql = f"INSERT INTO {self.table} ({cols_str}) VALUES ({placeholders})"
        return self.__execute_changes__(sql        = sql,
                                        params     = vals,
                                        type_query ='INSERT')

    def insert_dataframe(self,
                         dataframe: pd.DataFrame,
                         if_exists="append") -> int:
        try:
            num_rows = len(dataframe)
            dataframe.to_sql(self.table, self.db.connection, if_exists=if_exists, index=False)
            print(f"El DataFrame se insertó con éxito en la tabla {self.table}")
            self.db.commit_query(rows_df = num_rows)
            return num_rows
        except Exception as e:
            self.db.connection.rollback()
            print(f"❌ Error al insertar DataFrame en {self.table}: {e}")
            raise

    def insert_or_replace(self,
                         columns: list,
                         vals: list,
                         where_col: str = None,)-> int:
        
        cols_str = ", ".join(columns)
        placeholders = ", ".join(["?"] * len(columns))
        
        sql = f"INSERT OR REPLACE INTO {self.table} ({cols_str}) VALUES ({placeholders})"
        sql = +f" WHERE {where_col} = ?" if where_col else ""
        
        vals.append(vals[0]) if where_col else None
        return self.__execute_changes__(sql        = sql,
                                        params     = vals,
                                        type_query = 'INSERT OR REPLACE')       
        
    def update(self,
               columns  : list,
               vals     : list,
               where_col: str,
               params   : list,
               case     : bool = False,
               where_vals: list = None) -> int:

        if case == True:
            
            case_str = f'CASE {vals[0]} ' if case else ''
            parameters = tuple(params) if isinstance(params, list) else (params,)

            sql = f"UPDATE {self.table} SET {columns[0]} = {case_str }, {columns[1]} = ? \n WHERE {where_col} IN ({', '.join(['?'] * len(where_vals))})"

        else:
            set_str = ", ".join(f"{col}=?" for col in columns)
            sql = f"UPDATE {self.table} SET {set_str} \n WHERE {where_col} = ?"
            parameters = (*vals, params)
            
            
        print(f"SQL:\n {sql} \n Params:\n {parameters}")
        self.__execute_changes__(sql    = sql,
                                        params = parameters,
                                        type_query = 'UPDATE')

    def delete(self,
            where_cols,
            where_vals,
            cascade: bool = False,
            use_in: bool = False) -> int:

        if isinstance(where_cols, str):
            where_cols = [where_cols]
            where_vals = [where_vals]

        if len(where_cols) != len(where_vals):
            raise ValueError("Debe haber igual cantidad de campos y valores")

        # Eliminar la línea anterior de cascade porque no afecta al SQL estándar
        type_query = 'DELETE CASCADE' if cascade else 'DELETE'

        conditions = []
        params = []

        for col, val in zip(where_cols, where_vals):
            if val is None:
                continue  # No se incliuye la condición en el WHERE en si el parámetro es None
            
            if use_in and (isinstance(val, list) or isinstance(val, tuple)):
                placeholders = ','.join(['?'] * len(val))
                conditions.append(f"{col} IN ({placeholders})")
                params.extend(val)
                
            elif use_in and isinstance(val, str) and val.strip().upper().startswith("SELECT"):
                # Si es una subconsulta
                conditions.append(f"{col} IN ({val})")
                # No se agregan parámetros porque se asume que la subconsulta no tiene placeholders
            else:
                conditions.append(f"{col} = ?")
                params.append(val)

        where_clause = " AND ".join(conditions)
        sql = f"DELETE FROM {self.table} WHERE {where_clause}"

        return self.__execute_changes__(sql=sql,
                                        params=params,
                                        type_query=type_query)



    def case_string(self,
                    table : str,
                    when_then: dict,
                    when_vals : list,
                    then_vals : list = None,
                    elseClause: str = None,
                    max_case :bool = False,
                    alias : str = None ) -> str:
        """
        Genera una consulta CASE.

        Parámetros:
            - table: str------ Nombre de la tabla.
            - when_then: dict------ Diccionario con las claves 'when' y 'then' para la condición CASE.
            - cases: list------ Lista de casos a evaluar.
            - else_: str------ Valor ELSE opcional.
            - max_case: bool------ Si es True, agrega MAX a la cláusula CASE.
            - alias: str------ Alias opcional para el resultado de la cláusula CASE.
            
        Retorna:
            String de la parte CASE de la consulta.
        """
        case_clauses = []
        
        if then_vals:
            for when_val, then_val in zip(when_vals, then_vals):
                
                case_clause = f"\n WHEN {when_then['when']} = ? THEN  ?"

                    
                if max_case:
                    case_clause = f"MAX(CASE {case_clause}) AS '{when_val}'"
                    
                case_clauses.append(case_clause)
                            
            if elseClause:
                else_clause = f" ELSE '{elseClause}' END"
            else:
                else_clause = " END"
                        
            case_str =" ".join(case_clauses) + else_clause
                
        else:
            for when_val in when_vals:
                case_clause = f"WHEN {table}.{when_then["when"]} = '{when_val}' THEN {table}.{when_then["then"]}"
                
                if elseClause:
                    case_clause += f" ELSE '{elseClause}' END"
                else:
                    case_clause += " END"
                    
                if max_case:
                    case_clause = f"MAX(CASE {case_clause}) AS '{when_val}'"
                    
                case_clauses.append(case_clause)
        
            case_str =",\n".join(case_clauses)

            
        if alias:
            case_str += f" END AS {alias}"
            
        return case_str
    
    def subquery(self,
                 fields : list,
                 table  : str,
                 joins  : dict = None,
                 type_join: str = 'LEFT',
                 where  : dict = None,
                 limit  : int = None,
                 funct  : str = None) -> str:
        
        fields_clause = ", ".join(fields)
        fields_clause = f"{funct}({fields_clause})" if funct else fields_clause
        
        select_from = '(SELECT ' + fields_clause + f' FROM {table}'
        
        join_clauses = "".join(f" {type_join} JOIN {table} ON {condition}" for table, condition in joins.items()) if joins else ""
        
        where_clause = " WHERE " + " AND ".join([f"{col} = {vals}" for col, vals in where.items()]) if where else ""
        
        limit_clause = f' LIMIT {limit})' if limit else ')'

        return f"{select_from} {join_clauses} {where_clause} {limit_clause}"

    def format_coalesce(self, field):
        if isinstance(field, dict):
            # Solo toma el primer par clave-valor
            key, val = next(iter(field.items()))
            
            return f"COALESCE({", ".join(val)}, 'ninguno') AS {key}"
        return field














"""bd = Crud('base_de_datos', 'TABLA_PRINCIPAL')

print(bd.subquery(fields=['PROCESOS.NOMBRE'],
                  table='HISTORICOS',
                  joins={'PROCESOS': 'HISTORICOS.ID_PROCESO = PROCESOS.ID'},
                  where={
                         'HISTORICOS.CHASIS': 'VEHICULOS.CHASIS',
                         'HISTORICOS.ESTADO': "'TERMINADO'",
                         'HISTORICOS.FIN':   bd.subquery(fields= ['HISTORICOS.FIN'],
                                                        table  = 'HISTORICOS',
                                                        where  = {
                                                                  'HISTORICOS.CHASIS': 'VEHICULOS.CHASIS',
                                                                  'HISTORICOS.ESTADO': "'TERMINADO'",
                                                                },
                                                        funct  = 'MAX')
                         },
                  limit=1
                  )
      )"""


"""ejemple = Crud('base_de_datos', 'TABLA_PRINCIPAL')

print(ejemple.case_string(
    table = 'TIEMPOS_MODELOS',
    when_then = {'when': 'ID_PROCESO',
                 'then': 'TIEMPOS'},
    when_vals = ['LAV', 'PDI', 'PIN', 'COD'],
    max_case = True
))"""



"""
crud = Crud('base_de_datos','TABLA_PRINCIPAL')
resultados = crud.select_join(
    fields=['vehiculos.id', 'modelos.nombre', 'especificaciones.detalle'],
    joins= {'modelos': 'vehiculos.id_modelo = modelos.id',
            'especificaciones': 'vehiculos.id_especificacion = especificaciones.id'},
    where={
        'modelos.nombre': 'TOANO',
        'vehiculos.estado': 'ACTIVO'
    },
    order_by='vehiculos.id',
    type_join='RIGHT',
    distinct=True
)
"""