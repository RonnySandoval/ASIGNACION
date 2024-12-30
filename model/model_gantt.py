import model.model_datetime as model_datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import random as rdm
import controller.glo as glo
class Gantt():
    """
    Clase para la creación y gestión de diagramas de Gantt personalizados para técnicos y vehículos.

    Atributos:
        gantt_style: Estilo visual para los gráficos de Matplotlib, configurado en modo oscuro.
        graficos_vehiculos (dict): Diccionario para almacenar las figuras de Gantt relacionadas con vehículos.
        graficos_tecnicos (dict): Diccionario para almacenar las figuras de Gantt relacionadas con técnicos.
        colores (dict): Paleta de colores personalizados utilizados para los gráficos.
        colores_tecnicos (dict): Diccionario para almacenar colores asignados a cada técnico.
        colores_tec_disponibles (list): Lista de colores disponibles para asignar a técnicos.
        colores_vehiculos (dict): Diccionario para almacenar colores asignados a cada vehículo.
        colores_vh_disponibles (list): Lista de colores disponibles para asignar a vehículos.

    Métodos:
        __init__(): Inicializa los atributos de la clase.
        crear_gantt(nombre_grafico, items, inicio, horizonte):
            Crea y configura un gráfico de Gantt personalizado para técnicos.
    """
    def __init__(self, vehiculos, tecnicos, inicio, horizonte):

        plt.rcParams['axes.grid'] = False
        self.gantt_style = plt.style.use('dark_background')    # Activar modo oscuro en Matplotlib

        self.graficos_vehiculos = {}        # Diccionarios globales para almacenar las figuras
        self.graficos_tecnicos  = {}        # Diccionarios globales para almacenar las figuras

        self.colores_tecnicos = {}
        self.colores_vehiculos = {}

        self.gantt_tecnicos  = self.__crear_gantt__("tecnicos",  tecnicos,  inicio, horizonte)
        self.gantt_vehiculos = self.__crear_gantt__("vehiculos", vehiculos, inicio, horizonte)

    def __crear_gantt__(self, tipo, items, inicio, horizonte):   
        """
        Crea un gráfico de Gantt para técnicos con configuraciones personalizadas.

        Args:
            nombre_grafico (str): Nombre del gráfico, utilizado como clave en el diccionario `graficos_tecnicos`.
            items (list): Lista de técnicos o vehóculos que aparecerán en el eje Y del gráfico.
            Tipo (str): Tipo de gráfico
            inicio (datetime): Fecha y hora de inicio del diagrama de Gantt.
            horizonte (datetime): Fecha y hora que representan el límite derecho del diagrama.

        Returns:
            dict: Un diccionario que contiene los objetos relacionados con el gráfico de Gantt creado.
                  Incluye la figura, los ejes, la barra horizontal (`hbar`), los técnicos, el inicio y el horizonte.
        """
        hbar = 10
        num_items = len(items)
        iniciarEje = model_datetime.define_franja(str(inicio.date()))[glo.turnos.startAM.get()]
        fig, ax = plt.subplots()                           # Objetos del plot
        # Verificar que num_items sea mayor que 0 antes de establecer los límites del eje Y
        if num_items > 0:
            ax.set_ylim(0, num_items * hbar)  # Límites de eje Y
        else:
            ax.set_ylim(0, 1)  # Establecer un valor mínimo para evitar la advertencia

        diagrama = {
            "fig": fig,
            "ax": ax,
            "hbar": hbar,
            "items": items,
            "inicio": iniciarEje,
            "horizonte": horizonte,
            "etiq_barras": []
        }
        fig.subplots_adjust(top=1.0)            # Elimina el espacio superior
        fig.subplots_adjust(bottom=0.25)        # Configurar diseño de margen predeterminado
        # Configuración de ejes
        ax.set_xlabel('Fecha/hora')             # Etiqueta de eje X
        ax.set_ylabel(tipo.upper())             # Etiqueta de eje Y

        ax.set_xlim(iniciarEje, horizonte)      # Límites eje X
        ax.xaxis_date()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))  # Formato de fecha

        # Verificar que num_items sea mayor que 0 antes de establecer los límites del eje Y
        if num_items > 0:
            ax.set_ylim(0, num_items * hbar)  # Límites de eje Y
        else:
            ax.set_ylim(0, 1)  # Establecer un valor mínimo para evitar la advertencia


        # Configuración de límites y ticks en el eje Y
        if num_items > 0:                     # Verificar que num_items sea mayor que 0 antes de establecer los límites del eje Y
            ax.set_ylim(0, num_items * hbar)  # Límites de eje Y
            ax.set_yticks(np.arange(hbar / 2, num_items * hbar, hbar))       # Ubica etiquetas en el centro de cada barra
            ax.set_yticklabels(items)         # Etiquetas de técnicos
        else:
            ax.set_ylim(0, 1)  # Establecer un valor mínimo para evitar la advertencia                               # Límites de eje Y


        # Configuración de la grilla secundaria (para divisiones entre las barras)
        ax.set_yticks(range(hbar, num_items * hbar, hbar), minor=True)    # Divisiones menores en eje Y (grilla menor)
        ax.grid(True, axis='y', which='minor', color='white', linewidth=1)  # Mostrar solo la grilla menor

        # Deshabilitar la grilla principal en el eje Y para evitar el solapamiento con las etiquetas
        ax.grid(True, axis='y', which='major', color='black', linestyle='', linewidth=0.1)  # Grilla principal de color negro (si es necesario)

        # Configurar los ticks principales (ocultar las marcas de los ticks del eje Y)
        ax.tick_params(axis='y', which='major', length=0)  # Eliminar marcas en el eje Y, pero las etiquetas permanecen

        plt.xticks(rotation=90)                                                 # Rotar fechas en el eje X a 90 grados

        if tipo == "tecnicos":        # Guardar el diagrama en el diccionario global
            self.graficos_tecnicos[tipo] = diagrama

        if tipo == "vehiculos":        # Guardar el diagrama en el diccionario global
            self.graficos_vehiculos[tipo] = diagrama
        
        return diagrama

        self.colores_vehiculos = {}  # Para almacenar colores de vehículos
        self.colores_tecnicos = {}  # Para almacenar colores de técnicos

    def __asignar_color__(self, tipo, task):
        """
        Asigna un color a la tarea (vehículo o técnico), generando un color aleatorio
        si no se ha asignado previamente, y lo almacena para reutilización.

        Args:
            tipo (str): Tipo de gráfico, ya sea 'vehiculos' o 'tecnicos'.
            task (str): El identificador de la tarea (vehículo o técnico).
        
        Returns:
            str: El color asignado a la tarea en formato RGB (como string).
        """
        if tipo == "vehiculos":
            colores_asignados = self.colores_vehiculos
        elif tipo == "tecnicos":
            colores_asignados = self.colores_tecnicos
        else:
            raise ValueError(f"Tipo de gráfico '{tipo}' no válido")


        if task in colores_asignados:        # Verifica si ya se asignó un color previamente a la tarea
            return colores_asignados[task]
        
        color = self.__generar_color_random__()        # Si no se ha asignado color, generar uno aleatorio
        colores_asignados[task] = color        # Almacenar el color generado para reutilizarlo
        
        return color

    def __generar_color_random__(self):
        """
        Genera un color aleatorio en formato RGB (rango 0-255 para cada componente).
        
        Returns:
            str: El color generado en formato RGB (como string).
        """

        r, g, b = rdm.randint(30, 235), rdm.randint(30, 235), rdm.randint(30, 235)        # Generar valores aleatorios para R, G, B en el rango [0, 255]
        return (r / 255.0, g / 255.0, b / 255.0)        # Devolver el color en formato RGB

    def agregar_proceso(self, tipo, t0, duracion, proceso, task, item, color=None):
        """
        Agrega un proceso a un diagrama de Gantt, ya sea asociado a un técnico o a un vehículo, 
        dependiendo del tipo especificado.
        """

        if tipo == "vehiculos":        
            diagrama = self.graficos_vehiculos.get(tipo)
            color = self.__asignar_color__("vehiculos", task)            # Asignar color a la tarea si no tiene uno

        elif tipo == "tecnicos":        
            diagrama = self.graficos_tecnicos.get(tipo)
            color = self.__asignar_color__("tecnicos", task)            # Asignar color a la tarea si no tiene uno

        if diagrama is None:
            print(f"Error: El gráfico '{tipo}' no existe.")
            return

        items = diagrama["items"].tolist()
        ax    = diagrama["ax"]
        hbar  = diagrama["hbar"]

        ind_item = items.index(item)

        # Convertir datetime a número de matplotlib
        inicio_tarea_num = mdates.date2num(t0)
        duracion_num = duracion.total_seconds() / (24 * 3600)  # Duración en días

        rect_border = ax.broken_barh([(inicio_tarea_num, duracion_num)],
                                        (hbar * ind_item, hbar),
                                        facecolors='white',  # Color del borde
                                        edgecolor='white',   # Borde negro
                                        linewidth=3)         # Ancho del borde

        # Barra principal
        rect_bar = ax.broken_barh([(inicio_tarea_num, duracion_num)],
                                    (hbar * ind_item, hbar),
                                    facecolors=color)  # Color de la barra

        label = ax.text(x = inicio_tarea_num + duracion_num / 2,
                        y = hbar * ind_item + hbar / 2, 
                        s = f'{task}\n{duracion}\n({proceso})', 
                        va ="center",    ha="center",
                        color="white",  fontsize=6)  

        if "etiq_barras" not in diagrama:    # Guardar información de la barra y la etiqueta para futuras interacciones
            diagrama["etiq_barras"] = []
        diagrama["etiq_barras"].append({
                                        "rect"   : rect_bar,
                                        "border" : rect_border,
                                        "label"  : label,
                                        "item"   : item,
                                        "task"   : task,
                                        "proceso": proceso
                                        })

def generar_gantt(dataframe, Start, horizonte_calculado):
    
    inicio = Start
    chasises = dataframe["CHASIS"].unique()
    tecnicos = dataframe["TECNICO"].unique()

    graficosGantt = Gantt(vehiculos = chasises,
                          tecnicos  = tecnicos,
                          inicio    = inicio,
                          horizonte = horizonte_calculado)

    for index, registro in dataframe.iterrows():
        vehiculo = registro['CHASIS']
        proceso  = registro['PROCESO']
        start    = registro['INICIO'].to_pydatetime()
        end      = registro['FIN'].to_pydatetime()
        duracion = end - start 
        tecnico  = registro['TECNICO']

        if duracion == 0:  # evalua si la tarea no ocupa tiempo
            continue
        else:    
            graficosGantt.agregar_proceso(
                                            tipo     = "vehiculos",
                                            t0       = start,
                                            duracion = duracion,
                                            proceso  = proceso,
                                            task     = tecnico,
                                            item     = vehiculo
                )
            print(f"Se agregó {proceso} de {tecnico} a {vehiculo}")

            graficosGantt.agregar_proceso(
                                            tipo     = "tecnicos",
                                            t0       = start,
                                            duracion = duracion,
                                            proceso  = proceso,
                                            task     = vehiculo,
                                            item     = tecnico
                )
            print(f"Se agregó {proceso} de {vehiculo} a {tecnico}")

    configurar_zoom(fig = graficosGantt.gantt_tecnicos["fig"],
                    ax  = graficosGantt.gantt_tecnicos["ax"],
                    etiquetas_y = tecnicos,
                    etiquetas_barras = graficosGantt.gantt_tecnicos["etiq_barras"],
                    hbar =graficosGantt.gantt_tecnicos["hbar"])

    configurar_zoom(fig = graficosGantt.gantt_vehiculos["fig"],
                    ax  = graficosGantt.gantt_vehiculos["ax"],
                    etiquetas_y = chasises,
                    etiquetas_barras = graficosGantt.gantt_vehiculos["etiq_barras"],
                    hbar = graficosGantt.gantt_vehiculos["hbar"])

    return graficosGantt.gantt_tecnicos, graficosGantt.gantt_vehiculos

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
