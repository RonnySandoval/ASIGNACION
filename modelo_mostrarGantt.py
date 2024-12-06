import matplotlib.pyplot as plt
import numpy as np
import random as rdm
import matplotlib.dates as mdates
import matplotlib.patches as patches
import fechahora
import estilos

# Diccionarios globales para almacenar las figuras
graficos_vehiculos = {}
graficos_tecnicos = {}

colores = {
    "rojo": "#8B0000",  # Oscuro
    "verde_oscuro": "#006400",
    "azul_marino": "#000080",
    "amarillo": "#CCCC00",  # Oscuro
    "naranja": "#CC5500",  # Oscuro
    "violeta": "#6A0DAD",  # Oscuro
    "marrón": "#6F4F37",
    "negro": "#000000",
    "marrón_claro": "#4B3F26",  # Oscuro
    "gris": "#808080",
    "rojo_fuego": "#B22222",
    "azul_pavo": "#4682B4",  # Oscuro
    "rojo_rubí": "#9B111E",
    "verde_lima": "#228B22",  # Oscuro
    "azul_turquesa": "#008B8B",  # Oscuro
    "rosa": "#B23276",  # Oscuro
    "magenta": "#8B008B",  # Oscuro
    "gris_oscuro": "#A9A9A9",
    "perla": "#C0B0A4",  # Oscuro
    "coral": "#8B3E2F",  # Oscuro
    "fucsia": "#C71585",  # Oscuro
    "chocolate": "#8B4513",
    "caramelo": "#8B5A2B",  # Oscuro
    "turquesa_oscuro": "#00CED1",
    "esmeralda": "#2E8B57",  # Oscuro
    "perla_claro": "#C4C4C4",  # Oscuro
    "lavanda_oscuro": "#6A4C92",
    "rojo_oscuro": "#8B0000",
    "azul_acero": "#4682B4",
    "verde_menta": "#98FB98",  # Oscuro
    "verde_manzana": "#6B8E23",  # Oscuro
    "verde_pastel": "#66CDAA",  # Oscuro
    "verde_mar": "#2E8B57",
    "perla_gris": "#B8B8B8",  # Oscuro
    "lila": "#C8A2C8",
    "jade": "#006747",  # Oscuro
    "fucsia_claro": "#D700FF",  # Oscuro
    "salmon": "#D2691E",  # Oscuro
    "lavanda_claro": "#B080C7",  # Oscuro
    "verde_pino": "#228B22",
    "vino": "#800000",
    "azul_indigo": "#4B0082",
    "rosa_oscuro": "#C71585",
    "amarillo_claro": "#CCCC00",  # Oscuro
    "celeste": "#4682B4",  # Oscuro
    "esmeralda_claro": "#2E8B57",
    "rojo_claro": "#B22222",
    "naranja_oscuro": "#FF8C00",
    "gris_azulado": "#708090",
    "gris_verde": "#9E9E9E",
    "cobalto": "#0047AB",
    "ciruela": "#8E4585",
    "verde_agua": "#20B2AA",
    "acero": "#A2A2A1",
    "azul_piscina": "#2E8B57",  # Oscuro
    "granate": "#9E2A2F",
    "piedra": "#B6B6B6",
    "beige": "#F5F5DC",
    "melocotón": "#FFB07C",  # Oscuro
    "madera": "#C2B280",
    "azul_papel": "#5F9EA0",  # Oscuro
    "café_oscuro": "#3E2723",
    "carbón": "#333333",
    "acero_azul": "#4682B4",
    "beige_oscuro": "#C4A57C",  # Oscuro
    "rojo_ladrillo": "#8B0000",
    "oro": "#FFD700",
    "verde_turquesa": "#40E0D0",
    "morado_claro": "#8A2BE2",  # Oscuro
    "madera_oscuro": "#6F4F37",
    "pistacho": "#6E7B3C",  # Oscuro
    "burlington": "#7D3C29",
    "azul_golf": "#4B9CD3",
    "turquesa": "#40E0D0",
    "rosa_claro": "#D58D7A",  # Oscuro
    "salmón_claro": "#FF9E3B",  # Oscuro
    "lavanda": "#7A3D91",  # Oscuro
    "cielo": "#4B8BBE",  # Oscuro
    "rojo": "#8B0000",
    "rojo_oscuro": "#8B0000",
    "azul_galaxia": "#2A2D99",
    "naranja_claro": "#FF6600",  # Oscuro
    "madera_claro": "#9E7B4A",  # Oscuro
    "grana": "#9E2A2F",
    "morado": "#800080",
    "turquesa_claro": "#008B8B",
    "lima": "#9ACD32",  # Oscuro
    "gris_claro": "#A9A9A9",
    "gris_plata": "#A2A2A1",  # Oscuro
    "piedra_claro": "#A3A3A3",  # Oscuro
    "agua_marina": "#66CDAA",
    "pistacho_claro": "#7C9A1F",   # Oscuro
    "azul_noche": "#1A1A7D",
    "marrón_oscuro": "#3E2A47",
    "gris_plomo": "#5A5A5A",
    "rojo_morado": "#9B2335",
    "café_claro": "#4A2C2A",
    "rosa_palo": "#C88C8C",
    "madera_tierra": "#6F4F37",
    "gris_antracita": "#2F4F4F",
    "ocre": "#CC7722",
    "verde_grisaceo": "#6B8E23",
    "azul_tintado": "#4C6A92",
    "naranja_oscuro_2": "#D75B4E",
    "rojo_corcho": "#9C3D34",
    "gris_oscuro_2": "#6C6C6C",
    "verde_botella": "#006747",
    "morado_vino": "#800000",
    "verde_hoja": "#2F6B3E",
    "azul_oscuro_2": "#1D3C6A",
    "negro_azulado": "#0A0F3D",
    "amarillo_terroso": "#BDBB73",
    "gris_roto": "#8A8A8A",
    "marrón_toscano": "#6B4226",
    "rojo_granate": "#9B111E",
    "naranja_terroso": "#A53C2D",
    "agua_marina_oscuro": "#4B8F8C",
    "ocre_gris": "#B7A67E",
    "verde_subido": "#468C45",
    "rojo_frambuesa": "#990000",
    "morado_oscuro_2": "#5A3D6E",
    "cielo_piedra": "#8F8F8F",
    "verde_oscuro_2": "#006400",
    "azul_grisáceo": "#3B5F73",
    "verde_army": "#4B5320",
    "marrón_rico": "#7A3F32",
    "gris_oxido": "#706C61",
    "azul_gris_2": "#6A7F80",
    "café_miel": "#6B4F2F",
    "piedra_oscuro": "#5C5C5C",
    "madera_natural": "#8B6F47",
    "rojo_marrón": "#8B3A3A",
    "gris_plata_2": "#A2A2A1",
    "verde_oscuro_3": "#4B6A4E",
    "azul_claro_oscuro": "#003366",
    "amarillo_oscuro_2": "#7B7B00",
    "gris_como_piedra": "#B8B8B8",
    "madera_oscura_2": "#5D3F2C",
    "rojo_ladrillo_2": "#8B2A1F",
    "morado_oscuro_3": "#4E2C8C",
    "azul_grisáceo_2": "#6B7F89",
    "amarillo_tierra": "#9E7A2D",
    "marrón_cobarde": "#B67A3D",
    "verde_petróleo": "#2C6B3A",
    "rojo_cereza": "#9E1B32",
    "gris_plata_3": "#C0C0C0",
    "beige_oscuro_2": "#C3B091",
    "azul_mediterráneo": "#2C75B2",
    "verde_fango": "#4C5A3C",
    "rojo_oscuridad": "#8B0000",
    "café_turquesa": "#5B4D3A",
    "naranja_tetra": "#8B4500"

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
    iniciarEje = fechahora.define_franja(str(inicio.date()))[8]
    fig, gantt = plt.subplots()                           # Objetos del plot
    diagrama = {
        "fig": fig,
        "ejes": gantt,
        "hbar": hbar,
        "tecnicos": tecnicos,
        "inicio": iniciarEje,
        "horizonte": horizonte
    }

    # Configuración de ejes
    gantt.set_xlabel('Fecha/hora')             # Etiqueta de eje X
    gantt.set_ylabel('Técnicos')               # Etiqueta de eje Y

    gantt.set_xlim(iniciarEje, horizonte)      # Límites eje X
    gantt.xaxis_date()
    gantt.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))  # Formato de fecha

    # Configuración de límites y ticks en el eje Y
    gantt.set_ylim(0, num_tecnicos * hbar)                                 # Límites de eje Y
    gantt.set_yticks(np.arange(hbar / 2, num_tecnicos * hbar, hbar))       # Ubica etiquetas en el centro de cada barra
    gantt.set_yticklabels(tecnicos)                                        # Etiquetas de técnicos

    # Configuración de la grilla secundaria (para divisiones entre las barras)
    gantt.set_yticks(range(hbar, num_tecnicos * hbar, hbar), minor=True)    # Divisiones menores en eje Y (grilla menor)
    gantt.grid(True, axis='y', which='minor', color='white', linewidth=1)  # Mostrar solo la grilla menor

    # Deshabilitar la grilla principal en el eje Y para evitar el solapamiento con las etiquetas
    gantt.grid(True, axis='y', which='major', color='black', linestyle='', linewidth=0.1)  # Grilla principal de color negro (si es necesario)

    # Configurar los ticks principales (ocultar las marcas de los ticks del eje Y)
    gantt.tick_params(axis='y', which='major', length=0)  # Eliminar marcas en el eje Y, pero las etiquetas permanecen

    
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
    gantt = diagrama["ejes"]
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


    rect_border = gantt.broken_barh([(inicio_tarea_num, duracion_num)],
                                    (hbar * ind_tec, hbar),
                                    facecolors='white',  # Color del borde
                                    edgecolor='white',   # Borde negro
                                    linewidth=3)         # Ancho del borde

    # Barra principal
    rect_bar = gantt.broken_barh([(inicio_tarea_num, duracion_num)],
                                (hbar * ind_tec, hbar),
                                facecolors=color)  # Color de la barra


    label = gantt.text(x=inicio_tarea_num + duracion_num / 2,
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

# Función para mostrar un gráfico específico
def mostrar_grafico_tecnicos(nombre_grafico):
    diagrama = graficos_tecnicos.get(nombre_grafico)
    if diagrama is None:
        print(f"Error: El gráfico '{nombre_grafico}' no existe.")
        return

    plt.figure(diagrama["fig"].number)  # Seleccionar la figura por número
    plt.grid(color=estilos.grisOscuro)  # Ajusta el color de la grilla
    plt.show()


###################################################################################################################
########################################  GRÁFICOS PARA VEHÍCULOS  ################################################
###################################################################################################################

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
    gantt.set_ylabel('Vehículos')                      # Etiqueta de eje Y

    gantt.set_xlim(iniciarEje, horizonte)               # Límites eje X
    gantt.xaxis_date()
    gantt.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))  # Formato de fecha

    # Configuración de límites y ticks en el eje Y
    gantt.set_ylim(0, num_vehiculos * hbar)                                 # Límites de eje Y
    gantt.set_yticks(np.arange(hbar / 2, num_vehiculos * hbar, hbar))       # Ubica etiquetas en el centro de cada barra
    gantt.set_yticklabels(vehiculos)                                        # Etiquetas de técnicos

    # Configuración de la grilla secundaria (para divisiones entre las barras)
    gantt.set_yticks(range(hbar, num_vehiculos * hbar, hbar), minor=True)    # Divisiones menores en eje Y (grilla menor)
    gantt.grid(True, axis='y', which='minor', color='white', linewidth=1)  # Mostrar solo la grilla menor

    # Deshabilitar la grilla principal en el eje Y para evitar el solapamiento con las etiquetas
    gantt.grid(True, axis='y', which='major', color='black', linestyle='', linewidth=0.1)  # Grilla principal de color negro (si es necesario)

    # Configurar los ticks principales (ocultar las marcas de los ticks del eje Y)
    gantt.tick_params(axis='y', which='major', length=0)  # Eliminar marcas en el eje Y, pero las etiquetas permanecen

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
    gantt = diagrama["ejes"]
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


    rect_border = gantt.broken_barh([(inicio_tarea_num, duracion_num)],
                                    (hbar * ind_veh, hbar),
                                    facecolors='white',  # Color del borde
                                    edgecolor='white',   # Borde negro
                                    linewidth=3)         # Ancho del borde

    # Barra principal
    rect_bar = gantt.broken_barh([(inicio_tarea_num, duracion_num)],
                                (hbar * ind_veh, hbar),
                                facecolors=color)  # Color de la barra


    label = gantt.text(x=inicio_tarea_num + duracion_num / 2,
               y=hbar * ind_veh + hbar / 2, 
               s=f'{nombre}\n{duracion}\n({tecnico})', 
               va="center", ha="center", color="white", fontsize=6)  


    if "barras" not in diagrama:    # Guardar información de la barra y la etiqueta para futuras interacciones
        diagrama["etiq_barras"] = []
    diagrama["etiq_barras"].append({"rect": rect_bar,
                                    "label": label,
                                    "vehiculo": vehiculo,
                                    "nombre": nombre})

# Función para mostrar un gráfico específico
def mostrar_grafico_vehiculos(nombre_grafico):
    diagrama = graficos_vehiculos.get(nombre_grafico)
    if diagrama is None:
        print(f"Error: El gráfico con '{nombre_grafico}' no existe.")
        return

    plt.figure(diagrama["fig"].number)  # Seleccionar la figura por número
    plt.grid(color=estilos.grisOscuro)  # Ajusta el color de la grilla
    plt.show()

