import tkinter as tk
import customtkinter as ctk
import estilos


class VentanaNuevoVehiculo():
    def __init__(self):

        self.rootAux = ctk.CTkToplevel()
        self.rootAux.title("Programación de Planta")
        self.rootAux.config(background = estilos.grisAzuladoMedio)
        self.rootAux.iconbitmap("logo5.ico")
        self.rootAux.geometry("430x600")
        self.rootAux.resizable(False, False)

        self.frameTitulo   = ctk.CTkFrame(self.rootAux, fg_color=estilos.grisAzuladoMedio)
        self.frameTitulo.pack(expand=True, side="top", fill="both")
        self.frameEntradas = ctk.CTkFrame(self.rootAux, fg_color=estilos.grisAzuladoMedio)
        self.frameEntradas.pack(expand=True, side="bottom", fill="both", pady=10)

        self.varChasis = tk.StringVar() 
        self.varFecha = tk.StringVar() 
        self.varMarca = tk.StringVar()
        self.varModelo = tk.StringVar() 
        self.varColor = tk.StringVar() 
        self.varEstado = tk.StringVar() 
        self.varTel = tk.StringVar() 
        self.varPdi = tk.StringVar() 
        self.varLav = tk.StringVar() 
        self.varPin = tk.StringVar()
        self.varCal= tk.StringVar()
        self.varNoved = tk.StringVar()
        self.varSubcon = tk.StringVar() 
        self.varPedido = tk.StringVar()


        #LABEL PARA TITULO Y CAMPOS estilos.
        colorTitulo = estilos.grisAzuladoMedio
        colorLabel = estilos.grisAzuladoMedio
        colorEntry = estilos.grisAzuladoOscuro
        colorfuenteLabel = estilos.blancoFrio
        colorfuenteEntry = estilos.blancoFrio


        self.labelTitulo   = ctk.CTkLabel(self.frameTitulo, text = "CREAR NUEVO VEHICULO", font = estilos.textoGrande, fg_color = colorTitulo, text_color = colorfuenteLabel)
        self.labelTitulo.pack(expand=True, side="top", fill="x", padx=7, pady=10)

        self.labelChasis   = ctk.CTkLabel(self.frameEntradas, text = "CHASIS", font = estilos.texto1Medio, fg_color = colorLabel, text_color = colorfuenteLabel, anchor="w")
        self.labelChasis.grid(row=0,column=0, sticky="ew", padx=20, pady=3)

        self.labelFecha    = ctk.CTkLabel(self.frameEntradas, text = "FECHA ENTREGA", font = estilos.texto1Medio, fg_color = colorLabel, text_color = colorfuenteLabel, anchor="w")
        self.labelFecha.grid(row=1,column=0, sticky="ew", padx=20, pady=3)

        self.labelMarca    = ctk.CTkLabel(self.frameEntradas, text = "MARCA", font = estilos.texto1Medio, fg_color = colorLabel, text_color = colorfuenteLabel, anchor="w")
        self.labelMarca.grid(row=2,column=0, sticky="ew", padx=20, pady=3)

        self.labelModelo   = ctk.CTkLabel(self.frameEntradas, text = "MODELO", font = estilos.texto1Medio, fg_color = colorLabel, text_color = colorfuenteLabel, anchor="w")
        self.labelModelo.grid(row=3,column=0, sticky="ew", padx=20, pady=3)

        self.labelColor  = ctk.CTkLabel(self.frameEntradas, text = "COLOR", font = estilos.texto1Medio, fg_color = colorLabel, text_color = colorfuenteLabel, anchor="w")
        self.labelColor.grid(row=4,column=0, sticky="ew", padx=20, pady=3)

        self.labelEstado  = ctk.CTkLabel(self.frameEntradas, text = "ESTADO", font = estilos.texto1Medio, fg_color = colorLabel, text_color = colorfuenteLabel, anchor="w")
        self.labelEstado.grid(row=5,column=0, sticky="ew", padx=20, pady=3)

        self.labelTimeTel  = ctk.CTkLabel(self.frameEntradas, text = "Tiempos TELEQUINOX", font = estilos.texto1Medio, fg_color = colorLabel, text_color = colorfuenteLabel, anchor="w")
        self.labelTimeTel.grid(row=6,column=0, sticky="ew", padx=20, pady=3)

        self.labelTimePdi  = ctk.CTkLabel(self.frameEntradas, text = "Tiempos PDI" , font = estilos.texto1Medio, fg_color = colorLabel, text_color = colorfuenteLabel, anchor="w")
        self.labelTimePdi.grid(row=7,column=0, sticky="ew", padx=20, pady=3)

        self.labelTimeLav  = ctk.CTkLabel(self.frameEntradas, text = "Tiempos LAVADO", font = estilos.texto1Medio, fg_color = colorLabel, text_color = colorfuenteLabel, anchor="w")
        self.labelTimeLav.grid(row=8,column=0, sticky="ew", padx=20, pady=3)

        self.labelTimePin  = ctk.CTkLabel(self.frameEntradas, text = "Tiempos PINTURA", font = estilos.texto1Medio, fg_color = colorLabel, text_color = colorfuenteLabel, anchor="w")
        self.labelTimePin.grid(row=9,column=0, sticky="ew", padx=20, pady=3)

        self.labelTimeCal  = ctk.CTkLabel(self.frameEntradas, text = "Tiempos CALIDAD", font = estilos.texto1Medio, fg_color = colorLabel, text_color = colorfuenteLabel, anchor="w")
        self.labelTimeCal.grid(row=10,column=0, sticky="ew", padx=20, pady=3)

        self.labelNoved  = ctk.CTkLabel(self.frameEntradas, text = "NOVEDADES", font = estilos.texto1Medio, fg_color = colorLabel, text_color = colorfuenteLabel, anchor="w")
        self.labelNoved.grid(row=11,column=0, sticky="ew", padx=20, pady=3)

        self.labelSubcon  = ctk.CTkLabel(self.frameEntradas, text = "SUBCONTRATAR", font = estilos.texto1Medio, fg_color = colorLabel, text_color = colorfuenteLabel, anchor="w")
        self.labelSubcon.grid(row=12,column=0, sticky="ew", padx=20, pady=3)

        self.labelPedido  = ctk.CTkLabel(self.frameEntradas, text = "PEDIDO", font = estilos.texto1Medio, fg_color = colorLabel, text_color = colorfuenteLabel, anchor="w")
        self.labelPedido.grid(row=13,column=0, sticky="ew", padx=20, pady=3)

        #ENTRY PARA CAMPOS
        self.entryChasis = ctk.CTkEntry  (self.frameEntradas, font = estilos.numerosMedianos, fg_color = colorEntry, text_color = colorfuenteEntry, width=20, textvariable=self.varChasis) 
        self.entryFecha  = ctk.CTkEntry  (self.frameEntradas, font = estilos.numerosMedianos, fg_color = colorEntry, text_color = colorfuenteEntry, width=20, textvariable=self.varFecha) 
        self.entryMarca  = ctk.CTkEntry  (self.frameEntradas, font = estilos.numerosMedianos, fg_color = colorEntry, text_color = colorfuenteEntry, width=20, textvariable=self.varMarca)
        self.entryModelo = ctk.CTkEntry  (self.frameEntradas, font = estilos.numerosMedianos, fg_color = colorEntry, text_color = colorfuenteEntry, width=20, textvariable=self.varModelo)
        self.entryColor  = ctk.CTkEntry  (self.frameEntradas, font = estilos.numerosMedianos, fg_color = colorEntry, text_color = colorfuenteEntry, width=20, textvariable=self.varColor)
        self.entryEstado = ctk.CTkEntry  (self.frameEntradas, font = estilos.numerosMedianos, fg_color = colorEntry, text_color = colorfuenteEntry, width=20, textvariable=self.varEstado)
        self.entryTel    = ctk.CTkEntry  (self.frameEntradas, font = estilos.numerosMedianos, fg_color = colorEntry, text_color = colorfuenteEntry, width=20, textvariable=self.varTel)
        self.entryPdi    = ctk.CTkEntry  (self.frameEntradas, font = estilos.numerosMedianos, fg_color = colorEntry, text_color = colorfuenteEntry, width=20, textvariable=self.varPdi)
        self.entryLav    = ctk.CTkEntry  (self.frameEntradas, font = estilos.numerosMedianos, fg_color = colorEntry, text_color = colorfuenteEntry, width=20, textvariable=self.varLav)
        self.entryPin    = ctk.CTkEntry  (self.frameEntradas, font = estilos.numerosMedianos, fg_color = colorEntry, text_color = colorfuenteEntry, width=20, textvariable=self.varPin)
        self.entryCal    = ctk.CTkEntry  (self.frameEntradas, font = estilos.numerosMedianos, fg_color = colorEntry, text_color = colorfuenteEntry, width=20, textvariable=self.varCal)
        self.entryNoved  = ctk.CTkEntry  (self.frameEntradas, font = estilos.numerosMedianos, fg_color = colorEntry, text_color = colorfuenteEntry, width=20, textvariable=self.varNoved)
        self.entrySubcon = ctk.CTkEntry  (self.frameEntradas, font = estilos.numerosMedianos, fg_color = colorEntry, text_color = colorfuenteEntry, width=20, textvariable=self.varSubcon)
        self.entryPedido = ctk.CTkEntry  (self.frameEntradas, font = estilos.numerosMedianos, fg_color = colorEntry, text_color = colorfuenteEntry, width=20, textvariable=self.varPedido)



        self.entryChasis.grid(row=0 ,column=1, sticky="ew", pady=3)
        self.entryFecha.grid (row=1 ,column=1, sticky="ew", pady=3)
        self.entryMarca.grid (row=2 ,column=1, sticky="ew", pady=3)
        self.entryModelo.grid(row=3 ,column=1, sticky="ew", pady=3)
        self.entryColor.grid (row=4 ,column=1, sticky="ew", pady=3)
        self.entryEstado.grid(row=5 ,column=1, sticky="ew", pady=3)
        self.entryTel.grid   (row=6 ,column=1, sticky="ew", pady=3)
        self.entryPdi.grid   (row=7 ,column=1, sticky="ew", pady=3)
        self.entryLav.grid   (row=8 ,column=1, sticky="ew", pady=3)
        self.entryPin.grid   (row=9 ,column=1, sticky="ew", pady=3)
        self.entryCal.grid   (row=10,column=1, sticky="ew", pady=3)
        self.entryNoved.grid (row=11,column=1, sticky="ew", pady=3)
        self.entrySubcon.grid(row=12,column=1, sticky="ew", pady=3)
        self.entryPedido.grid(row=13,column=1, sticky="ew", pady=3)        

        self.buttonCancelar = ctk.CTkButton(self.frameEntradas,text="Cancelar", font=estilos.texto1Medio, fg_color=estilos.azulClaro, text_color=estilos.grisOscuro, hover_color = estilos.azulOscuro,
                                            command="")   
        self.buttonCancelar.grid(row=14, column=0, padx=22, pady=8)

        self.buttonAgregar = ctk.CTkButton(self.frameEntradas,text="Añadir", font=estilos.textoGrande, fg_color=estilos.naranjaClaro, text_color=estilos.grisOscuro, hover_color = estilos.naranjaOscuro,
                                           command="")    
        self.buttonAgregar.grid(row=14, column=1, padx=22, pady=8)            


        self.rootAux.mainloop()