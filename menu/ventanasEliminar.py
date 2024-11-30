import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkcalendar import Calendar
from tkinter import simpledialog
import time
from estilos import *
import datetime
import re
import glo
import BBDD


class VentanaEliminarTecnico():

    def __init__(self, bbdd):
        self.rootAux = ctk.CTkToplevel()                #crea ventana auxiliar
        self.rootAux.title("Eliminar Técnico")          #coloca titulo de ventana
        self.rootAux.geometry("485x320")                #dimensiones
        self.rootAux.resizable(False, False)            #deshabilita la redimension

        self.frameTitulo = ctk.CTkFrame(self.rootAux)
        self.frameTitulo.pack(expand=True, side="top", fill="both")
        self.frameEntradas = ctk.CTkFrame(self.rootAux)
        self.frameEntradas.pack(expand=True, side="bottom", fill="both", pady=10)

        self.labelTitulo = ctk.CTkLabel(self.frameTitulo, text="ELIMINAR TECNICO", font=textoGrande)
        self.labelTitulo.pack(expand=True, side="top", fill="x", padx=20, pady=20)

        self.varTecnico = tk.StringVar() 

        self.labelTecnico = ctk.CTkLabel(self.frameEntradas, text="TECNICO", font=texto1Bajo,  anchor="w")
        self.labelTecnico.grid(row=0, column=0, sticky="ew", padx=20, pady=5)

        self.entryTecnico = ctk.CTkOptionMenu(self.frameEntradas, font = numerosMedianos, fg_color= grisAzuladoClaro, width=20, variable=self.varTecnico)
        self.entryTecnico.grid(row=0 ,column=1, sticky="ew", pady=5)

        self.tecnicos = BBDD.leer_tecnicos_modificado(bbdd)
        self.ids_tecnicos = {tecnico[1]: tecnico[0] for tecnico in self.tecnicos}    # Crear diccionarios con comprensión
        self.entryTecnico.configure(values=[""]+list(self.ids_tecnicos.keys()))      # Configurar el OptionMenu con los valores del diccionario
        self.entryTecnico.set("")  

        self.buttonCancelar = ctk.CTkButton(self.frameEntradas, text="Cancelar", font = texto1Bajo,  fg_color = naranjaMedio,  command="")   
        self.buttonEliminar  = ctk.CTkButton(self.frameEntradas, text="Eliminar",  font = textoGrande, fg_color = azulMedio,  command="")
        self.buttonCancelar.grid(row=2, column=0, padx=22, pady=15)  
        self.buttonEliminar.grid(row=2, column=1, padx=22, pady=15)
                                                  # Establecer la cadena vacía como valor por defecto

        print(self.ids_tecnicos)

    def asignafuncion(self, funcionEliminar, funcionCancelar):               #Método para asignar la función al command button de aceptar y cancelar desde otro módulo.
        self.buttonEliminar.configure(command = funcionEliminar)
        self.buttonCancelar.configure(command = funcionCancelar)

class VentanaEliminarModelo():

    def __init__(self, bbdd):
        self.rootAux = ctk.CTkToplevel()                #crea ventana auxiliar
        self.rootAux.title("Eliminar Modelo")          #coloca titulo de ventana
        self.rootAux.geometry("485x320")                #dimensiones
        self.rootAux.resizable(False, False)            #deshabilita la redimension

        self.frameTitulo = ctk.CTkFrame(self.rootAux)
        self.frameTitulo.pack(expand=True, side="top", fill="both")
        self.frameEntradas = ctk.CTkFrame(self.rootAux)
        self.frameEntradas.pack(expand=True, side="bottom", fill="both", pady=10)

        self.labelTitulo = ctk.CTkLabel(self.frameTitulo, text="ELIMINAR MODELO", font=textoGrande)
        self.labelTitulo.pack(expand=True, side="top", fill="x", padx=20, pady=20)

        self.varModelo = tk.StringVar() 

        self.labelModelo = ctk.CTkLabel(self.frameEntradas, text="MODELO", font=texto1Bajo,  anchor="w")
        self.labelModelo.grid(row=0, column=0, sticky="ew", padx=20, pady=5)

        self.entryModelo = ctk.CTkOptionMenu(self.frameEntradas, font = numerosMedianos, fg_color= grisVerdeClaro, width=20, variable=self.varModelo)
        self.entryModelo.grid(row=0 ,column=1, sticky="ew", pady=5)

        self.dfModelos = BBDD.leer_tiempos_modelos_df(bbdd)
        self.marcas_modelos = [modelo for modelo in self.dfModelos['MODELO']]    # Crear diccionarios con comprensión
        self.entryModelo.configure(values=[""]+self.marcas_modelos)              # Configurar el OptionMenu con los valores del diccionario
        self.entryModelo.set("")                                                 # Establecer la cadena vacía como valor por defecto 

        self.buttonCancelar = ctk.CTkButton(self.frameEntradas, text="Cancelar", font = texto1Bajo,  fg_color = naranjaMedio,  command="")   
        self.buttonEliminar  = ctk.CTkButton(self.frameEntradas, text="Eliminar",  font = textoGrande, fg_color = azulMedio,  command="")
        self.buttonCancelar.grid(row=2, column=0, padx=22, pady=15)  
        self.buttonEliminar.grid(row=2, column=1, padx=22, pady=15)

        print(self.marcas_modelos)

    def asignafuncion(self, funcionEliminar, funcionCancelar):               #Método para asignar la función al command button de aceptar y cancelar desde otro módulo.
        self.buttonEliminar.configure(command = funcionEliminar)
        self.buttonCancelar.configure(command = funcionCancelar)