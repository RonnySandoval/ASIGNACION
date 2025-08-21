import tkinter as tk
import customtkinter as ctk
import database.BDqueries_before as BDqueries_before
import controller.glo as glo
from view.estilos import *

class ContenidoProcesos:

    def __init__(self, contenedor, bbdd):
        # Crear un Canvas en el frame de Tecnicos
        self.canvasProcesos = ctk.CTkCanvas(contenedor, bg=moradoOscuro, highlightthickness=0)
        self.canvasProcesos.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True)

        # Crear un Scrollbar y conectarlo con el Canvas
        self.scrollbarProcesos = ctk.CTkScrollbar(contenedor, orientation=ctk.VERTICAL, command=self.canvasProcesos.yview, width=20, button_color=blancoFrio)
        self.scrollbarProcesos.pack(side=ctk.LEFT, fill=ctk.Y)

        self.canvasProcesos.configure(yscrollcommand=self.scrollbarProcesos.set)
        self.canvasProcesos.bind('<Configure>', lambda e: self.canvasProcesos.configure(scrollregion=self.canvasProcesos.bbox("all")))

        # Crear un frame dentro del Canvas
        self.frameProcesosInterior = ctk.CTkFrame(self.canvasProcesos, fg_color=moradoOscuro)
        self.canvasProcesos.create_window((0, 0), window=self.frameProcesosInterior, anchor="ne")

        self.llenar_contenido(bbdd)

    def llenar_contenido(self, bbdd):

        self.labelTitulo = ctk.CTkLabel(self.frameProcesosInterior, text="PROCESOS", font=textoGrande, fg_color=grisOscuro, bg_color=blancoHueso)
        self.labelTitulo .grid(row=0, column=0, columnspan=4, sticky="ew", pady=5)

        # Encabezados
        self.labelIdProcesos = ctk.CTkLabel(self.frameProcesosInterior, text="ID", font=textoMedio, fg_color=grisOscuro, bg_color=blancoHueso, width=50)
        self.labelIdProcesos.grid(row=1, column=0, sticky="ew", padx=0)

        self.labelNombre = ctk.CTkLabel(self.frameProcesosInterior, text="NOMBRE", font=textoMedio, fg_color=grisOscuro, bg_color=blancoHueso, width=100)
        self.labelNombre.grid(row=1, column=1, sticky="ew", padx=0)

        self.labelDescripción = ctk.CTkLabel(self.frameProcesosInterior, text="DESCRIPCIÓN", font=textoMedio, fg_color=grisOscuro, bg_color=blancoHueso, width=350)
        self.labelDescripción.grid(row=1, column=2, sticky="ew", padx=0)

        self.labelVacio = ctk.CTkLabel(self.frameProcesosInterior, text="", font=textoMedio, fg_color=grisOscuro, bg_color=blancoHueso, width=80)
        self.labelVacio.grid(row=1, column=3, sticky="ew", padx=0)

        # Establecer el peso de las columnas para ajustar su ancho
        self.frameProcesosInterior.grid_columnconfigure(0, weight=0)  # ID
        self.frameProcesosInterior.grid_columnconfigure(1, weight=0)  # NOMBRE
        self.frameProcesosInterior.grid_columnconfigure(2, weight=0)  # ÁREA

        # Lee los nombres desde la BBDD y los almacena en variables
        fila = 0
        for filasProcesos in BDqueries_before.leer_procesos_completo(bbdd):
            columna = 0
            for columnasProcesos in filasProcesos:

                ################ LABELS ###############
                label_name_procesos = f"labelPROCESO_{fila}_{columna}_{filasProcesos}_{columnasProcesos}"
                print(label_name_procesos)

                # Crear etiquetas para técnicos con nombres desde la BD
                glo.lbl_procesos[label_name_procesos] = ctk.CTkLabel(
                    self.frameProcesosInterior, text=columnasProcesos,
                    font=texto1Medio, fg_color=moradoOscuro, bg_color=blancoHueso, anchor="w")  # Ancho especificado
                glo.lbl_procesos[label_name_procesos].grid(row=2 + fila, column=0 + columna, sticky="nsew", padx=0, pady=0)

                ################ CHECKBUTTON ###############
                int_name = f"checkIntvar-{filasProcesos[0]}"                          #nombre de variable asociada a las intvar
                print(int_name)
                glo.intVar_procesos[int_name] = tk.IntVar(value=1)                    # Guardar en el diccionario el nombre y la intvar

                self.check_name_proceso = filasProcesos[0]                            # nombre del checkbutton
                print(self.check_name_proceso)
                glo.check_procesos[self.check_name_proceso] = ctk.CTkCheckBox(
                    self.frameProcesosInterior, text="Incluir", 
                    bg_color=moradoOscuro, font=texto1Medio, fg_color=grisOscuro,
                    variable=glo.intVar_procesos[int_name])
                glo.check_procesos[self.check_name_proceso].grid(row= 2 + fila, column=3, sticky="ew", padx=10, pady=0)

                columna += 1
            fila += 1

        # Asegurarse que la columna de checkboxes también se ajusta
        self.frameProcesosInterior.grid_columnconfigure(3, weight=0)
        self.frameProcesosInterior.configure()

    def actualizar_contenido(self, bbdd):
        for widget in self.frameProcesosInterior.winfo_children():
            widget.destroy()

        self.llenar_contenido(bbdd)