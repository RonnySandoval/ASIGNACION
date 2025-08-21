import pandas as pd
import random
import math
import string
import datetime as dt
from database import BDmanage as man
from . import entities as entid
from . import OR3
from model import gantt_pruebas2 as gantt

path_db = 'C:/NUEVO_PORTATIL/GITHUB/ASIGNACION/planta_con_ensamble1.db'
with man.Database(path_db) as db:
    plant = entid.Plant(db=db)
    df_referencias = plant.df_referencias
    df_vehiculos = plant.df_trabajos
    df_modelos = plant.df_modelos_df
    df_tiempos_modelos = plant.df_tiempos_modelos
    df_procesos = plant.df_procesos
    df_dispatch = pd.read_excel('C:/NUEVO_PORTATIL/GITHUB/ASIGNACION/DESPACHOS_2024.xlsx')

random.seed(96)
def choice_one(df: pd.DataFrame, columns: list[str], locator: str):
    ident = random.choice(list(df[locator]))
    row = df[df[locator] == ident][columns].iloc[0]
    return row.to_dict()

def choice_many(n: int, df: pd.DataFrame, columns: list[str], locator: str):
    return pd.DataFrame([choice_one(df, columns, locator) for _ in range(n)])

def id_random(size: int, type='alphanumeric'):
    if type == 'alphanumeric':
        caracteres = string.ascii_uppercase + string.digits
        return ''.join(random.choices(caracteres, k=size))
    elif type == 'numeric':
        caracteres = string.digits
        return ''.join(random.choices(caracteres, k=size))
    elif type == 'alpha':
        caracteres = string.ascii_uppercase
        return ''.join(random.choices(caracteres, k=size))
    else:
        raise ValueError("Tipo inválido. Usa 'alphanumeric', 'numeric' o 'alpha' en el parámetro type.")

def ids_random(n: int, size: int, name:str, type='alphanumeric'):
    return pd.DataFrame({name: [id_random(size, type) for _ in range(n)]})

def choice_condition(df, col_reference, col_objective):
    def selector(row):
        valor_ref = row[col_reference]
        valores_posibles = df[df[col_reference] == valor_ref][col_objective]
        if not valores_posibles.empty:
            return random.choice(valores_posibles.tolist())
        else:
            return None
    return selector
    
def fluctuate_one(x:float, s:float):
    val = int(random.normalvariate(mu=x, sigma=s))
    return int(math.floor(val) if random.random() < 0.5 else math.ceil(val))

def choice_procces_one(procces: list):
    return random.choice(procces)

def simular_vehiculos(n: int, date : dt.datetime,  df_dispatch: pd.DataFrame,  df_references: pd.DataFrame):
        
    fecha_ingreso = str(date)
    id_pedido = 'SIM_'+str(random.randint(1,100))
    
    
    df_choice = choice_many(n= n, df  = df_dispatch, columns =['REFERENCIA'], locator ='REFERENCIA')
    df_choice['CHASIS'] = ids_random(n, size=16, name='CHASIS')
    df_choice['COLOR'] = df_choice.apply(choice_condition(df = df_dispatch,
                                                        col_reference='REFERENCIA',
                                                        col_objective='COLOR'), axis=1)
    df_choice = df_choice.merge(df_references[["REFERENCIA", "ID_MODELO"]],
                                on    = "REFERENCIA",
                                how   = "left")
    
    df_veh_simul = df_choice.copy()
    df_veh_simul = df_veh_simul[['CHASIS', 'ID_MODELO', 'COLOR', 'REFERENCIA']]
    df_veh_simul[['FECHA_INGRESO',
                'NOVEDADES',
                'SUBCONTRATAR',
                'ID_PEDIDO']] = [fecha_ingreso,
                                 'NO',
                                 'NO',
                                 id_pedido]
              
    return df_veh_simul

def simular_tiempos_vehiculos(df_tm: pd.DataFrame, df_veh: pd.DataFrame, initial: bool = False):
    df_tm_fluc = df_tm.copy()
    procces = list(df_tm['ID_PROCESO'].unique())
    
    # Generar variaciones a tiempos
    df_tm_fluc['TIEMPO'] = df_tm_fluc.apply(
        lambda row: fluctuate_one(row['TIEMPO'], s=0.15 * row['TIEMPO']) if initial == False
               else fluctuate_one(row['TIEMPO'], s=0.15 * row['TIEMPO']) if row['ID_PROCESO'] == procces else 0, axis=1)
    
    # añadir CHASIS y ID_PROCESO en base ambos dataframe
    df_cross = df_veh[['CHASIS']].merge(df_tm_fluc[['ID_PROCESO']].drop_duplicates(), how = "cross")
    
    # concatenar para generar columna  PROCESO_CHASIS
    df_cross['PROCESO_CHASIS'] = df_cross['ID_PROCESO'].astype(str) + '-' + df_cross['CHASIS'].astype(str)
    
    # añadir columna de ID_MODELO
    df_cross = df_cross.merge(df_veh[['CHASIS', 'ID_MODELO']], on='CHASIS', how='left')
    
    #crear el ID de tiempo modelo para consultarlo
    df_cross['PROCESO_MODELO'] = df_cross['ID_PROCESO'].astype(str) + '-' + df_cross['ID_MODELO'].astype(str)
    
    # añadir columna de TIEMPO en base a columna ID_MODELO
    df_cross = df_cross.merge(df_tm_fluc[['PROCESO_MODELO', 'TIEMPO']], on='PROCESO_MODELO', how='left')
    
    ##REORGANIZAR DATAFRAME
    df_tm_simul = df_cross[['PROCESO_CHASIS', 'ID_PROCESO', 'CHASIS', 'TIEMPO']]

    return df_cross

def simular_pedido(n: int, date: dt.datetime, df_dispatch: pd.DataFrame, df_references: pd.DataFrame, df_tm: pd.DataFrame):

    df_vehiculos = simular_vehiculos(n, date, df_dispatch, df_references)
    df_tiempos = simular_tiempos_vehiculos(df_tm, df_vehiculos)
    
    return df_vehiculos, df_tiempos

def simular_iniciales(n: int,
                      date: dt.datetime,
                      df_dispatch: pd.DataFrame,
                      df_references: pd.DataFrame,
                      df_tm: pd.DataFrame,
                      df_procesos: pd.DataFrame):
    
    df_vehiculos = simular_vehiculos(n, date, df_dispatch, df_references)
    df_tiempos = simular_tiempos_vehiculos(df_tm, df_vehiculos)
    df_tiempos_not_cero = df_tiempos[df_tiempos['TIEMPO'] != 0]
    elecciones = dict(df_tiempos_not_cero.groupby("CHASIS")["ID_PROCESO"].apply(lambda s: random.choice(s.unique())))    # Diccionario {chasis: proceso_aleatorio_existente}
    df_tiempos_unique = df_tiempos_not_cero[ df_tiempos_not_cero.apply(lambda r: r["ID_PROCESO"] == elecciones[r["CHASIS"]], axis=1)]    # Filtrar usando el mapeo anterior
    
    return df_vehiculos, df_tiempos, df_tiempos_unique

def simular_pedido_inciales(n_jobs: int,
                            n_init: int,
                            date: dt.datetime,
                            df_dispatch: pd.DataFrame,
                            df_references: pd.DataFrame,
                            df_tm: pd.DataFrame)-> dict:
      
    vh_init, tm_init, proc_init = simular_iniciales(n = n_init,
                                                                date = date,
                                                                df_dispatch = df_dispatch,
                                                                df_references = df_references,
                                                                df_tm = df_tm,
                                                                df_procesos = df_procesos)

    vh_pedi, tm_pedi = simular_pedido(n =n_jobs,
                                      date = date,
                                      df_dispatch = df_dispatch,
                                      df_references = df_references,
                                      df_tm = df_tm)

    #print('vehiculos_iniciales','\n', vh_init)
    #print('procesos_unicos','\n', proc_init)
    #print('tiempos_iniciales','\n', tm_init)
    return {'vehiculos_iniciales':vh_init,
            'tiempos_iniciales':tm_init,
            'procesos_unicos':proc_init,
            'vehiculos_pedido':vh_pedi,
            'tiempos_pedido':tm_pedi}

pedido_simulado = simular_pedido_inciales(n_jobs = 35,
                                          n_init = 30,
                                          date = dt.datetime.now().date(),
                                          df_dispatch = df_dispatch,
                                          df_references = df_referencias,
                                          df_tm = df_tiempos_modelos)

with man.Database(path_db) as db:
    plant_simulate = entid.Plant(db, simul = pedido_simulado)

model_init = OR3.modelOR(operarios               = list(set(plant_simulate.operarios)),
                        procesos_operarios       = plant_simulate.procesos_operarios,
                        trabajos                 = plant_simulate.trabajos_inic + plant_simulate.trabajos,
                        procesos_trabajos        = plant_simulate.procesos_trabajos_inic | plant_simulate.procesos_trabajos,
                        precedencias_por_trabajo = plant_simulate.precedencias_trabajos)

#model_init.objective_function(model_init.OBJ_MAX_NUM_TASK, time_limit=200)
#model_init.objective_function(model_init.OBJ_MIN_MAKESPAN_SIMPLE)


#[print (trabajo, procesos) for trabajo, procesos in model_init.procesos_trabajos.items()]
#[print (trabajo, precedencia) for trabajo, precedencia in model_init.precedencias_por_trabajo.items()]
#[print (tarea["id"], tarea["predecesoras"]) for tarea in model_init.tareas]
model_init.objective_function(type_objective=model_init.OBJ_MIN_MAKESPAN_SIMPLE)
#model_init.validate_consistency(time_limit=800)
model_init.solve_model()
#print(model_init.str_sequences())
#print(model_init.tareas_asignadas_df.to_string())
df_tareas = model_init.tareas_asignadas_df
df_tareas = df_tareas.rename(columns={'trabajo': 'CHASIS',
                                      'proceso': 'PROCESO',
                                      'inicio': 'INICIO',
                                      'fin': 'FIN',
                                      'operario_asignado': 'TECNICO'})
df_merged = df_tareas.merge(right = pd.concat([pedido_simulado['vehiculos_iniciales'],
                                               pedido_simulado['vehiculos_pedido']],
                                               ignore_index=True
                                            )[['CHASIS', 'ID_MODELO']],
                            on    = 'CHASIS',
                            how   = 'left')
#print(df_merged)
#print(model_init.str_sequences())

app_server, url_server = gantt.plot_gantt(df   =df_merged,
                                        items="TECNICO",
                                        tasks="PROCESO",
                                        filter2="ID_MODELO",
                                        filter1="CHASIS")
                                        
print(url_server)
#is_numeric = True

"""model_init.tareas_asignadas, makespan = model_init.solve_model(tiempo_max=5, debug=True)
[print(tarea) for tarea in model_init.tareas_asignadas.values()]
print(makespan)
model_init.resume()
print(model_init.tareas_asignadas_df)
#model = OR.modelOR(plant.operarios,
#                   plant.procesos_operarios,
#                   plant.trabajos,
#                   plant.procesos_trabajos,
#                   plant.precedencias_trabajos)"""
