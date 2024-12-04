#from modelo_clases import personal
#from modelo_instancias import pedido, horizonte_calculado
import modelo_mostrarGantt
#import datetime
import fechahora
import numpy as np

#######GANTT DE VEHICULOS#########
def generar_gantt_vehiculos(pedido, fechaStart, horaStart, horizonte_calculado):

    inicio = fechahora.parseDT(fechaStart, horaStart)
    lista_vehiculos =[]
    for tarea in pedido.vehiculos:
        datos_vehiculo = [tarea.id_chasis, tarea.modelo]                         #extrae la lista con nombres de vehículos
        lista_vehiculos.append(tarea.id_chasis)

    #generación de gráfico con etiquetas de ejes
    diagrama = modelo_mostrarGantt.crear_gantt_vehiculos("GRAFICO_DE_VEHICULOS_01",lista_vehiculos, inicio, horizonte_calculado)

    for tarea in pedido.vehiculos:

        for proceso in tarea.historico_estados:         # busca los parámetros de entrada para cada tarea del grafico
            nombre_proceso = proceso[0]                 # extrae el nombre del proceso del 1er elemento del atributo historico estados (proceso)
            init = proceso[1]                           # extrae el nombre del proceso del 2do elemento del atributo historico estados (inicio de proceso)
            duracion = proceso[2]- proceso[1]           # extrae el nombre del proceso del 2do y 3er elemento del atributo historico estados (inicio y fin de proceso)
            encargado = proceso[3]                      # extrae el nombre del proceso del 4to elemento del atributo historico estados (tecnico)
            if duracion == 0:                           # evalua si la tarea no ocupa tiempo
                continue
            else:    
                modelo_mostrarGantt.agregar_proceso(
                    "GRAFICO_DE_VEHICULOS_01",
                    init,
                    duracion, 
                    tarea.id_chasis,
                    nombre_proceso,
                    encargado
                )
                print(f"Se agregó {nombre_proceso} en {tarea.id_chasis}")

    configurar_zoom(fig = diagrama["fig"],
                    ax  = diagrama["ejes"],
                    etiquetas_y =lista_vehiculos,
                    etiquetas_barras = diagrama["etiq_barras"],
                    hbar =diagrama["hbar"])

    modelo_mostrarGantt.mostrar_grafico_vehiculos("GRAFICO_DE_VEHICULOS_01")

#######GANTT DE TECNICOS#########
def generar_gantt_tecnicos(personal, fechaStart, horaStart, horizonte_calculado):

    inicio = fechahora.parseDT(fechaStart, horaStart)
    lista_personas =[]
    print(personal)
    for persona in personal:
        datos_tecnico = [persona.id_tecnico, persona.nombre]                         #extrae la lista con nombres de vehículos
        lista_personas.append(persona.id_tecnico)

    #generación de gráfico con etiquetas de ejes
    diagrama = modelo_mostrarGantt.crear_gantt_tecnicos("GRAFICO_DE_TECNICOS_02", lista_personas, inicio, horizonte_calculado)

    for tarea in personal:

        for vehiculo in tarea.historico_asignacion:         # busca los parámetros de entrada para cada tarea del grafico
            id_vehiculo = vehiculo[0]                       # extrae el nombre del proceso del 1er elemento del atributo asignacion estados (vehiculo)
            init = vehiculo[1]                              # extrae el nombre del proceso del 2do elemento del atributo asignacion estados (inicio de vehiculo)
            duracion = vehiculo[2]- vehiculo[1]             # extrae el nombre del proceso del 2do y 3er elemento del atributo asignacion estados (inicio y fin de vehiculo)
            if duracion == 0:                               # evalua si la tarea no ocupa tiempo
                print(f"No se agregó {vehiculo} ")
                continue

            else:    
                modelo_mostrarGantt.agregar_vehiculo(
                    "GRAFICO_DE_TECNICOS_02",
                    init, duracion,
                    tarea.id_tecnico,
                    id_vehiculo
                    )
                print(f"Se agregó {id_vehiculo} en {tarea.id_tecnico} inicio: {init} y duracion {duracion}")
    
    configurar_zoom(fig = diagrama["fig"],
                ax  = diagrama["ejes"],
                etiquetas_y =lista_personas,
                etiquetas_barras = diagrama["etiq_barras"],
                hbar =diagrama["hbar"])
    modelo_mostrarGantt.mostrar_grafico_tecnicos("GRAFICO_DE_TECNICOS_02")

#MANEJO DEL EVENTO ZOOM DEL MOUSE
def configurar_zoom(fig, ax, etiquetas_y, etiquetas_barras, hbar):
    """Configura la interacción del zoom en el gráfico."""
    def on_scroll(event):
        if event.inaxes != ax:
            return

        # Obtén los límites actuales del eje x
        x_min, x_max = ax.get_xlim()
        range_x = x_max - x_min

        # Calcula el factor de zoom
        factor_zoom = 0.8 if event.button == 'up' else 1.25

        # Calcular nuevos límites
        nuevo_centro = event.xdata
        nuevo_min = nuevo_centro - (nuevo_centro - x_min) * factor_zoom
        nuevo_max = nuevo_centro + (x_max - nuevo_centro) * factor_zoom

        # Ajusta los límites del eje x
        ax.set_xlim(nuevo_min, nuevo_max)

        # Reajusta las etiquetas de eje Y para que permanezcan en el lugar correcto
        ax.set_yticks(
            np.arange(hbar / 2, hbar * len(etiquetas_y) - hbar / 2 + hbar, hbar)
        )
        ax.set_yticklabels(etiquetas_y)

        # Actualiza la visibilidad de las etiquetas de las barras
        for barra_info in etiquetas_barras:
            etiqueta = barra_info["label"]
            etiqueta.set_visible(True)          # Mostrar por defecto
            pos_x, _ = etiqueta.get_position()  # Coordenadas de la etiqueta
            print(f"Posición de etiqueta: {pos_x}, Rango: ({nuevo_min}, {nuevo_max})")
            if pos_x < nuevo_min or pos_x > nuevo_max:
                etiqueta.set_visible(False)     # Ocultar si está fuera de rango
        # Redibuja el gráfico
        fig.canvas.draw_idle()

    # Vincula el evento de scroll al gráfico
    fig.canvas.mpl_connect('scroll_event', on_scroll)



#generar_gantt_tecnicos(personal,  "2024-11-05", "08:45:00", horizonte_calculado)
#generar_gantt_vehiculos(pedido,  "2024-11-05", "08:45:00", horizonte_calculado)