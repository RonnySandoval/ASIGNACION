import  tkinter as tk
from    tkinter import ttk
import customtkinter as ctk
import BBDD
import  eventos as eventos
import  re
import  dicc_variables
from    estilos import *


# Configuración global del estilo de customtkinter
ctk.set_appearance_mode("dark")  # Modo oscuro por defecto
ctk.set_default_color_theme("dark-blue")  # Colores por defecto con tonos azulados

class ContenidoModelos():

    def __init__(self, contenedor, bbdd):
    

        # Crear un Canvas en el frame de Vehículos
        self.canvasVehiculos = ctk.CTkCanvas(contenedor, bg=grisAzuladoClaro)
        self.canvasVehiculos.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Crear un Scrollbar y conectarlo con el Canvas
        self.scrollbarVehiculos = ctk.CTkScrollbar(contenedor, orientation=ctk.VERTICAL, command=self.canvasVehiculos.yview)
        self.scrollbarVehiculos.pack(side=ctk.LEFT, fill=ctk.Y)

        self.canvasVehiculos.configure(yscrollcommand=self.scrollbarVehiculos.set)
        self.canvasVehiculos.bind('<Configure>', lambda e: self.canvasVehiculos.configure(scrollregion=self.canvasVehiculos.bbox("all")))

        # Crear un frame dentro del Canvas
        self.frameVehiculosInterior = ctk.CTkFrame(self.canvasVehiculos, bg_color=grisAzuladoClaro)
        self.canvasVehiculos.create_window((0, 0), window=self.frameVehiculosInterior, anchor="nw")



        ### Añadir contenido al frame interno ###
        #Titulo de marcas
        self.labelVehiculos = ctk.CTkLabel(self.frameVehiculosInterior, text="MARCAS - Modelos", font=textoBajo, fg_color=grisAzuladoClaro, anchor="w")
        self.labelVehiculos.grid(row=0, column=1, sticky="ew")

        #Titulo de tiempos
        self.labelTiemposVehiculos = ctk.CTkLabel(self.frameVehiculosInterior, text="Tiempos", font=textoBajo, fg_color=grisAzuladoClaro)
        self.labelTiemposVehiculos.grid(row=0, column=2, columnspan=5, sticky="ew")
        self.frameVehiculosInterior.grid_columnconfigure(1, weight=1)


        #Botón de crear modelo nuevo
        self.button_CrearModelo = ctk.CTkButton(master=self.frameVehiculosInterior,text="Crear Modelo", font=textoBajo, hover_color=grisOscuro, fg_color=grisAzuladoClaro, width=40, corner_radius=10,
                                    command=eventos.crear_modelo)
        self.button_CrearModelo.grid(row=0, column=7, padx=3)


        #Botones de editar modelo
        #button_variables_camMod = {}              #Diccionario para almacenar nombres de Botones de editar modelos
        for filasCambiarMod in range (1, BBDD.calcula_modelos(bbdd)
                                      
                                      +1):
            button_name = f"ButtonAgregar{filasCambiarMod}"
            dicc_variables.button_variables_camMod[button_name] = ctk.CTkButton(master=self.frameVehiculosInterior,text="Editar", font=textoMinimo, hover_color=grisAzuladoMedio, fg_color=grisAzuladoOscuro, width=40, corner_radius=10,
                                                                            command=lambda varBoton=button_name:eventos.editar_modelo(varBoton))
            dicc_variables.button_variables_camMod[button_name].grid(row=filasCambiarMod, column=0, padx=3)


        #label_variables_vehiculos = {}            # Diccionario para almacenar las variables de los Labels y sus textos

        #Lee los nombres desde la BBDD y los almacena en variables
        for filasVehiculos, textos in zip(range(1, BBDD.calcula_modelos(bbdd)+1), BBDD.leer_modelos(bbdd)):                 
            label_name_vehiculo = f"labelVehiculo{filasVehiculos}"
            print(label_name_vehiculo, textos[1], textos[2])
            # Crear etiquetas para vehículos con nombres segun BD
            dicc_variables.label_variables_vehiculos[label_name_vehiculo] = ctk.CTkLabel(self.frameVehiculosInterior, text=textos[1]+" - "+textos[0],
                                                                                    font=texto1Bajo, fg_color=grisAzuladoClaro, anchor="w")
            dicc_variables.label_variables_vehiculos[label_name_vehiculo].grid(row=filasVehiculos, column=1, sticky="ew")


        dfTiempos=BBDD.leer_tiempos_procesos(bbdd)
        print(dfTiempos)
        #Crea los campos con los tiempos de proceso 
        for columnastimes in range (1, BBDD.calcula_procesos(bbdd)+1):

            for filastimes in range (1, BBDD.calcula_modelos(bbdd)+1):
                string_name = f"textExtryTime{filastimes}_{columnastimes}"                              #Damos un nombre a la variable objeto
                dicc_variables.string_variables[string_name] = tk.StringVar()                           #Relacionamos el nombre a la variable
                texto_label = dicc_variables.label_variables_vehiculos[f"labelVehiculo{filastimes}"].cget("text")      #Extraemos el texto del label correspondiente a la marca-modelo
                palabra_modelo = re.search(r'\b(\w+)\b$', texto_label).group(1)                         #Filtramos la última palabra: "modelo"
                indice_fila = dfTiempos.index[dfTiempos['MODELO'] == palabra_modelo].tolist()  # Obtiene el índice de la fila
                titulo_columna=dfTiempos.columns[columnastimes]
                print("fila=", indice_fila, ". columna=", columnastimes + 1)

                #print(palabra_modelo)
                #Buscamos en BD el tiempo de proceso correspondiente al modelo

                dicc_variables.string_variables[string_name].set(dfTiempos.loc[indice_fila[0], titulo_columna])
                #dicc_variables.string_variables[string_name].set(CRUD.leer_tiempo(palabra_modelo, columnastimes + 1))
                entry_name = f"ExtryTime{filastimes}_{columnastimes}"
                print(entry_name, dicc_variables.string_variables[string_name])
                dicc_variables.entry_variables[entry_name] = tk.Entry(self.frameVehiculosInterior, font=numerosPequeños, width=4, bg=grisOscuro, fg=blancoCalido,
                                                                    textvariable=dicc_variables.string_variables[string_name])
                dicc_variables.entry_variables[entry_name].grid(row=filastimes, column=columnastimes + 1)

        # Configurar columnas para que se expandan
        self.frameVehiculosInterior.grid_columnconfigure(columnastimes + 1, weight=1)  # Configura la columna correspondiente al CTkEntry

        self.button_variables_agregVh = {}
        for filasAgregarVH in range (1, BBDD.calcula_modelos(bbdd)+1):
            self.button_name = f"ButtonAgregar{filasAgregarVH}"
            self.button_variables_agregVh[button_name] = ctk.CTkButton(master=self.frameVehiculosInterior,text="Añadir a Pedido", font=textoMinimo, hover_color=moradoMedio, fg_color=grisAzuladoOscuro, width=40, corner_radius=20,
                                                            command=lambda varBoton=button_name:eventos.agregar_a_pedido(varBoton))
            self.button_variables_agregVh[button_name].grid(row=filasAgregarVH, column= 7, padx=3)