import customtkinter as ctk
from estilos import *
import ventanas_topLevel as ventop
import eventos
import glo

class FrameGraficos:

    def __init__(self, master):

        ctk.set_appearance_mode("dark")
        self.titulo = f"GANTT DE HISTÓRICOS"
        self.master = master
        self.frameTitulo = ctk.CTkFrame(master, fg_color=negro)
        self.frameTitulo.pack(side="top", fill = "both")

        self.labelTitulo = ctk.CTkLabel(self.frameTitulo,  text = self.titulo, font = textoMedio, text_color = blancoFrio, bg_color = negro)
        self.labelTitulo.pack (side="top", fill="x")

        self.frameBotones = ctk.CTkFrame(master, fg_color="black")
        self.frameBotones.pack(side="top", fill="x", padx=5, pady=5)

        ctk.CTkButton(self.frameBotones, text="Técnicos",  command=lambda: self.mostrar_frame(self.frameTecnicos),  anchor="center").pack(side=ctk.LEFT, padx=25)
        ctk.CTkButton(self.frameBotones, text="Vehículos", command=lambda: self.mostrar_frame(self.frameVehiculos), anchor="center").pack(side=ctk.LEFT, padx=25)
        ctk.CTkButton(self.frameBotones, text="Tabla"    , command=lambda: self.mostrar_frame(self.frameTabla),   anchor="center").pack(side=ctk.LEFT, padx=25)

        self.frameEntradas = ctk.CTkFrame(master, fg_color=negro)
        self.frameEntradas.pack(expand=True, side="bottom", fill="both")
        self.df = None
        self.diagramas = None

        self.frameTecnicos = ctk.CTkFrame(self.frameEntradas)
        self.frameVehiculos = ctk.CTkFrame(self.frameEntradas)
        self.frameTabla = ctk.CTkFrame(self.frameEntradas)

        self.ganttTecnicos  = None
        self.ganttVehiculos = None
        self.tablaResumen   = None

    def consultar_graficos(self, bbdd):
        self.df, self.diagramas = eventos.generar_df_gantt(bbdd)
        self.__renderizar_graficos__(self.diagramas, self.df)

    def __renderizar_graficos__(self, diagramas, df):
        if glo.gantt == True:
            self.ganttTecnicos.destroy()  # Destruir el gráfico de técnicos
            self.ganttVehiculos.destroy()  # Destruir el gráfico de vehículos
            self.tablaResumen.destroy()  # Destruir la tabla de resumen

        glo.gantt = True
        self.ganttTecnicos  = ventop.GraficoGantt(self.frameTecnicos, diagramas["diagramaTecnicos"])
        self.ganttVehiculos = ventop.GraficoGantt(self.frameVehiculos, diagramas["diagramaVehiculos"])
        self.tablaResumen   = ventop.FrameTablaGenerica(master = self.frameTabla, nombreVentana="HISTÓRICOS", df=df)

        # Mostrar el primer frame
        self.mostrar_frame(self.frameTecnicos)

    def mostrar_frame(self, frame):
        # Si el frame ya está activo, no hacer nada
        if hasattr(self, "frame_actual") and self.frame_actual == frame:
            return
        
        # Ocultar todos los frames
        for fr in (self.frameTecnicos, self.frameVehiculos, self.frameTabla):
            fr.pack_forget()

        # Actualizar el frame activo y mostrarlo
        self.frame_actual = frame
        frame.pack(expand=True, side="top", fill="both", padx=20, pady=20)
