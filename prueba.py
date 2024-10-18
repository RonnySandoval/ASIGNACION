import tkinter as tk
import customtkinter as ctk
from estilos import grisAzuladoClaro, grisAzuladoMedio, grisAzuladoOscuro, grisMedio, grisOscuro, textoGrande, naranjaOscuro, blancoFrio, amarilloClaro, amarilloMedio, azulOscuro, moradoOscuro, moradoClaro, texto1Bajo, numerosMedianos, naranjaMedio, blancoHueso, azulMedio, moradoMedio, amarilloOscuro, grisVerdeMedio



class VentanaGestionaVehiculos():
    def __init__(self, accion, bbdd):


        self.varTel = tk.StringVar() 
        self.varPdi = tk.StringVar() 
        self.varLav = tk.StringVar() 
        self.varPin = tk.StringVar()
        self.varCal= tk.StringVar()

        self.labelTimeTel  = ctk.CTkLabel(self.frameEntradas, text = "Tiempos TELEQUINOX", font = texto1Bajo, anchor="w")
        self.labelTimeTel.grid(row=6,column=0, sticky="ew", padx=20, pady=2)
        self.entryTel = ctk.CTkEntry     (self.frameEntradas, font = numerosMedianos, width=20, textvariable=self.varTel)
        self.entryTel.grid(row=6 ,column=1, sticky="ew", pady=2)

        self.labelTimePdi  = ctk.CTkLabel(self.frameEntradas, text = "Tiempos PDI" , font = texto1Bajo, anchor="w")
        self.labelTimePdi.grid(row=7,column=0, sticky="ew", padx=20, pady=2)
        self.entryPdi = ctk.CTkEntry     (self.frameEntradas, font = numerosMedianos, width=20, textvariable=self.varPdi)
        self.entryPdi.grid(row=7 ,column=1, sticky="ew", pady=2)


        self.labelTimeLav  = ctk.CTkLabel(self.frameEntradas, text = "Tiempos LAVADO", font = texto1Bajo, anchor="w")
        self.labelTimeLav.grid(row=8,column=0, sticky="ew", padx=20, pady=2)
        self.entryLav = ctk.CTkEntry     (self.frameEntradas, font = numerosMedianos, width=20, textvariable=self.varLav)
        self.entryLav.grid(row=8 ,column=1, sticky="ew", pady=2)

        self.labelTimePin  = ctk.CTkLabel(self.frameEntradas, text = "Tiempos PINTURA", font = texto1Bajo, anchor="w")
        self.labelTimePin.grid(row=9,column=0, sticky="ew", padx=20, pady=2)
        self.entryPin = ctk.CTkEntry     (self.frameEntradas, font = numerosMedianos, width=20, textvariable=self.varPin)
        self.entryPin.grid(row=9 ,column=1, sticky="ew", pady=2)

        self.labelTimeCal  = ctk.CTkLabel(self.frameEntradas, text = "Tiempos CALIDAD", font = texto1Bajo, anchor="w")
        self.labelTimeCal.grid(row=10,column=0, sticky="ew", padx=20, pady=2)
        self.entryCal = ctk.CTkEntry     (self.frameEntradas, font = numerosMedianos, width=20, textvariable=self.varCal)
        self.entryCal.grid(row=10,column=1, sticky="ew", pady=2)
