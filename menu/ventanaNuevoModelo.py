import tkinter as tk
import customtkinter as ctk
import estilos

class VentanaNuevoModelo():       #Ventana para crear o editar modelos
    def __init__(self):

        self.rootAux = ctk.CTkToplevel()
        self.rootAux.title("Programación de Planta")
        self.rootAux.config(background = estilos.grisOscuro)
        self.rootAux.iconbitmap("logo5.ico")
        self.rootAux.geometry("450x400")
        self.rootAux.resizable(False, False)

        self.frameTitulo = ctk.CTkFrame(self.rootAux, fg_color=estilos.grisOscuro)
        self.frameTitulo.pack(expand=True, side="top", fill="both")
        self.frameEntradas = ctk.CTkFrame(self.rootAux, fg_color=estilos.grisOscuro)
        self.frameEntradas.pack(expand=True, side="bottom", fill="both", pady=10)

        # variables objeto para los entry. Deben ser parte del constructor, para poder usarlas en sus métodos
        self.varMarca = tk.StringVar()
        self.varModelo = tk.StringVar() 
        self.varTel = tk.StringVar() 
        self.varPdi = tk.StringVar() 
        self.varLav = tk.StringVar() 
        self.varPin = tk.StringVar()
        self.varCal= tk.StringVar()


        # Define colores
        colorTitulo = estilos.moradoMedio
        colorLabel = estilos.moradoMedio
        colorEntry = estilos.moradoMedio
        colorfuenteLabel = estilos.blancoFrio
        colorfuenteEntry = estilos.blancoFrio



        #LABEL PARA TITULO Y CAMPOS

        self.labelTitulo = ctk.CTkLabel(self.frameTitulo, text = "CREAR NUEVO MODELO", font = estilos.textoGrande, fg_color = colorTitulo, text_color = colorfuenteLabel)
        self.labelTitulo.pack(expand=True, side="top", fill="x", padx=20, pady=20)

        self.labelMarca    = ctk.CTkLabel(self.frameEntradas, text = "MARCA", font = estilos.texto1Medio, fg_color = colorLabel, text_color = colorfuenteLabel)
        self.labelMarca.grid(row=0,column=0, sticky="ew", padx=20, pady=5)

        self.labelModelo   = ctk.CTkLabel(self.frameEntradas, text = "MODELO", font = estilos.texto1Medio, fg_color = colorLabel, text_color = colorfuenteLabel)
        self.labelModelo.grid(row=1,column=0, sticky="ew", padx=20, pady=5)

        self.labelTimeTel  = ctk.CTkLabel(self.frameEntradas, text = "Tiempos Telequinox", font = estilos.texto1Medio, fg_color = colorLabel, text_color = colorfuenteLabel)
        self.labelTimeTel.grid(row=2,column=0, sticky="ew", padx=20, pady=5)

        self.labelTimePdi  = ctk.CTkLabel(self.frameEntradas, text = "Tiempos PDI" , font = estilos.texto1Medio, fg_color = colorLabel, text_color = colorfuenteLabel)
        self.labelTimePdi.grid(row=3,column=0, sticky="ew", padx=20, pady=5)

        self.labelTimeLav  = ctk.CTkLabel(self.frameEntradas, text = "Tiempos LAVADO", font = estilos.texto1Medio, fg_color = colorLabel, text_color = colorfuenteLabel)
        self.labelTimeLav.grid(row=4,column=0, sticky="ew", padx=20, pady=5)

        self.labelTimePin = ctk.CTkLabel(self.frameEntradas, text = "Tiempos PINTURA", font = estilos.texto1Medio, fg_color = colorLabel, text_color = colorfuenteLabel)
        self.labelTimePin.grid(row=5,column=0, sticky="ew", padx=20, pady=5)

        self.labelTimeCal  = ctk.CTkLabel(self.frameEntradas, text = "Tiempos CALIDAD", font = estilos.texto1Medio, fg_color = colorLabel, text_color = colorfuenteLabel)
        self.labelTimeCal.grid(row=6,column=0, sticky="ew", padx=20, pady=5)


        #ENTRY PARA CAMPOS
        self.entryMarca  = ctk.CTkEntry  (self.frameEntradas, font = estilos.numerosMedianos, fg_color = colorEntry, text_color = colorfuenteEntry, width=20, textvariable=self.varMarca)
        self.entryModelo = ctk.CTkEntry  (self.frameEntradas, font = estilos.numerosMedianos, fg_color = colorEntry, text_color = colorfuenteEntry, width=20, textvariable=self.varModelo)
        self.entryTel    = ctk.CTkEntry  (self.frameEntradas, font = estilos.numerosMedianos, fg_color = colorEntry, text_color = colorfuenteEntry, width=20, textvariable=self.varTel)
        self.entryPdi    = ctk.CTkEntry  (self.frameEntradas, font = estilos.numerosMedianos, fg_color = colorEntry, text_color = colorfuenteEntry, width=20, textvariable=self.varPdi)
        self.entryLav    = ctk.CTkEntry  (self.frameEntradas, font = estilos.numerosMedianos, fg_color = colorEntry, text_color = colorfuenteEntry, width=20, textvariable=self.varLav)
        self.entryPin    = ctk.CTkEntry  (self.frameEntradas, font = estilos.numerosMedianos, fg_color = colorEntry, text_color = colorfuenteEntry, width=20, textvariable=self.varPin)
        self.entryCal    = ctk.CTkEntry  (self.frameEntradas, font = estilos.numerosMedianos, fg_color = colorEntry, text_color = colorfuenteEntry, width=20, textvariable=self.varCal)

        self.entryMarca.grid (row=0,column=1, sticky="ew", pady=5)
        self.entryModelo.grid(row=1,column=1, sticky="ew", pady=5)
        self.entryTel.grid   (row=2,column=1, sticky="ew", pady=5)
        self.entryPdi.grid   (row=3,column=1, sticky="ew", pady=5)
        self.entryLav.grid   (row=4,column=1, sticky="ew", pady=5)
        self.entryPin.grid   (row=5,column=1, sticky="ew", pady=5)
        self.entryCal.grid   (row=6,column=1, sticky="ew", pady=5)

        self.buttonCancelar = ctk.CTkButton(self.frameEntradas,text="Cancelar", font = estilos.texto1Medio, fg_color = estilos.azulClaro, text_color = estilos.blancoHueso, hover_color = estilos.azulMedio, 
                                        command="")   
        self.buttonGuardar = ctk.CTkButton(self.frameEntradas,text="Guardar", font = estilos.textoGrande, fg_color = estilos.naranjaClaro, text_color = estilos.blancoFrio, hover_color = estilos.naranjaMedio,
                                        command="") 

        self.buttonCancelar.grid(row=7, column=0, padx=22, pady=10)
        self.buttonGuardar.grid(row=7, column=1, padx=22, pady=10)
    

        self.rootAux.mainloop()