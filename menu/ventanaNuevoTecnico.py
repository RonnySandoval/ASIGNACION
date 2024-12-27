import tkinter as tk
import customtkinter as ctk
import view.estilos as estilos


class VentanaNuevoTecnico():       #Ventana para crear o editar modelos
    def __init__(self):

        self.rootAux = ctk.CTkToplevel()
        self.rootAux.title("Crear Nuevo Tecnico")
        self.rootAux.config(background = estilos.grisVerdeOscuro)
        self.rootAux.iconbitmap("image\logo5.ico")
        self.rootAux.geometry("450x400")
        self.rootAux.resizable(False, False)

        self.frameTitulo = ctk.CTkFrame(self.rootAux, fg_color=estilos.grisVerdeOscuro)
        self.frameTitulo.pack(expand=True, side="top", fill="both")
        self.frameEntradas = ctk.CTkFrame(self.rootAux, fg_color=estilos.grisVerdeOscuro)
        self.frameEntradas.pack(expand=True, side="bottom", fill="both", pady=10)

        # variables objeto para los entry. Deben ser parte del constructor, para poder usarlas en sus métodos
        self.varNombre       = tk.StringVar()
        self.varApellido     = tk.StringVar()
        self.varDocumento    = tk.StringVar()
        self.varEspecialidad = tk.StringVar() 

        #LABEL PARA TITULO Y CAMPOS
        self.labelTitulo       = ctk.CTkLabel(self.frameTitulo,   text = "CREAR NUEVO TÉCNICO", font = estilos.textoGrande, text_color = estilos.blancoHueso, fg_color=estilos.grisVerdeOscuro)
        self.labelNombre       = ctk.CTkLabel(self.frameEntradas, text = "Nombre",              font = estilos.texto1Medio, text_color = estilos.blancoHueso, fg_color=estilos.grisVerdeOscuro)
        self.labelApellido     = ctk.CTkLabel(self.frameEntradas, text = "Apellido",            font = estilos.texto1Medio, text_color = estilos.blancoHueso, fg_color=estilos.grisVerdeOscuro)
        self.labelDocumento    = ctk.CTkLabel(self.frameEntradas, text = "Documento",           font = estilos.texto1Medio, text_color = estilos.blancoHueso, fg_color=estilos.grisVerdeOscuro)
        self.labelEspecialidad = ctk.CTkLabel(self.frameEntradas, text = "Especialidad",        font = estilos.texto1Medio, text_color = estilos.blancoHueso, fg_color=estilos.grisVerdeOscuro)

        self.labelTitulo.pack      (expand=True, side="top", fill="x", padx=20, pady=20)
        self.labelNombre.grid      (row=0, column=0, sticky="ew", padx=20, pady=5)
        self.labelApellido.grid    (row=1, column=0, sticky="ew", padx=20, pady=5)
        self.labelDocumento.grid   (row=2, column=0, sticky="ew", padx=20, pady=5)
        self.labelEspecialidad.grid(row=3, column=0, sticky="ew", padx=20, pady=5)

        #ENTRY PARA CAMPOS
        self.entryNombre = ctk.CTkEntry      (self.frameEntradas, font = estilos.numerosMedianos, text_color = estilos.blancoHueso, fg_color=estilos.grisOscuro, width=30, textvariable=self.varNombre)
        self.entryApellido = ctk.CTkEntry    (self.frameEntradas, font = estilos.numerosMedianos, text_color = estilos.blancoHueso, fg_color=estilos.grisOscuro, width=30, textvariable=self.varApellido)
        self.entryDocumento = ctk.CTkEntry   (self.frameEntradas, font = estilos.numerosMedianos, text_color = estilos.blancoHueso, fg_color=estilos.grisOscuro,  width=30, textvariable=self.varDocumento)
        self.entryEspecialidad = ctk.CTkEntry(self.frameEntradas, font = estilos.numerosMedianos, text_color = estilos.blancoHueso, fg_color=estilos.grisOscuro, width=30, textvariable=self.varEspecialidad)

        self.entryNombre.grid       (row=0, column=1, sticky="ew", pady=5)
        self.entryApellido.grid     (row=1, column=1, sticky="ew", pady=5)    
        self.entryDocumento.grid    (row=2, column=1, sticky="ew", pady=5)
        self.entryEspecialidad.grid (row=3, column=1, sticky="ew", pady=5)


        self.buttonCancelar = ctk.CTkButton(self.frameEntradas, text="Cancelar", font = estilos.texto1Medio,  fg_color = estilos.naranjaClaro, text_color = estilos.blancoFrio, hover_color = estilos.azulMedio,
                                        command="")   
        self.buttonGuardar  = ctk.CTkButton(self.frameEntradas, text="Guardar",  font = estilos.textoGrande, fg_color = estilos.azulMedio, text_color = estilos.blancoFrio, hover_color = estilos. naranjaMedio,
                                        command="")    

        self.buttonCancelar.grid(row=4, column=0, padx=22, pady=10)
        self.buttonGuardar.grid(row=4, column=1, padx=22, pady=10)

    def asignafuncion(self, funcionGuardar, funcionCancelar):
        self.buttonGuardar.configure(command = funcionGuardar)
        self.buttonCancelar.configure(command = funcionCancelar)