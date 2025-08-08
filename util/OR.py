# DATOS
"""
operarios = ["ninguno", "op1", "op2", "op3", "op4", "op5", "op6", "op7", "op8", "op9", "op10"]

procesos_operarios = {"op1": ["TEL",  "PDI"],
                      "op2": ["TEL",  "PDI"],
                      "op3": ["TEL"],
                      "op4":          ["PDI"],
                      "op5":                    ["LAV"],
                      "op6":                    ["LAV",],
                      "op8":                                ["CAL"],
                      "op9":                                ["CAL"],
                      "op10":                   ["LAV",     "CAL"]
                      }
                      
trabajos = ["tra1", "tra2", "tra3", "tra4", "tra5", "tra6", "tra7", "tra8", "tra9", "tra10", "tra11", "tra12", "tra13", "tra14"]

procesos_trabajos = {"tra1":  [("TEL",10), ("PDI", 5), ("LAV", 45), ("CAL", 8)], 
                     "tra2":  [("TEL",10), ("PDI", 5), ("LAV", 12), ("CAL", 5)], 
                     "tra3":  [("TEL", 0), ("PDI", 7), ("LAV", 12), ("CAL", 30)], 
                     "tra4":  [("TEL", 0), ("PDI", 5), ("LAV", 12), ("CAL", 3)], 
                     "tra5":  [("TEL", 0), ("PDI", 5), ("LAV", 10), ("CAL", 5)], 
                     "tra6":  [("TEL", 0), ("PDI", 5), ("LAV", 32), ("CAL", 5)], 
                     "tra7":  [("TEL", 6), ("PDI", 8), ("LAV", 12), ("CAL", 7)], 
                     "tra8":  [("TEL", 0), ("PDI", 5), ("LAV", 12), ("CAL", 5)], 
                     "tra9":  [("TEL",10), ("PDI", 5), ("LAV", 12), ("CAL", 5)], 
                     "tra10": [("TEL", 4), ("PDI", 5), ("LAV",  0), ("CAL", 5)], 
                     "tra11": [("TEL", 0), ("PDI", 15),("LAV", 16), ("CAL", 6)], 
                     "tra12": [("TEL",30), ("PDI", 5), ("LAV", 12), ("CAL", 5)], 
                     "tra13": [("TEL", 9), ("PDI", 2), ("LAV", 12), ("CAL", 5)], 
                     "tra14": [("TEL",11), ("PDI", 0), ("LAV", 11), ("CAL", 9)]}

precedencias = {
    'prece1' : {    # Precedencia Lineal
        "TEL": [],
        "PDI": ["TEL"],
        "LAV": ["PDI"],
        "CAL": ["LAV"]
        } ,
    'prece2' : {    # A y B sin precedencia, C depende de A y B
        "TEL": [],
        "PDI": [],
        "LAV": ["TEL", "PDI"],
        "CAL": ["LAV"],
        } ,
    'prece3' : {    # A y B sin precedencia, D depende de B y C
        "TEL": [],
        "PDI": [],
        "LAV": ["TEL"],
        "CAL": ["PDI","LAV"],
        } ,
    'prece4' : {    # C sin precedencia, A y B dependen de C
        "LAV": [],
        "TEL": ["LAV"],
        "PDI": ["LAV"],
        "CAL": ["TEL","PDI"],
        }
}

precedencias_trabajos = {
    "tra1":  precedencias["prece1"],
    "tra2":  precedencias["prece1"],
    "tra3":  precedencias["prece2"],
    "tra4":  precedencias["prece2"],
    "tra5":  precedencias["prece3"],
    "tra6":  precedencias["prece3"],
    "tra7":  precedencias["prece4"],
    "tra8":  precedencias["prece4"],
    "tra9":  precedencias["prece1"],
    "tra10": precedencias["prece2"],
    "tra11": precedencias["prece3"],
    "tra12": precedencias["prece4"],
    "tra13": precedencias["prece1"],
    "tra14": precedencias["prece2"]
    }

pesos_trabajo = {
    "tra1": 10,
    "tra2": 10,
    "tra3": 10,
    "tra4": 10,
    "tra5": 10,
    "tra6": 10,
    "tra7": 10,
    "tra8": 10,
    "tra9": 10,
    "tra10": 10,
}
"""


from ortools.sat.python import cp_model
import pandas as pd
class modelOR:
    """
    Clase para encapsular el modelo de programación por restricciones.
    Permite crear, añadir restricciones y resolver el modelo.
    """
    def __init__(self,
                 operarios: list,
                 procesos_operarios: dict,
                 trabajos: list,
                 procesos_trabajos: dict,
                 precedencias_por_trabajo: dict,
                 pesos_trabajo = {},
                 max_horizonte: int = None,
                 jobs_sched: list = None, 
                 opers_sched:list = None,
                 procs_sched:list = None):

        self.operarios = operarios
        self.procesos_operarios = procesos_operarios
        self.trabajos = trabajos
        self.procesos_trabajos = procesos_trabajos
        self.precedencias_por_trabajo = self.__preced_flat__(precedencias_por_trabajo)
        self.pesos_trabajo = pesos_trabajo
        self.jobs_sched  = jobs_sched, 
        self.opers_sched = opers_sched,
        self.procs_sched = procs_sched
        self.tareas = self.__taks_flat_or__()
        self.max_horizonte = sum(t["duracion"] for t in self.tareas) if max_horizonte is not None else max_horizonte
        self.tareas_finales = self.__final_tasks__()
        self.tareas_asignadas = {}
        self.tareas_asignadas_df = None
        self.model  = self.__create_model__()
        self.__add_constr_jobs__()
        self.__add_constr_oper__()
        self.current_objetive = None
        self.OBJ_MIN_MAKESPAN_PONDERADO = "MIN_MAKESPAN_PONDERADO"
        self.OBJ_MIN_MAKESPAN_SIMPLE = "MIN_MAKESPAN_SIMPLE"
        self._functions = { "MIN_MAKESPAN_PONDERADO": self.__obj_min_makespan_pondered__,
                             "MIN_MAKESPAN_SIMPLE": self.__obj_min_makespan__,}

    def __taks_flat_or__(self):
        """
        Aplana la lista de tareas para OR-Tools.
        param operarios: Lista de operarios.
        param procesos_operarios: Diccionario que relaciona operarios con los procesos que pueden realizar.
        param trabajos: Lista de trabajos.
        param procesos_trabajos: Diccionario que relaciona trabajos con los procesos y sus duraciones.
        return: Lista de tareas (diccionarios) con información necesaria para OR-Tools.
        """
            
        # Índices para OR-Tools
        operario_idx = {op: i for i, op in enumerate(self.operarios)}

        # Lista de tareas para OR-Tools
        tareas = []
        id_tarea = 0


        for trabajo_id in self.trabajos:
            print(self.procesos_trabajos)
            print(self.trabajos)
            
            no_en_diccionario = [elem for elem in self.trabajos if elem not in self.procesos_trabajos]
            print("NO EN DICCIONARIO:  ", no_en_diccionario)
            
            no_en_lista = [clave for clave in self.procesos_trabajos if clave not in self.trabajos]
            print("NO EN LISTA:  ", no_en_lista)
    

            lista_procesos = self.procesos_trabajos[trabajo_id]
            for orden, (proceso, duracion) in enumerate(lista_procesos):
                if duracion == 0 or self.procs_sched is None or proceso not in self.procs_sched:
                    continue  # No crear tarea si la duración es 0
                
                # Buscar operarios calificados
                posibles_operarios = [op for op in self.operarios  if  proceso in self.procesos_operarios.get(op, [])]
                
                if not posibles_operarios:
                    print(f"⚠️ Advertencia: No hay operarios que puedan hacer {proceso} en {trabajo_id}")
                tarea = {
                    "id": id_tarea,
                    "trabajo": trabajo_id,
                    "orden": orden,
                    "proceso": proceso,
                    "duracion": duracion,
                    "operarios_posibles": posibles_operarios,
                    "operarios_idx": [operario_idx[op] for op in posibles_operarios]
                }
                tareas.append(tarea)
                id_tarea += 1
                
        return tareas
    
    def __preced_flat__(self, precedencias):
        
        if 'all' in precedencias:
            return { trabajo: precedencias['all']  for trabajo in self.trabajos }
        else:
            return precedencias

    def __final_tasks__(self):
        """ 
        Finaliza las tareas, asegurando que cada trabajo tiene una tarea final.
        return: Lista de tareas finales, una por cada trabajo, con la tarea de mayor orden.
        """
        tareas_finales = []
        for trabajo in set(t["trabajo"] for t in self.tareas):
            orden_max = max(t2["orden"] for t2 in self.tareas if t2["trabajo"] == trabajo)
            tarea_final = next(t for t in self.tareas if t["trabajo"] == trabajo and t["orden"] == orden_max)
            tareas_finales.append(tarea_final)
            
        return tareas_finales
    
    def __create_model__(self):
        """
        Crea un modelo de programación por restricciones para las tareas dadas.
        param tareas: Lista de tareas (diccionarios) con información necesaria para OR-Tools.
        return: Modifica la lista de tareas añadiendo variables objeto de OR-tools para inicio, fin e intervalo.
        """
        model = cp_model.CpModel()

        for tarea in self.tareas:
            # Crear variables de tiempo
            tarea["start_var"] = model.NewIntVar(0, self.max_horizonte, f'start_{tarea["id"]}')
            tarea["end_var"]   = model.NewIntVar(0, self.max_horizonte, f'end_{tarea["id"]}')
            
            # Crear intervalo
            tarea["interval_var"] = model.NewIntervalVar(start = tarea["start_var"],
                                                         size  = tarea["duracion"],
                                                         end   = tarea["end_var"],
                                                         name  = f'interval_{tarea["id"]}' )
            if not tarea["operarios_idx"]:
                
                print(f'La tarea {tarea["id"]} del trabajo {tarea["trabajo"]} no tiene operarios disponibles para el proceso {tarea["proceso"]}.')
                #raise ValueError(f'La tarea {tarea["id"]} del trabajo {tarea["trabajo"]} no tiene operarios disponibles para el proceso {tarea["proceso"]}.')

            # Crear variable de operario (con valores permitidos)
            tarea["op_var"] = model.NewIntVarFromDomain(
                domain = cp_model.Domain.FromValues(tarea["operarios_idx"]),
                name   = f'op_{tarea["id"]}'
            )
        return model
    
    def __add_constr_jobs__(self):
        """ 
        Añade restricciones de precedencia entre tareas de diferentes trabajos en el modelo.
        return: Modifica el modelo añadiendo restricciones de precedencia entre tareas de diferentes trabajos.
        """
        #print('PRECEDENCIAS POR TRABAJO:', self.precedencias_por_trabajo)
        for trabajo, deps_dict in self.precedencias_por_trabajo.items():
            
            # Subconjunto de tareas del trabajo actual
            tareas_trabajo = [t for t in self.tareas if t["trabajo"] == trabajo]             # Filtrar las tareas para obtener solo las que pertenecen a un trabajo específico. 
            tareas_dict = {t["proceso"]: t for t in tareas_trabajo}                          # crear un dicc de tareas para el trabajo actual, donde la clave es el nombre del LAVeso y el valor es la tarea (diccionario) correspondiente.
            
            for t_dic in tareas_dict.items():
                print(t_dic)
            
            for proc_sucesor, lista_predecesores in deps_dict.items():
                if proc_sucesor not in tareas_dict: 
                    continue  # ese proceso no existe en este trabajo
                
                tarea_suc = tareas_dict[proc_sucesor]
                for proc_pre in lista_predecesores:
                    if proc_pre not in tareas_dict:
                        continue  # ese predecesor no existe en este trabajo
                    
                    tarea_pre = tareas_dict[proc_pre]
                    self.model.Add(tarea_pre["end_var"] <= tarea_suc["start_var"])           # Añadir al modelo la restricción de precedencia entre tareas del mismo trabajo.

    def __add_constr_oper__(self):
        """
        Añade restricciones de operarios a las tareas en el modelo.
        return: Modifica el modelo añadiendo restricciones de no solapamiento para los intervalos opcionales de cada operario.
        """
        
        for op_idx in range(len(self.operarios)):        # Para cada índice de operario
            intervalos_op = []

            for t in self.tareas:                        # Para cada tarea
                # Si el operario puede realizar la tarea, añadir su intervalo opcional al modelo.
                if op_idx in t["operarios_idx"]:
                    # Esta tarea puede ser asignada a este operario, así que su intervalo puede entrar solo si la tarea fue realmente asignada a él.
                    
                    presente = self.model.NewBoolVar(f'presente_t{t["id"]}_op{op_idx}')      # Definir una variable booleana que indica si la tarea está asignada al operario.
                    self.model.Add(t["op_var"] == op_idx).OnlyEnforceIf(presente)            # Añadir al modelo la restricción de que la tarea debe ser asignada al operario si la variable booleana es verdadera.
                    self.model.Add(t["op_var"] != op_idx).OnlyEnforceIf(presente.Not())      # Añadir al modelo la restricción de que la tarea no debe ser asignada al operario si la variable booleana es falsa.

                    intervalo_presente = self.model.NewOptionalIntervalVar(                  # Intervalo opcional que se activa si la tarea es asignada al operario.
                                                                    start      = t["start_var"],
                                                                    size       = t["duracion"],
                                                                    end        = t["end_var"],
                                                                    is_present = presente,
                                                                    name       = f'int_opt_t{t["id"]}_op{op_idx}'
                                                                    )

                    intervalos_op.append(intervalo_presente)            #Añadir el intervalo opcional a la lista de intervalos del operario.

            self.model.AddNoOverlap(intervalos_op)                      # Aplicar no solapamiento para este operario

    def __obj_min_makespan__(self):
        
        fin_sum = []

        for t in self.tareas_finales:
            peso = self.pesos_trabajo.get(t["trabajo"], 10)  # por defecto peso 10 si no está en el dict
            var_sum = self.model.NewIntVar(0, self.max_horizonte * peso, f'end_weighted_{t["id"]}')
            self.model.AddMultiplicationEquality(var_sum, [t["end_var"], peso])
            fin_sum.append(var_sum)
            
        # Definir la función objetivo como la suma de los tiempos de finalización
        self.model.Minimize(sum(fin_sum))  # Minimizar la suma de los tiempos de finalización
        print("🎯 Objetivo: Minimizar Makespan simple")
    
    def __obj_min_makespan_pondered__(self):
        
        fin_ponderados = []

        for t in self.tareas_finales:
            peso = self.pesos_trabajo.get(t["trabajo"], 10)  # por defecto peso 10 si no está en el dict
            var_ponderada = self.model.NewIntVar(0, self.max_horizonte * peso, f'end_weighted_{t["id"]}')
            self.model.AddMultiplicationEquality(var_ponderada, [t["end_var"], peso])
            fin_ponderados.append(var_ponderada)
            
        # Definir la función objetivo como la suma de los tiempos ponderados de finalización
        self.model.Minimize(sum(fin_ponderados))  # Minimizar la suma de los tiempos ponderados de finalización
        print("🎯 Objetivo: Minimizar Makespan ponderado")

    def __validate_model__(self):
        """
        Lanza excepción si alguna tarea no tiene operario con la especialidad requerida.
        """
        task_not_oper = []
        for tarea in self.tareas:
            if not tarea["operarios_posibles"]:
                task_not_oper.append(tarea["proceso"])
        if task_not_oper:
            raise ValueError(f"No hay operarios para el proceso {list(set(task_not_oper))}")
    
    def objective_function(self, type_objective: str):
        """Activa la función correspondiente según la constante elegida."""
        try:
            funcion = self._functions[type_objective]
            self.current_objetive = type_objective
            funcion()
        except KeyError:
            raise ValueError(f"Función Objetivo no reconocida: {type_objective}")
        
    def solve_model(self, tiempo_max=5):
        """
        Resuelve el modelo de programación por restricciones.
        return: Diccionario con las tareas asignadas y sus detalles.
        """
                # Validación previa: por ejemplo, verificar si todas las tareas tienen un operario asignable
        try:
            self.__validate_model__()
        except ValueError as e:
            print(f"¡¡MODELO INVÁLIDO!!: No se intentó resolver el modelo: {e}")
            return {}, None  
        
        solver = cp_model.CpSolver()
        solver.parameters.log_search_progress = True
        solver.parameters.max_time_in_seconds = tiempo_max  # Límite en segundos
        status = solver.Solve(self.model)
        print("Tiempo de solución:", solver.WallTime(), "segundos")

        
        if status == cp_model.INFEASIBLE:
            print("MODELO NO RESUELTO: Se intentó resolver el modelo, pero es infactible.")
            return {}, None
        
        elif status == cp_model.MODEL_INVALID:
            print("MODELO NO RESUELTO: Se intentó resolver el modelo, pero es inválido por una razón desconocida.")
            return {}, None
        
        elif status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            if status == cp_model.OPTIMAL:
                type_solution = 'OPTIMAL'
            if status == cp_model.FEASIBLE:
                type_solution = 'FEASIBLE'
            print(f"Solución {type_solution} encontrada:")
            
            tareas_asignadas = {}
            for tarea in self.tareas:
                operario_asignado = self.operarios.iloc[solver.Value(tarea["op_var"])] if solver.Value(tarea["op_var"]) >= 0 else "Ninguno"

                tareas_asignadas[tarea["id"]] = {
                    'id':       tarea["id"],
                    "trabajo":  tarea["trabajo"],
                    "proceso":  tarea["proceso"],
                    "inicio":   solver.Value(tarea["start_var"]),
                    "fin":      solver.Value(tarea["end_var"]),
                    "operario_asignado": operario_asignado
                    }
            print(f"Valor {type_solution} encontrado:", solver.ObjectiveValue())
            
            makespan = max(solver.Value(t["end_var"]) for t in self.tareas)
            self.tareas_asignadas_df = pd.DataFrame(tareas_asignadas).T
            return tareas_asignadas, makespan

"""
model = modelOR(operarios, procesos_operarios, trabajos, procesos_trabajos, precedencias_trabajos, pesos_trabajo)
model.obj_min_makespan_pondered()
model.tareas_asignadas, makespan = model.solve_model(tiempo_max=5)
    
[print(tarea) for tarea in model.tareas_asignadas.values()]
print(makespan)
"""
 
"""
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
 
 
 
 
 
 
 
"""
tareas = taks_flat_or(operarios, procesos_operarios, trabajos, procesos_trabajos)
model = create_model(tareas)
add_constr_jobs(model, tareas, precedencias_trabajos)
add_constr_oper(model, tareas, operarios)
tareas_finales = finalize_tasks(tareas)
finalize_tasks_pondered(tareas_finales, sum(t["duracion"] for t in tareas), pesos_trabajo)
tareas_asignadas, makespan = solve_model(model, tareas, tiempo_max=5)


[print(tarea) for tarea in tareas_asignadas.values()]
print("Makespan:", makespan)


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

dibujar_gantt(list(tareas_asignadas.values()))
"""