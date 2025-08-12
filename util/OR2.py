from ortools.sat.python import cp_model
import pandas as pd
from collections import deque

def verificar_factibilidad_horizonte(self, time_limit: int = None):
    """
    Verifica factibilidad por trabajo (grupo de procesos) respecto a un horizonte.
    - Si time_limit no se pasa, usa self.time_limit o self.max_horizonte.
    - Para cada trabajo calcula earliest_finish (pase hacia adelante) y
      detecta tareas que necesariamente NO pueden terminar antes del límite.
    - Imprime la ruta crítica, acumulados y las tareas 'fuera' (las que no caben).
    """
    # resolver límite
    if time_limit is None:
        time_limit = getattr(self, "time_limit", None)
    if time_limit is None:
        time_limit = getattr(self, "horizonte", None)
    if time_limit is None:
        time_limit = getattr(self, "max_horizonte", None)
    if time_limit is None:
        raise ValueError("No se encontró time_limit ni self.time_limit ni self.max_horizonte.")

    print("\n[VERIFICANDO FACTIBILIDAD DEL HORIZONTE]")
    print(f"Horizonte máximo permitido: {time_limit}")

    # Agrupar tareas por trabajo (si no hay campo 'trabajo', se agrupan en '_SIN_TRABAJO')
    trabajos = {}
    for t in self.tareas:
        key = t.get("trabajo", "_SIN_TRABAJO")
        trabajos.setdefault(key, []).append(t)

    any_problem = False

    for trabajo, tareas in trabajos.items():
        print(f"\n== Trabajo: {trabajo} (nº tareas: {len(tareas)}) ==")

        # Mapas rápidos
        id_map = {t["id"]: t for t in tareas}

        # Construir listas de predecesores y sucesores (solo dentro del mismo trabajo)
        preds = {tid: [] for tid in id_map}
        succs = {tid: [] for tid in id_map}

        for t in tareas:
            tid = t["id"]
            # soporta distintos nombres para la lista de predecesores
            raw_preds = t.get("precedencias") or t.get("predecesoras") or t.get("predecessors") or []
            # filtrar solo los predecesores que estén en el mismo trabajo
            p_list = [p for p in raw_preds if p in id_map]
            preds[tid] = p_list
            for p in p_list:
                succs[p].append(tid)

        # 1) Chequeo rápido: tarea individual más larga que el límite
        for t in tareas:
            if t.get("duracion", 0) > time_limit:
                print(f"❌ Tarea {t['id']} dura {t['duracion']} y excede el límite por sí sola.")
                any_problem = True

        # 2) Pase hacia adelante (CPM) para earliest_finish usando Kahn (topological)
        indeg = {tid: len(preds[tid]) for tid in id_map}
        q = deque([tid for tid, d in indeg.items() if d == 0])

        earliest_finish = {}             # earliest_finish[tid] = tiempo mínimo en el que puede terminar
        pred_for_ef = {}                 # para reconstruir la cadena que definió ese earliest_finish
        processed = 0

        while q:
            u = q.popleft()
            processed += 1
            if preds[u]:
                # earliest start = max(earliest_finish[p] for p in preds[u])
                pred_max = max(preds[u], key=lambda p: earliest_finish.get(p, 0))
                est = earliest_finish.get(pred_max, 0)
                earliest_finish[u] = est + int(id_map[u].get("duracion", 0))
                pred_for_ef[u] = pred_max
            else:
                earliest_finish[u] = int(id_map[u].get("duracion", 0))
                # pred_for_ef no existe para raíces

            # propagar
            for v in succs[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)

        if processed != len(id_map):
            print("⚠️  Se detectó un ciclo en las precedencias de este trabajo; algunas rutas no pudieron ordenarse topológicamente.")
            # No abortamos: intentamos detectar lo que sí podamos
            any_problem = True

        if not earliest_finish:
            print("⚠️  No se pudo calcular earliest_finish (posible problema de datos).")
            continue

        # 3) Encontrar tareas cuyo earliest_finish > time_limit (imposibles)
        impossible_tasks = [tid for tid, ef in earliest_finish.items() if ef > time_limit]
        if not impossible_tasks:
            print("✅ Todas las tareas (según precedencias) pueden terminar antes del límite.")
        else:
            any_problem = True
            print(f"❌ Tareas que NO pueden terminar antes del límite ({time_limit}):")
            # ordenarlas por earliest_finish descendente (más críticas primero)
            for tid in sorted(impossible_tasks, key=lambda x: earliest_finish[x], reverse=True):
                ef = earliest_finish[tid]
                # reconstruir camino que definió earliest_finish[tid]
                path = []
                cur = tid
                while True:
                    path.append(cur)
                    if cur in pred_for_ef:
                        cur = pred_for_ef[cur]
                    else:
                        break
                path = list(reversed(path))  # desde raíz hasta 'tid'

                # calcular duraciones y acumulados en ese camino
                duraciones = [int(id_map[n].get("duracion", 0)) for n in path]
                acumulados = []
                s = 0
                for d in duraciones:
                    s += d
                    acumulados.append(s)

                # primer índice donde se supera el límite
                idx_exceed = next((i for i, c in enumerate(acumulados) if c > time_limit), None)
                tareas_fuera = path[idx_exceed:] if idx_exceed is not None else []

                print(f" - Tarea {tid}: earliest_finish={ef}")
                print(f"   Camino crítico (raíz → ... → tarea): {' → '.join(map(str, path))}")
                print(f"   Duraciones: {duraciones}")
                print(f"   Acumulados: {acumulados}")
                if tareas_fuera:
                    print(f"   → Se excede en el índice {idx_exceed}, tareas fuera: {' → '.join(map(str, tareas_fuera))}")
                else:
                    print("   → Se excede pero no se identificaron tareas fuera (caso extraño).")

        # 4) Informar la mayor cadena / ruta crítica global del trabajo
        tid_max = max(earliest_finish.keys(), key=lambda k: earliest_finish[k])
        ef_max = earliest_finish[tid_max]
        # reconstruir ruta crítica global
        path = []
        cur = tid_max
        while True:
            path.append(cur)
            if cur in pred_for_ef:
                cur = pred_for_ef[cur]
            else:
                break
        path = list(reversed(path))
        print(f"Mayor cadena encontrada (earliest_finish={ef_max}): {' → '.join(map(str, path))}")
        if ef_max > time_limit:
            print(f"  (esta cadena supera el límite por {ef_max - time_limit} unidades)")

    if any_problem:
        print("\nResultado: SE ENCONTRARON PROBLEMAS DE FACTIBILIDAD con el horizonte dado.")
        return False
    else:
        print("\nResultado: TODO CABE DENTRO DEL HORIZONTE.")
        return True


class modelOR:
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
        self.jobs_sched  = jobs_sched
        self.opers_sched = opers_sched
        self.procs_sched = procs_sched
        self.tareas = self.__taks_flat_or__()
        self.max_horizonte = sum(t["duracion"] for t in self.tareas) if max_horizonte is None else max_horizonte
        self.tareas_finales = self.__final_tasks__()
        self.tareas_asignadas = {}
        self.tareas_asignadas_df = None
        self.__clean_procc_prece__()
        self.__flat_predec_task__()
        self.model  = self.__create_model__()
        self.const_count = -1
        self.__add_constr_jobs__()
        self.__add_constr_oper__()
        self.current_objetive = None
        self.OBJ_MIN_MAKESPAN_PONDERADO = "MIN_MAKESPAN_PONDERADO"
        self.OBJ_MIN_MAKESPAN_SIMPLE = "MIN_MAKESPAN_SIMPLE"
        self.OBJ_MAX_NUM_TASK = "MAX_NUM_TASK"
        self._functions = {
            "MIN_MAKESPAN_PONDERADO": self.__obj_min_makespan_pondered__,
            "MIN_MAKESPAN_SIMPLE": self.__obj_min_makespan__,
            "MAX_NUM_TASK": self.__obj_max_num_task__  # agregada función para maximizar tareas
        }
        
    def __taks_flat_or__(self):
        operario_idx = {op: i for i, op in enumerate(self.operarios)}
        tareas = []
        id_tarea = 0
        for trabajo_id in self.trabajos:
            lista_procesos = self.procesos_trabajos[trabajo_id]
            for orden, (proceso, duracion) in enumerate(lista_procesos):
                if (duracion == 0) or (  (self.procs_sched is not None)   and   (proceso not in self.procs_sched)  ):
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
    
    def __create_model__(self):
        model = cp_model.CpModel()
        self.var_index_map = {}  # Diccionario: índice interno ORTools -> (nombre_var, tarea_id)

        for tarea in self.tareas:
            # Crear variables
            tarea["start_var"] = model.NewIntVar(0, self.max_horizonte, f'start_{tarea["id"]}')
            tarea["end_var"] = model.NewIntVar(0, self.max_horizonte, f'end_{tarea["id"]}')
            tarea["presente"] = model.NewBoolVar(f'presente_t{tarea["id"]}')
            tarea["op_var"] = model.NewIntVarFromDomain(cp_model.Domain.FromValues(tarea["operarios_idx"]),
                                                        f'op_{tarea["id"]}' )

            self.var_index_map[tarea["start_var"].Index()] = ("start_var", tarea["id"])
            self.var_index_map[tarea["end_var"].Index()] = ("end_var", tarea["id"])
            self.var_index_map[tarea["presente"].Index()] = ("presente", tarea["id"])
            self.var_index_map[tarea["op_var"].Index()] = ("op_var", tarea["id"])

        # Log con información adicional
        with open('log_variables.txt', "w", encoding="utf-8") as log:
            for idx, (var_name, tarea_id) in sorted(self.var_index_map.items()):
                tarea = next((t for t in self.tareas if t["id"] == tarea_id), None)
                if tarea:
                    proceso = tarea.get("proceso", "N/A")
                    duracion = tarea.get("duracion", "N/A")
                    trabajo = tarea.get("trabajo", "N/A")
                    log.write(f"{idx} : Tarea ID {tarea_id} (Proceso={proceso}, Duracion={duracion}, Trabajo={trabajo}), Variable: {var_name}\n")

        return model


    def __add_constr_jobs__(self):
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
                id_constrain = f"R{self.next_iconst}jo "
                self.model.Add(tarea_pre["end_var"] <= tarea["start_var"]).OnlyEnforceIf(
                    [tarea_pre["presente"], tarea["presente"]]).WithName(id_constrain)
                log_lines.append(id_constrain + f"[Trabajo {trabajo}] ({tarea_pre['proceso']} → {tarea['proceso']}) " +
                                 f":   end({tarea_pre['id']})   <=    start({tarea['id']}) " +
                                 f"[OnlyIf: presente({tarea_pre['id']}), presente({tarea['id']})]" )
                
                if self.const_count == 12:
                    print(f"Creando restricción {id_constrain} para tareas {tarea_pre['id']} y {tarea['id']}")
                    print(f"  Condición: presente({tarea_pre['id']}) ⇒ presente({tarea['id']})")
                    print(f"  Duraciones: tarea {tarea_pre['id']}={tarea_pre['duracion']}, tarea {tarea['id']}={tarea['duracion']}")
                
                # Implicación presencia
                id_constrain = f"R{self.next_iconst}jo "
                self.model.AddImplication(tarea["presente"], tarea_pre["presente"]).WithName(id_constrain)
                log_lines.append(id_constrain + f"[Trabajo {trabajo}] ({tarea_pre['proceso']} → {tarea['proceso']}) " +
                                 f" : presente({tarea_pre['id']}) ⇒ presente({tarea['id']}) [Implication]"  )
                
                if self.const_count == 12:
                    print(f"Creando restricción {id_constrain} para tareas {tarea_pre['id']} y {tarea['id']}")
                    print(f"  Condición: presente({tarea['id']}) ⇒ presente({tarea_pre['id']})")
                    print(f"  Duraciones: tarea {tarea_pre['id']}={tarea_pre['duracion']}, tarea {tarea['id']}={tarea['duracion']}")
                        
        with open("log_constrains.txt", "w", encoding="utf-8") as f:
            f.write("\n=== RESTRICCIONES DE PROCESOS ===\n")
            f.write("\n".join(log_lines))
            
    def __add_constr_oper__(self):
        log_lines = []
        log_lines.append("=== RESTRICCIONES DE OPERARIOS ===")

        for t in self.tareas:
            presente_operarios = []
            t["presente_operarios_vars"] = {}
            trabajo = t["trabajo"]
            proceso = t["proceso"]

            for op_idx in range(len(self.operarios)):
                op_nombre = self.operarios[op_idx]
                if op_idx in t["operarios_idx"]:
                    presente_op = self.model.NewBoolVar(f'presente_t{t["id"]}_op{op_idx}')
                    t["presente_operarios_vars"][op_idx] = presente_op
                    presente_operarios.append(presente_op)

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
                    t["presente_operarios_vars"][op_idx] = self.model.NewBoolVar(f'presente_t{t["id"]}_op{op_idx}')
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
                intervalo_op = self.model.NewOptionalIntervalVar(
                    t["start_var"], t["duracion"], t["end_var"], presente_op,
                    f'int_opt_t{t["id"]}_op{op_idx}')
                intervalos_op.append(intervalo_op)
            self.model.AddNoOverlap(intervalos_op)
            log_lines.append(f"R{self.next_iconst}op " +
                             f"[No Overlap] Operario: {op_nombre} (op{op_idx}) ⇒ sin traslape entre tareas")


        with open("log_constrains.txt", "a", encoding="utf-8") as log:
            log.write("\n".join(log_lines) + "\n")
        return log_lines
            
    def __obj_max_num_task__(self, time_limit=None):
        validaciones = self.__validate_end_earliest_times__(time_limit=time_limit)
        print(f"------ LIMITE DE HORIZONTE: {time_limit}------")
        
        
        log_lines = []
        for tarea in validaciones:
            print(f"Validación tarea {tarea['id']}: Fin mínimo {tarea['tiempo_fin_min']}, ¿cumple límite? {tarea['cumple']}")

        self.is_scheduled_vars = {}
        for tarea in self.tareas:
            tarea["is_scheduled"] = self.model.NewBoolVar(f'scheduled_{tarea["id"]}')
            self.is_scheduled_vars[tarea["id"]] = tarea["is_scheduled"]

            id_constrain = f"R{self.next_iconst}ad "
            self.model.Add(tarea["presente"] == tarea["is_scheduled"]).WithName(id_constrain)
            log_lines.append(id_constrain + f"Restricción: presente({tarea['id']}) == scheduled_{tarea['id']}")

            tarea["interval_var"] = self.model.NewOptionalIntervalVar(
                tarea["start_var"],
                tarea["duracion"],
                tarea["end_var"],
                tarea["is_scheduled"],
                f'interval_{tarea["id"]}'
            )

            limite = time_limit if time_limit is not None else self.max_horizonte
            id_constrain = f"R{self.next_iconst}ad "
            self.model.Add(tarea["start_var"] < limite).OnlyEnforceIf(tarea["is_scheduled"]).WithName(id_constrain)
            
            id_constrain = f"R{self.next_iconst}ad "
            self.model.Add(tarea["end_var"] <= limite).OnlyEnforceIf(tarea["is_scheduled"]).WithName(id_constrain)
            
            log_lines.append(id_constrain + f"[EnforceIf] Límite de tiempo de tarea {tarea['id']}. Inicio < {limite}")
            log_lines.append(id_constrain + f"[EnforceIf] Límite de tiempo de tarea {tarea['id']}. Final <= {limite}")

        if time_limit is not None:
            for tarea in self.tareas:
                for sucesora in tarea.get("sucesoras", []):
                    id_constrain = f"R{self.next_iconst}ad "
                    self.model.AddImplication(tarea["is_scheduled"].Not(), sucesora["is_scheduled"].Not()).WithName(id_constrain)
                    log_lines.append(id_constrain  +  f"[Implication] Si tarea {tarea['id']} NO programada, sucesora {sucesora['id']} NO programada")

                for pred_id in tarea.get("predecesoras", []):
                    id_constrain = f"R{self.next_iconst}ad "
                    self.model.AddImplication(self.is_scheduled_vars[pred_id].Not(),tarea["is_scheduled"].Not()).WithName(id_constrain)
                    log_lines.append(id_constrain  +  f"[Implication] Si predecesora {pred_id} NO programada, tarea {tarea['id']} NO programada")

        self.model.Maximize(sum(self.is_scheduled_vars.values()))
        log_lines.append(f"FO{self.next_iconst}ad " + f"Función objetivo: maximizar suma de tareas programadas: {len(self.is_scheduled_vars)} variables")

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

    def __validate_operators__(self):
        print(f"Total tareas: {len(self.tareas)}, max horizonte: {self.max_horizonte}, time limit: {self.time_limit}")
        print("Duraciones de tareas:", [t['duracion'] for t in self.tareas])

        task_not_oper = []
        for tarea in self.tareas:
            if not tarea["operarios_posibles"]:
                task_not_oper.append(tarea["proceso"])
        if task_not_oper:
            raise ValueError(f"No hay operarios para el proceso {list(set(task_not_oper))}")

    def __validate_end_earliest_times__(self, time_limit):
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

    def objective_function(self, type_objective: str, time_limit: int = None):
        if time_limit is not None:
            self.time_limit = time_limit
        
        try:
            funcion = self._functions[type_objective]
            self.current_objetive = type_objective
            funcion(time_limit=self.time_limit)
        except KeyError:
            raise ValueError(f"Función Objetivo no reconocida: {type_objective}")
    
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

    def solve_model(self, tiempo_max=5, check = False):
        try:
            self.__validate_operators__()
        except ValueError as e:
            print(f"¡¡MODELO INVÁLIDO!!: No se intentó resolver el modelo: {e}")
            return {}, None
        
        solver = cp_model.CpSolver()
        solver.parameters.cp_model_probing_level = 2
        solver.parameters.log_search_progress = True
        solver.parameters.max_time_in_seconds = tiempo_max
        status = solver.Solve(self.model)
        print("Tiempo de solución:", solver.WallTime(), "segundos")
        print(solver.ResponseStats())


        if status == cp_model.INFEASIBLE:
            print("MODELO NO RESUELTO: Es infactible.")
            return {}, None
        elif status == cp_model.MODEL_INVALID:
            print("MODELO NO RESUELTO: Es inválido.")
            return {}, None
        elif status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            type_solution = 'OPTIMAL' if status == cp_model.OPTIMAL else 'FEASIBLE'
            print(f"Solución {type_solution} encontrada:")
            self.__check_times_solver__(solver) if check == True else None

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
                    "presente": int(presente)
                }

            print(f"Valor objetivo {type_solution}:", solver.ObjectiveValue())
            makespan = max(solver.Value(t["end_var"]) for t in self.tareas if solver.Value(t["presente"]) == 1)
            self.tareas_asignadas_df = pd.DataFrame(tareas_asignadas).T
            return tareas_asignadas, makespan

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
