import model.model_showGantt as model_showGantt
import model.model_datetime as model_datetime
import numpy as np

#######GANTT DE VEHICULOS#########
def generar_gantt_vehiculos(pedido, fechaStart, horaStart, horizonte_calculado):
    """
    args
        pedido: Objeto Pedido, con propiedades id_pedido, vehiculos(objetos Vehiculo), fecha_recepcion, plazo_entrega"
            att de Vehiculo:modelo, marca, tiempos_proceso, estado_inicial, color,
                            fecha_entrega, id_chasis, pedido, estado, novedades,
                            inicio, fin, tecnico_actual (Objeto Tecnico), libre, plazo, vueltas, historico_estados (tuplas con objetos Tecnico)
                                        att de Tecnico :  id_tecnico , nombre, especializacion, comienza,
                                                          termina , libre , vehiculo_actual , historico_asignacion (tuplas con lista de objetos Vehiculo)
        fechaStart: str con el formato de fecha
        fechhaHora: str con el formato de hora
        horizonte_calculado: datetime con formato fecha hora

    return
        None
    """

    inicio = model_datetime.parseDT(fechaStart, horaStart)
    lista_vehiculos =[]
    lista_vehiculos_modelos = []

    for tarea in pedido.vehiculos:
        datos_vehiculo = tarea.id_chasis + " (" + tarea.modelo + ")"                         #extrae la lista con nombres de vehículos
        lista_vehiculos.append(tarea.id_chasis)
        lista_vehiculos_modelos.append(datos_vehiculo)
    
    print(lista_vehiculos)
    #generación de gráfico con etiquetas de ejes
    diagrama = model_showGantt.crear_gantt_vehiculos("GRAFICO_DE_VEHICULOS_01", lista_vehiculos, inicio, horizonte_calculado)

    for tarea in pedido.vehiculos:

        for proceso in tarea.historico_estados:         # busca los parámetros de entrada para cada tarea del grafico
            nombre_proceso = proceso[0]                 # extrae el nombre del proceso del 1er elemento del atributo historico estados (proceso)
            init = proceso[1]                           # extrae el nombre del proceso del 2do elemento del atributo historico estados (inicio de proceso)
            duracion = proceso[2]- proceso[1]           # extrae el nombre del proceso del 2do y 3er elemento del atributo historico estados (inicio y fin de proceso)
            encargado = proceso[3]                      # extrae el nombre del proceso del 4to elemento del atributo historico estados (tecnico)
            if duracion == 0:                           # evalua si la tarea no ocupa tiempo
                continue
            else:    
                model_showGantt.agregar_proceso(
                    "GRAFICO_DE_VEHICULOS_01",
                    init,
                    duracion, 
                    tarea.id_chasis,
                    nombre_proceso,
                    encargado
                )
                print(f"Se agregó {nombre_proceso} en {tarea.id_chasis}")

    configurar_zoom(fig = diagrama["fig"],
                    ax  = diagrama["ax"],
                    etiquetas_y =lista_vehiculos_modelos,
                    etiquetas_barras = diagrama["etiq_barras"],
                    hbar =diagrama["hbar"])

    #modelo_mostrarGantt.mostrar_grafico_vehiculos("GRAFICO_DE_VEHICULOS_01")
    return diagrama

#######GANTT DE TECNICOS#########
def generar_gantt_tecnicos(personal, fechaStart, horaStart, horizonte_calculado):
    """"
    args
        personal: lista de objetos tecnico 
            att de Tecnico :  id_tecnico , nombre, especializacion, comienza , termina , libre , vehiculo_actual (Objeto Vehiculo) , historico_asignacion (tuplas con lista de objetos Vehiculo)
                att Vehiculo : modelo, marca, tiempos_proceso, estado_inicial, color,
                                fecha_entrega, id_chasis, pedido, estado, novedades,
                                inicio, fin, tecnico_actual, libre, plazo, historico_estados, vueltas
        fechaStart: str con el formato de fecha
        fechhaHora: str con el formato de hora
        horizonte_calculado: datetime con formato fecha hora

    return
        None
    """
    inicio = model_datetime.parseDT(fechaStart, horaStart)
    lista_nombre_personas =[]
    lista_personas =[]
    print(personal)
    for persona in personal:                         #extrae la lista con nombres de vehículos
        datos_tecnico = persona.nombre + " (" + persona.especializacion + ")"
        lista_nombre_personas.append(datos_tecnico)
        lista_personas.append(persona.id_tecnico)
    print(lista_personas)

    #generación de gráfico con etiquetas de ejes
    diagrama = model_showGantt.crear_gantt_tecnicos("GRAFICO_DE_TECNICOS_02", lista_personas, inicio, horizonte_calculado)

    for tarea in personal:

        for vehiculo in tarea.historico_asignacion:         # busca los parámetros de entrada para cada tarea del grafico
            id_vehiculo = vehiculo[0]                       # extrae el nombre del proceso del 1er elemento del atributo asignacion estados (vehiculo)
            init = vehiculo[1]                              # extrae el nombre del proceso del 2do elemento del atributo asignacion estados (inicio de vehiculo)
            duracion = vehiculo[2]- vehiculo[1]             # extrae el nombre del proceso del 2do y 3er elemento del atributo asignacion estados (inicio y fin de vehiculo)
            if duracion == 0:                               # evalua si la tarea no ocupa tiempo
                print(f"No se agregó {vehiculo} ")
                continue

            else:    
                model_showGantt.agregar_vehiculo(
                    "GRAFICO_DE_TECNICOS_02",
                    init, duracion,
                    tarea.id_tecnico,
                    id_vehiculo
                    )
                print(f"Se agregó {id_vehiculo} en {tarea.id_tecnico} inicio: {init} y duracion {duracion}")
    
    configurar_zoom(fig = diagrama["fig"],
                ax  = diagrama["ax"],
                etiquetas_y =lista_nombre_personas,
                etiquetas_barras = diagrama["etiq_barras"],
                hbar =diagrama["hbar"])
    #modelo_mostrarGantt.mostrar_grafico_tecnicos("GRAFICO_DE_TECNICOS_02")
    return diagrama

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

        # Configurar divisiones y etiquetas en el eje Y
        ax.set_yticks(np.arange(hbar / 2, hbar * len(etiquetas_y), hbar))       # Ubica etiquetas en el centro de cada barra
        ax.set_yticklabels(etiquetas_y)
        ax.set_yticks(range(hbar, len(etiquetas_y) * hbar, hbar), minor=True)  # Divisiones menores en eje Y (grilla menor)
        
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
