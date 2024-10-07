import tkinter as tk
import estilos


class VentanaNuevoVehiculo():
    def __init__(self):

        self.rootAux = tk.Toplevel()
        self.rootAux.title("Programación de Planta")
        self.rootAux.config(bg = estilos.grisAzuladoMedio)
        self.rootAux.iconbitmap("logo5.ico")
        self.rootAux.geometry("430x600")
        self.rootAux.resizable(False, False)

        self.frameTitulo   = tk.Frame(self.rootAux, bg=estilos.grisAzuladoMedio)
        self.frameTitulo.pack(expand=True, side="top", fill="both")
        self.frameEntradas = tk.Frame(self.rootAux, bg=estilos.grisAzuladoMedio)
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


        colorTitulo = estilos.grisAzuladoMedio
        colorLabel = estilos.grisAzuladoMedio
        colorEntry = estilos.grisAzuladoOscuro
        colorfuenteLabel = estilos.blancoFrio
        colorfuenteEntry = estilos.blancoFrio



        #LABEL PARA TITULO Y CAMPOSestilos.

        self.labelTitulo   = tk.Label(self.frameTitulo, text = "CREAR NUEVO TECNICO", font = estilos.textoGrande, bg = colorTitulo, fg = colorfuenteLabel)
        self.labelTitulo.pack(expand=True, side="top", fill="x", padx=7, pady=10)

        self.labelChasis   = tk.Label(self.frameEntradas, text = "CHASIS", font = estilos.texto1Bajo, bg = colorLabel, fg = colorfuenteLabel, anchor="w")
        self.labelChasis.grid(row=0,column=0, sticky="ew", padx=20, pady=3)

        self.labelFecha    = tk.Label(self.frameEntradas, text = "FECHA ENTREGA", font = estilos.texto1Bajo, bg = colorLabel, fg = colorfuenteLabel, anchor="w")
        self.labelFecha.grid(row=1,column=0, sticky="ew", padx=20, pady=3)

        self.labelMarca    = tk.Label(self.frameEntradas, text = "MARCA", font = estilos.texto1Bajo, bg = colorLabel, fg = colorfuenteLabel, anchor="w")
        self.labelMarca.grid(row=2,column=0, sticky="ew", padx=20, pady=3)

        self.labelModelo   = tk.Label(self.frameEntradas, text = "MODELO", font = estilos.texto1Bajo, bg = colorLabel, fg = colorfuenteLabel, anchor="w")
        self.labelModelo.grid(row=3,column=0, sticky="ew", padx=20, pady=3)

        self.labelColor  = tk.Label(self.frameEntradas, text = "COLOR", font = estilos.texto1Bajo, bg = colorLabel, fg = colorfuenteLabel, anchor="w")
        self.labelColor.grid(row=4,column=0, sticky="ew", padx=20, pady=3)

        self.labelEstado  = tk.Label(self.frameEntradas, text = "ESTADO", font = estilos.texto1Bajo, bg = colorLabel, fg = colorfuenteLabel, anchor="w")
        self.labelEstado.grid(row=5,column=0, sticky="ew", padx=20, pady=3)

        self.labelTimeTel  = tk.Label(self.frameEntradas, text = "Tiempos TELEQUINOX", font = estilos.texto1Bajo, bg = colorLabel, fg = colorfuenteLabel, anchor="w")
        self.labelTimeTel.grid(row=6,column=0, sticky="ew", padx=20, pady=3)

        self.labelTimePdi  = tk.Label(self.frameEntradas, text = "Tiempos PDI" , font = estilos.texto1Bajo, bg = colorLabel, fg = colorfuenteLabel, anchor="w")
        self.labelTimePdi.grid(row=7,column=0, sticky="ew", padx=20, pady=3)

        self.labelTimeLav  = tk.Label(self.frameEntradas, text = "Tiempos LAVADO", font = estilos.texto1Bajo, bg = colorLabel, fg = colorfuenteLabel, anchor="w")
        self.labelTimeLav.grid(row=8,column=0, sticky="ew", padx=20, pady=3)

        self.labelTimePin  = tk.Label(self.frameEntradas, text = "Tiempos PINTURA", font = estilos.texto1Bajo, bg = colorLabel, fg = colorfuenteLabel, anchor="w")
        self.labelTimePin.grid(row=9,column=0, sticky="ew", padx=20, pady=3)

        self.labelTimeCal  = tk.Label(self.frameEntradas, text = "Tiempos CALIDAD", font = estilos.texto1Bajo, bg = colorLabel, fg = colorfuenteLabel, anchor="w")
        self.labelTimeCal.grid(row=10,column=0, sticky="ew", padx=20, pady=3)

        self.labelNoved  = tk.Label(self.frameEntradas, text = "NOVEDADES", font = estilos.texto1Bajo, bg = colorLabel, fg = colorfuenteLabel, anchor="w")
        self.labelNoved.grid(row=11,column=0, sticky="ew", padx=20, pady=3)

        self.labelSubcon  = tk.Label(self.frameEntradas, text = "SUBCONTRATAR", font = estilos.texto1Bajo, bg = colorLabel, fg = colorfuenteLabel, anchor="w")
        self.labelSubcon.grid(row=12,column=0, sticky="ew", padx=20, pady=3)

        self.labelPedido  = tk.Label(self.frameEntradas, text = "PEDIDO", font = estilos.texto1Bajo, bg = colorLabel, fg = colorfuenteLabel, anchor="w")
        self.labelPedido.grid(row=13,column=0, sticky="ew", padx=20, pady=3)

        #ENTRY PARA CAMPOS

        self.entryChasis = tk.Entry  (self.frameEntradas, font = estilos.numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varChasis) 
        self.entryFecha = tk.Entry   (self.frameEntradas, font = estilos.numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varFecha) 
        self.entryMarca = tk.Entry   (self.frameEntradas, font = estilos.numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varMarca)
        self.entryModelo = tk.Entry  (self.frameEntradas, font = estilos.numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varModelo)
        self.entryColor = tk.Entry   (self.frameEntradas, font = estilos.numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varColor)
        self.entryEstado = tk.Entry  (self.frameEntradas, font = estilos.numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varEstado)
        self.entryTel = tk.Entry     (self.frameEntradas, font = estilos.numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varTel)
        self.entryPdi = tk.Entry     (self.frameEntradas, font = estilos.numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varPdi)
        self.entryLav = tk.Entry     (self.frameEntradas, font = estilos.numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varLav)
        self.entryPin = tk.Entry     (self.frameEntradas, font = estilos.numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varPin)
        self.entryCal = tk.Entry     (self.frameEntradas, font = estilos.numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varCal)
        self.entryNoved = tk.Entry   (self.frameEntradas, font = estilos.numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varNoved)
        self.entrySubcon = tk.Entry  (self.frameEntradas, font = estilos.numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varSubcon)
        self.entryPedido = tk.Entry  (self.frameEntradas, font = estilos.numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varPedido)



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

        self.buttonCancelar = tk.Button(self.frameEntradas,text="Cancelar", font=estilos.texto1Bajo, bg=estilos.grisAzuladoOscuro, fg=estilos.blancoHueso, command="")   
        self.buttonCancelar.grid(row=14, column=0, padx=22, pady=8)

        self.buttonAgregar = tk.Button(self.frameEntradas,text="Añadir", font=estilos.textoGrande, bg=estilos.azulMedio, fg=estilos.blancoFrio, command="")    
        self.buttonAgregar.grid(row=14, column=1, padx=22, pady=8)            


        self.rootAux.mainloop()