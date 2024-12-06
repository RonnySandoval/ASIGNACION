import customtkinter as ctk  # Usar customtkinter en lugar de tkinter
from   estilos import *
import mainMenu
import glo


# Configuración global del estilo de customtkinter
ctk.set_appearance_mode("dark")  # Modo oscuro por defecto
ctk.set_default_color_theme("dark-blue")  # Colores por defecto con tonos azulados

class ventanaRoot(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Programación de Planta")
        self.geometry("800x700")
        self.state('zoomed')
        self.iconbitmap("logo2.ico")

    def base_root(self, bbdd):
        # Crear la barra de navegación
        self.nav_frame = ctk.CTkFrame(self)
        self.nav_frame.pack(side=ctk.TOP, fill=ctk.X)

        # Botones de navegación
        ctk.CTkButton(self.nav_frame, text="Vehículos",  command=lambda: self.mostrar_frame(self.frameVehiculos), fg_color=moradoMedio, hover_color=moradoClaro).pack(side=ctk.LEFT, padx=5, pady=5)
        ctk.CTkButton(self.nav_frame, text="Planta",     command=lambda: self.mostrar_frame(self.framePlanta), fg_color=grisAzuladoOscuro, hover_color=azulClaro).pack(side=ctk.LEFT, padx=5, pady=5)
        ctk.CTkButton(self.nav_frame, text="Pedidos",    command=lambda: self.mostrar_frame(self.framePedidos), fg_color=azulOscuro, hover_color=azulClaro).pack(side=ctk.LEFT, padx=5, pady=5)
        ctk.CTkButton(self.nav_frame, text="Programas",  command=lambda: self.mostrar_frame(self.frameProgramas), fg_color=grisVerdeOscuro, hover_color=grisVerdeClaro).pack(side=ctk.LEFT, padx=5, pady=5)
        ctk.CTkButton(self.nav_frame, text="Históricos", command=lambda: self.mostrar_frame(self.frameHistoricos), fg_color=rojoOscuro, hover_color=rojoClaro).pack(side=ctk.LEFT, padx=5, pady=5)
        ctk.CTkButton(self.nav_frame, text="Referencias/Modelos", command=lambda: self.mostrar_frame(self.frameReferencias), fg_color=rojoMuyOscuro, hover_color=naranjaOscuro).pack(side=ctk.LEFT, padx=5, pady=5)

        #Label con el nombre de la planta 
        ctk.CTkLabel(self.nav_frame, text=bbdd, font=textoBajo, width=100).pack(side=ctk.RIGHT, padx=5, pady=5)
        
        
        # Crear frames sin empaquetarlos
        self.framePlanta      = ctk.CTkFrame(self, fg_color=moradoMedio)
        self.frameVehiculos   = ctk.CTkFrame(self, fg_color=grisAzuladoMedio)
        self.framePedidos     = ctk.CTkFrame(self, fg_color=azulOscuro)
        self.frameProgramas   = ctk.CTkFrame(self, fg_color=grisVerdeOscuro)
        self.frameHistoricos  = ctk.CTkFrame(self, fg_color=rojoOscuro)
        self.frameReferencias = ctk.CTkFrame(self, fg_color=rojoMuyOscuro)

        # Indicar "Cargando..." mientras los widgets se configuran
        loading_label = ctk.CTkLabel(self, text="Cargando...", font=texto1Medio)
        loading_label.pack(expand=True)

        # Retraso para cargar y mostrar los frames después de que sus widgets estén listos
        self.after(200, lambda: self.cargar_frames(loading_label))

    def cargar_frames(self, loading_label):
        # Ocultar el mensaje de carga
        loading_label.pack_forget()

        # Posicionar los frames ya cargados
        self.framePlanta.pack(expand=True, side="left", fill="both", padx=3, pady=3)
        self.frameVehiculos.pack(expand=True, side="left", fill="both", padx=3, pady=3)
        self.framePedidos.pack(expand=True, side="left", fill="both", padx=3, pady=3)
        self.frameProgramas.pack(expand=True, side="left", fill="both", padx=3, pady=3)
        self.frameHistoricos.pack(expand=True, side="left", fill="both", padx=3, pady=3)
        self.frameReferencias.pack(expand=True, side="left", fill="both", padx=3, pady=3)

        # Configuración de expansión en framePlanta
        self.framePlanta.grid_rowconfigure(0, weight=1)
        self.framePlanta.grid_columnconfigure(0, weight=1)
        self.framePlanta.grid_columnconfigure(1, weight=1)

        # Mostrar el primer frame
        self.mostrar_frame(self.framePedidos)

    def mostrar_frame(self, frame):

        for fr in (self.frameVehiculos,
                  self.framePlanta,
                  self.framePedidos,
                  self.frameProgramas,
                  self.frameHistoricos,
                  self.frameReferencias):
            fr.pack_forget()               # Ocultar todos los frames

        loading_label = ctk.CTkLabel(self, text="Cargando...", font=textoBajo)
        loading_label.pack(side="top", padx=3, pady=3)
        self.after(50, lambda: loading_label.pack_forget())

        # Asegurar la carga completa antes de mostrar
        frame.update_idletasks()  
        frame.pack(fill=ctk.BOTH, expand=True)

    def creaframeModelos(self):
        self.frameModelos = ctk.CTkFrame  (self.framePlanta, fg_color=grisAzuladoMedio, corner_radius=15)
        self.frameModelos.pack(expand=True, side="left", fill="both", padx=10, pady=10)
        self.frameTecMod = ctk.CTkFrame  (self.framePlanta, fg_color=grisAzuladoMedio,  corner_radius=15)
        self.frameTecMod.pack(expand=True, side="left", fill="both", padx=10, pady=10)
  
        # Configura `frameTecMod` para que sus hijos se expandan
        self.frameModelos.grid_rowconfigure(0, weight=1)  # Primera fila expandible (frameTecnicos)
        self.frameTecMod.grid_rowconfigure(0, weight=1)  # Primera fila expandible (frameTecnicos)
        self.frameTecMod.grid_rowconfigure(1, weight=1)  # Segunda fila expandible (frameProcesos)
        self.frameTecMod.grid_columnconfigure(0, weight=1)  # Expande la columna para los frames


        return self.frameModelos
    
    def creaframeTecnicos(self):
        self.frameTecnicos = ctk.CTkFrame (self.frameTecMod, fg_color=grisAzuladoMedio, corner_radius=15)
        self.frameTecnicos.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        return self.frameTecnicos
        
    def creaframeProcesos(self):
        self.frameProcesos = ctk.CTkFrame (self.frameTecMod, fg_color=grisAzuladoMedio, corner_radius=15)
        self.frameProcesos.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        return self.frameProcesos

    def ocultar_hasta_datos(self):
        # Ocultar todos los frames
        for fr in ( self.nav_frame,
                    self.frameVehiculos,
                    self.framePlanta,
                    self.framePedidos,
                    self.frameProgramas,
                    self.frameHistoricos,
                    self.frameReferencias):
            fr.pack_forget()  # Eliminar los frames de la interfaz

    def refrescar_contenido(self):
        # Ocultar todos los frames actuales
        for fr in (self.frameVehiculos,
                self.framePlanta,
                self.framePedidos,
                self.frameProgramas,
                self.frameHistoricos,
                self.frameReferencias):
            fr.pack_forget()  # Eliminar los frames de la interfaz

        # Opcionalmente, ocultar también los posibles mensajes de carga
        loading_label = ctk.CTkLabel(self, text="Refrescando...", font=textoBajo)
        loading_label.pack(side="top", padx=3, pady=3)
        
        # Usamos un pequeño retraso para que se pueda actualizar la interfaz antes de mostrar los frames
        self.after(200, lambda: loading_label.pack_forget())  # Elimina el mensaje de carga después de un corto retraso
        
        # Volver a empaquetar los frames (puedes optar por reorganizar el contenido si es necesario)
        self.framePlanta.pack(expand=True, side="left", fill="both", padx=3, pady=3)
        self.frameVehiculos.pack(expand=True, side="left", fill="both", padx=3, pady=3)
        self.framePedidos.pack(expand=True, side="left", fill="both", padx=3, pady=3)
        self.frameProgramas.pack(expand=True, side="left", fill="both", padx=3, pady=3)
        self.frameHistoricos.pack(expand=True, side="left", fill="both", padx=3, pady=3)
        self.frameReferencias.pack(expand=True, side="left", fill="both", padx=3, pady=3)

        # Volver a configurar el contenido de cada frame si es necesario
        self.mostrar_frame(self.framePedidos)  # O cualquier otro frame que quieras mostrar al final


#CREAR VENTANA PRINCIPAL CON SU MENÚ
root = ventanaRoot()
mainMenu.crearMenuPrincipal(root)
glo.raiz_principal = root
root.mainloop()