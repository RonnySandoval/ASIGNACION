import tkinter as tk
import estilos

class VentanaNuevoModelo():       #Ventana para crear o editar modelos
    def __init__(self):

        self.rootAux = tk.Toplevel()
        self.rootAux.title("Programación de Planta")
        self.rootAux.config(bg = estilos.grisOscuro)
        self.rootAux.iconbitmap("logo5.ico")
        self.rootAux.geometry("345x400")
        self.rootAux.resizable(False, False)

        self.frameTitulo = tk.Frame(self.rootAux, bg=estilos.grisOscuro)
        self.frameTitulo.pack(expand=True, side="top", fill="both")
        self.frameEntradas = tk.Frame(self.rootAux, bg=estilos.grisOscuro)
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

        self.labelTitulo = tk.Label(self.frameTitulo, text = "CREAR NUEVO MODELO", font = estilos.textoGrande, bg = colorTitulo, fg = colorfuenteLabel)
        self.labelTitulo.pack(expand=True, side="top", fill="x", padx=20, pady=20)

        self.labelMarca    = tk.Label(self.frameEntradas, text = "MARCA", font = estilos.texto1Bajo, bg = colorLabel, fg = colorfuenteLabel)
        self.labelMarca.grid(row=0,column=0, sticky="ew", padx=20, pady=5)

        self.labelModelo   = tk.Label(self.frameEntradas, text = "MODELO", font = estilos.texto1Bajo, bg = colorLabel, fg = colorfuenteLabel)
        self.labelModelo.grid(row=1,column=0, sticky="ew", padx=20, pady=5)

        self.labelTimeTel  = tk.Label(self.frameEntradas, text = "Tiempos Telequinox", font = estilos.texto1Bajo, bg = colorLabel, fg = colorfuenteLabel)
        self.labelTimeTel.grid(row=2,column=0, sticky="ew", padx=20, pady=5)

        self.labelTimePdi  = tk.Label(self.frameEntradas, text = "Tiempos PDI" , font = estilos.texto1Bajo, bg = colorLabel, fg = colorfuenteLabel)
        self.labelTimePdi.grid(row=3,column=0, sticky="ew", padx=20, pady=5)

        self.labelTimeLav  = tk.Label(self.frameEntradas, text = "Tiempos LAVADO", font = estilos.texto1Bajo, bg = colorLabel, fg = colorfuenteLabel)
        self.labelTimeLav.grid(row=4,column=0, sticky="ew", padx=20, pady=5)

        self.labelTimePin = tk.Label(self.frameEntradas, text = "Tiempos PINTURA", font = estilos.texto1Bajo, bg = colorLabel, fg = colorfuenteLabel)
        self.labelTimePin.grid(row=5,column=0, sticky="ew", padx=20, pady=5)

        self.labelTimeCal  = tk.Label(self.frameEntradas, text = "Tiempos CALIDAD", font = estilos.texto1Bajo, bg = colorLabel, fg = colorfuenteLabel)
        self.labelTimeCal.grid(row=6,column=0, sticky="ew", padx=20, pady=5)


        #ENTRY PARA CAMPOS
        self.entryMarca = tk.Entry   (self.frameEntradas, font = estilos.numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varMarca)
        self.entryModelo = tk.Entry  (self.frameEntradas, font = estilos.numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varModelo)
        self.entryTel = tk.Entry     (self.frameEntradas, font = estilos.numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varTel)
        self.entryPdi = tk.Entry     (self.frameEntradas, font = estilos.numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varPdi)
        self.entryLav = tk.Entry     (self.frameEntradas, font = estilos.numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varLav)
        self.entryPin = tk.Entry     (self.frameEntradas, font = estilos.numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varPin)
        self.entryCal = tk.Entry     (self.frameEntradas, font = estilos.numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varCal)

        self.entryMarca.grid (row=0,column=1, sticky="ew", pady=5)
        self.entryModelo.grid(row=1,column=1, sticky="ew", pady=5)
        self.entryTel.grid   (row=2,column=1, sticky="ew", pady=5)
        self.entryPdi.grid   (row=3,column=1, sticky="ew", pady=5)
        self.entryLav.grid   (row=4,column=1, sticky="ew", pady=5)
        self.entryPin.grid   (row=5,column=1, sticky="ew", pady=5)
        self.entryCal.grid   (row=6,column=1, sticky="ew", pady=5)

        self.buttonCancelar = tk.Button(self.frameEntradas,text="Cancelar", font = estilos.texto1Bajo, bg = estilos.grisAzuladoMedio, fg = estilos.blancoHueso, 
                                        command="")   
        self.buttonGuardar = tk.Button(self.frameEntradas,text="Guardar", font = estilos.textoGrande, bg = estilos.azulMedio, fg = estilos.blancoFrio,
                                        command="") 

        self.buttonCancelar.grid(row=7, column=0, padx=22, pady=10)
        self.buttonGuardar.grid(row=7, column=1, padx=22, pady=10)
    

        self.rootAux.mainloop()