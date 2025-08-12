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
        for tarea in self.tareas:
            tarea["start_var"] = model.NewIntVar(0, self.max_horizonte, f'start_{tarea["id"]}')
            tarea["end_var"]   = model.NewIntVar(0, self.max_horizonte, f'end_{tarea["id"]}')
            tarea["presente"] = model.NewBoolVar(f'presente_t{tarea["id"]}')
            tarea["op_var"] = model.NewIntVarFromDomain(
                cp_model.Domain.FromValues(tarea["operarios_idx"]),
                f'op_{tarea["id"]}'
            )
        return model
    
    def __add_constr_jobs__(self):
        for trabajo, deps_dict in self.precedencias_por_trabajo.items():
            tareas_trabajo = [t for t in self.tareas if t["trabajo"] == trabajo]
            tareas_dict = {t["proceso"]: t for t in tareas_trabajo}
            for proc_suc, lista_pre in deps_dict.items():
                if proc_suc not in tareas_dict:
                    continue
                tarea_suc = tareas_dict[proc_suc]
                for proc_pre in lista_pre:
                    if proc_pre not in tareas_dict:
                        continue
                    tarea_pre = tareas_dict[proc_pre]
                    # Restricción de precedencia (Regla de "menor que" combinada a presencia de valor lógico)
                    self.model.Add(tarea_pre["end_var"] <= tarea_suc["start_var"]).OnlyEnforceIf(
                        [tarea_pre["presente"], tarea_suc["presente"]]
                    )
                    # Si la sucesora está presente, el predecesor también
                    self.model.AddImplication(tarea_suc["presente"], tarea_pre["presente"])


    
    def __add_constr_oper__(self):
        for t in self.tareas:
            # Lista de variables bool para cada operario posible de la tarea
            presente_operarios = []
            t["presente_operarios_vars"] = {}
            for op_idx in range(len(self.operarios)):
                if op_idx in t["operarios_idx"]:
                    presente_op = self.model.NewBoolVar(f'presente_t{t["id"]}_op{op_idx}')
                    t["presente_operarios_vars"][op_idx] = presente_op
                    presente_operarios.append(presente_op)
                    
                    # Si asignado a ese operario implica tarea presente
                    self.model.AddImplication(presente_op, t["presente"])
                    
                    # Op_var == op_idx si presente_op == True
                    self.model.Add(t["op_var"] == op_idx).OnlyEnforceIf(presente_op)
                    self.model.Add(t["op_var"] != op_idx).OnlyEnforceIf(presente_op.Not())
                else:
                    # Para operarios no posibles, aseguramos que la variable booleana esté en falso (opcional)
                    t["presente_operarios_vars"][op_idx] = self.model.NewBoolVar(f'presente_t{t["id"]}_op{op_idx}')
                    self.model.Add(t["presente_operarios_vars"][op_idx] == 0)
            # Si la tarea está presente, exactamente un operario debe estar asignado
            self.model.Add(sum(presente_operarios) <= 1)
            self.model.Add(sum(presente_operarios) == 1).OnlyEnforceIf(t["presente"])
            self.model.Add(sum(presente_operarios) == 0).OnlyEnforceIf(t["presente"].Not())


        # Añadir restricción de no solapamiento para cada operario
        for op_idx in range(len(self.operarios)):
            intervalos_op = []
            for t in self.tareas:
                presente_op = t["presente_operarios_vars"][op_idx]
                intervalo_op = self.model.NewOptionalIntervalVar(
                    t["start_var"], t["duracion"], t["end_var"], presente_op,
                    f'int_opt_t{t["id"]}_op{op_idx}')
                intervalos_op.append(intervalo_op)
            self.model.AddNoOverlap(intervalos_op)

    def __obj_max_num_task__(self, time_limit=None):
        """
        Maximiza la cantidad de tareas programadas dentro del horizonte o de un límite dado.
        Si una tarea no entra en el límite, sus sucesoras tampoco se programan.
        """
        print("   ---LIMITE DE HORIZONTE---: ", time_limit)
        [print(tarea) for tarea in self.__check_end_earliest_times__(time_limit=time_limit)]
        
        self.is_scheduled_vars = {}
        # Si no se pasó un límite de tiempo, usamos el horizonte máximo
        #limite = getattr(self, "time_limit", self.max_horizonte)
        
        # Crear variables y restricciones por tarea
        for tarea in self.tareas:
            # Variable booleana: 1 si la tarea se programa, 0 si no
            tarea["is_scheduled"] = self.model.NewBoolVar(f'scheduled_{tarea["id"]}')
            self.is_scheduled_vars[tarea["id"]] = tarea["is_scheduled"]

            # conectar con la variable "presente" usada por el resto del modelo
            self.model.Add(tarea["presente"] == tarea["is_scheduled"])
            
            # Intervalo opcional
            tarea["interval_var"] = self.model.NewOptionalIntervalVar(
                tarea["start_var"],
                tarea["duracion"],
                tarea["end_var"],
                tarea["is_scheduled"],
                f'interval_{tarea["id"]}'
            )

            # Restricciones de límite de tiempo
            limite = time_limit if time_limit is not None else self.max_horizonte
            self.model.Add(tarea["start_var"] < limite).OnlyEnforceIf(tarea["is_scheduled"])
            self.model.Add(tarea["end_var"] <= limite).OnlyEnforceIf(tarea["is_scheduled"])

        # Restricción en cascada: si una tarea no se programa, sus sucesoras tampoco
        if time_limit is not None:
            for tarea in self.tareas:
                for sucesora in tarea.get("sucesoras", []):
                    self.model.AddImplication(tarea["is_scheduled"].Not(),  sucesora["is_scheduled"].Not())

        # Función objetivo: maximizar el número de tareas programadas
        self.model.Maximize(sum(self.is_scheduled_vars.values()))

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

    
    def __validate_model__(self):
        print(f"Total tareas: {len(self.tareas)}, max horizonte: {self.max_horizonte}, time limit: {self.time_limit}")
        print("Duraciones de tareas:", [t['duracion'] for t in self.tareas])

        task_not_oper = []
        for tarea in self.tareas:
            if not tarea["operarios_posibles"]:
                task_not_oper.append(tarea["proceso"])
        if task_not_oper:
            raise ValueError(f"No hay operarios para el proceso {list(set(task_not_oper))}")
    
    def objective_function(self, type_objective: str, time_limit: int = None):
        if time_limit is not None:
            self.time_limit = time_limit
        
        try:
            funcion = self._functions[type_objective]
            self.current_objetive = type_objective
            funcion(time_limit=self.time_limit)  # <- lo pasamos aquí
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

    def solve_model(self, tiempo_max=5, debug = False):
        try:
            self.__validate_model__()
        except ValueError as e:
            print(f"¡¡MODELO INVÁLIDO!!: No se intentó resolver el modelo: {e}")
            return {}, None
        
        solver = cp_model.CpSolver()
        solver.parameters.log_search_progress = True
        solver.parameters.max_time_in_seconds = tiempo_max
        status = solver.Solve(self.model)
        print("Tiempo de solución:", solver.WallTime(), "segundos")

        if status == cp_model.INFEASIBLE:
            print("MODELO NO RESUELTO: Es infactible.")
            return {}, None
        elif status == cp_model.MODEL_INVALID:
            print("MODELO NO RESUELTO: Es inválido.")
            return {}, None
        elif status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            type_solution = 'OPTIMAL' if status == cp_model.OPTIMAL else 'FEASIBLE'
            print(f"Solución {type_solution} encontrada:")
            self.__debug_check_solution__(solver) if debug == True else None

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

    def __check_end_earliest_times__(self, time_limit):
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

