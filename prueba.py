import customtkinter as ctk
import estilos

class Aplicacion(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Aplicación con Navegación")
        self.geometry("400x300")

        # Crear un Frame principal
        self.frame_principal = ctk.CTkFrame(self)
        self.frame_principal.pack(fill=ctk.BOTH, expand=True)

        # Crear los frames para mostrar
        self.Vehiculos = ctk.CTkFrame(self.frame_principal, fg_color="lightblue")
        self.Planta = ctk.CTkFrame(self.frame_principal, fg_color="lightgreen")
        self.Pedidos = ctk.CTkFrame(self.frame_principal, fg_color="lightcoral")
        self.Ordenes = ctk.CTkFrame(self.frame_principal, fg_color="lightgreen")
        self.Historicos = ctk.CTkFrame(self.frame_principal, fg_color="lightcoral")

        

        # Contenido de los frames
        ctk.CTkLabel(self.Vehiculos, text="Vehiculos", ).pack(pady=20)
        ctk.CTkButton(self.Vehiculos, text="Boton 1").pack(side=ctk.LEFT, padx=5, pady=5)
        ctk.CTkButton(self.Vehiculos, text="Boton 2").pack(side=ctk.RIGHT, padx=5, pady=5)

        ctk.CTkLabel(self.Planta, text="Técnicos").pack(pady=20)
        ctk.CTkButton(self.Planta, text="Boton 1").pack(side=ctk.LEFT, padx=5, pady=5)
        ctk.CTkButton(self.Planta, text="Boton 2").pack(side=ctk.RIGHT, padx=5, pady=5)
        
        ctk.CTkLabel(self.Pedidos, text="Pedidos").pack(pady=20)
        ctk.CTkButton(self.Pedidos, text="Boton 1").pack(side=ctk.LEFT, padx=5, pady=5)
        ctk.CTkButton(self.Pedidos, text="Boton 2").pack(side=ctk.RIGHT, padx=5, pady=5)

        ctk.CTkLabel(self.Ordenes, text="Órdenes").pack(pady=20)
        ctk.CTkButton(self.Ordenes, text="Boton 1").pack(side=ctk.LEFT, padx=5, pady=5)
        ctk.CTkButton(self.Ordenes, text="Boton 2").pack(side=ctk.RIGHT, padx=5, pady=5)

        ctk.CTkLabel(self.Historicos, text="Históricos").pack(pady=20)
        ctk.CTkButton(self.Historicos, text="Boton 1").pack(side=ctk.LEFT, padx=5, pady=5)
        ctk.CTkButton(self.Historicos, text="Boton 2").pack(side=ctk.RIGHT, padx=5, pady=5)

        # Crear la barra de navegación
        self.nav_frame = ctk.CTkFrame(self)
        self.nav_frame.pack(side=ctk.TOP, fill=ctk.X)

        # Botones de navegación
        ctk.CTkButton(self.nav_frame, text="Vehículos", command=lambda: self.mostrar_frame(self.Vehiculos)).pack(side=ctk.LEFT, padx=5, pady=5)
        ctk.CTkButton(self.nav_frame, text="Planta", command=lambda: self.mostrar_frame(self.Planta)).pack(side=ctk.LEFT, padx=5, pady=5)
        ctk.CTkButton(self.nav_frame, text="Pedidos", command=lambda: self.mostrar_frame(self.Pedidos)).pack(side=ctk.LEFT, padx=5, pady=5)
        ctk.CTkButton(self.nav_frame, text="Órdenes", command=lambda: self.mostrar_frame(self.Ordenes)).pack(side=ctk.LEFT, padx=5, pady=5)
        ctk.CTkButton(self.nav_frame, text="Históricos", command=lambda: self.mostrar_frame(self.Historicos)).pack(side=ctk.LEFT, padx=5, pady=5)

        # Mostrar el primer frame por defecto
        self.mostrar_frame(self.Planta)

    def mostrar_frame(self, frame):
        # Ocultar todos los frames
        for f in (self.Vehiculos, self.Planta, self.Pedidos, self.Ordenes, self.Historicos):
            f.pack_forget()
        # Mostrar el frame seleccionado
        frame.pack(fill=ctk.BOTH, expand=True)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # Modo oscuro
    ctk.set_default_color_theme("dark-blue")  # Tema azul oscuro
    app = Aplicacion()
    app.mainloop()
