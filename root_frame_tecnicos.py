import  tkinter as tk
from    tkinter import ttk
import  CRUD as CRUD
import  eventos as eventos
import  re
import  dicc_variables
from    estilos import *
import  Mod_programador
import  Objetos
import  Graficador
import  ventanas_emergentes
import  menu_principal


class ContenidoTecnicos():

    def __init__(self, contenedor):

        # Crear un Canvas en el frame de Tecnicos
        canvasTecnicos = tk.Canvas(contenedor, bg=moradoOscuro)
        canvasTecnicos.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Crear un Scrollbar y conectarlo con el Canvas
        scrollbarTecnicos = tk.Scrollbar(contenedor, orient=tk.VERTICAL, command=canvasTecnicos.yview)
        scrollbarTecnicos.pack(side=tk.LEFT, fill=tk.Y)

        canvasTecnicos.configure(yscrollcommand=scrollbarTecnicos.set)
        canvasTecnicos.bind('<Configure>', lambda e: canvasTecnicos.configure(scrollregion=canvasTecnicos.bbox("all")))

        # Crear un frame dentro del Canvas
        frameTecnicosInterior = tk.Frame(canvasTecnicos, bg=moradoOscuro)
        canvasTecnicos.create_window((0, 0), window=frameTecnicosInterior, anchor="ne")



        # Añadir contenido al frame interno

        labelIdTecnicos = tk.Label(frameTecnicosInterior, text="ID", font=textoMedio, bg=moradoOscuro, fg=blancoHueso)
        labelIdTecnicos.grid(row=0, column=0, sticky="we")

        labelTecnicos = tk.Label(frameTecnicosInterior, text="NOMBRE", font=textoMedio, bg=moradoOscuro, fg=blancoHueso)
        labelTecnicos.grid(row=0, column=1, sticky="we")

        labelAreaTecnicos = tk.Label(frameTecnicosInterior, text="ÁREA", font=textoMedio, bg=moradoOscuro, fg=blancoHueso)
        labelAreaTecnicos.grid(row=0, column=2, sticky="we")


        #Lee los nombres desde la BBDD y los almacena en variables
        fila = 0
        for filasTecnicos  in CRUD.leer_tecnicos():
            columna = 0
            for columnasTecnicos in filasTecnicos:
                label_name_tecnico = f"labeltecnico_{fila}_{columna}_{filasTecnicos}_{columnasTecnicos}"
                print(label_name_tecnico)

                # Crear etiquetas para vehículos con nombres segun BD
                dicc_variables.label_variables_tecnicos[label_name_tecnico] = tk.Label(frameTecnicosInterior, text=columnasTecnicos,
                                                                                        font=texto1Bajo, bg=moradoOscuro, fg=blancoHueso, anchor="w")
                dicc_variables.label_variables_tecnicos[label_name_tecnico].grid(row = 1 + fila, column = 0 + columna, sticky="ew")
                columna +=1
            fila += 1



        #Añadir CHEKLIST para incluir en la programación a los técnicos
        int_variables_tecnicos = {}         #Diccionario que tiene los nombres de las variables objeto
        check_variables_tecnicos = {}       #Diccionario que tiene los nombre de los checkbutton

        for filasCheck in range (1, CRUD.calcula_tecnicos()+1):
            int_name = f"checkName{filasCheck}"
            print(int_name)
            int_variables_tecnicos[int_name] = tk.IntVar(value=1)

            check_name_tecnico = f"checkTecnico{filasCheck}"
            print(check_name_tecnico)
            check_variables_tecnicos[check_name_tecnico] = tk.Checkbutton(frameTecnicosInterior, text="Programar", justify="left", bg=moradoOscuro, font=textoMinimo, fg=grisOscuro, anchor="w",
                                        variable=int_variables_tecnicos[int_name],onvalue=1, offvalue=0)
            check_variables_tecnicos[check_name_tecnico].grid(row=filasCheck, column=3, sticky="w")