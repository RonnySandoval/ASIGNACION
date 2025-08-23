from ortools.sat.python import cp_model
import pandas as pd
from collections import deque
import inspect


class modelOR:
    def __init__(self,
                 operarios: list,
                 procesos_operarios: dict,
                 trabajos: list,
                 procesos_trabajos: dict,
                 precedencias_por_trabajo: dict,
                 pesos_trabajo: dict = {},
                 max_horizonte: int = None,
                 jobs_sched: list = None, 
                 opers_sched:list = None,
                 procs_sched:list = None,
                 last_id_task: int = 0):
        """
        self.tareas: list[dict]
        {
            "id": int,
            "trabajo": str,
            "proceso": str,
            "duracion": int,
            "operarios_idx": list[int],
            "start_var": cp_model.IntVar,
            "end_var": cp_model.IntVar,
            "presente": cp_model.BoolVar,
            "op_var": cp_model.IntVar,
            "presente_operarios_vars": dict[int, cp_model.BoolVar],
            "interval_opt_op": list[Optional[cp_model.IntervalVar]],
            "interval_var": Optional[cp_model.IntervalVar]
        }
        """

        self.operarios = operarios
        self.procesos_operarios = procesos_operarios
        self.trabajos = trabajos
        self.procesos_trabajos = procesos_trabajos
        self.precedencias_por_trabajo = self.__preced_flat__(precedencias_por_trabajo)
        self.pesos_trabajo = pesos_trabajo
        self.jobs_sched  = jobs_sched
        self.opers_sched = opers_sched
        self.procs_sched = procs_sched
        self.operarios_idx = {}
        self.tareas = self.__taks_flat_or__(last_id_task)
        self.max_horizonte = sum(t["duracion"] for t in self.tareas) if max_horizonte is None else max_horizonte
        self.tareas_finales = self.__final_tasks__()
        self.tareas_asignadas = {}
        self.tareas_asignadas_df = None
        self.const_count = -1
        self.__clean_procc_prece__()
        self.__flat_predec_task__()
        self.__create_model__()
        self.__add_constr_jobs__()
        self.__add_constr_oper__()
        self.current_objetive = None
        self.OBJ_MIN_MAKESPAN_WEIGHTED = "MIN_MAKESPAN_WEIGHTED"
        self.OBJ_MIN_MAKESPAN_SIMPLE = "MIN_MAKESPAN_SIMPLE"
        self.OBJ_MAX_NUM_TASK = "MAX_NUM_TASK"
        self._functions = { "MIN_MAKESPAN_WEIGHTED": self.__obj_min_makespan_pondered__,
                            "MIN_MAKESPAN_SIMPLE": self.__obj_min_makespan__,
                            "MAX_NUM_TASK": self.__obj_max_num_task__}
        
    def __taks_flat_or__(self, last_id_task: int):
        operario_idx = {op: i for i, op in enumerate(self.operarios)}
        self.operarios_idx = operario_idx
        tareas = []
        id_tarea = last_id_task + 1 if last_id_task >= 0 else 0
        for trabajo_id in self.trabajos:
            lista_procesos = self.procesos_trabajos[trabajo_id]
            for orden, (proceso, duracion) in enumerate(lista_procesos):
                if (duracion == 0) or ((self.procs_sched is not None)   and   (proceso not in self.procs_sched)):
                    continue
                posibles_operarios = [op for op in self.operarios if proceso in self.procesos_operarios.get(op, [])]
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
            return {trabajo: precedencias['all'] for trabajo in self.trabajos}
        else:
            return precedencias
    
    def __final_tasks__(self):
        tareas_finales = []
        for trabajo in set(t["trabajo"] for t in self.tareas):
            orden_max = max(t2["orden"] for t2 in self.tareas if t2["trabajo"] == trabajo)
            tarea_final = next(t for t in self.tareas if t["trabajo"] == trabajo and t["orden"] == orden_max)
            tareas_finales.append(tarea_final)
        return tareas_finales

    def __clean_procc_prece__(self):
        for trabajo, procesos in self.procesos_trabajos.items():
            # 1. Convertir lista a dict para fácil acceso
            duraciones = dict(procesos)

            # 2. Obtener precedencias originales
            precedencias = self.precedencias_por_trabajo[trabajo]

            # 3. Detectar procesos con duración 0
            procesos_cero = [p for p, t in duraciones.items() if t == 0]

            for p_cero in procesos_cero:
                # Obtener el predecesor del proceso con duración 0
                predecesores = precedencias.get(p_cero, [])

                # Obtener sucesores (quién depende de este proceso)
                sucesores = [proc for proc, preds in precedencias.items() if p_cero in preds]

                # Reasignar precedencias: sucesores ahora dependen del predecesor
                for s in sucesores:
                    precedencias[s] = [p for p in precedencias[s] if p != p_cero] + predecesores

                # Eliminar el proceso de precedencias
                if p_cero in precedencias:
                    del precedencias[p_cero]

                # Eliminar de duraciones
                del duraciones[p_cero]

            # 4. Guardar cambios
            self.procesos_trabajos[trabajo] = list(duraciones.items())
            self.precedencias_por_trabajo[trabajo] = precedencias

    def __flat_predec_task__(self):
        for tarea in self.tareas:
            trabajo = tarea["trabajo"]
            proceso_actual = tarea["proceso"]

            # Lista ordenada de procesos para este trabajo ([(proc, dur), ...])
            secuencia = self.procesos_trabajos[trabajo]

            # Extraer solo los procesos en orden
            procesos_ordenados = [p for p, _ in secuencia]

            # Buscar índice del proceso actual
            idx = procesos_ordenados.index(proceso_actual)

            # Procesos anteriores
            procesos_previos = procesos_ordenados[:idx]

            # Buscar IDs de las tareas anteriores en self.tareas
            ids_previos = [
                t["id"] for t in self.tareas
                if t["trabajo"] == trabajo and t["proceso"] in procesos_previos
            ]

            # Añadir al diccionario de la tarea
            tarea["predecesoras"] = ids_previos

    def __create_model__(self):
        self.model = cp_model.CpModel()
        self.__add_vars__()

    def __add_vars__(self, log: bool = True):
        """
        Crea todas las variables necesarias para el modelo:
        - Variables de tiempo (start, end)
        - Variable de presencia (presente)
        - Variables de presencia por operario
        - Variable de asignación de operario
        - Intervalos opcionales por operario
        - Intervalo opcional general de la tarea
        Además, genera un log con información detallada.
        """

        self.var_index_map = {}  # índice interno ORTools -> (nombre_var, tarea_id)

        # 1. VARIABLES INICIO, FIN, PRESENTE Y DOMINIO DE OPERARIOS POR TAREA
        for tarea in self.tareas:
            tarea["start_var"] = self.model.NewIntVar(0, self.max_horizonte, f'start_{tarea["id"]}')
            tarea["end_var"]   = self.model.NewIntVar(0, self.max_horizonte, f'end_{tarea["id"]}')
            tarea["presente"]  = self.model.NewBoolVar(f'presente_t{tarea["id"]}')
            tarea["op_var"]    = self.model.NewIntVarFromDomain(
                                    cp_model.Domain.FromValues(tarea["operarios_idx"]),
                                    f'op_{tarea["id"]}'
                                )

            # Registrar en var_index_map
            self.var_index_map[tarea["start_var"].Index()] = ("start_var", tarea["id"])
            self.var_index_map[tarea["end_var"].Index()]   = ("end_var", tarea["id"])
            self.var_index_map[tarea["presente"].Index()]  = ("presente", tarea["id"])
            self.var_index_map[tarea["op_var"].Index()]    = ("op_var", tarea["id"])

        # 2. VARIABLES DE PRESENCIA POR OPERARIO
        for t in self.tareas:
            t["presente_operarios_vars"] = {}
            for op_idx in range(len(self.operarios)):
                t["presente_operarios_vars"][op_idx] = self.model.NewBoolVar(
                    f'presente_t{t["id"]}_op{op_idx}'
                )

        # 3. INTERVALOS OPCIONALES POR OPERARIO
        for op_idx in range(len(self.operarios)):
            for t in self.tareas:
                presente_op = t["presente_operarios_vars"][op_idx]
                t[f"interval_opt_op{op_idx}"] = self.model.NewOptionalIntervalVar(
                    t["start_var"],
                    t["duracion"],
                    t["end_var"],
                    presente_op,
                    f'int_opt_t{t["id"]}_op{op_idx}'
                )

        # 4. INTERVALO OPCIONAL GENERAL USANDO `presente`
        self.is_scheduled_vars = {} 
        for tarea in self.tareas:
            self.is_scheduled_vars[tarea["id"]] = tarea["presente"]
            tarea["interval_var"] = self.model.NewOptionalIntervalVar(
                tarea["start_var"],
                tarea["duracion"],
                tarea["end_var"],
                tarea["presente"], 
                f'interval_{tarea["id"]}'
            )
        #GENERAR LOG
        self.__log_variables__() if log == True else None

    def __add_constr_jobs__(self, log:bool = True):
        log_lines = []
        # Organizar tareas por trabajo y por id para búsqueda rápida
        tareas_por_trabajo = {}
        for tarea in self.tareas:
            tareas_por_trabajo.setdefault(tarea["trabajo"], {})
            tareas_por_trabajo[tarea["trabajo"]][tarea["id"]] = tarea

        for tarea in self.tareas:
            trabajo = tarea["trabajo"]
            predecesoras_ids = tarea.get("predecesoras", [])
            for id_pre in predecesoras_ids:
                # Obtener tarea predecesora por id
                tarea_pre = tareas_por_trabajo[trabajo].get(id_pre)
                if tarea_pre is None:
                    # Predecesora no encontrada, ignorar
                    continue
                
                # Restricción precedencia
                self.model.Add(tarea_pre["end_var"] <= tarea["start_var"]).OnlyEnforceIf([ tarea_pre["presente"],
                                                                                           tarea["presente"]])
                log_lines.append(f"R{self.next_iconst}jo "+
                                 f"[Trabajo {trabajo}] ({tarea_pre['proceso']} → {tarea['proceso']}) " +
                                 f" : end({tarea_pre['id']})   <=    start({tarea['id']}) " +
                                 f"[OnlyIf: presente({tarea_pre['id']}), presente({tarea['id']})]" )
                
                # Implicación presencia
                self.model.AddImplication(tarea["presente"],
                                          tarea_pre["presente"])
                log_lines.append(f"R{self.next_iconst}jo " +
                                 f"[Trabajo {trabajo}] ({tarea_pre['proceso']} → {tarea['proceso']}) " +
                                 f" : presente({tarea_pre['id']}) ⇒ presente({tarea['id']}) [Implication]"  )
        
        if log==True:        
            with open("log_constrains.txt", "w", encoding="utf-8") as f:
                f.write("\n=== RESTRICCIONES DE PROCESOS ===\n")
                f.write("\n".join(log_lines))
            
    def __add_constr_oper__(self, log:bool = True):
        log_lines = []

        for t in self.tareas:
            presente_operarios = []
            trabajo = t["trabajo"]
            proceso = t["proceso"]

            for op_idx in range(len(self.operarios)):
                op_nombre = self.operarios[op_idx]
                presente_op = t["presente_operarios_vars"][op_idx]
                presente_operarios.append(presente_op)
                
                if op_idx in t["operarios_idx"]:

                    self.model.AddImplication(presente_op, t["presente"])
                    log_lines.append(f"R{self.next_iconst}op "+
                                     f"[Implication] Tarea {t['id']} [Trabajo: {trabajo}, Proceso: {proceso}, Operario: {op_nombre} (op{op_idx})] asignada ⇒ tarea presente")

                    self.model.Add(t["op_var"] == op_idx).OnlyEnforceIf(presente_op)
                    log_lines.append(f"R{self.next_iconst}op "+
                                     f"[EnforceIf] Tarea {t['id']} [Trabajo: {trabajo}, Proceso: {proceso}, Operario: {op_nombre} (op{op_idx})] Presente  ⇒ op_var = {op_idx}")

                    self.model.Add(t["op_var"] != op_idx).OnlyEnforceIf(presente_op.Not())
                    log_lines.append(f"R{self.next_iconst}op "+
                                     f"[EnforceIf] Tarea {t['id']} [Trabajo: {trabajo}, Proceso: {proceso}, Operario: {op_nombre} (op{op_idx})] NO presente ⇒ op_var ≠ {op_idx}")

                else:
                    self.model.Add(t["presente_operarios_vars"][op_idx] == 0)
                    log_lines.append(f"R{self.next_iconst}op "+
                                     f"[Inhabilitado] Tarea {t['id']} [Trabajo: {trabajo}, Proceso: {proceso}, Operario: {op_nombre} (op{op_idx})] no puede asignarse ⇒ var = 0")

            self.model.Add(sum(presente_operarios) <= 1)
            self.model.Add(sum(presente_operarios) == 1).OnlyEnforceIf(t["presente"])
            self.model.Add(sum(presente_operarios) == 0).OnlyEnforceIf(t["presente"].Not())

            log_lines.append(f"R{self.next_iconst}op " + f"[Max 1] Tarea {t['id']} con máximo 1 operario asignado")
            log_lines.append(f"R{self.next_iconst}op " + f"[Exactamente 1] Tarea {t['id']} presente ⇒ exactamente un operario asignado")
            log_lines.append(f"R{self.next_iconst}op " + f"[Ninguno] Tarea {t['id']} no presente ⇒ 0 operarios asignados")

        for op_idx in range(len(self.operarios)):
            op_nombre = self.operarios[op_idx]
            intervalos_op = []
            for t in self.tareas:
                presente_op = t["presente_operarios_vars"][op_idx]
                intervalo_op = t[f"interval_opt_op{op_idx}"]
                intervalos_op.append(intervalo_op)
                
            self.model.AddNoOverlap(intervalos_op)
            log_lines.append(f"R{self.next_iconst}op " +  f"[No Overlap] Operario: {op_nombre} (op{op_idx}) ⇒ sin traslape entre tareas")

        if log ==True:
            with open("log_constrains.txt", "a", encoding="utf-8") as log:
                log.write("=== RESTRICCIONES DE OPERARIOS ===\n")
                log.write("\n".join(log_lines) + "\n")
            
        return log_lines
    
    def __obj_max_num_task__(self,
                             time_limit:int = None,
                             log:bool = True,
                             check_times:bool = False):
        """
        Función objetivo: maximizar el número de tareas programadas.
        Aplica restricciones para que las tareas no superen el límite de horizonte.
        """
        limit = time_limit if time_limit is not None else self.max_horizonte
        log_lines = []
        # Restricciones y objetivo
        for tarea in self.tareas:
            # Limitar inicio y fin si está presente
            id_constrain = f"R{self.next_iconst}ad "
            self.model.Add(tarea["start_var"] < limit).OnlyEnforceIf(tarea["presente"]).WithName(id_constrain)
            log_lines.append(id_constrain + f"[EnforceIf] Inicio < {limit} para tarea {tarea['id']}")

            id_constrain = f"R{self.next_iconst}ad "
            self.model.Add(tarea["end_var"] <= limit).OnlyEnforceIf(tarea["presente"]).WithName(id_constrain)
            log_lines.append(id_constrain + f"[EnforceIf] Fin <= {limit} para tarea {tarea['id']}")

        # Función objetivo: maximizar tareas presentes
        self.model.Maximize(sum(t["presente"] for t in self.tareas))
        log_lines.append(
            f"FO{self.next_iconst}ad Función objetivo: maximizar suma de tareas presentes ({len(self.tareas)} variables)"
        )
        if log==True:
            with open("log_constrains.txt", "a", encoding="utf-8") as f:
                f.write("\n=== RESTRICCIONES DE LIMITE DE TIEMPO ===\n")
                f.write("\n".join(log_lines))
                    
        return log_lines

    def __obj_min_makespan__(self):
        fin_sum = []
        for t in self.tareas_finales:
            peso = self.pesos_trabajo.get(t["trabajo"], 10)
            var_sum = self.model.NewIntVar(0, self.max_horizonte * peso, f'end_weighted_{t["id"]}')
            self.model.AddMultiplicationEquality(var_sum, [t["end_var"], peso])
            fin_sum.append(var_sum)
        self.model.Minimize(sum(fin_sum))
        print("🎯 Objetivo: Minimizar Makespan simple")
    
    def __obj_min_makespan_pondered__(self):
        fin_ponderados = []
        for t in self.tareas_finales:
            peso = self.pesos_trabajo.get(t["trabajo"], 10)
            var_ponderada = self.model.NewIntVar(0, self.max_horizonte * peso, f'end_weighted_{t["id"]}')
            self.model.AddMultiplicationEquality(var_ponderada, [t["end_var"], peso])
            fin_ponderados.append(var_ponderada)
        self.model.Minimize(sum(fin_ponderados))
        print("🎯 Objetivo: Minimizar Makespan ponderado")

    def objective_function(self, type_objective: str, time_limit: int = None, check_times: bool = False):
        
        if time_limit is not None:
            self.time_limit = time_limit if time_limit is not None else self.max_horizonte
            validaciones = self.__validate_end_earliest_times__(self.time_limit)
            print(f"------ LIMITE DE HORIZONTE: {time_limit} ------")
            
            if check_times ==True:        # validaciones previas
                for tarea in validaciones:
                    print(f"Validación tarea {tarea['id']}: Fin mínimo {tarea['tiempo_fin_min']}, "
                        f"¿cumple límite? {tarea['cumple']}" )
                    
        else:
            self.time_limit = self.max_horizonte
        
        try:
            funcion = self._functions[type_objective]
            self.current_objetive = type_objective
            if "time_limit" in inspect.signature(funcion).parameters:
                funcion(time_limit=self.time_limit)
            else:
                funcion()
        except KeyError:
            raise ValueError(f"Función Objetivo no reconocida: {type_objective}")
        
        with open("model.txt", "w") as f:
            f.write(str(self.model.Proto()))

    def solve_model(self, solver_time = 5, check_times = False):
        try:
            self.__validate_operators__()
        except ValueError as e:
            print(f"¡¡MODELO INVÁLIDO!!: No se intentó resolver el modelo: {e}")
            return {}, None
        
        solver = cp_model.CpSolver()
        solver.parameters.cp_model_probing_level = 2
        #solver.parameters.log_search_progress = True
        solver.parameters.max_time_in_seconds = solver_time
        status = solver.Solve(self.model)
        print("Tiempo de solución:", solver.WallTime(), "segundos")
        #print(solver.ResponseStats())


        if status == cp_model.INFEASIBLE:
            print("MODELO NO RESUELTO: Es infactible.")
            return {}, None
        elif status == cp_model.MODEL_INVALID:
            print("MODELO NO RESUELTO: Es inválido.")
            return {}, None
        elif status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            type_solution = 'OPTIMAL' if status == cp_model.OPTIMAL else 'FEASIBLE'
            print(f"Solución {type_solution} encontrada:")
            self.__check_times_solver__(solver) if check_times == True else None

            tareas_asignadas = {}
            for tarea in self.tareas:
                # si existe is_scheduled, use esa. Si no, caiga en presente (compatibilidad)
                is_sched_var = tarea.get("is_scheduled", tarea["presente"])
                presente = solver.Value(is_sched_var)
                if presente:
                    operario_asignado = self.operarios[solver.Value(tarea["op_var"])] if solver.Value(tarea["op_var"]) >= 0 else "Ninguno"
                    inicio = solver.Value(tarea["start_var"])
                    fin = solver.Value(tarea["end_var"])
                else:
                    operario_asignado = "Ninguno"
                    inicio = None
                    fin = None

                tareas_asignadas[tarea["id"]] = {
                    'id': tarea["id"],
                    "trabajo": tarea["trabajo"],
                    "proceso": tarea["proceso"],
                    "inicio": inicio,
                    "fin": fin,
                    "operario_asignado": operario_asignado,
                    #"presente": int(presente)
                }

            print(f"Valor objetivo {type_solution}:", solver.ObjectiveValue())
            makespan = max(solver.Value(t["end_var"]) for t in self.tareas if solver.Value(t["presente"]) == 1)
            self.tareas_asignadas_df = pd.DataFrame(tareas_asignadas).T
            return tareas_asignadas, makespan
            
    def str_sequences(self):
        lines = []
        for trabajo, precedencias in self.precedencias_por_trabajo.items():
            # Encontrar el primero (sin precedencias)
            secuencia = []
            restantes = set(precedencias.keys())
            while restantes:
                siguiente = next((p for p in restantes if all(pre not in restantes for pre in precedencias[p])), None)
                if siguiente is None:
                    break  # Evitar bucle infinito si hay ciclo
                restantes.remove(siguiente)
                # Buscar el tiempo del proceso (si existe en self.procesos_trabajos)
                tiempo = dict(self.procesos_trabajos.get(trabajo, [])).get(siguiente, None)
                if tiempo is not None:
                    secuencia.append(f"{siguiente}({tiempo})")
                else:
                    secuencia.append(siguiente)
            lines.append(f"{trabajo}: {' → '.join(secuencia)}")
        return "\n".join(lines)

    def resume(self):
        print("\n--- TAREAS APLANADAS ---")
        for tarea in self.tareas:
            id_tarea = tarea.get("id", "N/A")
            trabajo = tarea.get("trabajo", "N/A")
            proceso = tarea.get("proceso", "N/A")
            duracion = tarea.get("duracion", "N/A")
            ops = ", ".join(tarea.get("operarios_posibles", [])) or "Ninguno"
            print(f"[{id_tarea:>3}] Trabajo: {trabajo:<6} | Proceso: {proceso:<10} | Duración: {duracion:<3} | Ops posibles: {ops}")

        print("\n--- TAREAS ASIGNADAS ---")
        if not self.tareas_asignadas:
            print("(No hay tareas asignadas aún)")
            return

        for tarea_id, tarea in self.tareas_asignadas.items():
            trabajo = tarea.get("trabajo", "N/A")
            proceso = tarea.get("proceso", "N/A")
            inicio = tarea.get("inicio", "N/A")
            fin = tarea.get("fin", "N/A")
            presente = "Sí" if tarea.get("presente", 0) else "No"
            operario = tarea.get("operario_asignado", "N/A")
            print(f"[{tarea_id:>3}] Trabajo: {trabajo:<6} | Proceso: {proceso:<10} | Inicio: {inicio:<3} | Fin: {fin:<3} | Presente: {presente:<2} | Operario: {operario}")

    @property
    def next_iconst(self):
        self.const_count += 1
        return f"{self.const_count:07d}"
 
    def validate_consistency(self, time_limit=None):
        errores = []
        tareas = self.tareas
        
        # 1. Validar límite de horizonte y tareas presentes
        for tarea in tareas:
            fin_minimo = tarea.get("fin_minimo", None)
            id_tarea = tarea["id"]
            esta_presente = tarea.get("presente_valor", True)
            
            if fin_minimo is not None and time_limit is not None:
                if fin_minimo > time_limit and esta_presente:
                    errores.append(f"Tarea {id_tarea} tiene fin mínimo {fin_minimo} > límite {time_limit} pero está marcada como presente.")
            
        # 2. Validar coherencia en predecesoras y sucesoras según presencia
        id_a_tarea = {t["id"]: t for t in tareas}
        for tarea in tareas:
            id_tarea = tarea["id"]
            esta_presente = tarea.get("presente_valor", True)
            # Si la tarea está presente, todas sus predecesoras deben poder estar presentes
            for pred_id in tarea.get("predecesoras", []):
                tarea_pred = id_a_tarea.get(pred_id)
                if tarea_pred is None:
                    errores.append(f"Tarea {id_tarea} tiene predecesora desconocida {pred_id}")
                    continue
                pred_presente = tarea_pred.get("presente_valor", True)
                if esta_presente and not pred_presente:
                    errores.append(f"Tarea {id_tarea} está presente pero su predecesora {pred_id} NO está presente.")
            # Si la tarea no está presente, sus sucesoras tampoco deberían estar presentes
            if not esta_presente:
                for suc in tarea.get("sucesoras", []):
                    tarea_suc = id_a_tarea.get(suc)
                    if tarea_suc and tarea_suc.get("presente_valor", True):
                        errores.append(f"Tarea {id_tarea} NO está presente pero su sucesora {suc} está presente.")
                        
        # 3. Validar asignación posible de operarios
        for tarea in tareas:
            operarios_validos = tarea.get("operarios_idx", [])
            if tarea.get("presente_valor", True) and len(operarios_validos) == 0:
                errores.append(f"Tarea {tarea['id']} está presente pero NO tiene operarios habilitados.")
                
        
        if errores:
            print("### Errores de consistencia detectados:")
            for e in errores:
                print(" -", e)
            return False
        else:
            print("Validación previa: no se detectaron errores de consistencia.")
            return True

    def __validate_operators__(self):
        print( f"Total trabajos: {len(self.trabajos)}, "
            f"Total operarios: {len(self.operarios)}, "
            f"Total tareas: {len(self.tareas)}, "
            f"max horizonte: {self.max_horizonte}, "
            f"time limit: {self.time_limit}")

        #print("Duraciones de tareas:", [t['duracion'] for t in self.tareas])

        task_not_oper = []
        for tarea in self.tareas:
            if not tarea["operarios_posibles"]:
                task_not_oper.append(tarea["proceso"])
        if task_not_oper:
            raise ValueError(f"No hay operarios para el proceso {list(set(task_not_oper))}")

    def __validate_end_earliest_times__(self, time_limit:int):
        resultados = []
        # Mapeo rápido de id_tarea -> duración
        duraciones = {t["id"]: t["duracion"] for t in self.tareas}

        for tarea in self.tareas:
            # Sumar duraciones de las predecesoras
            tiempo_predecesoras = sum(duraciones[pid] for pid in tarea["predecesoras"])

            # Tiempo mínimo de finalización
            tiempo_fin_min = tiempo_predecesoras + tarea["duracion"]

            # Comparar con horizonte
            cumple = tiempo_fin_min <= time_limit

            resultados.append({
                "id": tarea["id"],
                "trabajo": tarea["trabajo"],
                "proceso": tarea["proceso"],
                "tiempo_fin_min": tiempo_fin_min,
                "cumple": cumple
            })

        return resultados 

    def __check_times_solver__(self, solver):
        """
        Verifica si las tareas finalizan dentro del horizonte, usando los valores del solver.
        """
        print("\n--- Verificación de tiempos (Solver) ---")
        for tarea in self.tareas:
            start_val = solver.Value(tarea["start_var"])
            end_val = solver.Value(tarea["end_var"])
            presente_val = solver.Value(tarea["presente"])
            
            if presente_val:
                # Mostramos predecesoras y tiempos
                print(f"Tarea {tarea['id']} ({tarea['trabajo']} - {tarea['proceso']}): "
                    f"start={start_val}, end={end_val}, límite={self.time_limit}, "
                    f"pred={tarea['predecesoras']}")

                if end_val > self.time_limit:
                    print(f"  ⚠️ ALERTA: excede el límite por {end_val - self.time_limit}unid")
        
        print("--- Fin de verificación ---\n")

    def _format_var_log(self, var, tarea, comment=""):
        """
        Devuelve un string formateado con la info detallada de la variable y la tarea.
        """
        return (f"Tarea ID {tarea['id']} "
                f"(Proceso={tarea.get('proceso','N/A')}, "
                f"Duración={tarea.get('duracion','N/A')}, "
                f"Trabajo={tarea.get('trabajo','N/A')}), "
                f"Variable: {var.Name()} "
                f"[{comment}]\n")
   
    def __log_variables__(self, filename="log_variables.txt"):
        """
        Genera un log plano con:
        Proceso, Operario, Trabajo, ID_tarea, Tipo de variable OR-Tools,
        nombre OR-Tools, clave en el diccionario y ID interno de OR-Tools.
        """
        def log_var(var, tarea, clave_dic, operario=None):
            if var is None:
                return ""
            tipo_var = type(var).__name__  # Ej: IntVar, IntervalVar, BoolVar
            return (
                f"Proceso={tarea.get('proceso', 'N/A')} | "
                f"Operario={operario if operario is not None else 'N/A'} | "
                f"Trabajo={tarea.get('trabajo', 'N/A')} | "
                f"ID_tarea={tarea.get('id', 'N/A')} | "
                f"Tipo={tipo_var} | "
                f"Nombre_ORtools={var.Name()} | "
                f"Clave_diccionario={clave_dic} | "
                f"ID_ORTools={var.Index()}\n"
            )

        with open(filename, "w", encoding="utf-8") as log:
            log.write("===== VARIABLES DEL MODELO =====\n")

            # --- Variables de Tiempo ---
            for tarea in self.tareas:
                log.write(log_var(tarea["start_var"], tarea, "start_var"))
                log.write(log_var(tarea["end_var"], tarea, "end_var"))

            # --- Variables de Presencia ---
            for tarea in self.tareas:
                log.write(log_var(tarea["presente"], tarea, "presente"))
                for op_idx, var in tarea["presente_operarios_vars"].items():
                    log.write(log_var(var, tarea, "presente_operarios_vars", op_idx))

            # --- Variables de Asignación de Operario ---
            for tarea in self.tareas:
                log.write(log_var(tarea["op_var"], tarea, "op_var"))

            # --- Intervalos Opcionales por Operario ---
            for tarea in self.tareas:
                for op_idx in range(len(self.operarios)):
                    interval_key = f"interval_opt_op{op_idx}"
                    if interval_key in tarea:
                        log.write(log_var(tarea[interval_key], tarea, interval_key, op_idx))

            # --- Intervalo principal ---
            for tarea in self.tareas:
                if "interval_var" in tarea:
                    log.write(log_var(tarea["interval_var"], tarea, "interval_var"))

        print(f"📄 Log de variables guardado en: {filename}")
