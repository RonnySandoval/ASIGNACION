import tkinter as tk
import customtkinter as ctk
import estilos


# Configuración global del estilo de customtkinter
ctk.set_appearance_mode("dark")  # Modo oscuro por defecto
ctk.set_default_color_theme("dark-blue")  # Colores por defecto con tonos azulados

class VentanaNuevaPlanta():       #Ventana para crear o editar modelos
    def __init__(self):

        self.rootAux = ctk.CTkToplevel()
        self.rootAux.title("Crear Nueva Planta")
        self.rootAux.config(background = estilos.grisOscuro)
        self.rootAux.iconbitmap("logo5.ico")
        self.rootAux.geometry("450x400")
        self.rootAux.resizable(False, False)

        self.frameTitulo = ctk.CTkFrame(self.rootAux, fg_color = estilos.grisOscuro)
        self.frameTitulo.pack(expand=True, side="top", fill="both")
        self.frameEntradas = ctk.CTkFrame(self.rootAux, fg_color=estilos.grisOscuro)
        self.frameEntradas.pack(expand=True, side="bottom", fill="both", pady=10)

        # variables objeto para los entry. Deben ser parte del constructor, paraétodos
        self.varNombre = tk.StringVar()
        self.varProcesos = tk.StringVar() 
        self.varDescripcion = tk.StringVar() 


        #LABEL PARA TITULO Y CAMPOS
        self.labelTitulo      = ctk.CTkLabel(self.frameTitulo, text = "CREAR NUEVA PLANTA", font = estilos.textoGrande, text_color = estilos.grisAzuladoOscuro, bg_color = estilos.moradoClaro)
        self.labelNombre      = ctk.CTkLabel(self.frameEntradas, text = "Nombre de Planta", font = estilos.texto1Medio, text_color = estilos.grisAzuladoOscuro, bg_color = estilos.moradoClaro)
        self.labelProcesos    = ctk.CTkLabel(self.frameEntradas, text = "Cantidad de Procesos", font = estilos.texto1Medio, text_color = estilos.grisAzuladoOscuro, bg_color = estilos.moradoClaro)
        self.labelDescripcion = ctk.CTkLabel(self.frameEntradas, text = "Descripción de Planta", font = estilos.texto1Medio,text_color = estilos.grisAzuladoOscuro, bg_color = estilos.moradoClaro)

        self.labelTitulo.pack     (expand=True, side="top", fill="x", padx=20, pady=20)
        self.labelNombre.grid     (row=0, column=0, sticky="ew", padx=20, pady=5)
        self.labelProcesos.grid   (row=1, column=0, sticky="ew", padx=20, pady=5)
        self.labelDescripcion.grid(row=2, column=0, sticky="ew", padx=20, pady=5)


        #ENTRY PARA CAMPOS
        self.entryNombre = ctk.CTkEntry     (self.frameEntradas, font = estilos.numerosMedianos, text_color = estilos.blancoHueso, bg_color=estilos.moradoOscuro, width=30, textvariable=self.varNombre)
        self.entryProcesos = ctk.CTkEntry   (self.frameEntradas, font = estilos.numerosMedianos, text_color = estilos.blancoHueso, bg_color=estilos.moradoOscuro, width=30, textvariable=self.varProcesos)
        self.entryDescripcion = ctk.CTkEntry(self.frameEntradas, font = estilos.numerosMedianos, text_color = estilos.blancoHueso, bg_color=estilos.moradoOscuro,  width=30, textvariable=self.varDescripcion)

        self.entryNombre.grid     (row=0,column=1, sticky="ew", pady=5)
        self.entryProcesos.grid   (row=1,column=1, sticky="ew", pady=5)
        self.entryDescripcion.grid(row=2,column=1, sticky="ew", pady=5)


        self.buttonCancelar = ctk.CTkButton(self.frameEntradas, text="Cancelar", font = estilos.texto1Bajo, text_color = estilos.grisOscuro, fg_color = estilos.azulClaro, hover_color = estilos.azulMedio,
                                        command="")   
        self.buttonGuardar  = ctk.CTkButton(self.frameEntradas, text="Guardar",  font = estilos.textoGrande, text_color = estilos.grisOscuro, fg_color = estilos.naranjaClaro,  hover_color = estilos.naranjaMedio,
                                        command="")    

        self.buttonCancelar.grid(row=7, column=0, padx=22, pady=10)
        self.buttonGuardar.grid(row=7, column=1, padx=22, pady=10)