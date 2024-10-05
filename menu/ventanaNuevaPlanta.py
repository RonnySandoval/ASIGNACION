import tkinter as tk
import estilos


class VentanaNuevaPlanta():       #Ventana para crear o editar modelos
    def __init__(self):

        self.rootAux = tk.Toplevel()
        self.rootAux.title("Crear Nueva Planta")
        self.rootAux.config(bg = estilos.moradoClaro)
        self.rootAux.iconbitmap("logo5.ico")
        self.rootAux.geometry("450x400")
        self.rootAux.resizable(False, False)

        self.frameTitulo = tk.Frame(self.rootAux, bg=estilos.moradoClaro)
        self.frameTitulo.pack(expand=True, side="top", fill="both")
        self.frameEntradas = tk.Frame(self.rootAux, bg=estilos.moradoClaro)
        self.frameEntradas.pack(expand=True, side="bottom", fill="both", pady=10)

        # variables objeto para los entry. Deben ser parte del constructor, para poder usarlas en sus métodos
        self.varNombre = tk.StringVar()
        self.varProcesos = tk.StringVar() 
        self.varDescripcion = tk.StringVar() 


        #LABEL PARA TITULO Y CAMPOS
        self.labelTitulo      = tk.Label(self.frameTitulo, text = "CREAR NUEVA PLANTA", font = estilos.textoGrande, fg = estilos.grisAzuladoOscuro, bg=estilos.moradoClaro)
        self.labelNombre      = tk.Label(self.frameEntradas, text = "Nombre de Planta", font = estilos.texto1Bajo, fg = estilos.grisAzuladoOscuro, bg=estilos.moradoClaro)
        self.labelProcesos    = tk.Label(self.frameEntradas, text = "Cantidad de Procesos", font = estilos.texto1Bajo, fg = estilos.grisAzuladoOscuro, bg=estilos.moradoClaro)
        self.labelDescripcion = tk.Label(self.frameEntradas, text = "Descripción de Planta", font = estilos.texto1Bajo, fg = estilos.grisAzuladoOscuro, bg=estilos.moradoClaro)

        self.labelTitulo.pack     (expand=True, side="top", fill="x", padx=20, pady=20)
        self.labelNombre.grid     (row=0,column=0, sticky="ew", padx=20, pady=5)
        self.labelProcesos.grid   (row=1,column=0, sticky="ew", padx=20, pady=5)
        self.labelDescripcion.grid(row=2,column=0, sticky="ew", padx=20, pady=5)


        #ENTRY PARA CAMPOS
        self.entryNombre = tk.Entry     (self.frameEntradas, font = estilos.numerosMedianos, fg = estilos.blancoHueso, bg=estilos.moradoOscuro, width=30, textvariable=self.varNombre)
        self.entryProcesos = tk.Entry   (self.frameEntradas, font = estilos.numerosMedianos, fg = estilos.blancoHueso, bg=estilos.moradoOscuro, width=30, textvariable=self.varProcesos)
        self.entryDescripcion = tk.Entry(self.frameEntradas, font = estilos.numerosMedianos, fg = estilos.blancoHueso, bg=estilos.moradoOscuro,  width=30, textvariable=self.varDescripcion)

        self.entryNombre.grid     (row=0,column=1, sticky="ew", pady=5)
        self.entryProcesos.grid   (row=1,column=1, sticky="ew", pady=5)
        self.entryDescripcion.grid(row=2,column=1, sticky="ew", pady=5)


        self.buttonCancelar = tk.Button(self.frameEntradas, text="Cancelar", font = estilos.texto1Bajo,  bg = estilos.grisAzuladoMedio, fg = estilos.blancoHueso,
                                        command="")   
        self.buttonGuardar  = tk.Button(self.frameEntradas, text="Guardar",  font = estilos.textoGrande, bg = estilos.azulMedio, fg = estilos.blancoFrio,
                                        command="")    

        self.buttonCancelar.grid(row=7, column=0, padx=22, pady=10)
        self.buttonGuardar.grid(row=7, column=1, padx=22, pady=10)