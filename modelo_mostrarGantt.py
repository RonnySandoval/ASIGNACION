import matplotlib.pyplot as plt
import numpy as np
import random as rdm
import matplotlib.dates as mdates
from matplotlib.patches import FancyBboxPatch
import fechahora
from datetime import datetime, timedelta


##################################################################################################################
########################################  GRÁFICOS PARA TÉCNICOS  ################################################
##################################################################################################################

# Diccionario global para almacenar las figuras
graficos_tecnicos = {}

# Función para crear el gráfico
def crear_gantt_tecnicos(nombre_grafico, tecnicos, inicio, horizonte):

    plt.style.use('dark_background')    # Activar modo oscuro en Matplotlib
    hbar = 10
    num_tecnicos = len(tecnicos)
    iniciarEje = fechahora.define_franja(str(inicio.date()))[8]
    fig, gantt = plt.subplots()  # Objetos del plot
    print(iniciarEje)

    diagrama = {
        "fig": fig,
        "ejes": gantt,
        "hbar": hbar,
        "tecnicos": tecnicos,
        "inicio": iniciarEje,
        "horizonte": horizonte
    }

    gantt.set_xlabel('Minutos')             # Etiqueta de eje X
    gantt.set_ylabel('Técnicos')            # Etiqueta de eje Y

    gantt.set_xlim(iniciarEje, horizonte)       # Límites eje X
    gantt.xaxis_date()
    gantt.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))  # Formato de fecha

    locator = mdates.MinuteLocator(byminute=range(0, 60, 30), tz=None)  # Define intervalos exactos
    gantt.xaxis.set_major_locator(locator)
    gantt.grid(True, axis="x", which="both")

    gantt.set_ylim(0, num_tecnicos * hbar)                                          # Límites de eje Y
    gantt.set_yticks(range(hbar, num_tecnicos * hbar, hbar), minor=True)            # Divisiones de eje de técnicos
    gantt.grid(True, axis="y", which="minor")
    gantt.set_yticks(np.arange(hbar / 2, hbar * num_tecnicos - hbar / 2 + hbar, hbar))       # Ubica etiquetas de técnicos
    gantt.set_yticklabels(tecnicos)                                                          # Etiquetas de técnicos

    plt.xticks(rotation=90)                  # Rotar las fechas del eje X a 90 grados para que queden verticales

    graficos_tecnicos[nombre_grafico] = diagrama        # Guardar el diagrama en el diccionario global

    return diagrama



# Función para agregar tareas
colores_vehiculos = {}
def agregar_vehiculo(nombre_grafico, t0, duracion, tecnico, nombre, color=None):
    diagrama = graficos_tecnicos.get(nombre_grafico)
    if diagrama is None:
        print(f"Error: El gráfico '{nombre_grafico}' no existe.")
        return

    tecnicos = diagrama["tecnicos"]
    gantt = diagrama["ejes"]
    hbar = diagrama["hbar"]

    if nombre in colores_vehiculos:
        color = colores_vehiculos[nombre]
    else:
        if color is None:
            color = (rdm.uniform(0, 0.7), rdm.uniform(0, 0.7), rdm.uniform(0, 0.7))
        colores_vehiculos[nombre] = color


    if color is None:
        color = (rdm.uniform(0, 0.7), rdm.uniform(0, 0.7), rdm.uniform(0, 0.7))

    ind_tec = tecnicos.index(tecnico)

    # Convertir datetime a número de matplotlib
    inicio_tarea_num = mdates.date2num(t0)
    duracion_num = duracion.total_seconds() / (24 * 3600)  # Duración en días


    gantt.broken_barh([(inicio_tarea_num, duracion_num)],
                      (hbar * ind_tec, hbar),
                      facecolors=color
                      )
    gantt.text(x=inicio_tarea_num + duracion_num / 2,
               y=hbar * ind_tec + hbar / 2,
               s=f'{nombre}\n({duracion})',
               va="center", ha="center",
               color="w", fontsize=6)

# Función para mostrar un gráfico específico
def mostrar_grafico_tecnicos(nombre_grafico):
    diagrama = graficos_tecnicos.get(nombre_grafico)
    if diagrama is None:
        print(f"Error: El gráfico '{nombre_grafico}' no existe.")
        return

    plt.figure(diagrama["fig"].number)  # Seleccionar la figura por número
    plt.show()




###################################################################################################################
########################################  GRÁFICOS PARA VEHÍCULOS  ################################################
###################################################################################################################
# Diccionario global para almacenar las figuras
graficos_vehiculos = {}         # Diccionario global para almacenar las figuras

# Función para crear el gráfico
def crear_gantt_vehiculos(nombre_grafico, vehiculos, inicio , horizonte):
    hbar = 10
    num_vehiculos = len(vehiculos)
    iniciarEje = fechahora.define_franja(str(inicio.date()))[8]
    fig, gantt = plt.subplots()  # Objetos del plot
    print("iniciar eje en:", iniciarEje)

    diagrama = {
        "fig": fig,
        "ejes": gantt,
        "hbar": hbar,
        "vehiculos": vehiculos,
        "inicio": iniciarEje,
        "horizonte": horizonte,
    }

    gantt.set_xlabel('Fecha/hora')                     # Etiqueta de eje X
    gantt.set_ylabel('Vehículos')                   # Etiqueta de eje Y

    gantt.set_xlim(iniciarEje, horizonte)               # Límites eje X
    gantt.xaxis_date()
    gantt.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))  # Formato de fecha

    locator = mdates.MinuteLocator(byminute=range(0, 60, 30), tz=None)  # Define intervalos exactos
    gantt.xaxis.set_major_locator(locator)
    gantt.grid(True, axis="x", which="both")

    gantt.set_ylim(0, num_vehiculos * hbar)                                 # Límites de eje Y
    gantt.set_yticks(range(hbar, num_vehiculos * hbar, hbar), minor=True)   # Divisiones de eje de técnicos
    gantt.grid(True, axis="y", which="minor")

    gantt.set_yticks(np.arange(hbar / 2, hbar * num_vehiculos - hbar / 2 + hbar, hbar))  # Etiquetas de técnicos
    gantt.set_yticklabels(vehiculos)

    plt.xticks(rotation=90)                  # Rotar las fechas del eje X a 90 grados para que queden verticales

    # Guardar el diagrama en el diccionario global
    graficos_vehiculos[nombre_grafico] = diagrama

    return diagrama



# Diccionario para almacenar los colores de cada técnico
colores_tecnicos = {}

# Función para agregar tareas
def agregar_proceso(nombre_grafico, t0, duracion, vehiculo, nombre, tecnico, color=None):
    diagrama = graficos_vehiculos.get(nombre_grafico)
    if diagrama is None:
        print(f"Error: El gráfico '{nombre_grafico}' no existe.")
        return

    vehiculos = diagrama["vehiculos"]
    gantt = diagrama["ejes"]
    hbar = diagrama["hbar"]

    if tecnico in colores_tecnicos:
        color = colores_tecnicos[tecnico]
    else:
        if color is None:
            color = (rdm.uniform(0, 0.7), rdm.uniform(0, 0.7), rdm.uniform(0, 0.7))
        colores_tecnicos[tecnico] = color

    ind_veh = vehiculos.index(vehiculo)

    # Convertir datetime a número de matplotlib
    inicio_tarea_num = mdates.date2num(t0)
    duracion_num = duracion.total_seconds() / (24 * 3600)  # Duración en días



    gantt.broken_barh(
        [(inicio_tarea_num, duracion_num)],
        (hbar * ind_veh, hbar),
        facecolors=color
        )
    gantt.text(x=inicio_tarea_num + duracion_num / 2,
               y=hbar * ind_veh + hbar / 2, 
               s=f'{nombre}\n{duracion}\n({tecnico})', 
               va="center", ha="center", color="w", fontsize=6)
    

# Función para mostrar un gráfico específico
def mostrar_grafico_vehiculos(nombre_grafico):
    diagrama = graficos_vehiculos.get(nombre_grafico)
    if diagrama is None:
        print(f"Error: El gráfico con '{nombre_grafico}' no existe.")
        return

    plt.figure(diagrama["fig"].number)  # Seleccionar la figura por número
    plt.show()
