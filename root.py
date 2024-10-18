import customtkinter as ctk  # Usar customtkinter en lugar de tkinter
from    estilos import *
import  menu_principal
import root_frame_modelos as frameVh
import root_frame_tecnicos as frameTec
import root_frame_vehiculos as framePed
import glo

# Configuración global del estilo de customtkinter
ctk.set_appearance_mode("dark")  # Modo oscuro por defecto
ctk.set_default_color_theme("dark-blue")  # Colores por defecto con tonos azulados

class ventanaRoot(ctk.CTk):
    def __init__(self, bbdd):
        super().__init__()

        self.title("Programación de Planta")
        self.geometry("800x700")
        self.state('zoomed')
        self.iconbitmap("logo8.ico")

        # Crear la barra de navegación
        self.nav_frame = ctk.CTkFrame(self)
        self.nav_frame.pack(side=ctk.TOP, fill=ctk.X)

        # Botones de navegación
        ctk.CTkButton(self.nav_frame, text="Vehículos",  command=lambda: self.mostrar_frame(self.frameVehiculos), fg_color=grisAzuladoOscuro, hover_color=azulClaro).pack(side=ctk.LEFT, padx=5, pady=5)
        ctk.CTkButton(self.nav_frame, text="Planta",     command=lambda: self.mostrar_frame(self.framePlanta), fg_color=moradoMedio, hover_color=moradoClaro).pack(side=ctk.LEFT, padx=5, pady=5)
        ctk.CTkButton(self.nav_frame, text="Pedidos",    command=lambda: self.mostrar_frame(self.framePedidos), fg_color=azulOscuro, hover_color=azulClaro).pack(side=ctk.LEFT, padx=5, pady=5)
        ctk.CTkButton(self.nav_frame, text="Órdenes",    command=lambda: self.mostrar_frame(self.frameOrdenes), fg_color=grisVerdeOscuro, hover_color=grisVerdeClaro).pack(side=ctk.LEFT, padx=5, pady=5)
        ctk.CTkButton(self.nav_frame, text="Históricos", command=lambda: self.mostrar_frame(self.frameHistoricos), fg_color=rojoOscuro, hover_color=rojoClaro).pack(side=ctk.LEFT, padx=5, pady=5)
        
        #Label con el nombre de la planta 
        ctk.CTkLabel(self.nav_frame, text=bbdd, font=textoBajo, width=100).pack(side=ctk.RIGHT, padx=5, pady=5)
        
        
        # Creación de los frames principales usando customtkinter CTkFrame
        self.framePlanta = ctk.CTkFrame   (self, fg_color=grisAzuladoMedio)
        self.frameVehiculos = ctk.CTkFrame (self, fg_color=moradoMedio)
        self.framePedidos = ctk.CTkFrame   (self, fg_color=azulOscuro)
        self.frameOrdenes = ctk.CTkFrame   (self, fg_color=grisVerdeOscuro)
        self.frameHistoricos = ctk.CTkFrame(self, fg_color=rojoOscuro)

        # Posicionar los frames 
        self.framePlanta    .pack(expand=True, side="left", fill="both", padx=3, pady=3)
        self.frameVehiculos .pack(expand=True, side="left", fill="both", padx=3, pady=3)
        self.framePedidos   .pack(expand=True, side="left", fill="both", padx=3, pady=3)
        self.frameOrdenes   .pack(expand=True, side="left", fill="both", padx=3, pady=3)
        self.frameHistoricos.pack(expand=True, side="left", fill="both", padx=3, pady=3)

# Configuramos el grid del frame padre (framePlanta) para que los frames hijos ocupen el espacio verticalmente
        self.framePlanta.grid_rowconfigure(0, weight=1)  # La única fila debe expandirse verticalmente
        self.framePlanta.grid_columnconfigure(0, weight=1)  # Expande la columna 0
        self.framePlanta.grid_columnconfigure(1, weight=1)  # Expande la columna 1
        self.framePlanta.grid_columnconfigure(2, weight=1)  # Expande la columna 2

        self.mostrar_frame(self.framePlanta)

    def mostrar_frame(self, frame):
        # Ocultar todos los frames
        for f in (self.frameVehiculos, self.framePlanta, self.framePedidos, self.frameOrdenes, self.frameHistoricos):
            f.pack_forget()
        # Mostrar el frame seleccionado
        frame.pack(fill=ctk.BOTH, expand=True)
    
    def creaframeModelos(self):
        self.frameModelos = ctk.CTkFrame  (self.framePlanta, fg_color=grisAzuladoMedio)
        self.frameModelos.grid(row=0, column=0, sticky="nsew")
        return self.frameModelos

    def creaframeTecnicos(self):
        self.frameTecnicos = ctk.CTkFrame (self.framePlanta, fg_color=grisAzuladoMedio)
        self.frameTecnicos.grid(row=0, column=1, sticky="nsew")
        return self.frameTecnicos
        
    def creaframeProcesos(self):
        self.frameProcesos = ctk.CTkFrame (self.framePlanta, fg_color=grisAzuladoMedio)
        self.frameTecnicos.grid(row=0, column=2, sticky="nsew")
        return self.frameProcesos


root = ventanaRoot(bbdd='planta_manta.db')
menu_principal.crearMenuPrincipal(root)


# Añadir contenidos a los frames
glo.stateFrame.contenidoDeModelos   = frameVh.ContenidoModelos(root.creaframeModelos(),
                                                               bbdd='planta_manta.db')

glo.stateFrame.contenidoDeTecnicos  = frameTec.ContenidoTecnicos(root.creaframeTecnicos(),
                                                                 bbdd='planta_manta.db')

glo.stateFrame.contenidoDeVehiculos = framePed.ContenidoVehiculos(root.frameVehiculos)

glo.stateFrame.vehiculos = framePed.TablaVehiculos(glo.stateFrame.contenidoDeVehiculos,
                                                   root.frameVehiculos, root)

glo.stateFrame.filtro    = framePed.FiltrosVehiculos(glo.stateFrame.vehiculos,

                                                     glo.stateFrame.contenidoDeVehiculos)



root.mainloop()
