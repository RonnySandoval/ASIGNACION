import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import customtkinter as ctk
from tkcalendar import Calendar
from tkinter import simpledialog
import time
from estilos import *
import datetime
import re
import glo
import BBDD


class VentanaImportarPedido():

    def __init__(self, bbdd):
        self.rootAux = ctk.CTkToplevel()                #crea ventana auxiliar
        self.rootAux.title("Importar Pedido")          #coloca titulo de ventana
        self.rootAux.geometry("500x260")                #dimensiones
        self.rootAux.resizable(False, False)            #deshabilita la redimension

        self.frameTitulo = ctk.CTkFrame(self.rootAux)
        self.frameTitulo.pack(side="top", fill="both")
        self.frameEntradas = ctk.CTkFrame(self.rootAux)
        self.frameEntradas.pack(side="bottom", fill="both", pady=10)

        self.labelTitulo = ctk.CTkLabel(self.frameTitulo, text="IMPORTAR UN PEDIDO DE VEHICULOS DESDE EXCEL", font=textoGrande)
        self.labelTitulo.pack(expand=True, side="top", fill="x", padx=20, pady=5)

        self.varSaltarFila = tk.StringVar() 
        self.labelSaltarFila = ctk.CTkLabel(self.frameEntradas, text="Saltar filas", font=texto1Medio,  anchor="w")
        self.labelSaltarFila.grid(row=0, column=0, sticky="ew", padx=20, pady=5)
        self.OptionSaltarFila = ctk.CTkOptionMenu(self.frameEntradas, font = numerosMedianos, fg_color= grisAzuladoClaro, width=20, variable=self.varSaltarFila)
        self.OptionSaltarFila.grid(row=0 ,column=1, sticky="ew", pady=5)
        self.fila = ["1","2","3","4","5","6","7","8","9","10"]
        self.OptionSaltarFila.configure(values=self.fila)      # Configurar el OptionMenu con los valores del diccionario
        self.OptionSaltarFila.set("1")

        self.varColumnas = tk.StringVar() 
        self.labelColumnas = ctk.CTkLabel(self.frameEntradas, text="Rango de Columnas", font=texto1Medio,  anchor="w")
        self.labelColumnas.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
        self.entryColumnas = ctk.CTkEntry(self.frameEntradas, font = numerosMedianos, fg_color= grisAzuladoClaro, width=20, textvariable=self.varColumnas)
        self.entryColumnas.grid(row=1, column=1, sticky="ew", pady=5)
        self.varColumnas.set("A:C")

        self.buttonCargar  = ctk.CTkButton(self.frameEntradas, text="Seleccionar Archivo",  font = textoGrande,
                                           fg_color = grisVerdeMedio,  hover_color = grisVerdeOscuro,
                                           command = self.seleccionarArchivo)
        self.buttonCargar.grid(row=4, column=0, padx=22, pady=15)

        self.ruta = ""
        self.labelruta = ctk.CTkLabel(self.frameEntradas, text= self.ruta, font=texto1Bajo,  anchor="w")
        self.labelruta.grid(row=5, columnspan=2, sticky="ew", padx=20, pady=2)


        self.buttonAceptar = ctk.CTkButton(self.frameEntradas, text="Aceptar", font = textoMedio,  fg_color = azulMedio,  command="")
        self.buttonAceptar.grid(row=6, column=0, padx=22, pady=5)  
        self.buttonCancelar = ctk.CTkButton(self.frameEntradas, text="Cancelar", font = texto1Bajo,  fg_color = naranjaMedio,  command="")
        self.buttonCancelar.grid(row=6, column=1, padx=22, pady=5)  

    def seleccionarArchivo(self):
        self.ruta = askopenfilename(
                                title="Seleccionar archivo Excel",
                                filetypes=[("Archivos Excel", "*.xlsx *.xls")]
                                )
        self.labelruta.configure(text=self.ruta)
        return self.ruta
        
    def asignafuncion(self, funcionAceptar, funcionCancelar):               #Método para asignar la función al command button de aceptar y cancelar desde otro módulo.
        self.buttonAceptar.configure(command = funcionAceptar)
        self.buttonCancelar.configure(command = funcionCancelar)

class VentanaImportarReferencias():

    def __init__(self, bbdd):
        self.rootAux = ctk.CTkToplevel()                #crea ventana auxiliar
        self.rootAux.title("Importar Referencias/Modelos")          #coloca titulo de ventana
        self.rootAux.geometry("500x260")                #dimensiones
        self.rootAux.resizable(False, False)            #deshabilita la redimension

        self.frameTitulo = ctk.CTkFrame(self.rootAux)
        self.frameTitulo.pack(side="top", fill="both")
        self.frameEntradas = ctk.CTkFrame(self.rootAux)
        self.frameEntradas.pack(side="bottom", fill="both", pady=10)

        self.labelTitulo = ctk.CTkLabel(self.frameTitulo, text="IMPORTAR REFERENCIAS DE MODELOS", font=textoGrande)
        self.labelTitulo.pack(expand=True, side="top", fill="x", padx=20, pady=5)

        self.varSaltarFila = tk.StringVar() 
        self.labelSaltarFila = ctk.CTkLabel(self.frameEntradas, text="Saltar filas", font=texto1Medio,  anchor="w")
        self.labelSaltarFila.grid(row=0, column=0, sticky="ew", padx=20, pady=5)
        self.OptionSaltarFila = ctk.CTkOptionMenu(self.frameEntradas, font = numerosMedianos, fg_color= grisAzuladoClaro, width=20, variable=self.varSaltarFila)
        self.OptionSaltarFila.grid(row=0 ,column=1, sticky="ew", pady=5)
        self.fila = ["0","1","2","3","4","5","6"]
        self.OptionSaltarFila.configure(values=self.fila)      # Configurar el OptionMenu con los valores del diccionario
        self.OptionSaltarFila.set("0")

        self.varColumnas = tk.StringVar() 
        self.labelColumnas = ctk.CTkLabel(self.frameEntradas, text="Rango de Columnas", font=texto1Medio,  anchor="w")
        self.labelColumnas.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
        self.entryColumnas = ctk.CTkEntry(self.frameEntradas, font = numerosMedianos, fg_color= grisAzuladoClaro, width=20, textvariable=self.varColumnas)
        self.entryColumnas.grid(row=1, column=1, sticky="ew", pady=5)
        self.varColumnas.set("A:B")

        self.buttonCargar  = ctk.CTkButton(self.frameEntradas, text="Seleccionar Archivo",  font = textoGrande,
                                           fg_color = grisVerdeMedio,  hover_color = grisVerdeOscuro,
                                           command = self.seleccionarArchivo)
        self.buttonCargar.grid(row=4, column=0, padx=22, pady=15)

        self.ruta = ""
        self.labelruta = ctk.CTkLabel(self.frameEntradas, text= self.ruta, font=texto1Bajo,  anchor="w")
        self.labelruta.grid(row=5, columnspan=2, sticky="ew", padx=20, pady=2)


        self.buttonAceptar = ctk.CTkButton(self.frameEntradas, text="Aceptar", font = textoMedio,  fg_color = azulMedio,  command="")
        self.buttonAceptar.grid(row=6, column=0, padx=22, pady=5)  
        self.buttonCancelar = ctk.CTkButton(self.frameEntradas, text="Cancelar", font = texto1Bajo,  fg_color = naranjaMedio,  command="")
        self.buttonCancelar.grid(row=6, column=1, padx=22, pady=5)  

    def seleccionarArchivo(self):
        self.ruta = askopenfilename(
                                title="Seleccionar archivo Excel",
                                filetypes=[("Archivos Excel", "*.xlsx *.xls")]
                                )
        self.labelruta.configure(text=self.ruta)
        return self.ruta
        
    def asignafuncion(self, funcionAceptar, funcionCancelar):               #Método para asignar la función al command button de aceptar y cancelar desde otro módulo.
        self.buttonAceptar.configure(command = funcionAceptar)
        self.buttonCancelar.configure(command = funcionCancelar)