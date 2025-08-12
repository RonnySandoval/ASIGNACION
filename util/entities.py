from database import BDcrud as BDcrud
from . import OR

class Plant():
    def __init__(self, db, simul:dict = None, jobs: list = None,  opers:list = None, procs:list = None):

        crud = {'Procesos'          : BDcrud.ProcesosCrud(db),
                'Vehiculos'         : BDcrud.VehiculosCrud(db),
                'TiemposVehiculos'  : BDcrud.TiemposVehiculosCrud(db),
                'Tecnicos'          : BDcrud.TecnicosCrud(db),
                'TecnicosProcesos'  : BDcrud.TecnicosProcesosCrud(db),
                'Referencias'       : BDcrud.ReferenciasCrud(db),
                'Modelos'           : BDcrud.ModelosCrud(db),
                'TiemposModelos'    : BDcrud.TiemposModelosCrud(db),
                'Historicos'        : BDcrud.HistoricosCrud(db)}
        
        self.df_operarios = crud['Tecnicos'].leer_tecnicos_df()
        self.df_trabajos  = crud['Vehiculos'].leer_vehiculos_df()
        self.df_procesos  = crud['Procesos'].leer_procesos_df()
        self.df_proc_oper = crud['TecnicosProcesos'].leer_tecnicos_procesos_df()
        self.df_referencias = crud['Referencias'].leer_referencias_modelos_df()
        self.df_modelos_df = crud['Modelos'].leer_modelos_df()
        self.df_tiempos_modelos = crud['TiemposModelos'].leer_procesos_modelos_df()
        self.df_historicos = crud['Historicos'].leer_historicos_completo_df()
        
        if simul is None:
            self.df_trabajos  = crud['Vehiculos'].leer_vehiculos_df()
            self.df_proc_trab = crud['TiemposVehiculos'].leer_tiempos_vehiculos_df()
        else:
            self.df_trabajos  = simul['vehiculos_pedido']
            self.df_proc_trab = simul['tiempos_iniciales']
            self.df_trabajos_inic  = simul['vehiculos_iniciales']
            self.df_proc_trab_inic = simul['tiempos_iniciales']
            self.df_proc_trab_uniq = simul['procesos_unicos']
        self.__flat__()
        if simul is not None:
            self.__flat_initial__()
        
    def __flat__(self, jobs: list = None,  opers:list = None, procs:list = None):
        
        self.jobs_sched, self.oper_sched, self.proc_sched = jobs, opers, procs
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
    
    def __flat_initial__(self):
        self.trabajos_inic = list(self.df_trabajos_inic['CHASIS'])
        self.trabajos_uniq = list(self.df_proc_trab_uniq['CHASIS'])
        self.procesos_inic = dict(zip(self.df_proc_trab_inic['CHASIS'],
                                      self.df_proc_trab_inic['ID_PROCESO']))
        self.procesos_uniq = dict(zip(self.df_proc_trab_uniq['CHASIS'],
                                      self.df_proc_trab_uniq['ID_PROCESO']))

        # Crear un diccionario para almacenar los procesos filtrados por vehículo
        self.procesos_trabajos_inic = {}  
        for trab in self.trabajos_uniq:
            time_list = []
            # Obtener secuencia del proceso inicial
            secuencia_uniq = self.df_procesos.loc[self.df_procesos['ID_PROCESO'] == self.procesos_uniq[trab], 'SECUENCIA']
            procesos = self.df_proc_trab_inic[self.df_proc_trab_inic['CHASIS'] == trab]['ID_PROCESO'].unique()       # Obtener todos los procesos únicos para ese vehículo
            
            for proc in procesos:
                secuencia_proc = self.df_procesos.loc[self.df_procesos['ID_PROCESO'] == proc, 'SECUENCIA']   # Obtener secuencia actual
                
                if not secuencia_proc.empty and not secuencia_uniq.empty:
                    if int(secuencia_proc.iloc[0]) >= int(secuencia_uniq.iloc[0]):
                        tiempo = self.df_proc_trab_inic.loc[(self.df_proc_trab_inic['CHASIS'] == trab)    & 
                                                            (self.df_proc_trab_inic['ID_PROCESO'] == proc),
                                                            'TIEMPO' ]
                        if not tiempo.empty:
                            time_list.append((proc, int(tiempo.iloc[0])))
                            
            self.procesos_trabajos_inic[trab] = time_list
            
        #print(f"-------TOTAL PROCESOS_TRABAJOS_INIC:   {len(self.procesos_trabajos_inic)}----------")
        #print("self.procesos_trabajos_inic:\n" + "\n".join(map(lambda item: f"{item[0]}: {item[1]}", self.procesos_trabajos_inic.items())))

        #print(f"-------TOTAL TRABAJOS_INIC:   {len(set(self.trabajos_inic))}----------")
        #print("self.trabajos_inic:\n" + "\n".join(map(str, self.trabajos_inic)))

        #print(f"-------TOTAL TRABAJOS_UNIQ:   {len(set(self.trabajos_uniq))}----------")
        #print("self.trabajos_uniq:\n" + "\n".join(map(str, self.trabajos_uniq)))
            
    def __filter_jobs_opers_procs__(self):
        # Filtra trabajos
        if self.jobs_sched is not None:
            trabajos = self.df_trabajos[self.df_trabajos["CHASIS"].isin(self.jobs_sched)]["CHASIS"].drop_duplicates()
        else:
            trabajos = list(self.df_trabajos["CHASIS"])

        # Filtra operarios
        if self.oper_sched is not None:
            operarios = self.df_operarios[self.df_operarios["ID_TECNICO"].isin(self.oper_sched)]["ID_TECNICO"].drop_duplicates()
        else:
            operarios = list(self.df_operarios["ID_TECNICO"])

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
    
    def resume(self, completed = False):
        print("\n🔍🔍🔍 Resumen del estado de planta :\n")

        print(f"🧾 Trabajos cargados : {len(self.df_trabajos)}")
        print(f"🧾 Operarios cargados : {len(self.df_operarios)}")
        print(f"🧾 Procesos cargados : {len(self.df_procesos)}")
        print(f"🔗 Especialidades de operario : {len(self.df_proc_oper)}")
        print(f"🔗 Procesos de trabajo   : {len(self.df_proc_trab)}")

        print("\n📌 Filtros activos:")
        print(f"   - Tareas aplanadas : " + f"{len(self.trabajos)} \n➤ {list(self.trabajos)}"
              if completed ==True else f"     • {len(self.trabajos)} de trabajos")
        
        print(f"   - Operarios aplanadas : " +  f"{len(self.operarios)} \n➤ {list(self.operarios)}"
              if completed ==True else f"     • {len(self.operarios)} de operarios")
        
        print(f"   - Procesos aplanados : " + f"{len(self.procesos)}\n ➤ {list(self.procesos.keys())}"
                if completed == True else f"     • {len(self.procesos)} de procesos")
        

        precendencias = list(self.precedencias_trabajos['all'].items())
        especialidades = list(self.procesos_operarios.items())
        tiempos = list(self.procesos_trabajos.items())
        tiempos_inic = list(self.procesos_trabajos_inic.items())
        points = ""

        if completed == False:
            especialidades = especialidades[:5]
            tiempos = tiempos[:5]
            points = "... (filas omitidas)"
            
        print("\n🔁 Precedencias:")
        for proc, prev in precendencias:
            print(f"     • {proc} ← {prev}")
        
        print("\n⚙️  Especialidades Operarios:")
        for op, procs in especialidades:
            print(f"     • Operario {op}: {len(procs)} procesos ➤ {procs}")
        print(points)
        
        print("\n🚗 Procesos y Tiempos por trabajo:")
        for trab, lista in tiempos:
            print(f"     • Trabajo {trab}: {len(lista)} procesos ➤ {lista}")
        print(points)
        
        print("\n      ---->  CONDICIONES INICIALES DE PEDIDO  <----      ")
        print(f"🚗   - Trabajos aplanados : " + f"{len(self.trabajos_inic)} \n➤ {list(self.trabajos_inic)}"
              if completed ==True else f"     • {len(self.trabajos_inic)} de trabajos")
        
        print("\n⚙️ Procesos y Tiempos por trabajo inicial:")
        for trab, lista in tiempos_inic:
            print(f"     • Trabajo {trab}: {len(lista)} procesos ➤ {lista}" )
        print(points)
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
   
class PlantFlat():
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
            trabajos = list(self.df_trabajos["CHASIS"])

        # Filtra operarios
        if self.oper_sched is not None:
            operarios = self.df_operarios[self.df_operarios["ID_TECNICO"].isin(self.oper_sched)]["ID_TECNICO"].drop_duplicates()
        else:
            operarios = list(self.df_operarios["ID_TECNICO"])

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
        

"""

jobs_sched = ['4674JU2856395', '6275UL7396126', '4885UJ1827427', '7405NL9458200', '274NX8288150', '5536FW2733288']
oper_sched = ['JaviSerr288441', 'OscaAria216811', 'SebaFlec602702', 'YersSanc938464', 'ReynSuar766853', 'RicaHern503905', 'DiegTemu886535', 'EdwiArco505661']
proc_sched = ['TEL', 'ENS', 'PIN', 'COD']

with BDman.Database('C:/NUEVO_PORTATIL/GITHUB/ASIGNACION/planta_con_ensamble1.db') as db:
    plant = PlantFlat(db=db,
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
                   procs_sched=proc_sched)"""



    
#[print(tarea) for tarea in model.tareas_asignadas.values()]
"""
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
"""