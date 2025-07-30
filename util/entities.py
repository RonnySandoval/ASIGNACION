from database import BDcrud as BDcrud
from database import BDmanage as BDman
from . import OR

class Plant():
    def __init__(self, db, jobs: list = None,  opers:list = None, procs:list = None):
            
        crud_P = BDcrud.ProcesosCrud(db)
        crud_V = BDcrud.VehiculosCrud(db)
        crud_TV = BDcrud.TiemposVehiculosCrud(db)
        crud_T = BDcrud.TecnicosCrud(db)
        crud_TP = BDcrud.TecnicosProcesosCrud(db)
        
        self.jobs_sched = jobs
        self.oper_sched = opers
        self.proc_sched = procs
        
        self.df_trabajos = crud_V.leer_vehiculos_df()
        self.df_operarios = crud_T.leer_tecnicos_df()
        self.df_procesos = crud_P.leer_procesos_df()
        self.df_proc_oper = crud_TP.leer_tecnicos_procesos_df()
        self.df_proc_trab = crud_TV.leer_tiempos_vehiculos_df()
        self.trabajos, self.operarios, self.procesos = self.__filter_jobs_opers_procs__()        
        self.precedencias_trabajos = {'all': self.__precedencia_unica__()}
        print(self.df_trabajos, self.df_operarios)
        self.procesos_operarios = {}
        for op in self.operarios:
            procesos = self.df_proc_oper[self.df_proc_oper['ID_TECNICO'] == op]['ID_PROCESO'].tolist()
            self.procesos_operarios[op] = procesos

        self.procesos_trabajos = {}  
        for trab in self.trabajos:
            time_list = []
            procesos = self.df_proc_trab[self.df_proc_trab['CHASIS'] == trab]['ID_PROCESO'].unique()    # Obtener todos los procesos únicos para ese vehículo
            
            for proc in procesos:
                filtro = self.df_proc_trab[ (self.df_proc_trab['CHASIS'] == trab) & 
                                    (self.df_proc_trab['ID_PROCESO'] == proc) ]                 # Filtrar la fila con ese chasis y proceso
                if not filtro.empty:
                    time_list.append((proc, int(filtro['TIEMPO'].iloc[0])))
            
            self.procesos_trabajos[trab] = time_list
        
    def __filter_jobs_opers_procs__(self):
        # Filtra trabajos
        if self.jobs_sched is not None:
            trabajos = self.df_trabajos[self.df_trabajos["CHASIS"].isin(self.jobs_sched)]["CHASIS"].drop_duplicates()
        else:
            trabajos = self.df_trabajos["CHASIS"]

        # Filtra operarios
        if self.oper_sched is not None:
            operarios = self.df_operarios[self.df_operarios["ID_TECNICO"].isin(self.oper_sched)]["ID_TECNICO"].drop_duplicates()
        else:
            operarios = self.df_operarios["ID_TECNICO"]

        # Filtra procesos
        if self.proc_sched is not None:
            df_proc = self.df_procesos[self.df_procesos['ID_PROCESO'].isin(self.proc_sched)].drop_duplicates()
            procesos = dict(zip(df_proc['ID_PROCESO'], df_proc['SECUENCIA']))
        else:
            procesos = dict(zip(self.df_procesos['ID_PROCESO'], self.df_procesos['SECUENCIA']))

        return trabajos, operarios, procesos

    def __precedencia_unica__(self):
        preced = {v: k for k, v in self.procesos.items()}   # Invertir el diccionario: secuencia -> ID_PROCESO
        secuencias_ordenadas = sorted(preced.keys())        # Obtener todas las secuencias disponibles, ordenadas

        precedencia_unica = {}        # Construir el diccionario de precedencia
        for key, val in self.procesos.items():
            prev = [s for s in secuencias_ordenadas if s < val] # Buscar la secuencia anterior más cercana
            if prev:
                secuencia_anterior = prev[-1]                   # la más cercana por debajo
                precedencia_unica[key] = [preced[secuencia_anterior]]
            else:
                precedencia_unica[key] = []
        return precedencia_unica
        



jobs_sched = ['4674JU2856395', '6275UL7396126', '4885UJ1827427', '7405NL9458200', '274NX8288150', '5536FW2733288']
oper_sched = ['JaviSerr288441', 'OscaAria216811', 'SebaFlec602702', 'YersSanc938464', 'ReynSuar766853', 'RicaHern503905', 'DiegTemu886535', 'EdwiArco505661']
proc_sched = ['TEL', 'ENS', 'PIN', 'COD']

db = BDman.Database('C:/NUEVO_PORTATIL/GITHUB/ASIGNACION/planta_con_ensamble1.db')
plant = Plant(db=db,
              jobs=jobs_sched,
              opers=oper_sched,
              procs=proc_sched)

model = OR.modelOR(plant.operarios,
                   plant.procesos_operarios,
                   plant.trabajos,
                   plant.procesos_trabajos,
                   plant.precedencias_trabajos,
                   jobs_sched=jobs_sched,
                   opers_sched=oper_sched,
                   procs_sched=proc_sched)



    
#[print(tarea) for tarea in model.tareas_asignadas.values()]

model.objective_function(type_objective=model.OBJ_MIN_MAKESPAN_SIMPLE)
model.tareas_asignadas, makespan = model.solve_model(tiempo_max=5)
print('makespan:  ', makespan)
print(plant.operarios)
print(model.tareas_asignadas_df)
#for tarea in model.tareas:
#    print(tarea)

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
def dibujar_gantt(tareas_asignadas):
    # Obtener trabajos únicos y asignar colores
    trabajos = sorted(set(t["trabajo"] for t in tareas_asignadas))
    trabajos_idx = {trabajo: i for i, trabajo in enumerate(trabajos)}
    
    # Colores por proceso
    procesos = list(set(t["proceso"] for t in tareas_asignadas))
    colores = plt.cm.get_cmap('tab20', len(procesos))
    color_proc = {proc: colores(i) for i, proc in enumerate(procesos)}

    fig, ax = plt.subplots(figsize=(12, 6))

    for tarea in tareas_asignadas:
        y = trabajos_idx[tarea["trabajo"]]
        inicio = tarea["inicio"]
        duracion = tarea["fin"] - tarea["inicio"]
        color = color_proc[tarea["proceso"]]
        label = f'{tarea["proceso"]} ({tarea["operario_asignado"]})'

        ax.barh(y, duracion, left=inicio, height=0.4, color=color, edgecolor='black')
        ax.text(inicio + duracion / 2, y, label, ha='center', va='center', fontsize=8, color='white')

    ax.set_yticks(range(len(trabajos)))
    ax.set_yticklabels(trabajos)
    ax.set_xlabel('Tiempo')
    ax.set_title('Diagrama de Gantt por Trabajo')
    ax.grid(True, axis='x', linestyle='--', alpha=0.5)

    # Leyenda por proceso
    patches = [mpatches.Patch(color=color_proc[p], label=p) for p in procesos]
    ax.legend(handles=patches, title="Proceso", bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.show()

dibujar_gantt(list(model.tareas_asignadas.values()))
