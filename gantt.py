import fechahora
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as patches
import random as rdm
import datetime

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
        self.graficos_tecnicos  = {}         # Diccionarios globales para almacenar las figuras

        self.colores = {
        "azul_noche": "#1A1A7D",
        "marrón_oscuro": "#3E2A47",
        "gris_plomo": "#5A5A5A",
        "café_claro": "#4A2C2A",
        "verde_hoja": "#2F6B3E",
        "azul_oscuro": "#003366",
        "naranja_oscuro": "#D75B4E",
        "rojo_vino": "#9B2335",
        "verde_gris": "#6B8E23",
        "gris_antracita": "#2F4F4F",
        "rojo_oscuro": "#8B0000",
        "madera_tierra": "#6F4F37",
        "verde_oscuro": "#006400",
        "morado_vino": "#800000",
        "azul_tintado": "#4C6A92",
        "marrón_rico": "#7A3F32",
        "rojo_granate": "#9B111E",
        "gris_plata": "#A2A2A1",
        "azul_mediterráneo": "#2C75B2",
        "verde_army": "#4B5320",
        "café_miel": "#6B4F2F",
        "amarillo_terroso": "#BDBB73",
        "gris_roto": "#8A8A8A",
        "rojo_cereza": "#9E1B32",
        "madera_natural": "#8B6F47",
        "verde_subido": "#468C45",
        "azul_grisáceo": "#3B5F73",
        "naranja_terroso": "#A53C2D",
        "madera_oscura": "#5D3F2C",
        "rojo_frambuesa": "#990000",
        "verde_turquesa": "#3F9C87",
        "gris_como_piedra": "#B8B8B8",
        "verde_oliva": "#6B8E23",
        "rojo_marrón": "#8B3A3A",
        "marrón_toscano": "#6B4226",
        "azul_galaxia": "#2A2D99",
        "rojo_oscuridad": "#8B0000",
        "azul_pavo": "#5F9EA0",
        "verde_agua": "#3C8D6E",
        "gris_azulado": "#708090",
        "verde_fango": "#4C5A3C",
        "azul_grisáceo_2": "#6B7F89",
        }

        self.colores_tecnicos = {}                                  # Diccionario para almacenar los colores de cada técnico
        self.colores_tec_disponibles = list(self.colores.values())  # Lista de valores (colores) del diccionario

        self.colores_vehiculos = {}                                 # Diccionario para almacenar los colores de cada vehiculo
        self.colores_vh_disponibles = list(self.colores.values())  # Lista de valores (colores) del diccionario

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
        iniciarEje = fechahora.define_franja(str(inicio.date()))[8]
        fig, ax = plt.subplots()                           # Objetos del plot
        diagrama = {
            "fig": fig,
            "ax": ax,
            "hbar": hbar,
            "items": items,
            "inicio": iniciarEje,
            "horizonte": horizonte
        }
        fig.subplots_adjust(top=1.0)            # Elimina el espacio superior
        fig.subplots_adjust(bottom=0.25)        # Configurar diseño de margen predeterminado
        # Configuración de ejes
        ax.set_xlabel('Fecha/hora')             # Etiqueta de eje X
        ax.set_ylabel(tipo.upper())             # Etiqueta de eje Y

        ax.set_xlim(iniciarEje, horizonte)      # Límites eje X
        ax.xaxis_date()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))  # Formato de fecha

        # Configuración de límites y ticks en el eje Y
        ax.set_ylim(0, num_items * hbar)                                 # Límites de eje Y
        ax.set_yticks(np.arange(hbar / 2, num_items * hbar, hbar))       # Ubica etiquetas en el centro de cada barra
        ax.set_yticklabels(items)                                        # Etiquetas de técnicos

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

    def agregar_proceso(self, tipo, t0, duracion, proceso, task, item, color=None):
        """
        Agrega un proceso a un diagrama de Gantt, ya sea asociado a un técnico o a un vehículo, 
        dependiendo del tipo especificado.


        Args:
        ----------
        nombre_grafico : str
            El nombre del gráfico al que se agregará el proceso.
        tipo : str
            Puede ser "tecnico" o "vehiculo", indicando el tipo de gráfico al que se refiere.
        t0 : datetime
            Fecha y hora de inicio del proceso.
        duracion : timedelta
            Duración del proceso.
        proceso : str
            Nombre o descripción del proceso asociado al task/item.
        task : str
            Identificador principal del proceso, puede ser un vehículo o tarea específica.
        item : str
            Identificador secundario, como el técnico asignado o el vehículo involucrado.
        color : str, opcional
            Color personalizado para la barra del proceso. Si no se especifica, se selecciona uno aleatoriamente.

        Procedure:
        --------
        - Verifica si el gráfico especificado existe en los datos globales.
        - Determina el color a usar para el proceso según el `task` o el `item`.
        - Convierte las fechas y tiempos en formatos compatibles con matplotlib.
        - Agrega una barra principal y un borde al gráfico.
        - Añade una etiqueta en la barra para identificar el proceso, incluyendo su duración y proceso.
        - Guarda la información de la barra y la etiqueta en el diagrama para futuras interacciones.

        Excepciones:
        ------------
        - Si el gráfico no existe, imprime un mensaje de error y no realiza ninguna acción.
        """
        if tipo == "vehiculos":        # Guardar el diagrama en el diccionario global
            
            diagrama = self.graficos_vehiculos.get(tipo)

            if task in self.colores_tecnicos:
                color = self.colores_tecnicos[task]
            else:
                if color is None:
                    # Sortear un color del diccionario
                    color = rdm.choice(self.colores_tec_disponibles)
                    self.colores_tec_disponibles.remove(color)  # Opcional: elimina el color para evitar repetirlo
                self.colores_tecnicos[task] = color


        if tipo == "tecnicos":        # Guardar el diagrama en el diccionario global
            diagrama = self.graficos_tecnicos.get(tipo)

            if task in self.colores_vehiculos:
                color = self.colores_vehiculos[task]
            else:
                if color is None:
                    # Sortear un color del diccionario
                    color = rdm.choice(self.colores_vh_disponibles)
                    self.colores_vh_disponibles.remove(color)  # Opcional: elimina el color para evitar repetirlo
                self.colores_vehiculos[task] = color


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
