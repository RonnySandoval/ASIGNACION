import tkinter as tk
import estilos


class VentanaNuevoPedido():       #Ventana para crear o editar modelos
    def __init__(self):

        self.rootAux = tk.Toplevel()
        self.rootAux.title("Crear Nueva Pedido")
        self.rootAux.config(bg = estilos.azulClaro)
        self.rootAux.iconbitmap("logo5.ico")
        self.rootAux.geometry("450x400")
        self.rootAux.resizable(False, False)

        self.frameTitulo = tk.Frame(self.rootAux, bg=estilos.azulClaro)
        self.frameTitulo.pack(expand=True, side="top", fill="both")
        self.frameEntradas = tk.Frame(self.rootAux, bg=estilos.azulClaro)
        self.frameEntradas.pack(expand=True, side="bottom", fill="both", pady=10)

        # variables objeto para los entry. Deben ser parte del constructor, para poder usarlas en sus métodos
        self.varDependCliente  = tk.StringVar()
        self.varFechaRecepcion = tk.StringVar() 
        self.varFechaEntrega   = tk.StringVar()
        self.varCantVehiculos   = tk.StringVar()


        #LABEL PARA TITULO Y CAMPOS
        self.labelTitulo          = tk.Label(self.frameTitulo,   text = "CREAR NUEVO PEDIDO", font = estilos.textoGrande, fg = estilos.grisAzuladoOscuro, bg=estilos.azulClaro)
        self.labelDependCliente   = tk.Label(self.frameEntradas, text = "Cliente/Depedencia", font = estilos.texto1Bajo, fg = estilos.grisAzuladoOscuro, bg=estilos.azulClaro)
        self.labelFechaRecepcion  = tk.Label(self.frameEntradas, text = "Fecha de Recepción", font = estilos.texto1Bajo, fg = estilos.grisAzuladoOscuro, bg=estilos.azulClaro)
        self.labelFechaEntrega    = tk.Label(self.frameEntradas, text = "Fecha de entrega"  , font = estilos.texto1Bajo, fg = estilos.grisAzuladoOscuro, bg=estilos.azulClaro)
        self.labelCantVehiculos   = tk.Label(self.frameEntradas, text = "Cantidad de Vehículos", font = estilos.texto1Bajo, fg = estilos.grisAzuladoOscuro, bg=estilos.azulClaro)



        self.labelTitulo.pack     (expand=True, side="top", fill="x", padx=20, pady=20)
        self.labelDependCliente.grid     (row=0,column=0, sticky="ew", padx=20, pady=5)
        self.labelFechaRecepcion.grid   (row=1,column=0, sticky="ew", padx=20, pady=5)
        self.labelFechaEntrega.grid(row=2,column=0, sticky="ew", padx=20, pady=5)
        self.labelCantVehiculos.grid(row=3,column=0, sticky="ew", padx=20, pady=5)


        #ENTRY PARA CAMPOS
        self.entryDependCliente = tk.Entry     (self.frameEntradas, font = estilos.numerosMedianos, fg = estilos.blancoHueso, bg=estilos.moradoOscuro, width=30, textvariable=self.varDependCliente)
        self.entryFechaRecepcion = tk.Entry   (self.frameEntradas, font = estilos.numerosMedianos, fg = estilos.blancoHueso, bg=estilos.moradoOscuro, width=30, textvariable=self.varFechaRecepcion)
        self.entryFechaEntrega = tk.Entry(self.frameEntradas, font = estilos.numerosMedianos, fg = estilos.blancoHueso, bg=estilos.moradoOscuro,  width=30, textvariable=self.varFechaEntrega)
        self.entryCantVehiculos = tk.Entry(self.frameEntradas, font = estilos.numerosMedianos, fg = estilos.blancoHueso, bg=estilos.moradoOscuro,  width=30, textvariable=self.varCantVehiculos)


        self.entryDependCliente .grid     (row=0,column=1, sticky="ew", pady=5)
        self.entryFechaRecepcion.grid   (row=1,column=1, sticky="ew", pady=5)
        self.entryFechaEntrega.grid(row=2,column=1, sticky="ew", pady=5)
        self.entryCantVehiculos.grid(row=3,column=1, sticky="ew", pady=5)


        self.buttonCancelar = tk.Button(self.frameEntradas, text="Cancelar", font = estilos.texto1Bajo,  bg = estilos.grisAzuladoMedio, fg = estilos.blancoHueso,
                                        command="")   
        self.buttonGuardar  = tk.Button(self.frameEntradas, text="Guardar",  font = estilos.textoGrande, bg = estilos.azulMedio, fg = estilos.blancoFrio,
                                        command="")    

        self.buttonCancelar.grid(row=7, column=0, padx=22, pady=10)
        self.buttonGuardar.grid(row=7, column=1, padx=22, pady=10)