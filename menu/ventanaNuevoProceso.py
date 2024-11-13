import tkinter as tk
import customtkinter as ctk
import estilos


class VentanaNuevoProceso():       #Ventana para crear o editar modelos
    def __init__(self):

        self.rootAux = ctk.CTkToplevel()
        self.rootAux.title("Crear Nuevo Proceso")
        self.rootAux.config(background = estilos.grisVerdeMedio)
        self.rootAux.iconbitmap("logo5.ico")
        self.rootAux.geometry("450x400")
        self.rootAux.resizable(False, False)

        self.frameTitulo = ctk.CTkFrame(self.rootAux, fg_color=estilos.grisVerdeMedio)
        self.frameTitulo.pack(expand=True, side="top", fill="both")
        self.frameEntradas = ctk.CTkFrame(self.rootAux, fg_color=estilos.grisVerdeMedio)
        self.frameEntradas.pack(expand=True, side="bottom", fill="both", pady=10)

        # variables objeto para los entry. Deben ser parte del constructor, para poder usarlas en sus métodos
        self.varNombre       = tk.StringVar()
        self.varIdProceso     = tk.StringVar()
        self.varDescripcion = tk.StringVar() 
        self.varSecuencia    = tk.StringVar() 
    
        #LABEL PARA TITULO Y CAMPOS
        self.labelTitulo       = ctk.CTkLabel(self.frameTitulo,   text = "CREAR PROCESO",           font = estilos.textoGrande, text_color = estilos.blancoHueso, fg_color=estilos.grisVerdeMedio)
        self.labelNombre       = ctk.CTkLabel(self.frameEntradas, text = "Nombre",                  font = estilos.texto1Medio, text_color = estilos.blancoHueso, fg_color=estilos.grisVerdeMedio)
        self.labelIdProceso     = ctk.CTkLabel(self.frameEntradas, text = "Identificador",           font = estilos.texto1Medio, text_color = estilos.blancoHueso, fg_color=estilos.grisVerdeMedio)
        self.labelDescripcion = ctk.CTkLabel(self.frameEntradas, text = "Descripción",             font = estilos.texto1Medio, text_color = estilos.blancoHueso, fg_color=estilos.grisVerdeMedio)
        self.labelSecuencia    = ctk.CTkLabel(self.frameEntradas, text = "Secuencia en el proceso", font = estilos.texto1Medio, text_color = estilos.blancoHueso, fg_color=estilos.grisVerdeMedio)

        self.labelTitulo.pack      (expand=True, side="top", fill="x", padx=20, pady=20)
        self.labelNombre.grid      (row=0, column=0, sticky="ew", padx=20, pady=5)
        self.labelIdProceso.grid    (row=1, column=0, sticky="ew", padx=20, pady=5)
        self.labelDescripcion.grid(row=2, column=0, sticky="ew", padx=20, pady=5)
        self.labelSecuencia.grid   (row=3, column=0, sticky="ew", padx=20, pady=5)

        #ENTRY PARA CAMPOS
        self.entryNombre    = ctk.CTkEntry      (self.frameEntradas, font = estilos.numerosMedianos, text_color = estilos.blancoHueso, fg_color=estilos.grisOscuro, width=30, textvariable=self.varNombre)
        self.entryIdProceso  = ctk.CTkEntry    (self.frameEntradas, font = estilos.numerosMedianos, text_color = estilos.blancoHueso, fg_color=estilos.grisOscuro, width=30, textvariable=self.varIdProceso)
        self.entryDescripcion = ctk.CTkEntry(self.frameEntradas, font = estilos.numerosMedianos, text_color = estilos.blancoHueso, fg_color=estilos.grisOscuro, width=30, textvariable=self.varDescripcion)
        self.entrySecuencia = ctk.CTkEntry   (self.frameEntradas, font = estilos.numerosMedianos, text_color = estilos.blancoHueso, fg_color=estilos.grisOscuro,  width=30, textvariable=self.varSecuencia)

        self.entryNombre.grid       (row=0, column=1, sticky="ew", pady=5)
        self.entryIdProceso.grid     (row=1, column=1, sticky="ew", pady=5)    
        self.entryDescripcion.grid (row=2, column=1, sticky="ew", pady=5)
        self.entrySecuencia.grid    (row=3, column=1, sticky="ew", pady=5)


        self.buttonCancelar = ctk.CTkButton(self.frameEntradas, text="Cancelar", font = estilos.texto1Bajo,  fg_color = estilos.azulClaro, text_color = estilos.grisOscuro, hover_color = estilos.azulMedio,
                                        command="")   
        self.buttonGuardar  = ctk.CTkButton(self.frameEntradas, text="Guardar",  font = estilos.textoGrande, fg_color = estilos.naranjaClaro, text_color = estilos.grisOscuro, hover_color = estilos. naranjaMedio,
                                        command="")    

        self.buttonCancelar.grid(row=4, column=0, padx=22, pady=10)
        self.buttonGuardar.grid(row=4, column=1, padx=22, pady=10)


    def asignaFuncion(self, funcionGuardar, funcionCancelar):
        self.buttonGuardar.configure(command = funcionGuardar)
        self.buttonCancelar.configure(command = funcionCancelar)