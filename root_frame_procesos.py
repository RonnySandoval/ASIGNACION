import tkinter as tk
import customtkinter as ctk
import BBDD
import eventos
import glo
from estilos import *

class ContenidoProcesos:

    def __init__(self, contenedor, bbdd):
        # Crear un Canvas en el frame de Tecnicos
        canvasProcesos = tk.Canvas(contenedor, bg=moradoOscuro)
        canvasProcesos.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Crear un Scrollbar y conectarlo con el Canvas
        scrollbarProcesos = ctk.CTkScrollbar(contenedor, orientation=ctk.VERTICAL, command=canvasProcesos.yview)
        scrollbarProcesos.pack(side=ctk.LEFT, fill=ctk.Y)

        canvasProcesos.configure(yscrollcommand=scrollbarProcesos.set)
        canvasProcesos.bind('<Configure>', lambda e: canvasProcesos.configure(scrollregion=canvasProcesos.bbox("all")))

        # Crear un frame dentro del Canvas
        frameProcesosInterior = ctk.CTkFrame(canvasProcesos, bg_color=grisOscuro)
        canvasProcesos.create_window((0, 0), window=frameProcesosInterior, anchor="ne")

        labelTitulo = ctk.CTkLabel(frameProcesosInterior, text="PROCESOS", font=textoGrande, fg_color=grisOscuro, bg_color=blancoHueso)
        labelTitulo .grid(row=0, column=0, columnspan=3, sticky="ew", padx=0, pady=0)

        # Encabezados
        labelIdProcesos = ctk.CTkLabel(frameProcesosInterior, text="ID", font=textoMedio, fg_color=grisOscuro, bg_color=blancoHueso, width=50)
        labelIdProcesos.grid(row=1, column=0, sticky="ew", padx=0, pady=5)

        labelNombre = ctk.CTkLabel(frameProcesosInterior, text="NOMBRE", font=textoMedio, fg_color=grisOscuro, bg_color=blancoHueso, width=100)
        labelNombre.grid(row=1, column=1, sticky="ew", padx=0, pady=5)

        labelDescripción = ctk.CTkLabel(frameProcesosInterior, text="DESCRIPCIÓN", font=textoMedio, fg_color=grisOscuro, bg_color=blancoHueso, width=100)
        labelDescripción.grid(row=1, column=2, sticky="ew", padx=0, pady=5)

        # Establecer el peso de las columnas para ajustar su ancho
        frameProcesosInterior.grid_columnconfigure(0, weight=0)  # ID
        frameProcesosInterior.grid_columnconfigure(1, weight=0)  # NOMBRE
        frameProcesosInterior.grid_columnconfigure(2, weight=0)  # ÁREA

        # Lee los nombres desde la BBDD y los almacena en variables
        fila = 0
        for filasProcesos in BBDD.leer_procesos_completo(bbdd):
            columna = 0
            for columnasProcesos in filasProcesos:
                label_name_procesos = f"labelPROCESO_{fila}_{columna}_{filasProcesos}_{columnasProcesos}"
                print(label_name_procesos)

                # Crear etiquetas para técnicos con nombres desde la BD
                glo.lbl_procesos[label_name_procesos] = ctk.CTkLabel(
                    frameProcesosInterior, text=columnasProcesos,
                    font=texto1Medio, fg_color=moradoOscuro, bg_color=blancoHueso, anchor="w")  # Ancho especificado
                glo.lbl_procesos[label_name_procesos].grid(row=2 + fila, column=0 + columna, sticky="nsew", padx=0, pady=0)
                columna += 1
            fila += 1
