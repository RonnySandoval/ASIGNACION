from . import BDmanage as man


class HistoricosCrud(man.Crud):
    def __init__(self, db: man.Database):
        super().__init__(db, table_name = "HISTORICOS")
        self.fields = ['CODIGO_ASIGNACION',
                       'CHASIS',
                       'ID_TECNICO',
                       'ID_PROCESO',
                       'OBSERVACIONES',
                       'INICIO',
                       'FIN',
                       'DURACION',
                       'ESTADO']
    
    def leer_historicos(self):
        return self.select(fields = '''
                           CODIGO_ASIGNACION,
                           CHASIS,
                           ID_TECNICO,
                           ID_PROCESO,
                           OBSERVACIONES,
                           INICIO,
                           FIN,
                           DURACION,
                           ESTADO''')
    
    def leer_historico_chasis(self, chasis):
        return self.select(where={'CHASIS': chasis},
                           fields = '''
                           CODIGO_ASIGNACION,
                           CHASIS,
                           ID_TECNICO,
                           ID_PROCESO,
                           OBSERVACIONES,
                           INICIO,
                           FIN,
                           DURACION,
                           ESTADO''')

    def leer_historicos_completo(self):
        return self.select(fields=[
                                    'HISTORICOS.CODIGO_ASIGNACION',
                                    'HISTORICOS.CHASIS',
                                    'TECNICOS.NOMBRE AS NOMBRE_PROCESO',
                                    'PROCESOS.NOMBRE AS NOMBRE_PROCESO',
                                    'VEHICULOS.ID_MODELO',
                                    'VEHICULOS.COLOR',
                                    'HISTORICOS.INICIO',
                                    'HISTORICOS.FIN',
                                    'HISTORICOS.DURACION',
                                    'HISTORICOS.ESTADO',
                                    'VEHICULOS.NOVEDADES',
                                    'HISTORICOS.OBSERVACIONES',
                                    'VEHICULOS.SUBCONTRATAR',
                                    'VEHICULOS.ID_PEDIDO'
                                ],
                            joins={
                                    'PROCESOS': 'HISTORICOS.ID_PROCESO = PROCESOS.ID_PROCESO',
                                    'TECNICOS': 'HISTORICOS.ID_TECNICO = TECNICOS.ID_TECNICO',
                                    'VEHICULOS': 'HISTORICOS.CHASIS = VEHICULOS.CHASIS'
                                },
                                distinct=True)

    def leer_historico_completo(self, chasis):
        return self.select(fields=[
                                    'HISTORICOS.CODIGO_ASIGNACION',
                                    'HISTORICOS.CHASIS',
                                    'TECNICOS.NOMBRE || ' ' || TECNICOS.APELLIDO AS NOMBRE_COMPLETO',
                                    'PROCESOS.NOMBRE',
                                    'VEHICULOS.ID_MODELO',
                                    'VEHICULOS.COLOR',
                                    'HISTORICOS.INICIO',
                                    'HISTORICOS.FIN',
                                    'HISTORICOS.DURACION',
                                    'HISTORICOS.ESTADO',
                                    'VEHICULOS.NOVEDADES',
                                    'HISTORICOS.OBSERVACIONES',
                                    'VEHICULOS.SUBCONTRATAR',
                                    'VEHICULOS.ID_PEDIDO'
                                ],
                            joins={
                                    'PROCESOS': 'HISTORICOS.ID_PROCESO = PROCESOS.ID_PROCESO',
                                    'TECNICOS': 'HISTORICOS.ID_TECNICO = TECNICOS.ID_TECNICO',
                                    'VEHICULOS': 'HISTORICOS.CHASIS = VEHICULOS.CHASIS'
                                },
                            where={
                                    'HISTORICOS.CHASIS': chasis
                                })

    def leer_historico_completo_porId(self, id):
        return self.select(fields=[
                            'HISTORICOS.CODIGO_ASIGNACION',
                            'HISTORICOS.CHASIS',
                            'TECNICOS.NOMBRE || ' ' || TECNICOS.APELLIDO AS NOMBRE_COMPLETO',
                            'PROCESOS.NOMBRE',
                            'VEHICULOS.ID_MODELO',
                            'VEHICULOS.COLOR',
                            'HISTORICOS.INICIO',
                            'HISTORICOS.FIN',
                            'HISTORICOS.DURACION',
                            'HISTORICOS.ESTADO',
                            'VEHICULOS.NOVEDADES',
                            'HISTORICOS.OBSERVACIONES',
                            'VEHICULOS.SUBCONTRATAR',
                            'VEHICULOS.ID_PEDIDO'
                        ],
                        joins={
                            'PROCESOS': 'HISTORICOS.ID_PROCESO = PROCESOS.ID_PROCESO',
                            'TECNICOS': 'HISTORICOS.ID_TECNICO = TECNICOS.ID_TECNICO',
                            'VEHICULOS': 'HISTORICOS.CHASIS = VEHICULOS.CHASIS'
                        },
                        where={'HISTORICOS.CODIGO_ASIGNACION': id})

    def leer_historicos_graficar(self):
        return self.select(fields=[
                            'HISTORICOS.CODIGO_ASIGNACION',
                            'HISTORICOS.CHASIS',
                            'VEHICULOS.ID_MODELO',
                            'VEHICULOS.REFERENCIA',
                            'VEHICULOS.COLOR',
                            'HISTORICOS.ID_TECNICO',
                            'TECNICOS.NOMBRE || TECNICOS.APELLIDO AS TECNICO',
                            'HISTORICOS.ID_PROCESO',
                            'PROCESOS.NOMBRE AS PROCESO',
                            'HISTORICOS.INICIO',
                            'HISTORICOS.FIN',
                            'HISTORICOS.DURACION',
                            'HISTORICOS.OBSERVACIONES',
                            'VEHICULOS.NOVEDADES',
                            'VEHICULOS.SUBCONTRATAR',
                            'VEHICULOS.ID_PEDIDO',
                            'PEDIDOS.CLIENTE',
                            'PEDIDOS.FECHA_RECEPCION',
                            'PEDIDOS.FECHA_INGRESO',
                            'PEDIDOS.ENTREGA_ESTIMADA',
                            'PEDIDOS.FECHA_ENTREGA'
                        ],
                        joins={
                            'VEHICULOS': 'VEHICULOS.CHASIS = HISTORICOS.CHASIS',
                            'TECNICOS': 'TECNICOS.ID_TECNICO = HISTORICOS.ID_TECNICO',
                            'PROCESOS': 'PROCESOS.ID_PROCESO = HISTORICOS.ID_PROCESO',
                            'PEDIDOS': 'PEDIDOS.ID_PEDIDO = VEHICULOS.ID_PEDIDO'
                        })
                        
    def insertar_historico(self, codigo, chasis, tec, proc, observ, start, end, delta, estado):
        return self.insert(columns=self.fields,
                           vals = [codigo, chasis, tec, proc, observ, start, end, delta, estado])
    
    def insertar_historicos_df(self, dataframe):
        return self.insert_dataframe(dataframe=dataframe)
    
    def actualizar_historico_estado(self, id, estado):
        return self.update(columns   = ['ESTADO',],
                           vals      = [estado,],
                           where_col = 'CODIGO_ASIGNACION',
                           params = id)

    def eliminar_historico(self, id_historico):
        return self.delete(where_cols = 'CODIGO_ASIGNACION',
                           where_vals = id_historico)

class InformacionCrud(man.Crud):
    def __init__(self, db: man.Database):
        super().__init__(db, table_name = "INFORMACION")
        self.fields = ['NOMBRE_PLANTA',
                       'DESCRIPCION',
                       'INICIA_AM',
                       'TERMIMNA_AM',
                       'INICIA_PM',
                       'TERMINA_PM']

    def leer_planta_info(self):
        return self.select()

    def insert_info_planta(self, nombre, descripcion, iniciaAM, terminaAM, iniciaPM, terminaPM):
        return self.insert(columns=self.fields,
                           vals= [nombre, descripcion, iniciaAM, terminaAM, iniciaPM, terminaPM])

    def actualizar_planta_info(self, nombre, descripcion, iniciaAM, terminaAM, iniciaPm, terminaPM):
        return self.update(columns=self.fields,
                           vals = [nombre, descripcion, iniciaAM, terminaAM, iniciaPm, terminaPM],
                           where_col='NOMBRE_PLANTA',
                           params=nombre)        #OJO! Error.. No hay un parámetro que indique el valor del WHERE, se asume que "nombre" no se cambió

class ModelosCrud(man.Crud):
    def __init__(self, db: man.Database):
        super().__init__(db, table_name = "MODELOS")
        self.fields = ['ID_MODELO', 'MARCA', 'MODELO', 'ESPECIFICACION']
        
    def leer_modelo(self, id_modelo):
        return self.select(where = {"ID_MODELO": id_modelo},
                    fetch  = "one", 
                    fields = 'ID_MODELO, MARCA, MODELO, ESPECIFICACION')
    
    def leer_modelos(self):
        return self.select(fields = 'ID_MODELO, MARCA, MODELO, ESPECIFICACION')
    
    def leer_modelos_marcas(self):
        return self.select(fields = 'ID_MODELO, MARCA')

    def leer_modelos_marcas_df(self):
        return self.select(fields= 'ID_MODELO, MARCA', as_dataframe=True)

    def leer_modelos_id_modelos_df(self):
        return self.select(fields= ' MODELO, ID_MODELO', as_dataframe=True)

    def leer_tiempos_modelos_df(self):
        
        tm_crud = TiemposModelosCrud(self.db)
        id_procesos =  tm_crud.obtener_ids_procesos()
        
        str_max_case = self.case_string(table = 'TIEMPOS_MODELOS',
                                        when_then= {'when':'ID_PROCESO',   'then':'TIEMPO'},
                                        when_vals = id_procesos,
                                        max_case=True)
        
        return self.select(fields    =['MODELOS.ID_MODELO',],
                            joins    ={'TIEMPOS_MODELOS'  : 'MODELOS.ID_MODELO             = TIEMPOS_MODELOS.ID_MODELO',
                                        'PROCESOS'          : 'TIEMPOS_MODELOS.ID_PROCESO = PROCESOS.ID_PROCESO'},
                            cases    = str_max_case,
                            group_by ='MODELOS.ID_MODELO',
                            order_by ='PROCESOS.SECUENCIA',
                            as_dataframe=True)

    def obtener_id_modelo(self, modelo):
        return self.select(fields= 'ID_MODELO',
                           distinct=True,
                           where={'MODELO': modelo},
                           fetch='one')

    def insertar_modelo(self, id, marca, modelo):
        return self.insert( columns =['ID_MODELO', 'MARCA', 'MODELO'],
                            vals   = [  id,         marca,    modelo])

    def insertar_modelos_df(self, dataframe):
        return self.insert_dataframe(dataframe=dataframe)

    def actualizar_modelo(self, id_anterior, marca, modelo, id_nuevo):
        return self.update(columns=['ID_MODELO', 'MARCA', 'MODELO'],
                           vals=[id_nuevo, marca, modelo],
                           where_col='ID_MODELO',
                           params=id_anterior)

    def eliminar_modelo(self, modelo):
        return self.delete(where_col='MODELO', where_val = modelo)

    def eliminar_modelo_completo(self, modelo):
        crud_TieMod = TiemposModelosCrud(self.db)
        
        crud_TieMod.eliminar_tiempo_modelo(modelo=modelo)
        self.eliminar_modelo(modelo=modelo)
    
class OrdenesCrud(man.Crud):
    def __init__(self, db: man.Database):
        super().__init__(db, table_name = "ORDENES")
        self.fields = ['CODIGO_ORDEN',
                       'ID_PROGRAMA',
                       'CHASIS',
                       'ID_TECNICO',
                       'ID_PROCESO',
                       'OBSERVACIONES',
                       'INICIO',
                       'FIN',
                       'DURACION',
                       'TIEMPO_PRODUCTIVO']
    
    def leer_orden(self, codigo):
        return self.select(where={'CODIGO_ORDEN': codigo})
    
    def leer_ordenes_completo(self):
        return self.select(fields=[
                                'ORDENES.CODIGO_ORDEN',
                                'ORDENES.CHASIS',
                                'ORDENES.INICIO',
                                'ORDENES.FIN',
                                'ORDENES.DURACION',
                                'ORDENES.TIEMPO_PRODUCTIVO',
                                'PROCESOS.NOMBRE',
                                'ORDENES.OBSERVACIONES',
                                'VEHICULOS.ID_MODELO',
                                'VEHICULOS.COLOR',
                                "TECNICOS.NOMBRE || ' ' || TECNICOS.APELLIDO AS TECNICO"
                            ],
                            joins={
                                'VEHICULOS': 'VEHICULOS.CHASIS = ORDENES.CHASIS',
                                'TECNICOS': 'TECNICOS.ID_TECNICO = ORDENES.ID_TECNICO',
                                'PROGRAMAS': 'PROGRAMAS.ID_PROGRAMA = ORDENES.ID_PROGRAMA',
                                'PROCESOS': 'PROCESOS.ID_PROCESO = ORDENES.ID_PROCESO'
                            })

    def leer_orden_completo_porId(self, codigo_orden):
        return self.select( fields=[
                                'ORDENES.CODIGO_ORDEN',
                                'ORDENES.CHASIS',
                                'VEHICULOS.ID_MODELO',
                                'VEHICULOS.COLOR',
                                "TECNICOS.NOMBRE || ' ' || TECNICOS.APELLIDO AS TECNICO",
                                'PROCESOS.NOMBRE',
                                'ORDENES.INICIO',
                                'ORDENES.FIN',
                                'ORDENES.DURACION',
                                'ORDENES.TIEMPO_PRODUCTIVO',
                                'ORDENES.ID_PROGRAMA',
                                'VEHICULOS.NOVEDADES',
                                'VEHICULOS.SUBCONTRATAR',
                                'ORDENES.OBSERVACIONES',
                                'VEHICULOS.ID_PEDIDO'
                            ],
                            joins={
                                'VEHICULOS': 'VEHICULOS.CHASIS = ORDENES.CHASIS',
                                'TECNICOS': 'TECNICOS.ID_TECNICO = ORDENES.ID_TECNICO',
                                'PROCESOS': 'PROCESOS.ID_PROCESO = ORDENES.ID_PROCESO'
                            },
                            where={'ORDENES.CODIGO_ORDEN': codigo_orden})
    
    def leer_ordenes_por_programa(self, programa):
        return self.select(fields=[
                                'ORDENES.CODIGO_ORDEN',
                                'ORDENES.CHASIS',
                                'ORDENES.INICIO',
                                'ORDENES.FIN',
                                'ORDENES.DURACION',
                                'ORDENES.TIEMPO_PRODUCTIVO',
                                'PROCESOS.NOMBRE',
                                'ORDENES.OBSERVACIONES',
                                'VEHICULOS.ID_MODELO',
                                'VEHICULOS.COLOR',
                                'TECNICOS.NOMBRE || TECNICOS.APELLIDO AS TECNICO'
                            ],
                            joins={
                                'VEHICULOS': 'VEHICULOS.CHASIS = ORDENES.CHASIS',
                                'TECNICOS': 'TECNICOS.ID_TECNICO = ORDENES.ID_TECNICO',
                                'PROGRAMAS': 'PROGRAMAS.ID_PROGRAMA = ORDENES.ID_PROGRAMA',
                                'PROCESOS': 'PROCESOS.ID_PROCESO = ORDENES.ID_PROCESO'
                            },
                            where={'PROGRAMAS.ID_PROGRAMA': programa})

    def leer_ordenes_graficar_programa(self, programa):
        return self.select(fields=[
                                'ORDENES.CODIGO_ORDEN',
                                'ORDENES.CHASIS',
                                'VEHICULOS.ID_MODELO',
                                'VEHICULOS.REFERENCIA',
                                'VEHICULOS.COLOR',
                                'ORDENES.ID_TECNICO',
                                "TECNICOS.NOMBRE || ' ' || TECNICOS.APELLIDO AS TECNICO",
                                'ORDENES.ID_PROCESO',
                                'PROCESOS.NOMBRE AS PROCESO',
                                'ORDENES.INICIO',
                                'ORDENES.FIN',
                                'ORDENES.DURACION',
                                'ORDENES.TIEMPO_PRODUCTIVO',
                                'ORDENES.OBSERVACIONES',
                                'VEHICULOS.NOVEDADES',
                                'VEHICULOS.SUBCONTRATAR',
                                'VEHICULOS.ID_PEDIDO',
                                'PEDIDOS.CLIENTE',
                                'PEDIDOS.FECHA_RECEPCION',
                                'PEDIDOS.FECHA_INGRESO',
                                'PEDIDOS.ENTREGA_ESTIMADA',
                                'PEDIDOS.FECHA_ENTREGA',
                                'ORDENES.ID_PROGRAMA'
                            ],
                            joins={
                                'VEHICULOS': 'VEHICULOS.CHASIS = ORDENES.CHASIS',
                                'TECNICOS': 'TECNICOS.ID_TECNICO = ORDENES.ID_TECNICO',
                                'PROGRAMAS': 'PROGRAMAS.ID_PROGRAMA = ORDENES.ID_PROGRAMA',
                                'PROCESOS': 'PROCESOS.ID_PROCESO = ORDENES.ID_PROCESO',
                                'PEDIDOS': 'PEDIDOS.ID_PEDIDO = PROGRAMAS.ID_PEDIDO'
                            },
                            where={'PROGRAMAS.ID_PROGRAMA': programa})

    def insertar_ordenes_df(self, dataframe):
        return self.insert_dataframe(dataframe=dataframe)

    def actualizar_orden(self, id_programa_anterior, id_programa_nuevo):
        return self.update(columns   = ['ID_PROGRAMA',],
                           vals      = [id_programa_nuevo,],
                           where_col = 'ID_PROGRAMA',
                           params = id_programa_anterior)

    def eliminar_orden(self, id_orden):
        return self.delete(where_cols='CODIGO_ORDEN', where_vals=id_orden)
    
    def eliminar_ordenes_por_programa(self, id_programa):
        return self.delete(where_cols='ID_PROGRAMA', where_vals=id_programa)

class PedidosCrud(man.Crud):
    def __init__(self, db: man.Database):
        super().__init__(db, table_name = "PEDIDOS")
        self.fields = ['ID_PEDIDO', 'CLIENTE', 'FECHA_RECEPCION', 'FECHA_INGRESO', 'ENTREGA_ESTIMADA', 'FECHA_ENTREGA','CONSECUTIVO']

    def leer_pedido(self, id_pedido):
        return self.select(where={"ID": id_pedido},
                    fetch="one", 
                    fields='''
                            ID_PEDIDO,
                            CLIENTE, 
                            FECHA_RECEPCION, 
                            FECHA_INGRESO, 
                            ENTREGA_ESTIMADA, 
                            FECHA_ENTREGA,
                            CONSECUTIVO
                            ''')

    def leer_pedidos(self):
        return self.select(fields='''
                                ID_PEDIDO,
                                CLIENTE, 
                                FECHA_RECEPCION, 
                                FECHA_INGRESO, 
                                ENTREGA_ESTIMADA, 
                                FECHA_ENTREGA,
                                CONSECUTIVO
                                ''')
    
    def leer_pedidos_df(self):
        return self.select(as_dataframe=True)

    def next_consecutivoPedido(self):
        consecutivo = self.select(fields=['MAX(CONSECUTIVO)'],
                           fetch='one')
        if consecutivo is None:
            return 1
        else:
            return consecutivo[0] + 1

    def insertar_pedido(self, id_pedido, cliente, fecha_recepcion, fecha_ingreso, fecha_estimada, fecha_entrega, consecutivo):
        return self.insert( columns=self.fields,
                            vals=[id_pedido,
                                     cliente,
                                     fecha_recepcion,
                                     fecha_ingreso,
                                     fecha_estimada,
                                     fecha_entrega,
                                     consecutivo])
    
    def actualizar_pedido(self, id_nuevo, cliente, fecha_recepcion, fecha_ingreso, fecha_estimada, fecha_entrega, consecutivo, id_anterior):
        return self.update( columns=self.fields,
                            vals=[id_nuevo, cliente, fecha_recepcion, fecha_ingreso, fecha_estimada, fecha_entrega, consecutivo],
                            where_col='ID_PEDIDO',
                            params=id_anterior)
    
    def eliminar_pedido(self, id_pedido):
        return self.delete(where_col='ID_PEDIDO',  where_val=id_pedido)

    def elminar_pedido_cascada(self, id_pedido):
        try:
            crud_Veh = VehiculosCrud(self.db)
            crud_TiV = TiemposVehiculosCrud(self.db)
            crud_Pro = PedidosCrud(self.db)
            crud_Ord = OrdenesCrud(self.db)
            
            subquery_vehiculos = crud_Veh.subquery(fields= ['CHASIS'],     table= crud_Veh.table, where={'ID_PEDIDO': id_pedido})
            subquery_programas = crud_Pro.subquery(fields=['ID_PROGRAMA'], table= crud_Pro.table, where={'ID_PEDIDO': id_pedido})
            
            delRow_pedidos   = self.delete    (where_cols='ID_PEDIDO',   where_vals = id_pedido,          cascade=True)
            delRow_vehiculos = crud_Veh.delete(where_cols='ID_PEDIDO',   where_vals = id_pedido,          cascade=True)
            delRow_tiempos   = crud_TiV.delete(where_cols='CHASIS',      where_vals = subquery_vehiculos, cascade=True, use_in=True)
            delRow_programas = crud_Pro.delete(where_cols='ID_PEDIDO',   where_vals = id_pedido,          cascade=True)
            delRow_ordenes   = crud_Ord.delete(where_cols='ID_PROGRAMA', where_vals = subquery_programas, cascade=True, use_in=True)
            
            
            request = (delRow_pedidos, delRow_vehiculos, delRow_tiempos, delRow_programas, delRow_ordenes)
            diccrequest = { 'pedidos'   : delRow_pedidos, 
                            'vehiculos' : delRow_vehiculos,
                            'tiempos'   : delRow_tiempos,
                            'programas' : delRow_programas, 
                            'ordenes'   : delRow_ordenes}
            
            print('query cascade: ', request)
                            
        except Exception as e:
            print(f"Error al eliminar el pedido en cascada: {e}")
            self.db.rollback()
            return e, None
    
    
        # Evaluar condiciones con match-case       (LAS CONDICIONES REPRESENTAN LA OCURRENCIA DE UNA TRANSACCIÓN INCORRECTA)
        incorrecta = False
        match request:
            # Condición 0: No se eliminó nada
            case (0, 0, 0, 0, 0):                             
                print("no hay ningún registro para el eliminar.")
                self.db.commit()  # Confirmar cambios si todo está correcto
                return diccrequest, incorrecta
            
            # Condición 1: Si no se eliminaron pedidos, tampoco deben eliminarse vehiculos, ni tiempos, ni programas, ni ordenes
            case (0, _, _, _, _) if (delRow_vehiculos != 0 or delRow_tiempos != 0 or delRow_programas != 0 or delRow_ordenes != 0):
                print("Error: Si no se eliminan pedidos, no pueden eliminarse vehículos, tiempos, programas ni órdenes. Cancelando.")
                self.db.rollback()  # Revertir cambios
                incorrecta = True
                return diccrequest, incorrecta
            
            # Condición 2: Si se eliminan pedidos, deben también vehículos y tiempos
            case (_, _, _, _, _) if delRow_pedidos != 0 and (delRow_vehiculos == 0 or delRow_tiempos == 0):
                print("Error: Si se eliminan pedidos, también deben eliminarse vehículos y tiempos. Cancelando.")
                self.db.rollback()  # Revertir cambios
                incorrecta = True
                return diccrequest, incorrecta
            
            # Condición 3: Si no se eliminan programas, no deben eliminarse órdenes
            case (_, _, _, 0, _) if delRow_ordenes != 0:                             
                print("Error: Si no se eliminan programas, no deben eliminarse órdenes. Cancelando.")
                self.db.rollback()  # Revertir cambios
                incorrecta = True
                return diccrequest, incorrecta
            
            # Condición 4: Si se eliminan programas, también deben eliminarse órdenes
            case (_, _, _, _, _) if (delRow_programas != 0 and delRow_ordenes == 0):    
                print("Error: Si se eliminan programas, también deben eliminarse órdenes. Cancelando.")
                self.db.rollback()  # Revertir cambios
                incorrecta = True
                return diccrequest, incorrecta

            # Condición 5: Si no se eliminan vehículos, tampoco deben eliminarse tiempos
            case (_, 0, _, _, _) if delRow_tiempos != 0:                             
                print("Error: Si no se eliminan vehículos, no deben eliminarse tiempos. Cancelando.")
                self.db.rollback()  # Revertir cambios
                incorrecta = True
                return diccrequest, incorrecta

            # Condición 6: Si se eliminan vehículos, también deben eliminarse tiempos
            case (_, _, _, _, _) if (delRow_vehiculos != 0 and delRow_tiempos == 0):    
                print("Error: Si se eliminan vehículos, también deben eliminarse tiempos. Cancelando.")
                self.db.rollback()  # Revertir cambios
                incorrecta = True
                return diccrequest, incorrecta

            # Si ninguna condicion de error se cumple, se confirma la transacción
            case _:                                 
                print("Eliminación completada correctamente.")
                self.db.commit()  # Confirmar cambios si todo está correcto
                return diccrequest, incorrecta

class ProcesosCrud(man.Crud):
    def __init__(self, db: man.Database):
        super().__init__(db, table_name = "PROCESOS")
        self.fields = [ 'ID_PROCESO', 'NOMBRE', 'DESCRIPCION','SECUENCIA']

    def leer_procesos_nombres(self):
        return self.select(fields='NOMBRE', order_by='SECUENCIA')

    def leer_procesos_completo(self):
        return self.select(fields=['ID_PROCESO', 'NOMBRE', 'DESCRIPCION', 'SECUENCIA'])

    def leer_procesos_secuencia(self):
        return self.select(fields=['NOMBRE'], order_by= 'SECUENCIA')
        
    def leer_procesos_df(self):
        return self.select(as_dataframe=True)

    def obtener_id_procesos_secuencia(self):
        return self.select(fields=['ID_PROCESO'],
                           order_by='SECUENCIA')
 
    def insertar_proceso(self, id, proceso, descripcion, secuencia):
        return self.insert(columns=self.fields,
                            vals=[id, proceso, descripcion, secuencia])

    def insertar_procesos_df(self, dataframe):
        return self.insert_dataframe(dataframe=dataframe)
    
    def actualizar_proceso(self, id_proceso, nombre, descripcion, secuencia, id_proceso_anterior):
        return self.update(columns=self.fields,
                           vals=[id_proceso, nombre, descripcion, secuencia],
                           where_col='ID_PROCESO',
                           params=id_proceso_anterior)
    
    def eliminar_proceso(self, id):
        return self.delete(where_col='ID_PROCESO', where_val = id)

    def eliminar_proceso_completo(self, id_proceso):
        crud_TecProc = TecnicosProcesosCrud(self.db)
        crud_TieMod = TiemposModelosCrud(self.db)
        
        self.eliminar_proceso(id_proceso)
        crud_TecProc.eliminar_tecnico_proceso_byProceso(id_proceso)
        crud_TieMod.eliminar_tiempo_modelo_byProceso(id_proceso)
        
class ProgramasCrud(man.Crud):
    def __init__(self, db: man.Database):
        super().__init__(db, table_name = "PROGRAMAS")
        self.fields = [ 'ID_PROGRAMA',
                        'ID_PEDIDO',
                        'DESCRIPCION',
                        'CONSECUTIVO',
                        'INICIA_AM',
                        'TERMINA_AM',
                        'INICIA_PM',
                        'TERMINA_PM']
        
    def leer_programa(self, id_programa):
        return self.select(where={"ID": id_programa},
                    fetch="one", 
                    fields='''
                            ID_PROGRAMA,
                            ID_PEDIDO,
                            DESCRIPCION,
                            CONSECUTIVO,
                            INICIA_AM,
                            TERMINA_AM,
                            INICIA_PM,
                            TERMINA_PM
                            ''')
        
    def leer_programas(self):
        return self.select(fields='''
                            ID_PROGRAMA,
                            ID_PEDIDO,
                            DESCRIPCION,
                            CONSECUTIVO
                            ''')

    def leer_programas_por_pedido(self, id_pedido):
        return self.select(where = {'ID_PEDIDO': id_pedido},
                           fields = ''' ID_PROGRAMA,
                                        ID_PEDIDO,
                                        DESCRIPCION,
                                        CONSECUTIVO''')

    def leer_turnos_programa(self, programa):
        return self.select(fields = ''' INICIA_AM,
                                        TERMINA_AM,
                                        INICIA_PM,
                                        TERMINA_PM''',
                            where = {'ID_PROGRAMA': programa},
                            fetch = 'one')

    def next_consecutivoPrograma(self):
        consecutivo = self.select(fields=['MAX(CONSECUTIVO)'],
                           fetch='one')
        if consecutivo is None:
            return 1
        else:
            return consecutivo[0] + 1
        
    def insertar_programa(self, nombrePrograma, descripcion, consecutivo, pedido, startAM, endAM, startPM, endPM):
        return self.insert(
                            columns=self.fields,
                            vals=[nombrePrograma,
                                     pedido,
                                     descripcion,
                                     consecutivo,
                                     startAM,
                                     endAM,
                                     startPM,
                                     endPM]
        )
    
    def actualizar_programa(self, id_programa, descripcion, consecutivo, id_pedido, id_programa_anterior):
        return self.update( columns =[ 'ID_PROGRAMA', 'DESCRIPCION',  'CONSECUTIVO', 'ID_PEDIDO'],
                            vals    =[ id_programa,    descripcion,    consecutivo,   id_pedido],
                            where_col='ID_PROGRAMA',
                            params=id_programa_anterior)

    def actualizar_programas_pedido(self, id_pedido, id_pedido_anterior):
        return self.update( columns =['ID_PEDIDO',],
                            vals  =[id_pedido,],
                            where_col='ID_PEDIDO',
                            params=id_pedido_anterior
        )

    def eliminar_programa(self, id_programa):
        return self.delete(where_col='ID_PROGRAMA',  where_val=id_programa)

class ReferenciasCrud(man.Crud):
    def __init__(self, db: man.Database):
        super().__init__(db, table_name = "MODELOS_REFERENCIAS")
        self.fields = ['REFERENCIA', 'ID_MODELO']

    def leer_referencias_modelos_df(self):
        return self.select(as_dataframe=True)

    def insertar_referencia(self, referencia , id_modelo):
        return self.insert(columns = self.fields,
                            vals   = [referencia , id_modelo])

    def insertar_referencias_df(self, dataframe):
        return self.insert_dataframe(dataframe=dataframe)
    
    def actualizar_referencia(self, referencia_nueva, id_modelo, referencia_anterior):
        return self.update(columns = self.fields,
                           vals = [referencia_nueva, id_modelo],
                           where_col = 'REFERENCIA',
                           params = id_modelo)
        
    def eliminar_referencia(self, referencia):
        return self.delete(where_col='REFERENCIA', where_val = referencia)

class TecnicosCrud(man.Crud):
    def __init__(self, db: man.Database):
        super().__init__(db, table_name = "TECNICOS")
        self.fields = ['ID_TECNICO', 'NOMBRE', 'APELLIDO', 'DOCUMENTO','ESPECIALIDAD']

    def leer_tecnicos(self):
        return self.select(fields = [
                                    'TECNICOS.ID_TECNICO',
                                    'TECNICOS.NOMBRE',
                                    'TECNICOS.APELLIDO',
                                    'TECNICOS.DOCUMENTO',
                                    'PROCESOS.NOMBRE'
                                    ],
                            joins={
                                    'TECNICOS_PROCESOS': 'TECNICOS_PROCESOS.ID_TECNICO = TECNICOS.ID_TECNICO',
                                    'PROCESOS': 'TECNICOS_PROCESOS.ID_PROCESO = PROCESOS.ID_PROCESO'
                                    },
                    
                            order_by= 'PROCESOS.SECUENCIA')

    def leer_tecnicos_df(self):
        return self.select(fields=[
                                'TECNICOS.ID_TECNICO',
                                'TECNICOS.NOMBRE',
                                'TECNICOS.APELLIDO',
                                'TECNICOS.DOCUMENTO',
                                'PROCESOS.NOMBRE'
                            ],
                            joins={
                                'TECNICOS_PROCESOS': 'TECNICOS_PROCESOS.ID_TECNICO = TECNICOS.ID_TECNICO',
                                'PROCESOS': 'TECNICOS_PROCESOS.ID_PROCESO = PROCESOS.ID_PROCESO'
                            },
                            order_by='PROCESOS.SECUENCIA',
                            as_dataframe=True)

    def leer_tecnicos_modificado(self):
        return self.select(fields=self.fields,
                            joins={
                                'TECNICOS_PROCESOS': 'TECNICOS_PROCESOS.ID_TECNICO = TECNICOS.ID_TECNICO',
                                'PROCESOS':          'TECNICOS_PROCESOS.ID_PROCESO = PROCESOS.ID_PROCESO'
                            },
                            order_by='PROCESOS.SECUENCIA')

    def leer_tecnicos_por_proceso(self, id_proceso):
        return self.select(fields=self.fields,
                            joins={
                                'TECNICOS_PROCESOS': 'TECNICOS_PROCESOS.ID_TECNICO = TECNICOS.ID_TECNICO',
                                'PROCESOS':          'TECNICOS_PROCESOS.ID_PROCESO = PROCESOS.ID_PROCESO'
                            },
                            where={'TECNICOS_PROCESOS.ID_PROCESO': id_proceso},
                            order_by='PROCESOS.SECUENCIA')
    
    def insertar_tecnico(self, id, nombre, apellido, documento, especialidad):
        return self.insert(columns = ['ID_TECNICO', 'NOMBRE', 'APELLIDO', 'DOCUMENTO','ESPECIALIDAD'],
                           vals    = [  id,          nombre,   apellido,   documento,  especialidad])

    def insert_tecnico_df(self, dataframe):
        return self.insert_dataframe(dataframe = dataframe)
    
    def actualizar_tecnico(self, id_tecnico, nombre, apellido, documento, especialidad, id_tecnico_anterior):
        return self.update(columns  = ['ID_TECNICO', 'NOMBRE', 'APELLIDO', 'DOCUMENTO','ESPECIALIDAD'],
                           vals     = [id_tecnico,    nombre,   apellido,   documento,  especialidad],
                           where_col='ID_TECNICO',
                           params=id_tecnico_anterior)
    
    def eliminar_tecnico(self, id_tecnico):
        return self.delete(where_col='ID_TECNICO', where_val=id_tecnico)

    def eliminar_tecnico_completo(self, id_tecnico):
        crud_TecPro = TecnicosProcesosCrud(self.db)
        crud_TecPro.eliminar_tecnico_proceso(id_tecnico = id_tecnico,
                                             id_proceso = None)
        self.eliminar_tecnico(id_tecnico=id_tecnico)
    
class TecnicosProcesosCrud(man.Crud):
    def __init__(self, db: man.Database):
        super().__init__(db, table_name = "TECNICOS_PROCESOS")
        self.fields = ['TEC_PROC', 'ID_TECNICO', 'ID_PROCESO']

    def leer_tecnicos_procesos_df(self):
        return self.select( fields=[
                                'TECNICOS_PROCESOS.TEC_PROC',
                                'TECNICOS_PROCESOS.ID_TECNICO',
                                'TECNICOS_PROCESOS.ID_PROCESO'
                            ],
                            joins    = {'PROCESOS': 'PROCESOS.ID_PROCESO = TECNICOS_PROCESOS.ID_PROCESO'},
                            order_by = 'PROCESOS.SECUENCIA',
                            as_dataframe=True)

    def insertar_tecnico_proceso(self, proc_tec, id_tecnico, id_proceso):
        return self.insert(columns = ['TEC_PROC', 'ID_TECNICO', 'ID_PROCESO'],
                           vals    = [  proc_tec, id_tecnico, id_proceso])
        
    def insert_tecnicos_procesos_df(self, dataframe):
        return self.insert_dataframe(dataframe=dataframe)

    def actualizar_tecnicos_proceso_many(self, ids_anteriores, ids_nuevos, id_proceso_nuevo):
        
        params = []
        for when_val, then_val in zip(ids_anteriores, ids_nuevos):
            params.extend([when_val, then_val])
        params.append(id_proceso_nuevo)
        params.extend(ids_anteriores)
        
        case_string = self.case_string( table      = self.table,
                                        when_then  = {'when': 'TEC_PROC', 'then': 'TEC_PROC'},
                                        when_vals  = ids_anteriores,
                                        then_vals  = ids_nuevos,
                                        elseClause = 'TEC_PROC')
        
        print(f"Case String: {case_string}")
        print(f"Params: {params}")
        return self.update(columns   = ['TEC_PROC', 'ID_PROCESO'],
                           vals      = [case_string, id_proceso_nuevo],
                           where_col = 'TEC_PROC',
                           where_vals= ids_anteriores,
                           params = params,
                           case      = True)

    def eliminar_tecnico_proceso(self, id_tecnico, id_proceso):
        return self.delete(where_cols=['ID_TECNICO','ID_PROCESO'],
                           where_vals=[id_tecnico, id_proceso])
    
    def eliminar_tecnico_proceso_byProceso(self, id_proceso):
        return self.delete(where_cols='ID_PROCESO',
                           where_vals= id_proceso)

class TiemposModelosCrud(man.Crud):
    def __init__(self, db: man.Database):
        super().__init__(db, table_name = "TIEMPOS_MODELOS")
        self.fields = ['PROCESO_MODELO','ID_PROCESO','ID_MODELO','TIEMPO']
    
    def leer_tiempos_modelos(self):
        return self.select(fields = 'PROCESO_MODELO, ID_PROCESO, ID_MODELO, TIEMPO')
    
    def leer_ids_proceso_modelo(self, proc_modelo):
        return self.select(where = {'ID_PEDIDO': proc_modelo},
                           fields = 'PROCESO_MODELO, ID_PROCESO, ID_MODELO, TIEMPO')

    def leer_procesos_modelos_df(self):
        return self.select(fields=[
                                'TIEMPOS_MODELOS.PROCESO_MODELO',
                                'TIEMPOS_MODELOS.ID_PROCESO',
                                'TIEMPOS_MODELOS.ID_MODELO',
                                'TIEMPOS_MODELOS.TIEMPO'
                            ],
                            joins    = {'PROCESOS': 'TIEMPOS_MODELOS.ID_PROCESO = PROCESOS.ID_PROCESO'},
                            order_by = 'PROCESOS.SECUENCIA')

    def obtener_id_proceso(self, proceso):
        return self.select(fields=['ID_PROCESO'],
                           distinct=True,
                           where={'NOMBRE': proceso},
                           fetch='one')

    def obtener_ids_procesos(self):
        return self.select(fields=['ID_PROCESO'],
                           distinct=True)
   
    def insertar_tiempo_modelo(self, procmodel, id_proceso, id_modelo, tiempo):
        return self.insert(columns = self.fields,
                           vals    = [ procmodel, id_proceso, id_modelo, tiempo])
        
    def insertar_tiempos_modelos_df(self, dataframe):
        return self.insert_dataframe(dataframe=dataframe)
    
    def insRem_tiempos_modelos_df(self, dataframe):
        data = [(row['PROCESO_MODELO'],
                 row['ID_PROCESO'],
                 row['ID_MODELO'],
                 row['TIEMPO']) for _, row in dataframe.iterrows()]
        
        return self.insert_or_replace(
            columns = self.fields, vals =  data)
            
    def actualizar_tiempo_modelo(self, procmodel, id_proceso, id_modelo, tiempo, procmodelo_anterior):
        return self.update( columns = ['PROCESO_MODELO','ID_PROCESO','ID_MODELO','TIEMPO'],
                            vals    = [ procmodel,       id_proceso,   id_modelo, tiempo,],
                            where_col = 'PROCESO_MODELO',
                            params = procmodelo_anterior) 

    def actualizar_proceso_modelos_many(self, ids_anteriores, ids_nuevos, id_proceso_nuevo):
        
        params = []
        for when_val, then_val in zip(ids_anteriores, ids_nuevos):
            params.extend([when_val, then_val])
        params.append(id_proceso_nuevo)
        params.extend(ids_anteriores)
        
        case_string = self.case_string( table      = self.table,
                                        when_then  = {'when': 'PROCESO_MODELO', 'then': 'PROCESO_MODELO'},
                                        when_vals  = ids_anteriores,
                                        then_vals  = ids_nuevos,
                                        elseClause = 'PROCESO_MODELO')
        
        print(f"Case String: {case_string}")
        print(f"Params: {params}")
        return self.update(columns   = ['PROCESO_MODELO', 'ID_PROCESO'],
                           vals      = [case_string, id_proceso_nuevo],
                           where_col = 'PROCESO_MODELO',
                           where_vals= ids_anteriores,
                           params = params,
                           case      = True)
        
    def eliminar_tiempo_modelo(self, modelo):
        return self.delete(where_col = 'PROCESO_MODELO', where_val = modelo)        # OJO PUEDE HABER UN ERROR CON EL CAMPO EN EL VALOR DEL WHERE... DEBERÍA SER proceso_modelo

    def eliminar_tiempo_modelo_byProceso(self, modelo):
        return self.delete(where_col = 'PROCESO_MODELO',
                           where_val = modelo)   ### OJO... ERROR CON EL CAMPO EN EL VALOR DEL WHERE... DEBERÍA SER proceso_modelo
        
class TiemposVehiculosCrud(man.Crud):
    def __init__(self, db: man.Database):
        super().__init__(db, table_name = "TIEMPOS_VEHICULOS")
        self.fields = ['PROCESO_CHASIS', 'ID_PROCESO', 'CHASIS', 'TIEMPO']
    
    def leer_tiempo_vehiculo(self, chasis, id_proceso):
        self.select(
                fields = ['ID_PROCESO', 'TIEMPO'],
                fetch  = 'one',
                where  = {'CHASIS'      : chasis,
                          'ID_PROCESO'  : id_proceso}
                    )

    def leer_tiempos_vehiculo(self, chasis):
        self.select(fields   = ['TIEMPOS_VEHICULOS.ID_PROCESO',
                                'TIEMPOS_VEHICULOS.TIEMPO'],
                    
                    joins    = {'PROCESOS': 'TIEMPOS_VEHICULOS.ID_PROCESO = PROCESOS.ID_PROCESO'},
                    
                    where    = {'TIEMPOS_VEHICULOS.CHASIS': chasis},
                    
                    order_by = 'PROCESOS.SECUENCIA')

    def leer_tiempos_vehiculos(self):
        return self.select(fields = self.fields)
    
    def leer_tiempos_vehiculos_df(self):
        return self.select(as_dataframe=True)
        
    def insertar_tiempo_vehiculo(self, procvehi, id_proceso, chasis, tiempo):
        self.insert(columns=['PROCESO_CHASIS', 'ID_PROCESO', 'CHASIS', 'TIEMPO'],
                    vals=   [ procvehi,         id_proceso,   chasis,   tiempo])

    def insert_tiempos_vehiculo_df(self, df):
        self.insert_dataframe(dataframe = df)

    def actualizar_tiempo_vehiculo(self, procvehi, id_proceso, chasis, tiempo, procvehi_anterior):
        self.update(columns   = ['PROCESO_CHASIS', 'ID_PROCESO', 'CHASIS', 'TIEMPO'],
                    vals      = [ procvehi,         id_proceso,   chasis,   tiempo],
                    where_col = 'PROCESO_CHASIS',
                    params = procvehi_anterior)

    def eliminar_tiempo_vehiculo(self, chasis):
        self.delete(where_col = 'CHASIS', where_val = chasis)

    def eliminar_vehiculos_tiempos_por_pedido(self, id_pedido):
        
        subquery_vehiculos = self.subquery(fields = ['CHASIS'],
                                           table  = 'VEHICULOS',
                                           where  = {'ID_PEDIDO': id_pedido})

        return self.delete(where_cols = 'CHASIS',
                           where_vals = subquery_vehiculos,
                           use_in     = True)
        
class VehiculosCrud(man.Crud):
    def __init__(self, db: man.Database):
        super().__init__(db, table_name = "VEHICULOS")
        self.fields = ['CHASIS',
                       'ID_MODELO',
                       'COLOR',
                       'REFERENCIA',
                       'FECHA_INGRESO',
                       'NOVEDADES',
                       'SUBCONTRATAR',
                       'ID_PEDIDO',]

    def leer_historicos_estado_pedidos_df(self, id_pedido):
        
        tm_crud = TiemposModelosCrud(self.db)
        id_procesos =  tm_crud.obtener_ids_procesos()
        
        str_max_case = self.case_string(table = 'HISTORICOS',
                                        when_then = {'when':'ID_PROCESO',   'then':'ESTADO'},
                                        when_vals = id_procesos,
                                        max_case  = True,
                                        elseClause= '-')
        
        return self.select(fields    =['VEHICULOS.CHASIS',
                                       'VEHICULOS.ID_MODELO',
                                       'VEHICULOS.COLOR',],
                            joins    ={'HISTORICOS'  : 'VEHICULOS.CHASIS      = HISTORICOS.CHASIS',
                                        'PROCESOS'   : 'HISTORICOS.ID_PROCESO = PROCESOS.ID_PROCESO'},
                            cases    = str_max_case,
                            where= {'VEHICULOS.ID_PEDIDO': id_pedido},
                            group_by ='VEHICULOS.CHASIS, VEHICULOS.ID_MODELO, VEHICULOS.COLOR',
                            order_by ='PROCESOS.SECUENCIA',
                            as_dataframe=True)

    def leer_vehiculo(self, chasis):
        return self.select(fields = {'CHASIS',
                                    'FECHA_INGRESO',
                                    'ID_MODELO',
                                    'COLOR',
                                    'NOVEDADES',
                                    'SUBCONTRATAR',
                                    'ID_PEDIDO'},
                            where = {"CHASIS": chasis},
                            fetch  = "one", )

    def leer_vehiculo_completo(self, chasis):
        return self.select(fields=[
                                'VEHICULOS.CHASIS',
                                'VEHICULOS.ID_MODELO',
                                'VEHICULOS.COLOR',
                                'VEHICULOS.REFERENCIA',
                                'VEHICULOS.FECHA_INGRESO',
                                'VEHICULOS.NOVEDADES',
                                'VEHICULOS.SUBCONTRATAR',
                                'VEHICULOS.ID_PEDIDO',
                                'TIEMPOS_VEHICULOS.ID_PROCESO',
                                'TIEMPOS_VEHICULOS.TIEMPO'
                            ],
                            joins={
                                'TIEMPOS_VEHICULOS': 'VEHICULOS.CHASIS = TIEMPOS_VEHICULOS.CHASIS'
                            },
                            where={'VEHICULOS.CHASIS': chasis})

    def leer_vehiculos_completos_marcamodelo(self):
        return self.select(fields=[
                                    'VEHICULOS.CHASIS',
                                    'VEHICULOS.FECHA_INGRESO',
                                    'MODELOS.MARCA',
                                    'MODELOS.MODELO',
                                    'VEHICULOS.COLOR',
                                    {'ID_PROCESO': [self.subquery(fields = ['PROCESOS.ID_PROCESO'],
                                                                    table  = 'HISTORICOS',
                                                                    joins  = {'PROCESOS': 'HISTORICOS.ID_PROCESO = PROCESOS.ID_PROCESO'},
                                                                    limit  = 1,
                                                                    where  = {
                                                                                'HISTORICOS.CHASIS': 'VEHICULOS.CHASIS',
                                                                                'HISTORICOS.ESTADO': " 'EN EJECUCION' ",
                                                                                }
                                                                    ),
                                                        self.subquery(fields = ['PROCESOS.ID_PROCESO'],
                                                                    table  = 'HISTORICOS',
                                                                    joins  = {'PROCESOS': 'HISTORICOS.ID_PROCESO = PROCESOS.ID_PROCESO'},
                                                                    limit  = 1,
                                                                    where  = {
                                                                                'HISTORICOS.CHASIS': 'VEHICULOS.CHASIS',
                                                                                'HISTORICOS.ESTADO': " 'TERMINADO' ",
                                                                                'HISTORICOS.FIN'   :  self.subquery(funct = 'MAX',
                                                                                                                    fields=['FIN'],
                                                                                                                    table = 'HISTORICOS',
                                                                                                                    where={
                                                                                                                            'HISTORICOS.CHASIS': 'VEHICULOS.CHASIS',
                                                                                                                            'HISTORICOS.ESTADO': " 'TERMINADO' "
                                                                                                                            },
                                                                                                                    )
                                                                                }
                                                                    )
                                                        ]
                                    },
                                    {'ESTADO': [self.subquery(fields = ['HISTORICOS.ESTADO'],
                                                                    table  = 'HISTORICOS',
                                                                    limit  = 1,
                                                                    where  = {
                                                                                'HISTORICOS.CHASIS': 'VEHICULOS.CHASIS',
                                                                                'HISTORICOS.ESTADO': " 'EN EJECUCION' ",
                                                                                }
                                                                    ),
                                                        self.subquery(fields = ['HISTORICOS.ESTADO'],
                                                                    table  = 'HISTORICOS',
                                                                    limit  = 1,
                                                                    where  = {
                                                                                'HISTORICOS.CHASIS': 'VEHICULOS.CHASIS',
                                                                                'HISTORICOS.ESTADO': " 'TERMINADO' ",
                                                                                'HISTORICOS.FIN'   :  self.subquery(funct = 'MAX',
                                                                                                                    fields=['FIN'],
                                                                                                                    table = 'HISTORICOS',
                                                                                                                    where={
                                                                                                                            'HISTORICOS.CHASIS': 'VEHICULOS.CHASIS',
                                                                                                                            'HISTORICOS.ESTADO': "'TERMINADO'"
                                                                                                                            }
                                                                                                                    )
                                                                                }
                                                                    )
                                                        ]
                                    },
                                    'VEHICULOS.NOVEDADES',
                                    'VEHICULOS.SUBCONTRATAR',
                                    'VEHICULOS.ID_PEDIDO',
                                ],
                           joins={
                                    'TIEMPOS_VEHICULOS': 'VEHICULOS.CHASIS = TIEMPOS_VEHICULOS.CHASIS',
                                    'MODELOS': 'VEHICULOS.ID_MODELO = MODELOS.ID_MODELO',
                                },      
                           group_by   = 'VEHICULOS.CHASIS',
                           as_dataframe=True
                           )

    def leer_vehiculo_por_modelo(self, id_modelo):
        return self.select( joins     = {'MODELOS': 'MODELOS.ID_MODELO = VEHICULOS.ID_MODELO'},
                            where     = {'MODELOS.ID_MODELO': id_modelo},
                            join_type = 'INNER' )

    def leer_vehiculos(self):
        return self.select(fields = {'CHASIS',
                                    'FECHA_INGRESO',
                                    'ID_MODELO',
                                    'COLOR',
                                    'NOVEDADES',
                                    'SUBCONTRATAR',
                                    'ID_PEDIDO'})
        
    def leer_vehiculos_df(self):
        return self.select(as_dataframe=True)

    def leer_vehiculos_completos_df(self):
        return self.select(fields=[
                                'VEHICULOS.CHASIS',
                                'VEHICULOS.FECHA_INGRESO',
                                'VEHICULOS.ID_MODELO',
                                'VEHICULOS.COLOR',
                                {'NOMBRE_PROCESO': [self.subquery(fields = ['PROCESOS.NOMBRE'],
                                                                  table  = 'HISTORICOS',
                                                                  joins  = {'PROCESOS': 'HISTORICOS.ID_PROCESO = PROCESOS.ID_PROCESO'},
                                                                  limit  = 1,
                                                                  where  = {
                                                                            'HISTORICOS.CHASIS': 'VEHICULOS.CHASIS',
                                                                            'HISTORICOS.ESTADO': " 'EN EJECUCION' ",
                                                                            }
                                                                 ),
                                                    self.subquery(fields = ['PROCESOS.NOMBRE'],
                                                                  table  = 'HISTORICOS',
                                                                  joins  = {'PROCESOS': 'HISTORICOS.ID_PROCESO = PROCESOS.ID_PROCESO'},
                                                                  limit  = 1,
                                                                  where  = {
                                                                            'HISTORICOS.CHASIS': 'VEHICULOS.CHASIS',
                                                                            'HISTORICOS.ESTADO': " 'TERMINADO' ",
                                                                            'HISTORICOS.FIN'   :  self.subquery(funct = 'MAX',
                                                                                                                fields=['FIN'],
                                                                                                                table = 'HISTORICOS',
                                                                                                                where={
                                                                                                                        'HISTORICOS.CHASIS': 'VEHICULOS.CHASIS',
                                                                                                                        'HISTORICOS.ESTADO': "'TERMINADO'"
                                                                                                                        },
                                                                                                                )
                                                                            }
                                                                 )
                                                    ]
                                 },
                                {'ESTADO': [self.subquery(fields = ['HISTORICOS.ESTADO'],
                                                                  table  = 'HISTORICOS',
                                                                  limit  = 1,
                                                                  where  = {
                                                                            'HISTORICOS.CHASIS': 'VEHICULOS.CHASIS',
                                                                            'HISTORICOS.ESTADO': " 'EN EJECUCION' ",
                                                                            }
                                                                 ),
                                                    self.subquery(fields = ['HISTORICOS.ESTADO'],
                                                                  table  = 'HISTORICOS',
                                                                  limit  = 1,
                                                                  where  = {
                                                                            'HISTORICOS.CHASIS': 'VEHICULOS.CHASIS',
                                                                            'HISTORICOS.ESTADO': " 'TERMINADO' ",
                                                                            'HISTORICOS.FIN'   :  self.subquery(funct = 'MAX',
                                                                                                                fields=['FIN'],
                                                                                                                table = 'HISTORICOS',
                                                                                                                where={
                                                                                                                        'HISTORICOS.CHASIS': 'VEHICULOS.CHASIS',
                                                                                                                        'HISTORICOS.ESTADO': "'TERMINADO'"
                                                                                                                        }
                                                                                                                )
                                                                            }
                                                                 )
                                                    ]
                                 },
                                'VEHICULOS.NOVEDADES',
                                'VEHICULOS.SUBCONTRATAR',
                                'VEHICULOS.ID_PEDIDO',],                           
                           group_by   = 'VEHICULOS.CHASIS',
                           as_dataframe=True
                           )

    def leer_vehiculos_por_pedido_df(self, pedido):
                return self.select(fields=[
                                            'VEHICULOS.CHASIS',
                                            'VEHICULOS.ID_MODELO',
                                            'VEHICULOS.COLOR',
                                            {'NOMBRE_PROCESO': [self.subquery(fields = ['PROCESOS.NOMBRE'],
                                                                            table  = 'HISTORICOS',
                                                                            joins  = {'PROCESOS': 'HISTORICOS.ID_PROCESO = PROCESOS.ID_PROCESO'},
                                                                            limit  = 1,
                                                                            where  = {
                                                                                        'HISTORICOS.CHASIS': 'VEHICULOS.CHASIS',
                                                                                        'HISTORICOS.ESTADO': " 'EN EJECUCION' ",
                                                                                        }
                                                                            ),
                                                                self.subquery(fields = ['PROCESOS.NOMBRE'],
                                                                            table  = 'HISTORICOS',
                                                                            joins  = {'PROCESOS': 'HISTORICOS.ID_PROCESO = PROCESOS.ID_PROCESO'},
                                                                            limit  = 1,
                                                                            where  = {
                                                                                        'HISTORICOS.CHASIS': 'VEHICULOS.CHASIS',
                                                                                        'HISTORICOS.ESTADO': " 'TERMINADO' ",
                                                                                        'HISTORICOS.FIN'   :  self.subquery(funct = 'MAX',
                                                                                                                            fields=['FIN'],
                                                                                                                            table = 'HISTORICOS',
                                                                                                                            where={
                                                                                                                                    'HISTORICOS.CHASIS': 'VEHICULOS.CHASIS',
                                                                                                                                    'HISTORICOS.ESTADO': "'TERMINADO'"
                                                                                                                                    },
                                                                                                                            )
                                                                                        }
                                                                            )
                                                                ]
                                            },
                                            {'ESTADO': [self.subquery(fields = ['HISTORICOS.ESTADO'],
                                                                            table  = 'HISTORICOS',
                                                                            limit  = 1,
                                                                            where  = {
                                                                                        'HISTORICOS.CHASIS': 'VEHICULOS.CHASIS',
                                                                                        'HISTORICOS.ESTADO': " 'EN EJECUCION' ",
                                                                                        }
                                                                            ),
                                                                self.subquery(fields = ['HISTORICOS.ESTADO'],
                                                                            table  = 'HISTORICOS',
                                                                            limit  = 1,
                                                                            where  = {
                                                                                        'HISTORICOS.CHASIS': 'VEHICULOS.CHASIS',
                                                                                        'HISTORICOS.ESTADO': " 'TERMINADO' ",
                                                                                        'HISTORICOS.FIN'   :  self.subquery(funct = 'MAX',
                                                                                                                            fields=['FIN'],
                                                                                                                            table = 'HISTORICOS',
                                                                                                                            where={
                                                                                                                                    'HISTORICOS.CHASIS': 'VEHICULOS.CHASIS',
                                                                                                                                    'HISTORICOS.ESTADO': "'TERMINADO'"
                                                                                                                                    }
                                                                                                                            )
                                                                                        }
                                                                            )
                                                                ]
                                            },
                                        ], 
                                    joins    = {'PEDIDOS': 'VEHICULOS.ID_PEDIDO = PEDIDOS.ID_PEDIDO'},
                                    where    = {'PEDIDOS.ID_PEDIDO': pedido},                   
                                    group_by = 'VEHICULOS.CHASIS',
                                    as_dataframe=True
                            )

    def leer_tiempos_vehiculos_df(self):
        
        tm_crud = TiemposModelosCrud(self.db)
        id_procesos =  tm_crud.obtener_ids_procesos()
        
        str_max_case = self.case_string(table = 'TIEMPOS_VEHICULOS',
                                        when_then= {'when':'ID_PROCESO',   'then':'TIEMPO'},
                                        when_vals = id_procesos,
                                        max_case=True)
        
        return self.select(fields    =['VEHICULOS.CHASIS',],
                            joins    ={'TIEMPOS_VEHICULOS'  : 'VEHICULOS.CHASIS             = TIEMPOS_VEHICULOS.CHASIS',
                                        'PROCESOS'          : 'TIEMPOS_VEHICULOS.ID_PROCESO = PROCESOS.ID_PROCESO'},
                            cases    = str_max_case,
                            group_by ='VEHICULOS.CHASIS',
                            order_by ='PROCESOS.SECUENCIA',
                            as_dataframe=True)

    def insertar_vehiculo(self, chasis, fecha_ingreso, id_modelo, color, novedades, subcontratar, id_pedido):
        return self.insert(columns = ['CHASIS', 'FECHA_INGRESO', 'ID_MODELO', 'COLOR', 'NOVEDADES','SUBCONTRATAR', 'ID_PEDIDO'],
                            vals   = [ chasis,   fecha_ingreso,   id_modelo,   color,   novedades,   subcontratar, id_pedido])
        
    def insertar_vehiculos_df(self, df):
        return self.insert_dataframe(dataframe=df)

    def actualizar_vehiculos_pedido(self, id_anterior, id_nuevo):
        return self.update(columns   = ['ID_PEDIDO',],   vals      = [id_nuevo,],
                           where_col = 'ID_PEDIDO',      params = id_anterior)

    def eliminar_vehiculos_por_pedido(self, id_pedido):
        return self.delete(where_col='ID_PEDIDO', where_val=id_pedido)
    
    def eliminar_vehiculo(self, chasis):
        return self.delete(where_col='CHASIS',
                           where_val=chasis)
    
    def eliminar_vehiculo_completo(self, chasis):
        crud_TiV = TiemposVehiculosCrud(self.db)
        crud_TiV.eliminar_tiempo_vehiculo(chasis)
        self.eliminar_vehiculo(chasis)




with man.Database('planta_con_ensamble1.db') as db:
    #crud_TV = TiemposVehiculosCrud(db)
    #rud_TV.actualizar_tiempo_vehiculo('COD-7405NL9458200', 'COD', '7405NL9458200', 12, 'COD-7405NL9458200')
    pass
    #obj = crud_programas = ProgramasCrud(db)
    #print(crud_programas.next_consecutivoPrograma())
    
    
    

    #obj = TiemposModelosCrud(db)
    #obj.actualizar_tiempo_modelo(procmodel='Pintura_anterior',
    #                                    id_proceso='001',
    #                                    id_modelo='Modelo1',
    #                                    tiempo=10,
    #                                    procmodelo_anterior='Pintura_anterior'
    #                                    )
    
    
    
    #obj = TiemposModelosCrud(db)
    #print(obj.actualizar_proceso_modelos_many(ids_anteriores=['Pintura_anterior', 'Ensamblaje_anterior', 'Lavado_anterior'],
    #                                    ids_nuevos=['Pintura Nueva', 'Ensamblaje Nueva', 'Lavado Nuevo'],
    #                                    id_proceso_nuevo='001'))
    

    
    #obj = TecnicosProcesosCrud(db)
    #print(obj.actualizar_tecnicos_proceso_many(
    #                                    ids_anteriores=['Pintura_anterior', 'Ensamblaje_anterior', 'Lavado_anterior'],
    #                                    ids_nuevos=['Pintura Nueva', 'Ensamblaje Nueva', 'Lavado Nuevo'],
    #                                    id_proceso_nuevo='001'))

    
    #crud_vehiculos = VehiculosCrud(db)
    #crud_vehiculos.leer_vehiculos_por_pedido_df('SIMULADO2_2')
        
        
    #crud_tiemposvehiculos = TiemposVehiculosCrud(db)
    #print(crud_tiemposvehiculos.leer_tiempo_vehiculo('AAH55SDF4G4FDS', 'PDI'))
    
    
    #crud_vehiculos = VehiculosCrud(db)
    #print(crud_vehiculos.leer_historicos_estado_pedidos_df('FOTON3_3'))
    
    
    #crud_modelos = ModelosCrud(db)
    #print(crud_modelos.leer_tiempos_modelos_df())
    
    
    #crud_historicos = HistoricosCrud(db)
    #resultados = crud_historicos.leer_historicos_completo()
    #resultados = crud_historicos.select(fields = 
    #    ['CODIGO_ASIGNACION', 'CHASIS', 'ID_TECNICO', 'ID_PROCESO', 'OBSERVACIONES', 'INICIO', 'FIN', 'DURACION', 'ESTADO'],  where = {'ID_PROCESO': 'PDI'},
    #     fetch='all', as_dataframe=True, distinct=True)
    #print(resultados)



    #crud_vehiculos = VehiculosCrud(db)
    #print(crud_vehiculos.leer_vehiculo_completo('CHASIS1234'))   
    
    
    
    #crud_procesos, crud_programas, crud_pedidos = ProcesosCrud(db), ProgramasCrud(db), PedidosCrud(db)
    #crud_procesos.insertar_proceso(id='BLA', proceso = 'BLABLABLAA', descripcion='PRUEBAA', secuencia=8)
    #crud_procesos.actualizar_proceso(id_proceso='BLA1', nombre = 'BLABLABLAA', descripcion='PRUEBAA', secuencia=8, id_proceso_anterior='BLA')
    #crud_procesos.eliminar_proceso('BLI')
    #cambios = db.track_affected
    #procesos_df = crud_procesos.leer_procesos_df()
    #print(procesos_df, "\n" ,"cambios: ")
    #print(cambios)
