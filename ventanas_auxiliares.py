import tkinter as tk
#from tkinter import ttk
from tkcalendar import Calendar
from tkinter import simpledialog
import time
from estilos import grisAzuladoClaro, grisAzuladoMedio, grisAzuladoOscuro, grisMedio, grisOscuro, textoGrande, naranjaOscuro, blancoFrio, amarilloClaro, amarilloMedio, azulOscuro, moradoOscuro, moradoClaro, texto1Bajo, numerosMedianos, naranjaMedio, blancoHueso, azulMedio, moradoMedio, amarilloOscuro, grisVerdeMedio
import datetime
import re

######################################################################################################
################################### VENTANA PARA AGREGAR Y EDITAR MODELOS ############################
######################################################################################################

class VentanaCreaEdita():       #Ventana para crear o editar modelos
    def __init__(self, accion):
        self.accion = accion
        self.rootAux = tk.Toplevel()
        self.rootAux.title("Programación de Planta")
        self.rootAux.config(bg = grisOscuro)
        self.rootAux.iconbitmap("logo5.ico")
        self.rootAux.geometry("345x400")
        self.rootAux.resizable(False, False)

        self.frameTitulo = tk.Frame(self.rootAux, bg=grisOscuro)
        self.frameTitulo.pack(expand=True, side="top", fill="both")
        self.frameEntradas = tk.Frame(self.rootAux, bg=grisOscuro)
        self.frameEntradas.pack(expand=True, side="bottom", fill="both", pady=10)

        # variables objeto para los entry. Deben ser parte del constructor, para poder usarlas en sus métodos
        self.varMarca = tk.StringVar()
        self.varModelo = tk.StringVar() 
        self.varTel = tk.StringVar() 
        self.varPdi = tk.StringVar() 
        self.varLav = tk.StringVar() 
        self.varPin = tk.StringVar()
        self.varCal= tk.StringVar()

        self.setup_ui()

    def setup_ui(self):
        # Define colors basandose en el parámetro accion (EDITAR o CREAR)
        if self.accion == "EDITAR":
            colorTitulo = grisMedio
            colorLabel = grisMedio      
            colorEntry = grisMedio
            colorfuenteLabel = blancoFrio
            colorfuenteEntry = blancoFrio
        elif self.accion == "CREAR":
            colorTitulo = moradoMedio
            colorLabel = moradoMedio
            colorEntry = moradoMedio
            colorfuenteLabel = blancoFrio
            colorfuenteEntry = blancoFrio



        #LABEL PARA TITULO Y CAMPOS
        self.titulo = self.accion
        self.labelTitulo = tk.Label(self.frameTitulo, text = self.titulo + " MODELO", font = textoGrande, bg = colorTitulo, fg = colorfuenteLabel)
        self.labelTitulo.pack(expand=True, side="top", fill="x", padx=20, pady=20)

        self.labelMarca    = tk.Label(self.frameEntradas, text = "MARCA", font = texto1Bajo, bg = colorLabel, fg = colorfuenteLabel)
        self.labelMarca.grid(row=0,column=0, sticky="ew", padx=20, pady=5)

        self.labelModelo   = tk.Label(self.frameEntradas, text = "MODELO", font = texto1Bajo, bg = colorLabel, fg = colorfuenteLabel)
        self.labelModelo.grid(row=1,column=0, sticky="ew", padx=20, pady=5)

        self.labelTimeTel  = tk.Label(self.frameEntradas, text = "Tiempos Telequinox", font = texto1Bajo, bg = colorLabel, fg = colorfuenteLabel)
        self.labelTimeTel.grid(row=2,column=0, sticky="ew", padx=20, pady=5)

        self.labelTimePdi  = tk.Label(self.frameEntradas, text = "Tiempos PDI" , font = texto1Bajo, bg = colorLabel, fg = colorfuenteLabel)
        self.labelTimePdi.grid(row=3,column=0, sticky="ew", padx=20, pady=5)

        self.labelTimeLav  = tk.Label(self.frameEntradas, text = "Tiempos LAVADO", font = texto1Bajo, bg = colorLabel, fg = colorfuenteLabel)
        self.labelTimeLav.grid(row=4,column=0, sticky="ew", padx=20, pady=5)

        self.labelTimePin = tk.Label(self.frameEntradas, text = "Tiempos PINTURA", font = texto1Bajo, bg = colorLabel, fg = colorfuenteLabel)
        self.labelTimePin.grid(row=5,column=0, sticky="ew", padx=20, pady=5)

        self.labelTimeCal  = tk.Label(self.frameEntradas, text = "Tiempos CALIDAD", font = texto1Bajo, bg = colorLabel, fg = colorfuenteLabel)
        self.labelTimeCal.grid(row=6,column=0, sticky="ew", padx=20, pady=5)


        #ENTRY PARA CAMPOS
        self.entryMarca = tk.Entry   (self.frameEntradas, font = numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varMarca)
        self.entryModelo = tk.Entry  (self.frameEntradas, font = numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varModelo)
        self.entryTel = tk.Entry     (self.frameEntradas, font = numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varTel)
        self.entryPdi = tk.Entry     (self.frameEntradas, font = numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varPdi)
        self.entryLav = tk.Entry     (self.frameEntradas, font = numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varLav)
        self.entryPin = tk.Entry     (self.frameEntradas, font = numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varPin)
        self.entryCal = tk.Entry     (self.frameEntradas, font = numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varCal)

        self.entryMarca.grid (row=0,column=1, sticky="ew", pady=5)
        self.entryModelo.grid(row=1,column=1, sticky="ew", pady=5)
        self.entryTel.grid   (row=2,column=1, sticky="ew", pady=5)
        self.entryPdi.grid   (row=3,column=1, sticky="ew", pady=5)
        self.entryLav.grid   (row=4,column=1, sticky="ew", pady=5)
        self.entryPin.grid   (row=5,column=1, sticky="ew", pady=5)
        self.entryCal.grid   (row=6,column=1, sticky="ew", pady=5)

        self.buttonCancelar = tk.Button(self.frameEntradas,text="Cancelar", font=texto1Bajo, bg=grisAzuladoMedio, fg=blancoHueso)   
        self.buttonGuardar = tk.Button(self.frameEntradas,text="Guardar", font=textoGrande, bg=azulMedio, fg=blancoFrio)    

        self.buttonCancelar.grid(row=7, column=0, padx=22, pady=10)
        self.buttonGuardar.grid(row=7, column=1, padx=22, pady=10)

        
    def set_values(self, datos):
        #Método que ingresa en los entrys los valores de la lista parámetro. Estó será usado en el modulo eventos para pegar los datos de la ventana principal
        self.varMarca.set(datos[0])
        self.varModelo.set(datos[1])
        self.varTel.set(datos[2])
        self.varPdi.set(datos[3])
        self.varLav.set(datos[4])
        self.varPin.set(datos[5])
        self.varCal.set(datos[6])      

    def asignafuncionBoton(self, funcionGuardar, funcionCancelar):
        #Método para asignar la función al command button de guardar y cancelar desde otro módulo.
        self.buttonGuardar.configure(command =funcionGuardar)
        self.buttonCancelar.configure(command =funcionCancelar)


        self.rootAux.mainloop()

###########################################################################################



class VentanaGestionaPedido():
    def __init__(self, accion):
        self.accion = accion
        self.rootAux = tk.Toplevel()
        self.rootAux.title("Programación de Planta")
        self.rootAux.config(bg = grisAzuladoMedio)
        self.rootAux.iconbitmap("logo5.ico")
        self.rootAux.geometry("400x700")
        self.rootAux.resizable(False, False)

        self.frameTitulo = tk.Frame(self.rootAux, bg=grisAzuladoMedio)
        self.frameTitulo.pack(expand=True, side="top", fill="both")
        self.frameEntradas = tk.Frame(self.rootAux, bg=grisAzuladoMedio)
        self.frameEntradas.pack(expand=True, side="bottom", fill="both", pady=10)

        self.varChasis = tk.StringVar() 
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

        self.setup_ui()

    def setup_ui(self):
        # Define colors basandose en el parámetro accion (EDITAR o CREAR)
        if self.accion == "MODIFICAR":
            colorTitulo = moradoOscuro
            colorLabel = moradoOscuro     
            colorEntry = moradoOscuro
            colorfuenteLabel = blancoFrio
            colorfuenteEntry = blancoFrio
        elif self.accion == "AGREGAR":
            colorTitulo = grisAzuladoMedio
            colorLabel = grisAzuladoMedio
            colorEntry = grisAzuladoMedio
            colorfuenteLabel = blancoFrio
            colorfuenteEntry = blancoFrio



        #LABEL PARA TITULO Y CAMPOS
        self.titulo = self.accion
        self.labelTitulo   = tk.Label(self.frameTitulo, text = self.titulo + " VEHICULO A PEDIDO", font = textoGrande, bg = colorTitulo, fg = colorfuenteLabel)
        self.labelTitulo.pack(expand=True, side="top", fill="x", padx=20, pady=20)

        self.labelChasis   = tk.Label(self.frameEntradas, text = "CHASIS", font = texto1Bajo, bg = colorLabel, fg = colorfuenteLabel, anchor="w")
        self.labelChasis.grid(row=0,column=0, sticky="ew", padx=20, pady=5)

        self.labelFecha    = tk.Label(self.frameEntradas, text = "FECHA ENTREGA", font = texto1Bajo, bg = colorLabel, fg = colorfuenteLabel, anchor="w")
        self.labelFecha.grid(row=1,column=0, sticky="ew", padx=20, pady=5)

        self.labelMarca    = tk.Label(self.frameEntradas, text = "MARCA", font = texto1Bajo, bg = colorLabel, fg = colorfuenteLabel, anchor="w")
        self.labelMarca.grid(row=2,column=0, sticky="ew", padx=20, pady=5)

        self.labelModelo   = tk.Label(self.frameEntradas, text = "MODELO", font = texto1Bajo, bg = colorLabel, fg = colorfuenteLabel, anchor="w")
        self.labelModelo.grid(row=3,column=0, sticky="ew", padx=20, pady=5)

        self.labelColor  = tk.Label(self.frameEntradas, text = "COLOR", font = texto1Bajo, bg = colorLabel, fg = colorfuenteLabel, anchor="w")
        self.labelColor.grid(row=4,column=0, sticky="ew", padx=20, pady=5)

        self.labelEstado  = tk.Label(self.frameEntradas, text = "ESTADO", font = texto1Bajo, bg = colorLabel, fg = colorfuenteLabel, anchor="w")
        self.labelEstado.grid(row=5,column=0, sticky="ew", padx=20, pady=5)

        self.labelTimeTel  = tk.Label(self.frameEntradas, text = "Tiempos TELEQUINOX", font = texto1Bajo, bg = colorLabel, fg = colorfuenteLabel, anchor="w")
        self.labelTimeTel.grid(row=6,column=0, sticky="ew", padx=20, pady=5)

        self.labelTimePdi  = tk.Label(self.frameEntradas, text = "Tiempos PDI" , font = texto1Bajo, bg = colorLabel, fg = colorfuenteLabel, anchor="w")
        self.labelTimePdi.grid(row=7,column=0, sticky="ew", padx=20, pady=5)

        self.labelTimeLav  = tk.Label(self.frameEntradas, text = "Tiempos LAVADO", font = texto1Bajo, bg = colorLabel, fg = colorfuenteLabel, anchor="w")
        self.labelTimeLav.grid(row=8,column=0, sticky="ew", padx=20, pady=5)

        self.labelTimePin  = tk.Label(self.frameEntradas, text = "Tiempos PINTURA", font = texto1Bajo, bg = colorLabel, fg = colorfuenteLabel, anchor="w")
        self.labelTimePin.grid(row=9,column=0, sticky="ew", padx=20, pady=5)

        self.labelTimeCal  = tk.Label(self.frameEntradas, text = "Tiempos CALIDAD", font = texto1Bajo, bg = colorLabel, fg = colorfuenteLabel, anchor="w")
        self.labelTimeCal.grid(row=10,column=0, sticky="ew", padx=20, pady=5)

        self.labelNoved  = tk.Label(self.frameEntradas, text = "NOVEDADES", font = texto1Bajo, bg = colorLabel, fg = colorfuenteLabel, anchor="w")
        self.labelNoved.grid(row=11,column=0, sticky="ew", padx=20, pady=5)

        self.labelSubcon  = tk.Label(self.frameEntradas, text = "SUBCONTRATAR", font = texto1Bajo, bg = colorLabel, fg = colorfuenteLabel, anchor="w")
        self.labelSubcon.grid(row=12,column=0, sticky="ew", padx=20, pady=5)


        #ENTRY PARA CAMPOS

        self.entryChasis = tk.Entry  (self.frameEntradas, font = numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varChasis) 
        self.entryFecha = tk.Entry   (self.frameEntradas, font = numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varFecha) 
        self.entryMarca = tk.Entry   (self.frameEntradas, font = numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varMarca)
        self.entryModelo = tk.Entry  (self.frameEntradas, font = numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varModelo)
        self.entryColor = tk.Entry   (self.frameEntradas, font = numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varColor)
        self.entryEstado = tk.Entry  (self.frameEntradas, font = numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varEstado)
        self.entryTel = tk.Entry     (self.frameEntradas, font = numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varTel)
        self.entryPdi = tk.Entry     (self.frameEntradas, font = numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varPdi)
        self.entryLav = tk.Entry     (self.frameEntradas, font = numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varLav)
        self.entryPin = tk.Entry     (self.frameEntradas, font = numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varPin)
        self.entryCal = tk.Entry     (self.frameEntradas, font = numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varCal)
        self.entryNoved = tk.Entry   (self.frameEntradas, font = numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varNoved)
        self.entrySubcon = tk.Entry  (self.frameEntradas, font = numerosMedianos, bg = colorEntry, fg = colorfuenteEntry, width=20, textvariable=self.varSubcon)

        self.entryChasis.grid(row=0 ,column=1, sticky="ew", pady=5)
        self.entryFecha.grid (row=1 ,column=1, sticky="ew", pady=5)
        self.entryMarca.grid (row=2 ,column=1, sticky="ew", pady=5)
        self.entryModelo.grid(row=3 ,column=1, sticky="ew", pady=5)
        self.entryColor.grid (row=4 ,column=1, sticky="ew", pady=5)
        self.entryEstado.grid(row=5 ,column=1, sticky="ew", pady=5)
        self.entryTel.grid   (row=6 ,column=1, sticky="ew", pady=5)
        self.entryPdi.grid   (row=7 ,column=1, sticky="ew", pady=5)
        self.entryLav.grid   (row=8 ,column=1, sticky="ew", pady=5)
        self.entryPin.grid   (row=9 ,column=1, sticky="ew", pady=5)
        self.entryCal.grid   (row=10,column=1, sticky="ew", pady=5)
        self.entryNoved.grid (row=11,column=1, sticky="ew", pady=5)
        self.entrySubcon.grid(row=12,column=1, sticky="ew", pady=5)

        self.buttonCancelar = tk.Button(self.frameEntradas,text="Cancelar", font=texto1Bajo, bg=grisAzuladoOscuro, fg=blancoHueso, command="")   
        self.buttonCancelar.grid(row=13, column=0, padx=22, pady=10)

        if self.accion == "AGREGAR":
            self.buttonAgregar = tk.Button(self.frameEntradas,text="Agregar", font=textoGrande, bg=azulMedio, fg=blancoFrio, command="")    
            self.buttonAgregar.grid(row=13, column=1, padx=22, pady=10)

        if self.accion == "MODIFICAR":
            self.buttonAgregar = tk.Button(self.frameEntradas,text="Reemplazar", font=textoGrande, bg=azulMedio, fg=blancoFrio, command="")    
            self.buttonAgregar.grid(row=13, column=1, padx=22, pady=10)            


    def set_values(self, datos, accion):
        if accion == 'AGREGAR':
            self.varMarca.set(datos[0])
            self.varModelo.set(datos[1])
            self.varTel.set(datos[2])
            self.varPdi.set(datos[3])
            self.varLav.set(datos[4])
            self.varPin.set(datos[5])
            self.varCal.set(datos[6])   

        if accion == 'MODIFICAR':
            self.varChasis.set(datos[0])
            self.varFecha.set(datos[1])
            self.varMarca.set(datos[2])
            self.varModelo.set(datos[3])
            self.varColor.set(datos[4])
            self.varEstado.set(datos[5])
            self.varTel.set(datos[6])
            self.varPdi.set(datos[7])
            self.varLav.set(datos[8])
            self.varPin.set(datos[9])
            self.varCal.set(datos[10])
            self.varNoved.set(datos[11])
            self.varSubcon.set(datos[12])
    
    def asignafuncionBoton(self, funcionAgregar, funcionCancelar):
        #Método para asignar la función al command button de guardar y cancelar desde otro módulo.
        self.buttonAgregar.configure(command =funcionAgregar)
        self.buttonCancelar.configure(command =funcionCancelar)

        self.rootAux.mainloop()





class EstableceFechaHora():
    def __init__(self):
        self.rootAux = tk.Toplevel()
        self.rootAux.title("Iniciar programa")
        self.rootAux.config(bg = grisAzuladoMedio)
        self.rootAux.iconbitmap("logo5.ico")
        self.rootAux.geometry("300x300")
        self.rootAux.resizable(False, False)

        self.frameTitulo = tk.Frame(self.rootAux, bg=grisAzuladoMedio)
        self.frameTitulo.pack(expand=True, side="top", fill="both")
        self.frameEntradas = tk.Frame(self.rootAux, bg=grisAzuladoMedio)
        self.frameEntradas.pack(expand=True, side="bottom", fill="both", pady=10)


        self.labelTitulo   = tk.Label(self.frameTitulo, text = "Iniciar programa en", font = textoGrande, bg = grisAzuladoMedio, fg = blancoFrio)
        self.labelTitulo.pack(expand=True, side="top", fill="x", padx=20, pady=20)
        self.labelFecha    = tk.Label(self.frameEntradas, text = "FECHA", font = texto1Bajo, bg = grisAzuladoMedio, fg = blancoFrio, anchor="w")
        self.labelFecha.grid(row=1,column=0, sticky="ew", padx=20, pady=5)
        self.labelHora   = tk.Label(self.frameEntradas, text = "HORA", font = texto1Bajo, bg = grisAzuladoMedio, fg = blancoFrio, anchor="w")
        self.labelHora.grid(row=2,column=0, sticky="ew", padx=20, pady=5)


        self.varFecha = tk.StringVar() 
        self.varHora = tk.StringVar()
        self.entryFecha = tk.Entry   (self.frameEntradas, font = numerosMedianos, bg = grisAzuladoClaro, fg = blancoFrio, width=20, textvariable=self.varFecha) 
        self.entryHora = tk.Entry   (self.frameEntradas, font = numerosMedianos, bg = grisAzuladoClaro, fg = blancoFrio, width=20, textvariable=self.varHora,
                                     validate='focusout', validatecommand=(self.rootAux.register(self.validar_hora), '%P'))  # %P es el valor propuesto
        self.entryFecha.grid (row=1 ,column=1, sticky="ew", pady=5)
        self.entryHora.grid (row=2 ,column=1, sticky="ew", pady=5)
        self.entryFecha.bind("<Button-1>", self.mostrar_calendario)
        self.entryHora.bind("<Button-1>", self.seleccionar_hora)

        self.buttonCancelar = tk.Button(self.frameEntradas, text="Cancelar", font = texto1Bajo,  bg = naranjaMedio, fg = blancoHueso,  command="")   
        self.buttonAceptar  = tk.Button(self.frameEntradas, text="Aceptar",  font = textoGrande, bg = azulMedio, fg = blancoFrio,  command="")
        self.buttonCancelar.grid(row=3, column=0, padx=22, pady=10)  
        self.buttonAceptar.grid(row=3, column=1, padx=22, pady=10)

        self.llenar_hora_actual()

    def mostrar_calendario(self, event):
        #Muestra un calendario para seleccionar la fecha
        top = tk.Toplevel(self.rootAux)
        top.grab_set()
        cal = Calendar(top, selectmode='day', date_pattern="yyyy-mm-dd")
        cal.pack(pady=20)

        def seleccion_fecha():
            self.varFecha.set(cal.get_date())
            top.destroy()

        btnSeleccionar = tk.Button(top, text="Seleccionar", command=seleccion_fecha)
        btnSeleccionar.pack()

    def llenar_hora_actual(self):
        #Prellena el Entry de hora con la hora actual en formato HH:MM
        self.varHora.set(datetime.datetime.now().strftime("%H:%M:%S"))



    def seleccionar_hora(self, event):
        #Despliega una ventana para seleccionar la hora
        hora = simpledialog.askstring("Seleccionar Hora", "Ingrese la hora (HH:MM:SS):", parent=self.rootAux)
        if self.validar_hora(hora):
            self.varHora.set(hora)
        else:
            tk.messagebox.showerror("Error", "Formato de hora inválido. Use HH:MM:SS")


    def validar_hora(self, valor_propuesto):        #Valida que el formato de la hora sea HH:MM. Retorna True si es válido, False de lo contrario.

        if re.fullmatch(r'([01]\d|2[0-3]):([0-5]\d):([0-5]\d)', valor_propuesto):
            return True
        elif valor_propuesto == "":
            # Permitir que el campo esté vacío si el usuario lo elimina
            return True
        else:
            tk.messagebox.showerror("Error de validación", "Formato de hora inválido. Use HH:MM:SS (24 horas).")
            return False


    def asignaFuncion(self, funcionAceptar, funcionCancelar):
        self.buttonAceptar.configure(command = funcionAceptar)
        self.buttonCancelar.configure(command = funcionCancelar)

     
        self.rootAux.mainloop()