import pandas as pd
import numpy as np
import random
import math
import string
import datetime as dt
from database import BDmanage as man
from . import entities as entid
from . import OR3
from model import gantt_pruebas2 as gantt

def choice_one(df: pd.DataFrame, columns: list[str], locator: str)-> dict:
    ident = random.choice(list(df[locator]))
    row = df[df[locator] == ident][columns].iloc[0]
    return row.to_dict()

def choice_many(n: int, df: pd.DataFrame, columns: list[str], locator: str)-> pd.DataFrame:
    return pd.DataFrame([choice_one(df, columns, locator) for _ in range(n)])

def id_random(size: int, type='alphanumeric')-> str:
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

def ids_random(n: int, size: int, name:str, type='alphanumeric')-> pd.DataFrame:
    return pd.DataFrame({name: [id_random(size, type) for _ in range(n)]})

def choice_condition(df, col_reference, col_objective)-> callable:
    def selector(row):
        valor_ref = row[col_reference]
        valores_posibles = df[df[col_reference] == valor_ref][col_objective]
        if not valores_posibles.empty:
            return random.choice(valores_posibles.tolist())
        else:
            return None
    return selector
    
def fluctuate_one(x:float, s:float)-> int:
    val = int(random.normalvariate(mu=x, sigma=s))
    return int(math.floor(val) if random.random() < 0.5 else int(math.ceil(val)))

def choice_procces_one(procces: list)-> str:
    return random.choice(procces)

def simulate_jobs(n: int, date : dt.datetime,  df_dispatch: pd.DataFrame,  df_references: pd.DataFrame)->pd.DataFrame:
        
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

def simulate_times_jobs(df_tm: pd.DataFrame, df_veh: pd.DataFrame, initial: bool = False)->pd.DataFrame:
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

def simulate_batch(n: int, date: dt.datetime, df_dispatch: pd.DataFrame, df_references: pd.DataFrame, df_tm: pd.DataFrame)->tuple[pd.DataFrame, pd.DataFrame]:

    df_vehiculos = simulate_jobs(n, date, df_dispatch, df_references)
    df_tiempos = simulate_times_jobs(df_tm, df_vehiculos)
    
    return df_vehiculos, df_tiempos

def simulate_initials(n: int, date: dt.datetime, df_dispatch: pd.DataFrame, df_references: pd.DataFrame, df_tm: pd.DataFrame)->tuple[pd.DataFrame]:
    
    df_vehiculos = simulate_jobs(n, date, df_dispatch, df_references)
    df_tiempos = simulate_times_jobs(df_tm, df_vehiculos)
    df_tiempos_not_cero = df_tiempos[df_tiempos['TIEMPO'] != 0]
    elecciones = dict(df_tiempos_not_cero.groupby("CHASIS")["ID_PROCESO"].apply(lambda s: choice_procces_one(s.unique())))    # Diccionario {chasis: proceso_aleatorio_existente}
    df_tiempos_unique = df_tiempos_not_cero[ df_tiempos_not_cero.apply(lambda r: r["ID_PROCESO"] == elecciones[r["CHASIS"]], axis=1)]    # Filtrar usando el mapeo anterior
    
    return df_vehiculos, df_tiempos, df_tiempos_unique

def simulate_batch_initials(n_jobs: int,
                            date: dt.datetime,
                            df_dispatch: pd.DataFrame,
                            df_references: pd.DataFrame,
                            df_tm: pd.DataFrame,
                            n_init: int = None,
                            df_pending: pd.DataFrame = None ,
                            plant_simulate_prev:entid.Plant=None)-> dict:
    if df_pending is not None:
        vh_init, tm_init, proc_init = generate_df_initials(df_pending, plant_simulate_prev)
    
    else:
        vh_init, tm_init, proc_init = simulate_initials(n = n_init,
                                                        date = date,
                                                        df_dispatch = df_dispatch,
                                                        df_references = df_references,
                                                        df_tm = df_tm)

    vh_pedi, tm_pedi = simulate_batch(n =n_jobs,
                                      date = date,
                                      df_dispatch = df_dispatch,
                                      df_references = df_references,
                                      df_tm = df_tm)

    return {'vehiculos_iniciales':vh_init,
            'tiempos_iniciales':tm_init,
            'procesos_unicos':proc_init,
            'vehiculos_pedido':vh_pedi,
            'tiempos_pedido':tm_pedi}

def apply_schedule(plant_simulate: entid.Plant,
                   purchase_simulate: dict,
                   minutes_workday:int = None,
                   last_id_task:int = 0,
                   jobs_pending: list[str] = None,
                   solver_time = 5)-> tuple[OR3.modelOR, pd.DataFrame, pd.DataFrame]:
    """Simula la aplicacion de un horario a los operarios"""
            
    weights_jobs = {jobs_pending: 20} if jobs_pending is not None else {}
    model_OR = OR3.modelOR (operarios                = plant_simulate.operarios,
                            procesos_operarios       = plant_simulate.procesos_operarios,
                            trabajos                 = plant_simulate.trabajos_inic + plant_simulate.trabajos,
                            procesos_trabajos        = plant_simulate.procesos_trabajos_inic | plant_simulate.procesos_trabajos,
                            precedencias_por_trabajo = plant_simulate.precedencias_trabajos,
                            pesos_trabajo            = weights_jobs,
                            last_id_task             = last_id_task)

    model_OR.objective_function(type_objective=model_OR.OBJ_MIN_MAKESPAN_WEIGHTED)
    model_OR.solve_model(solver_time=solver_time)
    df_tareas = model_OR.tareas_asignadas_df
    df_tareas = df_tareas.rename(columns={'trabajo': 'CHASIS',
                                          'proceso': 'PROCESO',
                                          'inicio' : 'INICIO',
                                          'fin'    : 'FIN',
                                          'operario_asignado': 'TECNICO'})
    df_merged = df_tareas.merge(right = pd.concat([purchase_simulate['vehiculos_iniciales'],
                                                  purchase_simulate['vehiculos_pedido']],
                                                  ignore_index=True)[['CHASIS', 'ID_MODELO']],
                                on    = 'CHASIS',
                                how   = 'left')
    if  isinstance(minutes_workday, int):
        df_workday = df_merged[df_merged['FIN'] <= minutes_workday + 10]
        df_nextday = df_merged[df_merged['FIN'] > minutes_workday]
        return model_OR, df_workday, df_nextday


    return model_OR, df_merged, None

def generate_df_initials(df_pending: pd.DataFrame, plant_simulate_prev: entid.Plant)-> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    
    list_jobs = list(df_pending['CHASIS'].unique())
    
    df_jobs = plant_simulate_prev.df_trabajos_inic
    df_procjobs = plant_simulate_prev.df_proc_trab_inic
    df_procjobs_uniq = plant_simulate_prev.df_proc_trab_uniq
    
    df_vehiculos = df_jobs[df_jobs["CHASIS"].isin(list_jobs)]
    df_tiempos = df_procjobs[df_procjobs["CHASIS"].isin(list_jobs)]
    df_tiempos_unique = df_procjobs_uniq[df_procjobs_uniq["CHASIS"].isin(list_jobs)]
    
    return df_vehiculos, df_tiempos, df_tiempos_unique

class Simulation():
    def __init__(self, plant:entid.Plant, df_dispatch: pd.DataFrame, day:dt.datetime = None):
        
        self.day = dt.datetime.now().date() if day is None else day
        self.plant = plant
        self.df_dispatch = df_dispatch
        self.batchs_simulated = []
        self.plants_simulated = []
        self.models = []
        self.schedules_day = []
        self.pendings_day = []
        self.jobs_scheduled_day = []
        self.jobs_scheduled_all = []
        self.jobs_pendings_day = []
        self.jobs_pendings_all = []
        
    def __simulate_batch_0__(self, n_init: int, n_jobs: int, minutes_workday:int = 480, solver_time:int = 3):
        dict_batch_simulated = simulate_batch_initials(n_jobs         = n_jobs,
                                                       n_init         = n_init,
                                                       date           = self.day,
                                                       df_dispatch    = self.df_dispatch,
                                                       df_references  = plant.df_referencias,
                                                       df_tm          = plant.df_tiempos_modelos)
        plant_simulated = entid.Plant_simulated(simul = dict_batch_simulated, plant= self.plant)        
        
        model, df_schedule, df_pending = apply_schedule(plant_simulated,
                                                        dict_batch_simulated,
                                                        minutes_workday,
                                                        solver_time)
        df_jobs_pending = df_pending[['CHASIS']].drop_duplicates()
        df_jobs_scheduled = df_schedule[['CHASIS']].drop_duplicates()
        
        [lista.append(data) for lista, data in zip(
            [self.batchs_simulated, self.plants_simulated, self.models, self.schedules_day, self.pendings_day, self.jobs_pendings_day, self.jobs_scheduled_day],
            [dict_batch_simulated,  plant_simulated,       model,       df_schedule,    df_pending,    df_jobs_pending,    df_jobs_scheduled  ] ) ]
        
        df_schedule["ITERACION"] = 0
        df_schedule["DIA"] = self.day
        self.last_id_task = df_schedule['id'].max()
        
        self.df_total_schedule = df_schedule.copy()

    def __simulate_batch_i__(self, i: int, n_jobs: int, minutes_workday:int = 480, solver_time = 3):
        dict_batch_simulated = simulate_batch_initials(n_jobs              = n_jobs,
                                                       date                = self.day,
                                                       df_dispatch         = self.df_dispatch,
                                                       df_references       = self.plant.df_referencias,
                                                       df_tm               = self.plant.df_tiempos_modelos,
                                                       df_pending          = self.pendings_day[i-1],
                                                       plant_simulate_prev = self.plants_simulated[i-1])
        plant_simulated = entid.Plant_simulated(simul = dict_batch_simulated, plant= self.plant)
        
        model, df_schedule, df_pending = apply_schedule(plant_simulated,
                                                        dict_batch_simulated,
                                                        minutes_workday = minutes_workday,
                                                        last_id_task    = self.last_id_task,
                                                        solver_time     = solver_time)
        df_jobs_pending = df_pending[['CHASIS']].drop_duplicates()
        df_jobs_scheduled = df_schedule[['CHASIS']].drop_duplicates()
        
        [lista.append(data) for lista, data in zip(
            [self.batchs_simulated,
             self.plants_simulated,
             self.models,
             self.schedules_day,
             self.pendings_day,
             self.jobs_pendings_day,
             self.jobs_scheduled_day],
                                        [dict_batch_simulated, 
                                        plant_simulated,      
                                        model,      
                                        df_schedule,   
                                        df_pending,   
                                        df_jobs_pending,   
                                        df_jobs_scheduled  ] ) ]
        
        df_schedule["ITERACION"] = i
        df_schedule["DIA"] = self.day
        self.last_id_task = df_schedule['id'].max()
        
        self.df_total_schedule = pd.concat([self.df_total_schedule, df_schedule], ignore_index=True)
    
    def simulate_many_days(self,
                           n_days: int,
                           n_init: int,
                           n_jobs: int,
                           minutes_workday:int = 480,
                           oscilate_jobs:int=0,
                           solver_time = 3,
                           path_excel:str = None)-> pd.DataFrame:
        self.__simulate_batch_0__(n_init=n_init, n_jobs=n_jobs, minutes_workday=minutes_workday, solver_time=solver_time)
        
        for i in range(1, n_days + 1):
            self.day = self.day + dt.timedelta(days=1)
            randjobs = n_jobs + random.randint(-oscilate_jobs, oscilate_jobs) if oscilate_jobs > 0 else n_jobs
            self.__simulate_batch_i__(i=i, n_jobs=randjobs, minutes_workday=minutes_workday, solver_time=solver_time)
        
        if path_excel is not None:
            self.df_total_schedule.to_excel(path_excel + 'total_schedule.xlsx', index=False)
            
        self.performance_op = self.__calculate_performance__(self.df_total_schedule, minutes_workday)
        (self.jobs_scheduled_all, self.jobs_pendings_all) = self.__calculate_resume_jobs__()
        
        return self.df_total_schedule
  
    def __calculate_performance__(self, df_total_schedule: pd.DataFrame, time_day: int)-> pd.DataFrame:

        df_total_schedule["DURACION"] = df_total_schedule["FIN"] - df_total_schedule["INICIO"]
        df_performance_op = df_total_schedule.groupby(["TECNICO", "DIA"])["DURACION"].sum().reset_index()
        df_performance_op = df_performance_op.rename(columns={"DURACION": "TIEMPO_PRODUCTIVO"})
        df_performance_op["PRODUCTIVIDAD"] = df_performance_op["TIEMPO_PRODUCTIVO"] / time_day
        return df_performance_op
    
    def __calculate_resume_jobs__(self)-> pd.DataFrame:
        procceses = list(self.plant.df_procesos['ID_PROCESO'])
        df_jobs_scheduled = pd.concat(self.jobs_scheduled_day, ignore_index=True).drop_duplicates().reset_index(drop=True)
        df_jobs_scheduled[procceses] = np.nan
        
        df_jobs_pending = pd.concat(self.jobs_pendings_day, ignore_index=True).drop_duplicates().reset_index(drop=True)
        df_jobs_pending[procceses] = np.nan
        
        # Primero, crea un diccionario para búsqueda rápida: (CHASIS, ID_PROCESO) -> clave_entero
        lookup_sched, lookup_pend = {}, {}
        for clave_sched, df_sched in enumerate(self.schedules_day):
            lookup_sched.update({(row["CHASIS"], row["PROCESO"]): clave_sched for _, row in df_sched.iterrows()})
        
        for clave_pend, df_pend in enumerate(self.pendings_day):
            lookup_pend.update({(row["CHASIS"], row["PROCESO"]): clave_pend for _, row in df_pend.iterrows()})
        
        # Ahora, para cada columna de proceso en jobs_scheduled_all, asigna el valor si hay coincidencia
        for procces in procceses:
            df_jobs_scheduled[procces] = df_jobs_scheduled.apply(
                    lambda row: lookup_sched.get((row["CHASIS"], procces),
                                                 np.nan), axis=1)
            
            df_jobs_pending[procces] = df_jobs_pending.apply(
                    lambda row: lookup_pend.get((row["CHASIS"], procces),
                                                 np.nan), axis=1)
        return df_jobs_scheduled, df_jobs_pending
    
random.seed(95)
path = 'C:/NUEVO_PORTATIL/GITHUB/ASIGNACION/'
path_db = path + 'planta_con_ensamble1.db'
df_dispatch = pd.read_excel(path + 'DESPACHOS_2024.xlsx')

with man.Database(path_db) as db:
    plant = entid.Plant(db=db)
    
sim = Simulation(plant=plant, df_dispatch=df_dispatch)
df_total_schedule = sim.simulate_many_days(n_days=6, n_init=30, n_jobs=20,
                                           minutes_workday=480,  oscilate_jobs=6,
                                           solver_time=4,  path_excel=path)
sim.performance_op.to_excel(path + 'performance_operarios.xlsx', index=False)
sim.jobs_scheduled_all.to_excel(path+ 'performance_resume_jobs.xlsx', index=False)
sim.jobs_pendings_all.to_excel(path+ 'performance_pending_jobs.xlsx', index=False)
    
    
    

"""day = dt.datetime.now().date()
batch_simulated = simulate_batch_initials(  n_jobs          = 50,
                                                n_init          = 40,
                                                date            = dt.datetime.now().date(),
                                                df_dispatch     = df_dispatch,
                                                df_references   = plant.df_referencias,
                                                df_tm           = plant.df_tiempos_modelos)
plant_simulated = entid.Plant_simulated(simul = batch_simulated, plant= plant)
model_i, df_schedule_i, df_pending_i = apply_schedule(plant_simulated, batch_simulated, minutes_workday=480)
df_schedule_i["ITERACION"] = 0
df_schedule_i["DIA"] = day

df_total_schedule = df_schedule_i.copy()
batchs_simulated, plants_simulated, models, schedules, pendinds = [], [], [], [], []
last_id_task = df_schedule_i['id'].max()

for i in range(1, 10):
    day = dt.datetime.now().date() + dt.timedelta(days=i)
    batch_simulated_i = simulate_batch_initials(n_jobs              = 50,
                                                date                = day,
                                                df_dispatch         = df_dispatch,
                                                df_references       = plant.df_referencias,
                                                df_tm               = plant.df_tiempos_modelos,
                                                df_pending          = df_pending_i,
                                                plant_simulate_prev = plant_simulated)
    plant_simulated_i = entid.Plant_simulated(simul = batch_simulated_i, plant= plant)
    
    model_i, df_schedule_i, df_pending_i = apply_schedule(plant_simulated_i,
                                                            batch_simulated_i,
                                                            minutes_workday = 480,
                                                            last_id_task    = last_id_task,
                                                            solver_time     = 3)
    
    [lista.append(valor) for lista, valor in zip(
        [batchs_simulated,  plants_simulated,  models,  schedules,     pendinds],
        [batch_simulated_i, plant_simulated_i, model_i, df_schedule_i, df_pending_i]
        )
    ]

    df_schedule_i["ITERACION"] = i
    df_schedule_i["DIA"] = day
    last_id_task = df_schedule_i['id'].max()
    df_total_schedule = pd.concat([df_total_schedule, df_schedule_i], ignore_index=True)

df_total_schedule.to_excel('C:/NUEVO_PORTATIL/GITHUB/ASIGNACION/total_schedule.xlsx', index=False)
print(df_total_schedule)

"""
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
