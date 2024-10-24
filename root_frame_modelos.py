import  tkinter as tk
from    tkinter import ttk
import customtkinter as ctk
import BBDD
import  eventos as eventos
import  re
import  glo
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


        self.llenar_contenido(bbdd)



    def llenar_contenido(self, bbdd):

        #####################################################
        ############Botón de CREAR modelo nuevo##############
        #####################################################
        self.button_CrearModelo = ctk.CTkButton(master=self.frameVehiculosInterior,text="Crear Modelo", font=textoBajo,
                                                hover_color=grisOscuro, fg_color=grisAzuladoClaro, border_color=blancoFrio,
                                                border_width=1,width=40, corner_radius=10,
                                                command= lambda:eventos.crear_modelo(bbdd))
        self.button_CrearModelo.grid(row=0, column=7, padx=3)
        

        #####################################################
        ############ Botones de EDITAR modelo ###############
        #####################################################
        for filasCambiarMod in range (1, BBDD.calcula_modelos(bbdd)+1):

            button_name = f"ButtonAgregar{filasCambiarMod}"
            glo.btt_editModelos[button_name] = ctk.CTkButton(master=self.frameVehiculosInterior,text="Editar", font=textoBajo,
                                                             fg_color=grisAzuladoOscuro, width=40, corner_radius=10,
                                                            command=lambda varBoton=button_name:eventos.editar_modelo(varBoton, bbdd))
            glo.btt_editModelos[button_name].grid(row=1+filasCambiarMod, column=0, padx=3)


        #############################################################
        ################## LABEL DE MODELOS #########################
        #############################################################
        #Lee los nombres desde la BBDD y los almacena en variables
        for filasModelos, textos in zip(range(1, BBDD.calcula_modelos(bbdd)+1),
                                          BBDD.leer_modelos(bbdd)):                 
            label_name_modelo = f"labelVehiculo{filasModelos}"
            print(label_name_modelo, textos[1], textos[2])
            # Crear etiquetas para vehículos con nombres segun BD
            glo.lbl_Modelos[label_name_modelo] = ctk.CTkLabel(self.frameVehiculosInterior, text=textos[0],
                                                                                   font=texto1Medio, fg_color=grisAzuladoClaro, anchor="w")
            glo.lbl_Modelos[label_name_modelo].grid(row=1+filasModelos, column=1, sticky="ew")


        #############################################################
        ################# ENTRY PARA TIEMPOS ########################
        #############################################################

        # CREAR LOS LABEL PARA ID DE PROCESOS
        dfTiempos = BBDD.leer_tiempos_modelos_procesos(bbdd)
        print(dfTiempos)
        titlesDf = dfTiempos.columns.tolist()
        titlesDf.pop(0)
        titlesDf.sort()
        columnaProceso = 0
        #CONSTRUIR LABEL EN UNA FILA CON TANTAS COLUMNAS COMO PROCESOS HAYA
        for proceso in titlesDf:
            columnaProceso += 1
            label_proceso_modelo = f"labelproceso_{proceso}_{columnaProceso}"
            print(label_proceso_modelo)

            glo.lbl_modelProcesos[label_proceso_modelo] = ctk.CTkLabel(self.frameVehiculosInterior, text=proceso,
                                                                        font=textoBajo, fg_color=grisOscuro, bg_color=blancoHueso, anchor="w")
            glo.lbl_modelProcesos[label_proceso_modelo].grid(row=0, column=1+columnaProceso, sticky="nsew", padx=1, pady=1)
            

        #Crea los campos con los tiempos de proceso 
        for columnastimes in range (1, BBDD.calcula_procesos(bbdd)+1):

            for filastimes in range (1, BBDD.calcula_modelos(bbdd)+1):
                string_name = f"textExtryTime{filastimes}_{columnastimes}"                     #Damos un nombre a la variable objeto
                glo.strVar_Tiempos[string_name] = tk.StringVar()                               #Relacionamos el nombre a la variable
                texto_label = glo.lbl_Modelos[f"labelVehiculo{filastimes}"].cget("text")       #Extraemos el texto del label correspondiente a la marca-modelo
                palabra_modelo = re.search(r'\b(\w+)\b$', texto_label).group(1)                #Filtramos la última palabra: "modelo"
                indice_fila = dfTiempos.index[dfTiempos['MODELO'] == palabra_modelo].tolist()  # Obtiene el índice de la fila
                titulo_columna=dfTiempos.columns[columnastimes]
                print("fila=", indice_fila, ". columna=", columnastimes + 1)

                #Buscamos en BD el tiempo de proceso correspondiente al modelo
                glo.strVar_Tiempos[string_name].set(dfTiempos.loc[indice_fila[0], titulo_columna])
                entry_name = f"ExtryTime{filastimes}_{columnastimes}"                           #Damos un nombre al entry
                print(entry_name, glo.strVar_Tiempos[string_name])
                glo.ent_Tiempos[entry_name] = tk.Entry(self.frameVehiculosInterior, font=numerosPequeños, width=4, bg=grisOscuro, fg=blancoCalido,
                                                                    textvariable=glo.strVar_Tiempos[string_name])
                glo.ent_Tiempos[entry_name].grid(row=1+filastimes, column=columnastimes + 1)


        ############################################################
        ############ Botones de INGRESAR un vehiculo #########
        ############################################################

        # Configurar columnas para que se expandan
        self.frameVehiculosInterior.grid_columnconfigure(columnastimes + 1, weight=1)  # Configura la columna correspondiente al CTkEntry

        self.button_variables_agregMod = {}
        for filasAgregarVH in range (1, BBDD.calcula_modelos(bbdd)+1):
            button_name = f"ButtonAgregar{filasAgregarVH}"
            self.button_variables_agregMod[button_name] = ctk.CTkButton(master=self.frameVehiculosInterior,text="Añadir a Pedido", font=textoBajo, fg_color=grisAzuladoOscuro, width=40, corner_radius=20,
                                                            command=lambda varBoton=button_name:eventos.agregar_a_pedido(varBoton, bbdd))
            self.button_variables_agregMod[button_name].grid(row=1+filasAgregarVH, column= 7, padx=3)

    def actualizar_contenido(self, bbdd):
        for widget in self.frameVehiculosInterior.winfo_children():
            widget.destroy()

        self.llenar_contenido(bbdd)
