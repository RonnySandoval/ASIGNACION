import tkinter as tk
from tkinter.filedialog import askopenfilename
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
        self.rootAux.lift()  # Eleva la ventana Toplevel para que esté al frente
        self.rootAux.attributes('-topmost', 1)  # También puede asegurar que quede al frente

        self.frameTitulo = ctk.CTkFrame(self.rootAux, fg_color = estilos.grisOscuro)
        self.frameTitulo.pack(expand=True, side="top", fill="both")
        self.frameEntradas = ctk.CTkFrame(self.rootAux, fg_color=estilos.grisOscuro)
        self.frameEntradas.pack(expand=True, side="top", fill="both", pady=10)
        self.frameVista = ctk.CTkFrame(self.rootAux, fg_color=estilos.grisOscuro)
        self.frameVista.pack(expand=True, side="bottom", fill="both")

        # variables objeto para los entry. Deben ser parte del constructor, paraétodos
        self.varNombre      = tk.StringVar()
        self.varProcesos    = tk.StringVar() 
        self.varTecnicos    = tk.StringVar()
        self.varMarcas      = tk.StringVar()
        self.varDescripcion = tk.StringVar() 
        self.ruta = ""

        #LABEL PARA TITULO Y CAMPOS
        self.labelTitulo      = ctk.CTkLabel(self.frameTitulo,   text = "CREAR NUEVA PLANTA", font = estilos.textoGrande, text_color = estilos.blancoFrio, bg_color = estilos.grisOscuro)
        self.labelNombre      = ctk.CTkLabel(self.frameEntradas, text = "Nombre de Planta", font = estilos.texto1Medio, text_color = estilos.blancoFrio, bg_color = estilos.grisOscuro)
        #self.labelProcesos    = ctk.CTkLabel(self.frameEntradas, text = "Cantidad de Procesos", font = estilos.texto1Medio, text_color = estilos.blancoFrio, bg_color = estilos.grisOscuro)
        #self.labelTecnicos    = ctk.CTkLabel(self.frameEntradas, text = "Cantidad de Tecnicos", font = estilos.texto1Medio, text_color = estilos.blancoFrio, bg_color = estilos.grisOscuro)
        #self.labelMarcas      = ctk.CTkLabel(self.frameEntradas, text = "Cantidad de Marcas", font = estilos.texto1Medio, text_color = estilos.blancoFrio, bg_color = estilos.grisOscuro)
        self.labelDescripcion = ctk.CTkLabel(self.frameEntradas, text = "Descripción de Planta", font = estilos.texto1Medio,text_color = estilos.blancoFrio, bg_color = estilos.grisOscuro)
        self.labelRuta      = ctk.CTkLabel(self.frameVista, text = self.ruta, font = estilos.texto1Medio,text_color = estilos.blancoFrio, bg_color = estilos.grisOscuro)       

        self.labelTitulo.pack     (expand=True, side="top", fill="x", padx=20, pady=20)
        self.labelNombre.grid     (row=0, column=0, sticky="ew", padx=20, pady=5)
        #self.labelProcesos.grid  (row=1, column=0, sticky="ew", padx=20, pady=5)
        #self.labelTecnicos.grid  (row=2, column=0, sticky="ew", padx=20, pady=5)
        #self.labelMarcas.grid    (row=3, column=0, sticky="ew", padx=20, pady=5)
        self.labelDescripcion.grid(row=2, column=0, sticky="ew", padx=20, pady=5)
        self.labelRuta.grid       (row=0, column=0, padx=20, pady=5)

        #ENTRY PARA CAMPOS
        self.entryNombre      = ctk.CTkEntry(self.frameEntradas, font = estilos.numerosMedianos, text_color = estilos.blancoHueso, bg_color=estilos.moradoOscuro, width=30, textvariable=self.varNombre)
        #self.entryProcesos    = ctk.CTkEntry(self.frameEntradas, font = estilos.numerosMedianos, text_color = estilos.blancoHueso, bg_color=estilos.moradoOscuro, width=30, textvariable=self.varProcesos)
        #self.entryTecnicos    = ctk.CTkEntry(self.frameEntradas, font = estilos.numerosMedianos, text_color = estilos.blancoHueso, bg_color=estilos.moradoOscuro, width=30, textvariable=self.varTecnicos)
        #self.entryMarcas      = ctk.CTkEntry(self.frameEntradas, font = estilos.numerosMedianos, text_color = estilos.blancoHueso, bg_color=estilos.moradoOscuro, width=30, textvariable=self.varMarcas)
        self.entryDescripcion = ctk.CTkEntry(self.frameEntradas, font = estilos.numerosMedianos, text_color = estilos.blancoHueso, bg_color=estilos.moradoOscuro, width=30, textvariable=self.varDescripcion)

        self.entryNombre.grid     (row=0,column=1, sticky="ew", pady=5)
        #self.entryProcesos.grid   (row=1,column=1, sticky="ew", pady=5)
        #self.entryTecnicos.grid   (row=2,column=1, sticky="ew", pady=5)
        #self.entryMarcas.grid     (row=3,column=1, sticky="ew", pady=5)
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

    def asignafuncion(self, funcionVistaPrevia, funcionCancelar):               #Método para asignar la función al command button de aceptar y cancelar desde otro módulo.
        self.buttonVistaPrevia.configure(command = funcionVistaPrevia)    
        self.buttonCancelar.configure(command = funcionCancelar)
    
    def seleccionarArchivo(self):
        self.ruta = askopenfilename(
                                title="Seleccionar archivo Excel",
                                filetypes=[("Archivos Excel", "*.xlsx *.xls")]
                                )
        self.labelRuta.configure(text=self.ruta)
        return self.ruta
