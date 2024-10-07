import  tkinter as tk
from    tkinter import ttk
import  CRUD as CRUD
import  eventos as eventos
import  re
import  dicc_variables
from    estilos import *
#import  Mod_programador
#import  Objetos
#import  Graficador
#import  ventanas_emergentes
import  menu

class ContenidoVehiculos():

    def __init__(self, contenedor):
    

        # Crear un Canvas en el frame de Vehículos
        canvasVehiculos = tk.Canvas(contenedor, bg=grisAzuladoClaro)
        canvasVehiculos.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Crear un Scrollbar y conectarlo con el Canvas
        scrollbarVehiculos = tk.Scrollbar(contenedor, orient=tk.VERTICAL, command=canvasVehiculos.yview)
        scrollbarVehiculos.pack(side=tk.LEFT, fill=tk.Y)

        canvasVehiculos.configure(yscrollcommand=scrollbarVehiculos.set)
        canvasVehiculos.bind('<Configure>', lambda e: canvasVehiculos.configure(scrollregion=canvasVehiculos.bbox("all")))

        # Crear un frame dentro del Canvas
        frameVehiculosInterior = tk.Frame(canvasVehiculos, bg=grisAzuladoClaro)
        canvasVehiculos.create_window((0, 0), window=frameVehiculosInterior, anchor="nw")



        ### Añadir contenido al frame interno ###
        #Titulo de marcas
        labelVehiculos = tk.Label(frameVehiculosInterior, text="MARCAS - Modelos", font=textoBajo, bg=grisAzuladoClaro, fg=blancoHueso, anchor="w")
        labelVehiculos.grid(row=0, column=1, sticky="ew")

        #Titulo de tiempos
        labelTiemposVehiculos = tk.Label(frameVehiculosInterior, text="Tiempos", font=textoBajo, bg=grisAzuladoClaro, fg=blancoHueso)
        labelTiemposVehiculos.grid(row=0, column=2, columnspan=5, sticky="ew")
        frameVehiculosInterior.grid_columnconfigure(1, weight=1)


        #Botón de crear modelo nuevo
        button_CrearModelo = tk.Button(frameVehiculosInterior,text="Crear Modelo", font=textoBajo, bg=grisOscuro, fg=grisClaro,
                                    command=eventos.crear_modelo)
        button_CrearModelo.grid(row=0, column=7, padx=3)


        #Botones de editar modelo
        #button_variables_camMod = {}              #Diccionario para almacenar nombres de Botones de editar modelos
        for filasCambiarMod in range (1, CRUD.calcula_modelos()+1):
            button_name = f"ButtonAgregar{filasCambiarMod}"
            dicc_variables.button_variables_camMod[button_name] = tk.Button(frameVehiculosInterior,text="Editar", font=textoMinimo, bg=grisAzuladoMedio, fg=blancoHueso,
                                                                            command=lambda varBoton=button_name:eventos.editar_modelo(varBoton))
            dicc_variables.button_variables_camMod[button_name].grid(row=filasCambiarMod, column=0, padx=3)


        #label_variables_vehiculos = {}            # Diccionario para almacenar las variables de los Labels y sus textos

        #Lee los nombres desde la BBDD y los almacena en variables
        for filasVehiculos, textos in zip(range(1, CRUD.calcula_modelos()+1), CRUD.leer_modelos()):                 
            label_name_vehiculo = f"labelVehiculo{filasVehiculos}"
            print(label_name_vehiculo)

            # Crear etiquetas para vehículos con nombres segun BD
            dicc_variables.label_variables_vehiculos[label_name_vehiculo] = tk.Label(frameVehiculosInterior, text=textos[0]+" - "+textos[1],
                                                                                    font=texto1Bajo, bg=grisAzuladoClaro, fg=blancoHueso, anchor="w")
            dicc_variables.label_variables_vehiculos[label_name_vehiculo].grid(row=filasVehiculos, column=1, sticky="ew")



        # Diccionarios para almacenar las variables y los textos de los entry de tiempos por filas_columnas, ejemplo textExtryTime1_9
        #string_variables = {}
        #entry_variables = {}

        #Crea los campos con los tiempos de proceso 
        for columnastimes in range (1,6):

            for filastimes in range (1, CRUD.calcula_modelos()+1):
                #Damos un nombre a la variable objeto
                string_name = f"textExtryTime{filastimes}_{columnastimes}"
                #print(string_name)
                #Relacionamos el nombre a la variable
                dicc_variables.string_variables[string_name] = tk.StringVar()
                #Extraemos el texto del label correspondiente a la marca-modelo
                texto_label = dicc_variables.label_variables_vehiculos[f"labelVehiculo{filastimes}"].cget("text")
                #Filtramos la última palabra: "modelo"
                palabra_modelo = re.search(r'\b(\w+)\b$', texto_label).group(1)

                #Buscamos en BD el tiempo de proceso correspondiente al modelo
                dicc_variables.string_variables[string_name].set(CRUD.leer_tiempo(palabra_modelo, columnastimes + 1))
                entry_name = f"ExtryTime{filastimes}_{columnastimes}"
                #print(entry_name)
                dicc_variables.entry_variables[entry_name] = tk.Entry(frameVehiculosInterior, font=numerosPequeños, width=4, bg=grisAzuladoClaro, fg=blancoHueso,
                                                                    textvariable=dicc_variables.string_variables[string_name])
                dicc_variables.entry_variables[entry_name].grid(row=filastimes, column=columnastimes + 1)

        button_variables_agregVh = {}
        for filasAgregarVH in range (1, CRUD.calcula_modelos()+1):
            button_name = f"ButtonAgregar{filasAgregarVH}"
            button_variables_agregVh[button_name] = tk.Button(frameVehiculosInterior,text="Añadir a Pedido", font=textoMinimo, bg=moradoMedio, fg=blancoHueso,
                                                            command=lambda varBoton=button_name:eventos.agregar_a_pedido(varBoton))
            button_variables_agregVh[button_name].grid(row=filasAgregarVH, column= 7, padx=3)