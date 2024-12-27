import customtkinter as ctk
import database.BBDD as BBDD
import  controller.controller as controller
import  controller.glo as glo
from    view.estilos import *
from menu import submenu_importar as sub_importar

# Configuración global del estilo de customtkinter
ctk.set_appearance_mode("dark")  # Modo oscuro por defecto
ctk.set_default_color_theme("dark-blue")  # Colores por defecto con tonos azulados

class ContenidoReferencias():

    def __init__(self, contenedor, bbdd):
        # Crear un Canvas en el frame de Vehículos
        self.canvasReferencias = ctk.CTkCanvas(contenedor, bg=rojoMuyOscuro, highlightthickness=0)
        self.canvasReferencias.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True)

        # Crear un Scrollbar y conectarlo con el Canvas
        self.scrollbarReferencias = ctk.CTkScrollbar(contenedor, orientation=ctk.VERTICAL, command=self.canvasReferencias.yview, width=20, button_color=blancoFrio)
        self.scrollbarReferencias.pack(side=ctk.LEFT, fill=ctk.Y)

        self.canvasReferencias.configure(yscrollcommand=self.scrollbarReferencias.set)
        self.canvasReferencias.bind('<Configure>', lambda e: self.canvasReferencias.configure(scrollregion=self.canvasReferencias.bbox("all")))

        # Crear un frame dentro del Canvas
        self.frameReferenciasInterior = ctk.CTkFrame(self.canvasReferencias, bg_color=grisAzuladoClaro)
        self.canvasReferencias.create_window((0, 0), window=self.frameReferenciasInterior, anchor="nw")


        self.llenar_contenido(bbdd)

        # Vincular la rueda del mouse al desplazamiento del Canvas
        self.canvasReferencias.bind_all("<MouseWheel>", self.on_mouse_wheel)  # Para Windows y Linux
        self.canvasReferencias.bind_all("<Button-4>", self.on_mouse_wheel)    # Para sistemas basados en X11
        self.canvasReferencias.bind_all("<Button-5>", self.on_mouse_wheel)

    def on_mouse_wheel(self, event):
        self.canvasReferencias.yview_scroll(-1 * (event.delta // 120), "units")

    def llenar_contenido(self, bbdd):

        #Titulo de marcas modelos
        self.labelIdModelos = ctk.CTkLabel(self.frameReferenciasInterior, text="MARCAS - Modelos", font=textoBajo, fg_color=grisOscuro, anchor="w")
        self.labelIdModelos.grid(row=0, column=1, sticky="ew")

        #Titulo de Referencias
        self.labelReferencias = ctk.CTkLabel(self.frameReferenciasInterior, text="REFERENCIAS", font=textoBajo, fg_color=grisOscuro)
        self.labelReferencias.grid(row=0, column=2, sticky="ew")
        self.frameReferenciasInterior.grid_columnconfigure(1, weight=1)
        
        #############################################################################################
        ################################ Botón de IMPORTAR referencia ################################
        #############################################################################################
        self.button_AnadirReferencia = ctk.CTkButton(master=self.frameReferenciasInterior,text="Importar\nReferencias", font=textoBajo,
                                                hover_color=grisOscuro, fg_color=naranjaOscuro, border_color=blancoFrio,
                                                border_width=1,width=40, corner_radius=10,
                                                command= lambda:sub_importar.vent_importar_referencias_modelos(bbdd))
        self.button_AnadirReferencia.grid(row=0, column=0, padx=3, pady=5)
        ############################################################################################
        ############################################################################################


        #############################################################################################
        ################################ Botón de CREAR referencia ##################################
        #############################################################################################
        self.button_AnadirReferencia = ctk.CTkButton(master=self.frameReferenciasInterior,text="Añadir\nReferencia", font=textoBajo,
                                                hover_color=grisOscuro, fg_color=amarilloOscuro, border_color=blancoFrio,
                                                border_width=1,width=40, corner_radius=10,
                                                command= lambda:controller.crear_referencia(bbdd))
        self.button_AnadirReferencia.grid(row=0, column=7, padx=3, pady=5)
        ############################################################################################
        ############################################################################################

        
        ############################################################################################
        ################################ Botones de EDITAR modelo ##################################
        ############################################################################################
        self.df_Modelos_referencias = BBDD.leer_referencias_modelos_df(bbdd)
        self.df_Modelos_referencias = self.df_Modelos_referencias.sort_values(by='ID_MODELO', ascending=True)
        print("el dataframe de referencias es\n:" , self.df_Modelos_referencias)
        self.idModelos = self.df_Modelos_referencias['ID_MODELO'].to_list()
        self.referencias = self.df_Modelos_referencias['REFERENCIA'].to_list()
        print("la lista de modelos es0:\n", self.idModelos)
        print("la lista de referencias es:\n", self.referencias)

        for filasCambiarMod in range (1, len(self.df_Modelos_referencias)+1):

            button_name = f"ButtonAgregar{filasCambiarMod}"
            glo.btt_editModelos[button_name] = ctk.CTkButton(master=self.frameReferenciasInterior,text="Editar", font=textoBajo,
                                                             fg_color=azulOscuro, width=40, corner_radius=15,
                                                            command=lambda varBoton=button_name:controller.editar_referencia(varBoton, bbdd))
            glo.btt_editModelos[button_name].grid(row=1+filasCambiarMod, column=0, padx=2, sticky = "ew")
        ############################################################################################
        ############################################################################################
                 

        ###########################################################################################
        ################################ LABEL DE REFERENCIAS #####################################
        ###########################################################################################
        #Lee los nombres desde la BBDD y los almacena en variables
        for filas, modelo, referencia in zip(range(1, len(self.df_Modelos_referencias)+1), self.idModelos, self.referencias):                 
            label_name_IdModelo = f"labelIdModelo{filas}"
            print(label_name_IdModelo, modelo)
            # Crear etiquetas para referencias con nombres segun BD
            glo.lbl_IdModelos[label_name_IdModelo] = ctk.CTkLabel(self.frameReferenciasInterior, text=modelo,
                                                                                   font=texto1Medio, fg_color=grisAzuladoOscuro, anchor="w")
            glo.lbl_IdModelos[label_name_IdModelo].grid(row=1+filas, column=1, padx=3, sticky="ew")

            label_name_referencia = f"labelReferencia{filas}"
            print(label_name_referencia, referencia)
            # Crear etiquetas para referencias con nombres segun BD
            glo.lbl_Referencias[label_name_referencia] = ctk.CTkLabel(self.frameReferenciasInterior, text=referencia,
                                                                                   font=texto1Medio, fg_color=grisAzuladoOscuro, anchor="w")
            glo.lbl_Referencias[label_name_referencia].grid(row=1+filas, column=2, padx=3, sticky="ew")
        ############################################################################################
        ############################################################################################

             
        ###########################################################################################
        ############################## Botones de ELIMINAR UNA REFERENCIA##########################
        ###########################################################################################
        self.button_variables_Eliminar= {}
        for filasEliminar in range (1, len(self.df_Modelos_referencias)+1):
            button_name = f"ButtonAgregar{filasEliminar}"
            self.button_variables_Eliminar[button_name] = ctk.CTkButton(master=self.frameReferenciasInterior,text="Eliminar",
                                                                        font=textoBajo, fg_color=rojoMuyOscuro, hover_color = naranjaMedio,width=40, corner_radius=20,
                                                                        command=lambda varBoton=button_name:controller.borrar_referencia(varBoton, bbdd))
            self.button_variables_Eliminar[button_name].grid(row=1+filasEliminar, column= 7, padx=3, pady=2)
        ############################################################################################
        ############################################################################################

    def actualizar_contenido(self, bbdd):
        for widget in self.frameReferenciasInterior.winfo_children():
            widget.destroy()

        self.llenar_contenido(bbdd)
