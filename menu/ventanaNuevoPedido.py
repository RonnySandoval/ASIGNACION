import tkinter as tk
import customtkinter as ctk
import view.estilos as estilos
import controller.glo as glo


class VentanaNuevoPedido():       #Ventana para crear o editar modelos
    def __init__(self, bbdd):

        self.rootAux = ctk.CTkToplevel()
        self.rootAux.title("Crear Nueva Pedido")
        self.rootAux.config(background = estilos.grisAzuladoOscuro)
        self.rootAux.iconbitmap("image\logo5.ico")
        self.rootAux.geometry("450x400")
        self.rootAux.resizable(False, False)

        self.frameTitulo = ctk.CTkFrame(self.rootAux, fg_color=estilos.grisAzuladoOscuro)
        self.frameTitulo.pack(expand=True, side="top", fill="both")
        self.frameEntradas = ctk.CTkFrame(self.rootAux, fg_color=estilos.grisAzuladoOscuro)
        self.frameEntradas.pack(expand=True, side="bottom", fill="both", pady=10)

        # variables objeto para los entry. Deben ser parte del constructor, para poder usarlas en sus métodos
        self.varNombre  = tk.StringVar()
        self.varDependCliente  = tk.StringVar()
        self.varFechaRecepcion  = tk.StringVar()
        self.varFechaIngreso = tk.StringVar() 
        self.varFechaEstimada   = tk.StringVar()
        self.varFechaEntrega   = tk.StringVar()

        #LABEL PARA TITULO Y CAMPOS
        self.labelTitulo          = ctk.CTkLabel(self.frameTitulo,   text = "CREAR NUEVO PEDIDO", font = estilos.textoGrande, text_color = estilos.blancoFrio, fg_color=estilos.grisAzuladoOscuro)
        self.labelNombre          = ctk.CTkLabel(self.frameEntradas, text = "Fecha de Recepción", font = estilos.texto1Bajo, text_color = estilos.blancoFrio, fg_color=estilos.grisAzuladoOscuro)
        self.labelDependCliente   = ctk.CTkLabel(self.frameEntradas, text = "Cliente/Depedencia", font = estilos.texto1Bajo, text_color = estilos.blancoFrio, fg_color=estilos.grisAzuladoOscuro)
        self.labelFechaRecepcion  = ctk.CTkLabel(self.frameEntradas, text = "Fecha de Recepción", font = estilos.texto1Bajo, text_color = estilos.blancoFrio, fg_color=estilos.grisAzuladoOscuro)
        self.labelFechaIngreso    = ctk.CTkLabel(self.frameEntradas, text = "Fecha de Ingreso", font = estilos.texto1Bajo, text_color = estilos.blancoFrio, fg_color=estilos.grisAzuladoOscuro)
        self.labelFechaEstimada   = ctk.CTkLabel(self.frameEntradas, text = "Fecha estimada"   , font = estilos.texto1Bajo, text_color = estilos.blancoFrio, fg_color=estilos.grisAzuladoOscuro)
        self.labelFechaEntrega    = ctk.CTkLabel(self.frameEntradas, text = "Fecha de entrega"  , font = estilos.texto1Bajo, text_color = estilos.blancoFrio, fg_color=estilos.grisAzuladoOscuro)

        self.labelTitulo.pack        (expand=True, side="top", fill="x", padx=20, pady=20)
        self.labelNombre.grid        (row=0, column=0, sticky="ew", padx=20, pady=5)       
        self.labelDependCliente.grid (row=1, column=0, sticky="ew", padx=20, pady=5) 
        self.labelFechaRecepcion.grid(row=2, column=0, sticky="ew", padx=20, pady=5)
        self.labelFechaIngreso.grid  (row=3, column=0, sticky="ew", padx=20, pady=5)
        self.labelFechaEstimada.grid (row=4, column=0, sticky="ew", padx=20, pady=5)
        self.labelFechaEntrega.grid  (row=5, column=0, sticky="ew", padx=20, pady=5)

        #ENTRY PARA CAMPOS
        self.entryNombre = ctk.CTkEntry        (self.frameEntradas, font = estilos.numerosMedianos, text_color = estilos.blancoHueso, fg_color=estilos.grisOscuro, width=30, textvariable=self.varNombre)
        self.entryDependCliente = ctk.CTkEntry (self.frameEntradas, font = estilos.numerosMedianos, text_color = estilos.blancoHueso, fg_color=estilos.grisOscuro, width=30, textvariable=self.varDependCliente)
        self.entryFechaRecepcion = ctk.CTkEntry(self.frameEntradas, font = estilos.numerosMedianos, text_color = estilos.blancoHueso, fg_color=estilos.grisOscuro, width=30, textvariable=self.varFechaRecepcion)
        self.entryFechaIngreso = ctk.CTkEntry  (self.frameEntradas, font = estilos.numerosMedianos, text_color = estilos.blancoHueso, fg_color=estilos.grisOscuro, width=30, textvariable=self.varFechaIngreso)
        self.entryFechaEstimada = ctk.CTkEntry (self.frameEntradas, font = estilos.numerosMedianos, text_color = estilos.blancoHueso, fg_color=estilos.grisOscuro, width=30, textvariable=self.varFechaEstimada)
        self.entryFechaEntrega = ctk.CTkEntry  (self.frameEntradas, font = estilos.numerosMedianos, text_color = estilos.blancoHueso, fg_color=estilos.grisOscuro, width=30, textvariable=self.varFechaEntrega)

        self.entryNombre.grid         (row=0, column=1, sticky="ew", pady=5)
        self.entryDependCliente .grid (row=1, column=1, sticky="ew", pady=5)
        self.entryFechaRecepcion.grid (row=2, column=1, sticky="ew", pady=5)
        self.entryFechaIngreso.grid   (row=3, column=1, sticky="ew", pady=5)
        self.entryFechaEstimada.grid  (row=4, column=1, sticky="ew", pady=5) 
        self.entryFechaEntrega.grid   (row=5, column=1, sticky="ew", pady=5)

        self.buttonCancelar = ctk.CTkButton(self.frameEntradas, text="Cancelar", font = estilos.texto1Bajo,  fg_color = estilos.naranjaMedio, text_color = estilos.blancoHueso, hover_color = estilos.naranjaClaro,
                                        command="")   
        self.buttonGuardar  = ctk.CTkButton(self.frameEntradas, text="Guardar",  font = estilos.textoGrande, fg_color = estilos.azulMedio, text_color = estilos.blancoFrio, hover_color = estilos.azulClaro,
                                        command="")    

        self.buttonCancelar.grid(row=6, column=0, padx=22, pady=10)
        self.buttonGuardar.grid(row=6, column=1, padx=22, pady=10)
       
        glo.strVar_newPedido['nombre'] = self.varNombre
        glo.strVar_newPedido['cliente'] = self.varDependCliente
        glo.strVar_newPedido['fecha_recepcion'] = self.varFechaRecepcion
        glo.strVar_newPedido['fecha_ingreso']   = self.varFechaIngreso
        glo.strVar_newPedido['fecha_estimada']  = self.varFechaEstimada
        glo.strVar_newPedido['fecha_entrega']   = self.varFechaEntrega

    def asignafuncion(self, funcionGuardar, funcionCancelar):
        self.buttonGuardar.configure(command = funcionGuardar)
        self.buttonCancelar.configure(command = funcionCancelar)