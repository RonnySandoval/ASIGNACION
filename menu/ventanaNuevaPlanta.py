import tkinter as tk
from tkinter.filedialog import askopenfilename
import customtkinter as ctk
import re

import view.ventanas_emergentes as ventanas_emergentes
import view.estilos as estilos

# Configuración global del estilo de customtkinter
ctk.set_appearance_mode("dark")  # Modo oscuro por defecto
ctk.set_default_color_theme("dark-blue")  # Colores por defecto con tonos azulados

class VentanaNuevaPlanta():       #Ventana para crear o editar modelos
    def __init__(self):

        self.rootAux = ctk.CTkToplevel()
        self.rootAux.title("Crear Nueva Planta")
        self.rootAux.config(background = estilos.grisOscuro)
        self.rootAux.geometry("450x400")
        self.rootAux.lift()  # Eleva la ventana Toplevel para que esté al frente
        self.rootAux.attributes('-topmost', 1)  # También puede asegurar que quede al frente

        self.frameTitulo = ctk.CTkFrame(self.rootAux, fg_color = estilos.grisOscuro)
        self.frameTitulo.pack(expand=True, side="top", fill="both")
        self.frameEntradas = ctk.CTkFrame(self.rootAux, fg_color=estilos.grisOscuro)
        self.frameEntradas.pack(expand=True, side="top", fill="both", pady=10)
        self.frameHorarios = ctk.CTkFrame(self.rootAux, fg_color=estilos.grisOscuro)
        self.frameHorarios.pack(expand=True, side="top", fill="both")
        self.frameVista = ctk.CTkFrame(self.rootAux, fg_color=estilos.grisOscuro)
        self.frameVista.pack(expand=True, side="bottom", fill="both")

        # variables objeto para los entry. Deben ser parte del constructor, paraétodos
        self.varNombre      = tk.StringVar()
        self.varDescripcion = tk.StringVar() 
        self.ruta = ""

        #LABEL PARA TITULO Y CAMPOS
        self.labelTitulo      = ctk.CTkLabel(self.frameTitulo,   text = "CREAR NUEVA PLANTA", font = estilos.textoGrande, text_color = estilos.blancoFrio, bg_color = estilos.grisOscuro)
        self.labelNombre      = ctk.CTkLabel(self.frameEntradas, text = "Nombre de Planta", font = estilos.texto1Medio, text_color = estilos.blancoFrio, bg_color = estilos.grisOscuro)
        self.labelDescripcion = ctk.CTkLabel(self.frameEntradas, text = "Descripción de Planta", font = estilos.texto1Medio,text_color = estilos.blancoFrio, bg_color = estilos.grisOscuro)
        self.labelRuta      = ctk.CTkLabel(self.frameVista, text = self.ruta, font = estilos.texto1Medio,text_color = estilos.blancoFrio, bg_color = estilos.grisOscuro)       

        self.labelTitulo.pack     (expand=True, side="top", fill="x", padx=20, pady=20)
        self.labelNombre.grid     (row=0, column=0, sticky="ew", padx=20, pady=5)
        self.labelDescripcion.grid(row=2, column=0, sticky="ew", padx=20, pady=5)
        self.labelRuta.grid       (row=0, column=0, padx=20, pady=5)

        #ENTRY PARA CAMPOS
        self.entryNombre      = ctk.CTkEntry(self.frameEntradas, font = estilos.numerosMedianos, text_color = estilos.blancoHueso, fg_color=estilos.grisOscuro, width=30, textvariable=self.varNombre)
        self.entryDescripcion = ctk.CTkTextbox(self.frameEntradas, font = estilos.numerosMedianos, text_color = estilos.blancoHueso, fg_color=estilos.grisOscuro, width=30, height=112, border_width=2, border_color=estilos.grisMedio)

        self.entryNombre.grid     (row=0,column=1, sticky="ew", pady=5)
        self.entryDescripcion.grid(row=2,column=1, sticky="ew", pady=5)

        self.buttonCancelar = ctk.CTkButton(self.frameEntradas, text="Cancelar", font = estilos.texto1Bajo, text_color = estilos.blancoFrio,
                                            fg_color = estilos.azulOscuro, hover_color = estilos.azulMedio, command="")
        self.buttonCancelar.grid(row=4, column=0, padx=22, pady=10)

        self.buttonCargar  = ctk.CTkButton(self.frameEntradas, text="Cargar Datos",  font = estilos.textoGrande, text_color = estilos.blancoFrio,
                                              fg_color = estilos.naranjaOscuro,  hover_color = estilos.naranjaMedio, command=self.seleccionarArchivo)    
        self.buttonCargar.grid(row=4, column=1, padx=22, pady=10)
        
        self.buttonVistaPrevia= ctk.CTkButton(self.frameVista, text="Vista Previa",  font = estilos.textoGrande, text_color = estilos.blancoFrio,
                                              fg_color = estilos.verdeMedio,  hover_color = estilos.verdeClaro, command="")    
        self.buttonVistaPrevia.grid(row=1, column=0, padx=22, pady=10)

        self.construyeCamposHorarios()
            
    def construyeCamposHorarios(self):

        self.frameTurnos = ctk.CTkFrame(self.frameHorarios, fg_color=estilos.grisOscuro)
        self.frameTurnos.pack(fill="both", side="bottom")

        self.labelTurnoAM = ctk.CTkLabel(self.frameTurnos, text="TURNO AM", anchor="center", width=20)
        self.labelTurnoAM.grid(row=0, column=0, columnspan = 4, padx=5)

        self.labelTurnoPM = ctk.CTkLabel(self.frameTurnos, text="TURNO PM", anchor="center", width=20)
        self.labelTurnoPM.grid(row=0, column=4, columnspan = 4, padx=5)

        # Configurar columnas: 
        for columna in range(0,7):
            # Las columnas 0 y 5 son las de los extremos (espacio vacío).
            self.frameTurnos.grid_columnconfigure(columna, weight=1)  # Espacio izquierdo

        self.varInicia_AM = tk.StringVar(value="08:00")
        self.entryIniciaAM = ctk.CTkEntry(self.frameTurnos, font = estilos.numerosGrandes, textvariable = self.varInicia_AM, width=60)
        self.entryIniciaAM.grid(row=1, column=1, padx=5, pady=5)
        self.entryIniciaAM.bind("<FocusOut>", self.validar_hora)

        self.varTermina_AM = tk.StringVar(value="12:00")
        self.entryTerminaAM = ctk.CTkEntry(self.frameTurnos, font = estilos.numerosGrandes, textvariable = self.varTermina_AM, width=60)
        self.entryTerminaAM.grid(row=1, column=2, padx=5, pady=5)
        self.entryTerminaAM.bind("<FocusOut>", self.validar_hora)

        self.varInicia_PM = tk.StringVar(value="14:00")
        self.entryIniciaPM = ctk.CTkEntry(self.frameTurnos, font = estilos.numerosGrandes, textvariable = self.varInicia_PM, width=60)
        self.entryIniciaPM.grid(row=1, column=5, padx=5, pady=5)
        self.entryIniciaPM.bind("<FocusOut>", self.validar_hora)

        self.varTermina_PM = tk.StringVar(value="18:00")
        self.entryTerminaPM = ctk.CTkEntry(self.frameTurnos, font = estilos.numerosGrandes, textvariable = self.varTermina_PM, width=60)
        self.entryTerminaPM.grid(row=1, column=6, padx=5, pady=5)
        self.entryTerminaPM.bind("<FocusOut>", self.validar_hora)

    def asignafuncion(self, funcionVistaPrevia, funcionCancelar):               #Método para asignar la función al command button de aceptar y cancelar desde otro módulo.
        self.buttonVistaPrevia.configure(command = funcionVistaPrevia)    
        self.buttonCancelar.configure(command = funcionCancelar)
        
    def validar_hora(self, event):
        """Valida que el formato sea HH:MM en los Entry al perder el foco"""
        entry = event.widget
        texto = entry.get()

        if texto:  # Solo validar si no está vacío
            if not re.match(r'^\d{2}:\d{2}$', texto):  # Valida el formato HH:MM
                ventanas_emergentes.messagebox.showerror("Formato de Hora Inválido",
                                                         f"'{texto}' no es un formato válido.\nUtilice 'HH:MM'.")
                entry.focus_set()  # Vuelve a enfocar el Entry
                entry.delete(0, tk.END)  # Borra el contenido inválido

    def seleccionarArchivo(self):
        self.ruta = askopenfilename(
                                title="Seleccionar archivo Excel",
                                filetypes=[("Archivos Excel", "*.xlsx *.xls")]
                                )
        self.labelRuta.configure(text=self.ruta)
        return self.ruta
