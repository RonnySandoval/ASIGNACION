import tkinter as tk
import customtkinter as ctk
import estilos
import pandas as pd

class VentanaDefinirProcesos():
    def __init__(self, datosStep1):

        self.rootAux = ctk.CTkToplevel()
        self.rootAux.title("Crear Nueva Planta")
        self.rootAux.config(background = estilos.grisOscuro)
        self.rootAux.iconbitmap("logo5.ico")
        self.rootAux.geometry("850x500")

        self.frameTitulo = ctk.CTkFrame(self.rootAux, fg_color = estilos.grisOscuro)
        self.frameTitulo.pack(expand=True, side="top", fill="both")
        self.frameEntradas = ctk.CTkFrame(self.rootAux, fg_color=estilos.grisOscuro)
        self.frameEntradas.pack(expand=True, side="bottom", fill="both", pady=10, padx=10)

        self.labelTitulo = ctk.CTkLabel(self.frameTitulo,   text = f"Definir procesos para\nPlanta {datosStep1["nombre"]}",
                                               font = estilos.textoMedio, text_color = estilos.blancoFrio, bg_color = estilos.grisOscuro)
        self.labelTitulo.pack(expand=True, side="top", fill="both")

        self.labelNombre        = ctk.CTkLabel(self.frameEntradas,   text = "Nombre",      font = estilos.textoMedio, text_color = estilos.blancoFrio, bg_color = estilos.grisOscuro)
        self.labelId            = ctk.CTkLabel(self.frameEntradas,   text = "Id Proceso",  font = estilos.textoMedio, text_color = estilos.blancoFrio, bg_color = estilos.grisOscuro)
        self.labelDescripcion   = ctk.CTkLabel(self.frameEntradas,   text = "Descripción", font = estilos.textoMedio, text_color = estilos.blancoFrio, bg_color = estilos.grisOscuro)
        self.labelSecuencia     = ctk.CTkLabel(self.frameEntradas,   text = "Secuencia",   font = estilos.textoMedio, text_color = estilos.blancoFrio, bg_color = estilos.grisOscuro)

        self.labelNombre     .grid(row=0, column=1, sticky="ew", padx=20, pady=5)
        self.labelId         .grid(row=0, column=2, sticky="ew", padx=20, pady=5)
        self.labelDescripcion.grid(row=0, column=3, sticky="ew", padx=20, pady=5)
        self.labelSecuencia  .grid(row=0, column=4
                                   , sticky="ew", padx=20, pady=5)

        self.cantidadProcesos = int(datosStep1["cantidadProcesos"])
        self.dicc_Entry_Procesos     = {}
        self.dicc_StringVar_Procesos = {}
        self.encabezados = ["nombre","id","descripcion","secuencia"]
        self.genera_formulario()

        self.buttonAtras      = ctk.CTkButton(self.frameEntradas, text="Atrás",     font = estilos.textoGrande, text_color = estilos.blancoFrio,
                                              fg_color = estilos.rojoMedio,     hover_color = estilos.rojoOscuro, corner_radius=25, command="")  
        self.buttonCancelar   = ctk.CTkButton(self.frameEntradas, text="Cancelar",  font = estilos.texto1Bajo, text_color = estilos.blancoFrio,
                                              fg_color = estilos.naranjaMedio,        hover_color = estilos.naranjaOscuro, corner_radius=25, command="")   
        self.buttonCargar  = ctk.CTkButton(self.frameEntradas, text="Cargar",       font = estilos.texto1Bajo, text_color = estilos.blancoFrio,
                                              fg_color = estilos.azulMedio,     hover_color = estilos.azulOscuro, corner_radius=25, command="")
        self.buttonSiguiente  = ctk.CTkButton(self.frameEntradas, text="Siguiente", font = estilos.textoGrande, text_color = estilos.blancoFrio,
                                              fg_color = estilos.grisVerdeMedio,     hover_color = estilos.grisVerdeOscuro, corner_radius=25, command="")

        self.buttonAtras.grid    (row= self.cantidadProcesos + 2, column=1, pady=25)
        self.buttonCancelar.grid (row= self.cantidadProcesos + 2, column=2, pady=25)
        self.buttonCargar.grid   (row= self.cantidadProcesos + 2, column=3, pady=25)   
        self.buttonSiguiente.grid(row= self.cantidadProcesos + 2, column=4, pady=25)

    def genera_formulario(self):
        for fila in (range (1, self.cantidadProcesos+1)):

            for columna in self.encabezados:
                ctk.CTkLabel(self.frameEntradas,
                            text = "Proceso",
                            font = estilos.textoMedio,
                            text_color = estilos.blancoFrio,
                            bg_color = estilos.grisOscuro).grid(row=fila,
                                                                column=0,
                                                                sticky="ew",
                                                                padx=20,
                                                                pady=5)
                
                string_name = f"text_Fila{fila}_Columna{columna}"                  # Damos un nombre a la variable objeto
                self.dicc_StringVar_Procesos[string_name] = tk.StringVar()         # Relacionamos el nombre a la variable en el diccionario de StringVar
                entry_name = string_name                                            # Damos un nombre al entry 
                print(entry_name, self.dicc_StringVar_Procesos[string_name])

                self.dicc_StringVar_Procesos[entry_name] = ctk.CTkEntry(self.frameEntradas, font=estilos.textoMedio, width=50, bg_color=estilos.grisOscuro,
                                                                    textvariable=self.dicc_StringVar_Procesos[string_name])
                self.dicc_StringVar_Procesos[entry_name].grid(row=fila, column = self.encabezados.index(columna) + 1, sticky="nsew", padx=2, pady=2)

            self.frameEntradas.grid_columnconfigure(fila, weight=2)  # Configura la columna correspondiente al CTkEntry

    def genera_df_datos(self):
        for clave, valor in self.dicc_StringVar_Procesos.items(): print(clave, " : ", valor.get())

        dicc_para_dataframe = {}
        for key, value in self.dicc_StringVar_Procesos.items():          # Extraer fila y columna
            fila = int(key.split("Fila")[1].split("_")[0])
            columna = key.split("Columna")[1]
            
            if fila not in dicc_para_dataframe:                 # Agregar valor al diccionario procesado
                dicc_para_dataframe[fila] = {}
            dicc_para_dataframe[fila][columna] = value.get()

        self.df = pd.DataFrame.from_dict(dicc_para_dataframe, orient='index')  # Crear el DataFrame
        print(self.df)

    def asignafuncion(self, funcionAtras, funcionCargar, funcionCancelar, funcionSiguiente):               #Método para asignar la función al command button de aceptar y cancelar desde otro módulo.

        self.buttonAtras.configure(command = funcionAtras)
        self.buttonAtras.configure(command = funcionCargar)       
        self.buttonCancelar.configure(command = funcionCancelar)
        self.buttonSiguiente.configure(command = funcionSiguiente)