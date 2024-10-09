import Mod_clases as mclas


listaOrdenes = []
def programa_inmediato(pedido, tecnicos, horizonte):

    vehiculos_por_programar = pedido.vehiculos.copy()                   # Extrae una copia de la lista de vehiculos
    contador = 0
    while len(vehiculos_por_programar) > 0:

        tiempos_restantes = list(map(lambda vh: sum(vh.tiempos_proceso), vehiculos_por_programar))                      #crea una lista con solo el total de tiempos restante de cada vehiculo
        indice_min_time = tiempos_restantes.index(min(tiempos_restantes))                                               #busca el índice con tiempo restante menor
        vehiculo_min_time = vehiculos_por_programar[indice_min_time]                                                    #busca el índice con tiempo restante menor

        ultimo_estado = vehiculo_min_time.estado                                        #Extrae el ultimo estado en el constructor
        siguiente_estado = mclas.orden_procesos[mclas.orden_procesos.index(ultimo_estado) + 1]      #Obtiene el siguiente estado o proceso de la secuencia
        print(f"{vehiculo_min_time.id_chasis} necesita {siguiente_estado}")

        tecnicos_disponibles = list(filter(lambda persona: siguiente_estado in persona.especializacion, tecnicos))      # incluye soloaquellos técnicos de la especialidad correcta
        tecnicos_disponibles.sort(key = lambda op: op.termina)                                                          #ordena técnicos por tiempo de menor a mayor

        
        tiempos_disponibles = list(map(lambda operario: operario.termina, tecnicos_disponibles))                        #crea una lista solo con los tiempos
        tiempos_disponibles.sort()         
        print(f"tecnicos disponibles: \n {tecnicos_disponibles}")                                                                             #ordena tiempos de menor a mayor
        tecnico_min_time = tecnicos_disponibles[0]

        #print(tiempos_disponibles)
        #print(tecnicos_disponibles)


        for times in tiempos_disponibles:                                                               #buscamos en la lista de técnicos
            print(f"{times}+{vehiculo_min_time.obtener_tiempo_proceso(siguiente_estado)}")

            asignado = False

            if times + vehiculo_min_time.obtener_tiempo_proceso(siguiente_estado) <= horizonte:         #verificamos que el tiempo asignado no supere el horizonte
                print("OK. Aun no se supera el horizonte")
                tecnico_min_time.asignar_vehiculo(vehiculo_min_time)                                    #SE ASIGNA VEHICULO A TÉCNICO desde el método en la clase técnico
                asignado = True
                print(f"asignado = {asignado} {tecnico_min_time.nombre} al vehiculo {vehiculo_min_time.id_chasis} en {siguiente_estado}")
                
                listaOrdenes.append(mclas.OrdenProduccion(vehiculo_min_time, siguiente_estado, tecnico_min_time, vehiculo_min_time.inicio, vehiculo_min_time.fin, vehiculo_min_time.pedido))
                print(listaOrdenes[-1])
                listaOrdenes[-1].almacenar_orden()
                break
        
        if asignado == False:
            print(f"No se asignó {vehiculo_min_time.id_chasis}")

                
        vehiculos_por_programar.remove(vehiculo_min_time)        #REMOVEMOS DE LA LISTA EL VEHICULO QUE SE ACABA DE ASIGNAR               
        print(f"--------------------------vuelta {contador}")

        contador = contador + 1
    return pedido.vehiculos

#programa_inmediato(pedido_quito06, personal, 700)


def programa_completo(pedido, tecnicos, horizonte):

    vehiculos_por_programar = pedido.vehiculos.copy()                   # Extrae una copia de la lista de vehiculos
    contador = 0
    while len(vehiculos_por_programar) > 0 :

        ind_est_actuales = list(map(lambda vh: mclas.orden_procesos.index(vh.estado),vehiculos_por_programar))        # encuentra una lista con los estado actuales de cada vehículo
        print(f"estados: {ind_est_actuales}")
        for vehic in vehiculos_por_programar:                          #bucle para mostrar en consola el resumen de estados de cada vehiculo
            print(vehic)
        


        tiempos_restantes = [
            sum(vh.tiempos_proceso[ind_est:] if ind_est < len(vh.tiempos_proceso) else [0,0]) for vh, ind_est in zip(vehiculos_por_programar, ind_est_actuales)
            ]
            #crea una lista con solo el total de tiempos restante de cada vehiculo
        print(tiempos_restantes)


        indice_min_time = tiempos_restantes.index(max(tiempos_restantes))                                               #busca el índice con tiempo mayor
        vehiculo_min_time = vehiculos_por_programar[indice_min_time]                                                    #busca el vehiculo con tiempo restante mayor

        ultimo_estado = vehiculo_min_time.estado                                        #Extrae el ultimo estado en el constructor
        siguiente_estado = mclas.orden_procesos[mclas.orden_procesos.index(ultimo_estado) + 1]      #Obtiene el siguiente estado o proceso de la secuencia
        
        if siguiente_estado == "DESPACHO":
            print(f"<<<<<<<<<Vehiculo {vehiculo_min_time.id_chasis} en despacho>>>>>>>>>")
            vehiculos_por_programar.remove(vehiculo_min_time)
            contador = contador + 1
            continue

        tecnicos_disponibles = list(filter(lambda persona: siguiente_estado in persona.especializacion, tecnicos))      # incluye soloaquellos técnicos de la especialidad correcta
        tecnicos_disponibles.sort(key = lambda op: op.termina)                                                          #ordena técnicos por tiempo de menor a mayor

        tiempos_disponibles = list(map(lambda operario: operario.termina, tecnicos_disponibles))                        #crea una lista solo con los tiempos
        tiempos_disponibles.sort()                                                                                      #ordena tiempos de menor a mayor
        tecnico_min_time = tecnicos_disponibles[0]

        #print(tiempos_disponibles)
        #print(tecnicos_disponibles)


        for times in tiempos_disponibles:                                                               #buscamos en la lista de técnicos
            print(f"{times}+{vehiculo_min_time.obtener_tiempo_proceso(siguiente_estado)}")

            asignado = False

            if times + vehiculo_min_time.obtener_tiempo_proceso(siguiente_estado) <= horizonte:         #verificamos que el tiempo asignado no supere el horizonte
                print("OK. Aun no se supera el horizonte")
                tecnico_min_time.asignar_vehiculo(vehiculo_min_time)                                    #SE ASIGNA VEHICULO A TÉCNICO desde el método en la clase técnico
                asignado = True
                print(f"asignado = {asignado}. Se asignó {vehiculo_min_time.id_chasis} a {tecnico_min_time.id_tecnico} en el proceso {siguiente_estado}\n\n")                
                listaOrdenes.append(mclas.OrdenProduccion(vehiculo_min_time, siguiente_estado, tecnico_min_time, vehiculo_min_time.inicio, vehiculo_min_time.fin, vehiculo_min_time.pedido))
                print(listaOrdenes[-1])
                listaOrdenes[-1].almacenar_orden()
                break
        
        if asignado == False:
            print(f"No se asignó {vehiculo_min_time.id_chasis}")

        if vehiculo_min_time.estado == 'calidad':
            vehiculos_por_programar.remove(vehiculo_min_time)        #REMOVEMOS DE LA LISTA EL VEHICULO QUE SE ACABA DE ASIGNAR               
        
        print (f"vuelta #{contador}\n---------------------------------")
        contador = contador + 1

    return pedido.vehiculos


def calcular_horizonte(pedido):
    return max(map(lambda vh: vh.fin, pedido.vehiculos))