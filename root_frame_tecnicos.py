import tkinter as tk
import customtkinter as ctk
import BBDD
import eventos
import glo
from estilos import *

class ContenidoTecnicos:

    def __init__(self, contenedor, bbdd):
        # Crear un Canvas en el frame de Tecnicos
        self.canvasTecnicos = tk.Canvas(contenedor, bg=moradoOscuro)
        self.canvasTecnicos.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Crear un Scrollbar y conectarlo con el Canvas
        self.scrollbarTecnicos = ctk.CTkScrollbar(contenedor, orientation=ctk.VERTICAL, command=self.canvasTecnicos.yview)
        self.scrollbarTecnicos.pack(side=ctk.LEFT, fill=ctk.Y)

        self.canvasTecnicos.configure(yscrollcommand=self.scrollbarTecnicos.set)
        self.canvasTecnicos.bind('<Configure>', lambda e: self.canvasTecnicos.configure(scrollregion=self.canvasTecnicos.bbox("all")))

        # Crear un frame dentro del Canvas
        self.frameTecnicosInterior = ctk.CTkFrame(self.canvasTecnicos, bg_color=grisOscuro)
        self.canvasTecnicos.create_window((0, 0), window=self.frameTecnicosInterior, anchor="ne")

        self.labelTitulo = ctk.CTkLabel(self.frameTecnicosInterior, text="TECNICOS", font=textoGrande, fg_color=grisOscuro, bg_color=blancoHueso, width=50)
        self.labelTitulo .grid(row=0, column=0, columnspan=3, sticky="ew", padx=0, pady=0)

        # Encabezados
        self.labelIdTecnicos = ctk.CTkLabel(self.frameTecnicosInterior, text="ID", font=textoMedio, fg_color=grisOscuro, bg_color=blancoHueso, width=100)
        self.labelIdTecnicos.grid(row=1, column=0, sticky="ew", padx=0, pady=5)

        self.labelTecnicos = ctk.CTkLabel(self.frameTecnicosInterior, text="NOMBRE", font=textoMedio, fg_color=grisOscuro, bg_color=blancoHueso, width=100)
        self.labelTecnicos.grid(row=1, column=1, sticky="ew", padx=0, pady=5)

        self.labelAreaTecnicos = ctk.CTkLabel(self.frameTecnicosInterior, text="ÁREA", font=textoMedio, fg_color=grisOscuro, bg_color=blancoHueso, width=100)
        self.labelAreaTecnicos.grid(row=1, column=2, sticky="ew", padx=0, pady=5)

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
                ##################  LABELS  #################

                label_name_tecnico = f"labeltecnico_{fila}_{columna}_{filasTecnicos[1]}_{columnasTecnicos}"
                print(label_name_tecnico)

                # Crear etiquetas para técnicos con nombres desde la BD
                glo.lbl_Tecnicos[label_name_tecnico] = ctk.CTkLabel(
                    self.frameTecnicosInterior, text=columnasTecnicos,
                    font=texto1Bajo, fg_color=moradoOscuro, bg_color=blancoHueso, anchor="w", width=50)  # Ancho especificado
                glo.lbl_Tecnicos[label_name_tecnico].grid(row= 2 + fila, column=0 + columna, sticky="ew", padx=0, pady=0)


                ################ CHECKBUTTON ###############

                int_name = f"checkIntvar-{filasTecnicos[0]}"                                         #nombre de variable asociada a las intvar
                print(int_name)
                glo.intVar_tecnicos[int_name] = tk.IntVar(value=1)                    # Guardar en el diccionario el nombre y la intvar

                self.check_name_tecnico = f"checkButton-{fila}"                       # nombre del checkbutton
                print(self.check_name_tecnico)
                glo.check_tecnicos[self.check_name_tecnico] = ctk.CTkCheckBox(
                    self.frameTecnicosInterior, text="Programar", 
                    bg_color=moradoOscuro, font=textoMinimo, fg_color=grisOscuro,
                    variable=glo.intVar_tecnicos[int_name])
                glo.check_tecnicos[self.check_name_tecnico].grid(row= 2 + fila, column=3, sticky="ew", padx=10, pady=0)

                columna += 1
            fila += 1


        # Asegurarse que la columna de checkboxes también se ajusta
        self.frameTecnicosInterior.grid_columnconfigure(3, weight=0)

