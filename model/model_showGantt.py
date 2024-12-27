import matplotlib.pyplot as plt
import numpy as np
import random as rdm
import matplotlib.dates as mdates
import model.model_datetime as model_datetime
import controller.glo as glo
# Diccionarios globales para almacenar las figuras
graficos_vehiculos = {}
graficos_tecnicos = {}

colores = {
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

colores_tecnicos = {}                               # Diccionario para almacenar los colores de cada técnico
colores_tec_disponibles = list(colores.values())  # Lista de valores (colores) del diccionario

colores_vehiculos = {}                              # Diccionario para almacenar los colores de cada vehiculo
colores_vh_disponibles = list(colores.values())  # Lista de valores (colores) del diccionario

plt.rcParams['axes.grid'] = False
##################################################################################################################
########################################  GRÁFICOS PARA TÉCNICOS  ################################################
##################################################################################################################

# Función para crear el gráfico
def crear_gantt_tecnicos(nombre_grafico, tecnicos, inicio, horizonte):
    plt.style.use('dark_background')    # Activar modo oscuro en Matplotlib
    hbar = 10
    num_tecnicos = len(tecnicos)
    iniciarEje = model_datetime.define_franja(str(inicio.date()))[glo.turnos.startAM.get()]
    fig, ax = plt.subplots()                           # Objetos del plot
    diagrama = {
        "fig": fig,
        "ax": ax,
        "hbar": hbar,
        "tecnicos": tecnicos,
        "inicio": iniciarEje,
        "horizonte": horizonte
    }

    # Configuración de ejes
    ax.set_xlabel('Fecha/hora')             # Etiqueta de eje X
    ax.set_ylabel('Técnicos')               # Etiqueta de eje Y

    ax.set_xlim(iniciarEje, horizonte)      # Límites eje X
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))  # Formato de fecha

    # Configuración de límites y ticks en el eje Y
    ax.set_ylim(0, num_tecnicos * hbar)                                 # Límites de eje Y
    ax.set_yticks(np.arange(hbar / 2, num_tecnicos * hbar, hbar))       # Ubica etiquetas en el centro de cada barra
    ax.set_yticklabels(tecnicos)                                        # Etiquetas de técnicos

    # Configuración de la grilla secundaria (para divisiones entre las barras)
    ax.set_yticks(range(hbar, num_tecnicos * hbar, hbar), minor=True)    # Divisiones menores en eje Y (grilla menor)
    ax.grid(True, axis='y', which='minor', color='white', linewidth=1)  # Mostrar solo la grilla menor

    # Deshabilitar la grilla principal en el eje Y para evitar el solapamiento con las etiquetas
    ax.grid(True, axis='y', which='major', color='black', linestyle='', linewidth=0.1)  # Grilla principal de color negro (si es necesario)

    # Configurar los ticks principales (ocultar las marcas de los ticks del eje Y)
    ax.tick_params(axis='y', which='major', length=0)  # Eliminar marcas en el eje Y, pero las etiquetas permanecen

    
    plt.xticks(rotation=90)                                                 # Rotar fechas en el eje X a 90 grados

    # Guardar el diagrama en el diccionario global
    graficos_tecnicos[nombre_grafico] = diagrama
    return diagrama

# Función para agregar tareas
def agregar_vehiculo(nombre_grafico, t0, duracion, tecnico, nombre, color=None):
    diagrama = graficos_tecnicos.get(nombre_grafico)
    if diagrama is None:
        print(f"Error: El gráfico '{nombre_grafico}' no existe.")
        return

    tecnicos = diagrama["tecnicos"]
    ax = diagrama["ax"]
    hbar = diagrama["hbar"]

    if nombre in colores_vehiculos:
        color = colores_vehiculos[nombre]
    else:
        if color is None:
            # Sortear un color del diccionario
            color = rdm.choice(colores_vh_disponibles)
            colores_vh_disponibles.remove(color)  # Opcional: elimina el color para evitar repetirlo
        colores_vehiculos[nombre] = color

    ind_tec = tecnicos.index(tecnico)

    # Convertir datetime a número de matplotlib
    inicio_tarea_num = mdates.date2num(t0)
    duracion_num = duracion.total_seconds() / (24 * 3600)  # Duración en días


    rect_border = ax.broken_barh([(inicio_tarea_num, duracion_num)],
                                    (hbar * ind_tec, hbar),
                                    facecolors='white',  # Color del borde
                                    edgecolor='white',   # Borde negro
                                    linewidth=3)         # Ancho del borde

    # Barra principal
    rect_bar = ax.broken_barh([(inicio_tarea_num, duracion_num)],
                                (hbar * ind_tec, hbar),
                                facecolors=color)  # Color de la barra


    label = ax.text(x=inicio_tarea_num + duracion_num / 2,
               y=hbar * ind_tec + hbar / 2,
               s=f'{nombre}\n({duracion})',
               va="center", ha="center",
               color="white", fontsize=6)
    


    if "barras" not in diagrama:    # Guardar información de la barra y la etiqueta para futuras interacciones
        diagrama["etiq_barras"] = []
    diagrama["etiq_barras"].append({"rect": rect_bar,
                               "label": label,
                               "tecnico": tecnico,
                               "nombre": nombre})
"""
# Función para mostrar un gráfico específico
def mostrar_grafico_tecnicos(nombre_grafico):
    diagrama = graficos_tecnicos.get(nombre_grafico)
    if diagrama is None:
        print(f"Error: El gráfico '{nombre_grafico}' no existe.")
        return

    plt.figure(diagrama["fig"].number)  # Seleccionar la figura por número
    plt.grid(color=estilos.grisOscuro)  # Ajusta el color de la grilla
    plt.show()
"""

###################################################################################################################
########################################  GRÁFICOS PARA VEHÍCULOS  ################################################
###################################################################################################################

# Función para crear el gráfico
def crear_gantt_vehiculos(nombre_grafico, vehiculos, inicio , horizonte):
    hbar = 10
    num_vehiculos = len(vehiculos)
    iniciarEje = model_datetime.define_franja(str(inicio.date()))[glo.turnos.startAM.get()]
    fig, ax = plt.subplots()  # Objetos del plot
    print("iniciar eje en:", iniciarEje)

    diagrama = {
        "fig": fig,
        "ax": ax,
        "hbar": hbar,
        "vehiculos": vehiculos,
        "inicio": iniciarEje,
        "horizonte": horizonte,
    }

    ax.set_xlabel('Fecha/hora')                     # Etiqueta de eje X
    ax.set_ylabel('Vehículos')                      # Etiqueta de eje Y

    ax.set_xlim(iniciarEje, horizonte)               # Límites eje X
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))  # Formato de fecha

    # Configuración de límites y ticks en el eje Y
    ax.set_ylim(0, num_vehiculos * hbar)                                 # Límites de eje Y
    ax.set_yticks(np.arange(hbar / 2, num_vehiculos * hbar, hbar))       # Ubica etiquetas en el centro de cada barra
    ax.set_yticklabels(vehiculos)                                        # Etiquetas de técnicos

    # Configuración de la grilla secundaria (para divisiones entre las barras)
    ax.set_yticks(range(hbar, num_vehiculos * hbar, hbar), minor=True)    # Divisiones menores en eje Y (grilla menor)
    ax.grid(True, axis='y', which='minor', color='white', linewidth=1)  # Mostrar solo la grilla menor

    # Deshabilitar la grilla principal en el eje Y para evitar el solapamiento con las etiquetas
    ax.grid(True, axis='y', which='major', color='black', linestyle='', linewidth=0.1)  # Grilla principal de color negro (si es necesario)

    # Configurar los ticks principales (ocultar las marcas de los ticks del eje Y)
    ax.tick_params(axis='y', which='major', length=0)  # Eliminar marcas en el eje Y, pero las etiquetas permanecen

    plt.xticks(rotation=90)                  # Rotar las fechas del eje X a 90 grados para que queden verticales

    # Guardar el diagrama en el diccionario global
    graficos_vehiculos[nombre_grafico] = diagrama

    return diagrama

# Función para agregar tareas
def agregar_proceso(nombre_grafico, t0, duracion, vehiculo, nombre, tecnico, color=None):
    diagrama = graficos_vehiculos.get(nombre_grafico)
    if diagrama is None:
        print(f"Error: El gráfico '{nombre_grafico}' no existe.")
        return

    vehiculos = diagrama["vehiculos"]
    ax = diagrama["ax"]
    hbar = diagrama["hbar"]

    if tecnico in colores_tecnicos:
        color = colores_tecnicos[tecnico]
    else:
        if color is None:
            # Sortear un color del diccionario
            color = rdm.choice(colores_tec_disponibles)
            colores_tec_disponibles.remove(color)  # Opcional: elimina el color para evitar repetirlo
        colores_tecnicos[tecnico] = color

    ind_veh = vehiculos.index(vehiculo)

    # Convertir datetime a número de matplotlib
    inicio_tarea_num = mdates.date2num(t0)
    duracion_num = duracion.total_seconds() / (24 * 3600)  # Duración en días


    rect_border = ax.broken_barh([(inicio_tarea_num, duracion_num)],
                                    (hbar * ind_veh, hbar),
                                    facecolors='white',  # Color del borde
                                    edgecolor='white',   # Borde negro
                                    linewidth=3)         # Ancho del borde

    # Barra principal
    rect_bar = ax.broken_barh([(inicio_tarea_num, duracion_num)],
                                (hbar * ind_veh, hbar),
                                facecolors=color)  # Color de la barra


    label = ax.text(x=inicio_tarea_num + duracion_num / 2,
               y=hbar * ind_veh + hbar / 2, 
               s=f'{nombre}\n{duracion}\n({tecnico})', 
               va="center", ha="center", color="white", fontsize=6)  


    if "barras" not in diagrama:    # Guardar información de la barra y la etiqueta para futuras interacciones
        diagrama["etiq_barras"] = []
    diagrama["etiq_barras"].append({"rect": rect_bar,
                                    "label": label,
                                    "vehiculo": vehiculo,
                                    "nombre": nombre})

