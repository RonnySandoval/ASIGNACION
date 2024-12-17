import tkinter as tk
import customtkinter as ctk
import BBDD
import glo
from estilos import *

class ContenidoTecnicos:

    def __init__(self, contenedor, bbdd):
        # Crear un Canvas en el frame de Tecnicos
        self.canvasTecnicos = ctk.CTkCanvas(contenedor, bg=moradoOscuro, highlightthickness=0)
        self.canvasTecnicos.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True)

        # Crear un Scrollbar y conectarlo con el Canvas
        self.scrollbarTecnicos = ctk.CTkScrollbar(contenedor, orientation=ctk.VERTICAL, command=self.canvasTecnicos.yview, width=20,  button_color=blancoFrio)
        self.scrollbarTecnicos.pack(side=ctk.LEFT, fill=ctk.Y)

        self.canvasTecnicos.configure(yscrollcommand=self.scrollbarTecnicos.set)
        self.canvasTecnicos.bind('<Configure>', lambda e: self.canvasTecnicos.configure(scrollregion=self.canvasTecnicos.bbox("all")))

        # Crear un frame dentro del Canvas
        self.frameTecnicosInterior = ctk.CTkFrame(self.canvasTecnicos, fg_color=moradoOscuro)
        self.canvasTecnicos.create_window((0, 0), window=self.frameTecnicosInterior, anchor="ne")

        self.labelTitulo = ctk.CTkLabel(self.frameTecnicosInterior, text="TECNICOS", font=textoGrande, fg_color=grisOscuro, bg_color=blancoHueso, width=50)
        self.labelTitulo .grid(row=0, column=0, columnspan=4, sticky="ew", pady=5)

        # Encabezados
        self.labelIdTecnicos = ctk.CTkLabel(self.frameTecnicosInterior, text="ID", font=textoMedio, fg_color=grisOscuro, bg_color=blancoHueso, width=150)
        self.labelIdTecnicos.grid(row=1, column=0, sticky="ew")

        self.labelTecnicos = ctk.CTkLabel(self.frameTecnicosInterior, text="NOMBRE", font=textoMedio, fg_color=grisOscuro, bg_color=blancoHueso, width=150)
        self.labelTecnicos.grid(row=1, column=1, sticky="ew")

        self.labelAreaTecnicos = ctk.CTkLabel(self.frameTecnicosInterior, text="ÁREA", font=textoMedio, fg_color=grisOscuro, bg_color=blancoHueso, width=150)
        self.labelAreaTecnicos.grid(row=1, column=2, sticky="ew")

        self.labelAreaVacio = ctk.CTkLabel(self.frameTecnicosInterior, text="", font=textoMedio, fg_color=grisOscuro, bg_color=blancoHueso, width=150)
        self.labelAreaVacio.grid(row=1, column=3, sticky="ew")

        # Establecer el peso de las columnas para ajustar su ancho
        self.frameTecnicosInterior.grid_columnconfigure(0, weight=0)  # ID
        self.frameTecnicosInterior.grid_columnconfigure(1, weight=0)  # NOMBRE
        self.frameTecnicosInterior.grid_columnconfigure(2, weight=0)  # ÁREA

        self.personal = BBDD.leer_tecnicos_modificado(bbdd)
        # Lee los nombres desde la BBDD y los almacena en variables
        fila = 0
        for filasTecnicos in self.personal:
            columna = 0
            for columnasTecnicos in filasTecnicos:
                ####################################  LABELS  ############################################

                label_name_tecnico = f"labeltecnico_{fila}_{columna}_{filasTecnicos[1]}_{columnasTecnicos}"
                print(label_name_tecnico)

                # Crear etiquetas para técnicos con nombres desde la BD
                glo.lbl_Tecnicos[label_name_tecnico] = ctk.CTkLabel(
                    self.frameTecnicosInterior, text=columnasTecnicos,
                    font=texto1Medio, fg_color=moradoOscuro, bg_color=blancoHueso, anchor="w", width=150)  # Ancho especificado
                glo.lbl_Tecnicos[label_name_tecnico].grid(row= 2 + fila, column=0 + columna, sticky="ew", padx=0, pady=0)


                ################################## CHECKBUTTON ##########################################

                int_name = f"checkIntvar-{filasTecnicos[0]}"                          #nombre de variable asociada a las intvar
                print(int_name)
                glo.intVar_tecnicos[int_name] = tk.IntVar(value=1)                    # Guardar en el diccionario el nombre y la intvar

                self.check_name_tecnico = filasTecnicos[0]                            # nombre del checkbutton
                print(self.check_name_tecnico)
                glo.check_tecnicos[self.check_name_tecnico] = ctk.CTkCheckBox(
                    self.frameTecnicosInterior, text="Programar", 
                    bg_color=moradoOscuro, font=texto1Medio, fg_color=grisOscuro,
                    variable=glo.intVar_tecnicos[int_name])
                glo.check_tecnicos[self.check_name_tecnico].grid(row= 2 + fila, column=3, sticky="ew", padx=10, pady=0)

                columna += 1
                
            fila += 1


        # Asegurarse que la columna de checkboxes también se ajusta
        self.frameTecnicosInterior.grid_columnconfigure(3, weight=0)
        self.frameTecnicosInterior.configure()

        # Vincular la rueda del mouse al desplazamiento del Canvas
        self.canvasTecnicos.bind_all("<MouseWheel>", self.on_mouse_wheel)  # Para Windows y Linux
        self.canvasTecnicos.bind_all("<Button-4>", self.on_mouse_wheel)    # Para sistemas basados en X11
        self.canvasTecnicos.bind_all("<Button-5>", self.on_mouse_wheel)

    def on_mouse_wheel(self, event):
        self.canvasTecnicos.yview_scroll(-1 * (event.delta // 120), "units")
