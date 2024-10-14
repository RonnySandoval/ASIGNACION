from Mod_clases import personal
from Mod_objetos import pedido_quito06
import gantt
import datetime
import fechahora


#######GANTT DE VEHICULOS#########
def generar_gantt_vehiculos(pedido, fechaStart, horaStart, horizonte_calculado):


    inicio = fechahora.parseDT(fechaStart, horaStart)
    lista_vehiculos =[]
    for tarea in pedido.vehiculos:
        datos_vehiculo = [tarea.id_chasis, tarea.modelo]                         #extrae la lista con nombres de vehículos
        lista_vehiculos.append(tarea.id_chasis)

    #generación de gráfico con etiquetas de ejes
    gantt.crear_gantt_vehiculos("GRAFICO_DE_VEHICULOS_01",lista_vehiculos, inicio, horizonte_calculado)

    for tarea in pedido.vehiculos:

        for proceso in tarea.historico_estados:         #busca los parámetros de entrada para cada tarea del grafico
            nombre_proceso = proceso[0]                 #extrae el nombre del proceso del 1er elemento del atributo historico estados (proceso)
            init = proceso[1]                         #extrae el nombre del proceso del 2do elemento del atributo historico estados (inicio de proceso)
            duracion = proceso[2]- proceso[1]           #extrae el nombre del proceso del 2do y 3er elemento del atributo historico estados (inicio y fin de proceso)
            encargado = proceso[3]                      #extrae el nombre del proceso del 4to elemento del atributo historico estados (tecnico)
            if duracion == 0:                           #evalua si la tarea no ocupa tiempo
                continue
            else:    
                gantt.agregar_proceso(
                    "GRAFICO_DE_VEHICULOS_01",
                    init,
                    duracion, 
                    tarea.id_chasis,
                    nombre_proceso,
                    encargado
                )
                print(f"Se agregó {nombre_proceso} en {tarea.id_chasis}")
        
    gantt.mostrar_grafico_vehiculos("GRAFICO_DE_VEHICULOS_01")



#######GANTT DE TECNICOS#########
def generar_gantt_tecnicos(personal, fechaStart, horaStart, horizonte_calculado):

    inicio = fechahora.parseDT(fechaStart, horaStart)
    lista_personas =[]
    print(personal)
    for persona in personal:
        datos_tecnico = [persona.id_tecnico, persona.nombre]                         #extrae la lista con nombres de vehículos
        lista_personas.append(persona.id_tecnico)

    #generación de gráfico con etiquetas de ejes
    gantt.crear_gantt_tecnicos("GRAFICO_DE_TECNICOS_02", lista_personas, inicio, horizonte_calculado)

    for tarea in personal:

        for vehiculo in tarea.historico_asignacion:         #busca los parámetros de entrada para cada tarea del grafico
            id_vehiculo = vehiculo[0]                       #extrae el nombre del proceso del 1er elemento del atributo asignacion estados (vehiculo)
            init = vehiculo[1]                            #extrae el nombre del proceso del 2do elemento del atributo asignacion estados (inicio de vehiculo)
            duracion = vehiculo[2]- vehiculo[1]             #extrae el nombre del proceso del 2do y 3er elemento del atributo asignacion estados (inicio y fin de vehiculo)
            if duracion == 0:                               #evalua si la tarea no ocupa tiempo
                print(f"No se agregó {vehiculo} ")
                continue

            else:    
                gantt.agregar_vehiculo(
                    "GRAFICO_DE_TECNICOS_02",
                    init, duracion,
                    tarea.id_tecnico,
                    id_vehiculo
                    )
                print(f"Se agregó {id_vehiculo} en {tarea.id_tecnico} inicio: {init} y duracion {duracion}")
        
    gantt.mostrar_grafico_tecnicos("GRAFICO_DE_TECNICOS_02")



#generar_gantt_tecnicos(personal, datetime.datetime(2024,10,8,12,57), horizonte_calculado)
#generar_gantt_vehiculos(pedido_quito06, datetime.datetime(2024,10,8,12,57), horizonte_calculado)