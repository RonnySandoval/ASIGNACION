import tkinter as tk
import customtkinter as ctk
import BBDD
import eventos
import glo
from estilos import *

class ContenidoTecnicos:

    def __init__(self, contenedor, bbdd):
        # Crear un Canvas en el frame de Tecnicos
        canvasTecnicos = tk.Canvas(contenedor, bg=moradoOscuro)
        canvasTecnicos.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Crear un Scrollbar y conectarlo con el Canvas
        scrollbarTecnicos = ctk.CTkScrollbar(contenedor, orientation=ctk.VERTICAL, command=canvasTecnicos.yview)
        scrollbarTecnicos.pack(side=ctk.LEFT, fill=ctk.Y)

        canvasTecnicos.configure(yscrollcommand=scrollbarTecnicos.set)
        canvasTecnicos.bind('<Configure>', lambda e: canvasTecnicos.configure(scrollregion=canvasTecnicos.bbox("all")))

        # Crear un frame dentro del Canvas
        frameTecnicosInterior = ctk.CTkFrame(canvasTecnicos, bg_color=grisOscuro)
        canvasTecnicos.create_window((0, 0), window=frameTecnicosInterior, anchor="ne")

        # Encabezados
        labelIdTecnicos = ctk.CTkLabel(frameTecnicosInterior, text="ID", font=textoMedio, fg_color=grisOscuro, bg_color=blancoHueso, width=100)
        labelIdTecnicos.grid(row=0, column=0, sticky="ew", padx=0, pady=5)

        labelTecnicos = ctk.CTkLabel(frameTecnicosInterior, text="NOMBRE", font=textoMedio, fg_color=grisOscuro, bg_color=blancoHueso, width=100)
        labelTecnicos.grid(row=0, column=1, sticky="ew", padx=0, pady=5)

        labelAreaTecnicos = ctk.CTkLabel(frameTecnicosInterior, text="ÁREA", font=textoMedio, fg_color=grisOscuro, bg_color=blancoHueso, width=100)
        labelAreaTecnicos.grid(row=0, column=2, sticky="ew", padx=0, pady=5)

        # Establecer el peso de las columnas para ajustar su ancho
        frameTecnicosInterior.grid_columnconfigure(0, weight=0)  # ID
        frameTecnicosInterior.grid_columnconfigure(1, weight=0)  # NOMBRE
        frameTecnicosInterior.grid_columnconfigure(2, weight=0)  # ÁREA

        # Lee los nombres desde la BBDD y los almacena en variables
        fila = 0
        for filasTecnicos in BBDD.leer_tecnicos_modificado(bbdd):
            columna = 0
            for columnasTecnicos in filasTecnicos:
                label_name_tecnico = f"labeltecnico_{fila}_{columna}_{filasTecnicos}_{columnasTecnicos}"
                print(label_name_tecnico)

                # Crear etiquetas para técnicos con nombres desde la BD
                glo.lbl_Tecnicos[label_name_tecnico] = ctk.CTkLabel(
                    frameTecnicosInterior, text=columnasTecnicos,
                    font=texto1Bajo, fg_color=moradoOscuro, bg_color=blancoHueso, anchor="w", width=50)  # Ancho especificado
                glo.lbl_Tecnicos[label_name_tecnico].grid(row=1 + fila, column=0 + columna, sticky="ew", padx=0, pady=0)
                columna += 1
            fila += 1

        # Añadir Checkboxes para incluir en la programación a los técnicos
        int_variables_tecnicos = {}  # Diccionario que tiene los nombres de las variables objeto
        check_variables_tecnicos = {}  # Diccionario que tiene los nombres de los checkbuttons

        for filasCheck in range(1, BBDD.calcula_tecnicos(bbdd) + 1):
            int_name = f"checkName{filasCheck}"
            print(int_name)
            int_variables_tecnicos[int_name] = tk.IntVar(value=1)

            check_name_tecnico = f"checkTecnico{filasCheck}"
            print(check_name_tecnico)
            check_variables_tecnicos[check_name_tecnico] = ctk.CTkCheckBox(
                frameTecnicosInterior, text="Programar", 
                bg_color=moradoOscuro, font=textoMinimo, fg_color=grisOscuro,
                variable=int_variables_tecnicos[int_name])
            check_variables_tecnicos[check_name_tecnico].grid(row=filasCheck, column=3, sticky="ew", padx=10, pady=0)

        # Asegurarse que la columna de checkboxes también se ajusta
        frameTecnicosInterior.grid_columnconfigure(3, weight=0)

