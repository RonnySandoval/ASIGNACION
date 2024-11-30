import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkcalendar import Calendar
from tkinter import simpledialog
import time
from estilos import *
import datetime
import re
import glo
import BBDD

class VentanaCreaEditaModelo():
    def __init__(self, accion, bbdd):
        self.accion = accion
        self.rootAux = ctk.CTkToplevel()                #crea ventana auxiliar
        self.rootAux.attributes('-topmost', True)       #posiciona al frente de la pantalla
        self.rootAux.title("Programación de Planta")    #coloca titulo de ventana
        self.rootAux.geometry("385x480")                #dimensiones
        self.rootAux.resizable(False, False)            #deshabilita la redimension

        self.frameTitulo = ctk.CTkFrame(self.rootAux)
        self.frameTitulo.pack(expand=True, side="top", fill="both")
        self.frameEntradas = ctk.CTkFrame(self.rootAux)
        self.frameEntradas.pack(expand=True, side="bottom", fill="both", pady=10)

        self.defineAccionyEstilo()  # Determinar el título y el color

        # Variables objeto para los entry
        self.varMarca = ctk.StringVar()
        self.varModelo = ctk.StringVar()

        # LABEL PARA TITULO Y CAMPOS
        self.titulo = self.accion
        self.labelTitulo = ctk.CTkLabel(self.frameTitulo, text=self.titulo + " MODELO", font=textoGrande, text_color=self.colorfuenteLabel)
        self.labelTitulo.pack(expand=True, side="top", fill="x", padx=20, pady=20)

        self.labelMarca = ctk.CTkLabel(self.frameEntradas, text="MARCA", font=texto1Bajo, text_color=self.colorfuenteLabel,  anchor="w")
        self.labelMarca.grid(row=0, column=0, sticky="ew", padx=20, pady=5)

        self.labelModelo = ctk.CTkLabel(self.frameEntradas, text="MODELO", font=texto1Bajo, text_color=self.colorfuenteLabel,  anchor="w")
        self.labelModelo.grid(row=1, column=0, sticky="ew", padx=20, pady=5)

        # ENTRY PARA CAMPOS
        self.entryMarca = ctk.CTkEntry(self.frameEntradas, font=numerosMedianos, textvariable=self.varMarca)
        self.entryModelo = ctk.CTkEntry(self.frameEntradas, font=numerosMedianos, textvariable=self.varModelo)

        self.entryMarca.grid(row=0, column=1, sticky="ew", pady=5, padx=20)
        self.entryModelo.grid(row=1, column=1, sticky="ew", pady=5, padx=20)

        self.construyeCamposProcesos(bbdd)  # Crear campos para los procesos

        # BOTONES DE GUARDAR Y CANCELAR
        self.buttonCancelar = ctk.CTkButton(self.frameEntradas, text="Cancelar", font=texto1Bajo, fg_color=grisAzuladoMedio, text_color=blancoHueso)
        self.buttonGuardar = ctk.CTkButton(self.frameEntradas, text="Guardar", font=textoGrande, fg_color=azulMedio, text_color=blancoFrio)

        self.buttonCancelar.grid(row=self.num + 3, column=0, padx=22, pady=10)
        self.buttonGuardar.grid(row=self.num + 3, column=1, padx=22, pady=10)

    def defineAccionyEstilo(self):
        if self.accion == "EDITAR":
            self.colorfuenteLabel = blancoFrio
        elif self.accion == "CREAR":
            self.colorfuenteLabel = blancoFrio

    def construyeCamposProcesos(self, bbdd):
        self.procesos = BBDD.leer_procesos(bbdd)  # leer BD para obtener una lista con los procesos
        self.num = 0

        self.frameEntradas.grid_columnconfigure(0, weight=1)  # Columna para labels
        self.frameEntradas.grid_columnconfigure(1, weight=1)  # Columna para entrys
        
        for proceso in self.procesos:
            self.num += 1
            self.name = f"proceso{proceso}"  # Clave del diccionario con stringVars
            glo.strVar_nuevosTiemposMod[self.name] = ctk.StringVar()

            # LABELS CON LOS NOMBRES DE PROCESOS
            glo.lbl_nuevosTiemposMod[self.name] = ctk.CTkLabel(self.frameEntradas, text=f"Tiempo {proceso}", font=texto1Bajo, text_color=self.colorfuenteLabel,
                                                           anchor="w", width=12)
            glo.lbl_nuevosTiemposMod[self.name].grid(row=2 + self.num, column=0, sticky="ew", padx=20, pady=5)

            # ENTRY PARA TIEMPOS DE PROCESO
            glo.ent_nuevosTiemposMod[self.name] = ctk.CTkEntry(self.frameEntradas, font=numerosMedianos, textvariable=glo.strVar_nuevosTiemposMod[self.name], width=12)
            glo.ent_nuevosTiemposMod[self.name].grid(row=2 + self.num, column=1, sticky="ew", padx=20 , pady=5)

    def set_values(self, datos):
        
        self.varMarca.set(datos["marca"])
        self.varModelo.set(datos["modelo"])

        for clave in datos:
            clave_modificada = "proceso" + clave
            if clave_modificada in glo.strVar_nuevosTiemposMod:
                glo.strVar_nuevosTiemposMod[clave_modificada].set(datos[clave])

    def asignafuncion(self, funcionGuardar, funcionCancelar):
        self.buttonGuardar.configure(command=funcionGuardar)
        self.buttonCancelar.configure(command=funcionCancelar)
        self.rootAux.mainloop()

class VentanaGestionaVehiculos():
    def __init__(self, accion, bbdd):
        self.accion = accion
        self.rootAux = ctk.CTkToplevel()                #crea ventana auxiliar
        self.rootAux.attributes('-topmost', True)       #posiciona al frente de la pantalla
        self.rootAux.title("Programación de Planta")    #coloca titulo de ventana
        self.rootAux.geometry("400x700")                #dimensiones
        self.rootAux.resizable(False, False)            #deshabilita la redimension
        self.procesos = BBDD.leer_procesos(bbdd)  # leer BD para obtener una lista con los procesos

        self.frameTitulo = ctk.CTkFrame(self.rootAux, fg_color=grisAzuladoMedio, height=10)
        self.frameTitulo.pack(expand=True, side="top", fill = "both")
        self.frameEntradas = ctk.CTkFrame(self.rootAux, fg_color=grisAzuladoMedio)
        self.frameEntradas.pack(expand=True, side="bottom", fill="both")

        self.varChasis = tk.StringVar() 
        self.varFecha = tk.StringVar() 
        self.varMarca = tk.StringVar()
        self.varModelo = tk.StringVar() 
        self.varColor = tk.StringVar() 
        self.varEstado = tk.StringVar() 


        self.varNoved = tk.StringVar()
        self.varSubcon = tk.StringVar() 
        self.varPedido = tk.StringVar() 

        self.defineAccionyEstilo()

        #LABEL PARA TITULO Y CAMPOS
        self.titulo = self.accion
        self.labelTitulo   = ctk.CTkLabel(self.frameTitulo, text = self.titulo + " VEHICULO", font = textoGrande)
        self.labelTitulo.pack(expand=True, side="top", fill="x", padx=20, pady=5)


        self.labelChasis   = ctk.CTkLabel(self.frameEntradas, text = "CHASIS", font = texto1Bajo, anchor="w")
        self.labelChasis.grid(row=0,column=0, sticky="ew", padx=20, pady=5)
        self.entryChasis = ctk.CTkEntry  (self.frameEntradas, font = numerosMedianos, width=12, textvariable=self.varChasis) 
        self.entryChasis.grid(row=0 ,column=1, sticky="ew", padx=20 , pady=5)

        self.labelFecha    = ctk.CTkLabel(self.frameEntradas, text = "FECHA ENTREGA", font = texto1Bajo, anchor="w")
        self.labelFecha.grid(row=1,column=0, sticky="ew", padx=20, pady=5)
        self.entryFecha = ctk.CTkEntry   (self.frameEntradas, font = numerosMedianos, width=12, textvariable=self.varFecha)
        self.entryFecha.grid (row=1 ,column=1, sticky="ew", padx=20 , pady=5)

        self.labelMarca    = ctk.CTkLabel(self.frameEntradas, text = "MARCA", font = texto1Bajo, anchor="w")
        self.labelMarca.grid(row=2,column=0, sticky="ew", padx=20, pady=5)
        self.entryMarca = ctk.CTkEntry   (self.frameEntradas, font = numerosMedianos, width=12, textvariable=self.varMarca)
        self.entryMarca.grid (row=2 ,column=1, sticky="ew", padx=20 , pady=5)

        self.labelModelo   = ctk.CTkLabel(self.frameEntradas, text = "MODELO", font = texto1Bajo, anchor="w")
        self.labelModelo.grid(row=3,column=0, sticky="ew", padx=20, pady=5)
        self.entryModelo = ctk.CTkEntry  (self.frameEntradas, font = numerosMedianos, width=12, textvariable=self.varModelo)
        self.entryModelo.grid(row=3 ,column=1, sticky="ew", padx=20 , pady=5)

        self.labelColor  = ctk.CTkLabel(self.frameEntradas, text = "COLOR", font = texto1Bajo, anchor="w")
        self.labelColor.grid(row=4,column=0, sticky="ew", padx=20, pady=5)
        self.entryColor = ctk.CTkEntry   (self.frameEntradas, font = numerosMedianos, width=12, textvariable=self.varColor)
        self.entryColor.grid (row=4 ,column=1, sticky="ew", padx=20 , pady=5)

        self.labelEstado  = ctk.CTkLabel(self.frameEntradas, text = "ESTADO", font = texto1Bajo, anchor="w")
        self.labelEstado.grid(row=5,column=0, sticky="ew", padx=20, pady=5)
        self.entryEstado = ctk.CTkEntry  (self.frameEntradas, font = numerosMedianos, width=12, textvariable=self.varEstado)
        self.entryEstado.grid(row=5 ,column=1, sticky="ew", padx=20 , pady=5)

        self.construyeCamposProcesos(bbdd)

        self.labelNoved  = ctk.CTkLabel(self.frameEntradas, text = "NOVEDADES", font = texto1Bajo, anchor="w")
        self.labelNoved.grid(row=len(self.procesos)+7, column=0, sticky="ew", padx=20, pady=5)
        self.entryNoved = ctk.CTkEntry   (self.frameEntradas, font = numerosMedianos, width=12, textvariable=self.varNoved)
        self.entryNoved.grid (row=len(self.procesos)+7, column=1, sticky="ew", padx=20 , pady=5)

        self.labelSubcon  = ctk.CTkLabel(self.frameEntradas, text = "SUBCONTRATAR", font = texto1Bajo, anchor="w")
        self.labelSubcon.grid(row=len(self.procesos)+8,column=0, sticky="ew", padx=20, pady=5)
        self.entrySubcon = ctk.CTkEntry  (self.frameEntradas, font = numerosMedianos, width=12, textvariable=self.varSubcon)
        self.entrySubcon.grid(row=len(self.procesos)+8,column=1, sticky="ew", padx=20 , pady=5)

        self.labelPedido  = ctk.CTkLabel(self.frameEntradas, text = "ID_PEDIDO", font = texto1Bajo, anchor="w")
        self.labelPedido.grid(row=len(self.procesos)+9,column=0, sticky="ew", padx=20, pady=5)
        self.entryPedido = ctk.CTkEntry  (self.frameEntradas, font = numerosMedianos, width=12, textvariable=self.varPedido)
        self.entryPedido.grid(row=len(self.procesos)+9,column=1, sticky="ew", padx=20 , pady=5)


        self.buttonCancelar = ctk.CTkButton(self.frameEntradas,text="Cancelar", font=texto1Bajo, bg_color=grisAzuladoOscuro, command="")   
        self.buttonCancelar.grid(row=len(self.procesos)+10, column=0, padx=22, pady=10)

        if self.accion == "AGREGAR":
            self.buttonAgregar = ctk.CTkButton(self.frameEntradas,text="Agregar", font=textoGrande, bg_color=azulMedio, command="")    
            self.buttonAgregar.grid(row=len(self.procesos)+10, column=1, padx=22, pady=10)

        if self.accion == "MODIFICAR":
            self.buttonAgregar = ctk.CTkButton(self.frameEntradas,text="Reemplazar", font=textoGrande, bg_color=azulMedio, command="")    
            self.buttonAgregar.grid(row=len(self.procesos)+10, column=1, padx=22, pady=10)            

    def defineAccionyEstilo(self):
        if self.accion == "AGREGAR":
            self.colorfuenteLabel = blancoFrio
        elif self.accion == "MODIFICAR":
            self.colorfuenteLabel = blancoFrio

    def construyeCamposProcesos(self, bbdd):

        self.num = 0

        self.frameEntradas.grid_columnconfigure(0, weight=1)  # Columna para labels
        self.frameEntradas.grid_columnconfigure(1, weight=1)  # Columna para entrys
        
        for proceso in self.procesos:
            self.num += 1
            self.name = f"proceso{proceso}"  # Clave del diccionario con stringVars
            glo.strVar_nuevosTiemposVeh[self.name] = ctk.StringVar()

            # LABELS CON LOS NOMBRES DE PROCESOS
            glo.lbl_nuevosTiemposVeh[self.name] = ctk.CTkLabel(self.frameEntradas, text=f"Tiempo {proceso}", font=texto1Bajo, text_color=self.colorfuenteLabel,
                                                           anchor="w", width=12)
            glo.lbl_nuevosTiemposVeh[self.name].grid(row=6 + self.num, column=0, sticky="ew", padx=20, pady=5)

            # ENTRY PARA TIEMPOS DE PROCESO
            glo.ent_nuevosTiemposVeh[self.name] = ctk.CTkEntry(self.frameEntradas, font=numerosMedianos, textvariable=glo.strVar_nuevosTiemposVeh[self.name], width=12)
            glo.ent_nuevosTiemposVeh[self.name].grid(row=6 + self.num, column=1, sticky="ew", padx=20 , pady=5)

    def set_values(self, datos, tiempos, accion):

        if accion == "AGREGAR":
            self.varMarca.set(datos["marca"])
            self.varModelo.set(datos["modelo"]) 

            print(datos)
            for clave in datos:
                clave_modificada = "proceso" + clave
                if clave_modificada in glo.strVar_nuevosTiemposMod:
                    glo.strVar_nuevosTiemposVeh[clave_modificada].set(datos[clave])


        if accion == "MODIFICAR":
            self.varChasis.set(datos[0])
            self.varFecha.set(datos[1])
            self.varMarca.set(datos[2])
            self.varModelo.set(datos[3])
            self.varColor.set(datos[4])
            self.varEstado.set(datos[5])
            self.varNoved.set(datos[6])
            self.varSubcon.set(datos[7])
            self.varPedido.set(datos[8])

            for clave, valor in zip(glo.strVar_nuevosTiemposMod, tiempos):
                print("Los valores de tiempos en el modulo ventana_auxiliares son: ", valor[1])
                glo.strVar_nuevosTiemposVeh[clave].set(valor[1])
    
    def asignafuncion(self, funcionAgregar, funcionCancelar):
        #Método para asignar la función al command button de guardar y cancelar desde otro módulo.
        self.buttonAgregar.configure(command = funcionAgregar)
        self.buttonCancelar.configure(command = funcionCancelar)

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
        top = ctk.CTkToplevel(self.rootAux)
        top.title("Seleccionar Fecha")
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

class VentanaAsignaVehiculo():
    
    def __init__(self, chasis, bbdd):
        self.rootAux = ctk.CTkToplevel()                #crea ventana auxiliar
        self.rootAux.title("Programación de Planta")    #coloca titulo de ventana
        self.rootAux.geometry("385x420")                #dimensiones
        self.rootAux.resizable(False, False)            #deshabilita la redimension

        self.frameTitulo = ctk.CTkFrame(self.rootAux)
        self.frameTitulo.pack(expand=True, side="top", fill="both")
        self.frameEntradas = ctk.CTkFrame(self.rootAux)
        self.frameEntradas.pack(expand=True, side="bottom", fill="both", pady=10)

        self.vehiculo = chasis
        self.labelTitulo = ctk.CTkLabel(self.frameTitulo, text="ASIGNAR  " + chasis, font=textoGrande)
        self.labelTitulo.pack(expand=True, side="top", fill="x", padx=20, pady=20)

        self.varTecnico = tk.StringVar() 
        self.varProceso = tk.StringVar()
        self.varFecha   = tk.StringVar() 
        self.varHora    = tk.StringVar()
        self.varObser   = tk.StringVar()
        self.varEstado   = tk.StringVar()

        self.labelTecnico = ctk.CTkLabel(self.frameEntradas, text="TECNICO", font=texto1Bajo,  anchor="w")
        self.labelTecnico.grid(row=0, column=0, sticky="ew", padx=20, pady=5)
        self.labelProceso = ctk.CTkLabel(self.frameEntradas, text="PROCESO", font=texto1Bajo,  anchor="w")
        self.labelProceso.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
        self.labelFecha = ctk.CTkLabel(self.frameEntradas, text="FECHA", font=texto1Bajo,  anchor="w")
        self.labelFecha.grid(row=2, column=0, sticky="ew", padx=20, pady=5)
        self.labelHora = ctk.CTkLabel(self.frameEntradas, text="HORA", font=texto1Bajo,  anchor="w")
        self.labelHora.grid(row=3, column=0, sticky="ew", padx=20, pady=5)
        self.labelObser = ctk.CTkLabel(self.frameEntradas, text="OBSERVACIONES", font=texto1Bajo,  anchor="w")
        self.labelObser.grid(row=4, column=0, sticky="ew", padx=20, pady=5)
        self.labelEstado = ctk.CTkLabel(self.frameEntradas, text="ESTADO", font=texto1Bajo,  anchor="w")
        self.labelEstado.grid(row=5, column=0, sticky="ew", padx=20, pady=5)

        self.entryTecnico = ctk.CTkOptionMenu (self.frameEntradas, font = numerosMedianos, fg_color= grisAzuladoClaro, width=20, variable=self.varTecnico)
        self.entryProceso = ctk.CTkOptionMenu (self.frameEntradas, font = numerosMedianos, fg_color = grisAzuladoClaro, width=20, variable=self.varProceso) 
        self.entryFecha   = ctk.CTkEntry      (self.frameEntradas, font = numerosMedianos, fg_color = grisAzuladoClaro, width=20, textvariable=self.varFecha) 
        self.entryHora    = ctk.CTkEntry      (self.frameEntradas, font = numerosMedianos, fg_color = grisAzuladoClaro, width=20, textvariable=self.varHora,
                                                validate='focusout', validatecommand=(self.rootAux.register(self.validar_hora), '%P'))  # %P es el valor propuesto
        self.entryObser   = ctk.CTkEntry      (self.frameEntradas, font = numerosMedianos, fg_color = grisAzuladoClaro, width=20, textvariable=self.varObser)
        self.entryEstado  = ctk.CTkOptionMenu (self.frameEntradas, font = numerosMedianos, fg_color= grisAzuladoClaro, width=20, variable=self.varEstado)


        self.entryTecnico.grid(row=0 ,column=1, sticky="ew", pady=5)
        self.entryProceso.grid(row=1 ,column=1, sticky="ew", pady=5)        
        self.entryFecha.grid  (row=2 ,column=1, sticky="ew", pady=5)
        self.entryHora.grid   (row=3 ,column=1, sticky="ew", pady=5)
        self.entryObser.grid  (row=4 ,column=1, sticky="ew", pady=5)
        self.entryEstado.grid  (row=5 ,column=1, sticky="ew", pady=5)        

        self.entryFecha.bind("<Button-1>", self.mostrar_calendario)
        self.entryHora.bind("<Button-1>", self.seleccionar_hora)

        self.buttonCancelar = ctk.CTkButton(self.frameEntradas, text="Cancelar", font = texto1Bajo,  fg_color = naranjaMedio,  command="")   
        self.buttonAceptar  = ctk.CTkButton(self.frameEntradas, text="Aceptar",  font = textoGrande, fg_color = azulMedio,  command="")
        self.buttonCancelar.grid(row=6, column=0, padx=22, pady=15)  
        self.buttonAceptar.grid(row=6, column=1, padx=22, pady=15)

        self.tecnicos = BBDD.leer_tecnicos_modificado(bbdd)
        self.procesos = BBDD.leer_procesos_completo(bbdd)

        # Crear diccionarios con comprensión
        self.ids_tecnicos = {tecnico[1]: tecnico[0] for tecnico in self.tecnicos}
        self.ids_procesos = {proceso[1]: proceso[0] for proceso in self.procesos}

        # Configurar el OptionMenu con los valores del diccionario
        self.entryTecnico.configure(values=[""]+list(self.ids_tecnicos.keys()))
        self.entryProceso.configure(values=[""]+list(self.ids_procesos.keys()))
        self.entryEstado.configure(values=["PENDIENTE", "EN EJECUCIÓN", "TERMINADO"])
        # Establecer la cadena vacía como valor por defecto
        self.entryTecnico.set("")
        self.entryProceso.set("")
        self.entryEstado.set("EN EJECUCION")

        print(self.ids_tecnicos)
        print(self.ids_procesos)
        self.llenar_hora_actual()

    def mostrar_calendario(self, event):
        #Muestra un calendario para seleccionar la fecha
        top = ctk.CTkToplevel(self.rootAux)
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

        if re.fullmatch(r'([01]\d|2[0-3]):([0-5]\d):([0-5]\d)', valor_propuesto):   # utiliza una expresión regular para formatear la hora
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

class VentanaMuestraInfoVH():
    def __init__(self, bbdd, historicos, vehiculo):
        self.datosGenerales = historicos[0][1], vehiculo[1], vehiculo[2]
        self.datosEspecificos = [(tupla[3], tupla[8], tupla[2], tupla[5], tupla[6], tupla[7], tupla[4]) for tupla in historicos]

        print("datos generales es :", self.datosGenerales)
        print("datos específicos es :", self.datosEspecificos)

        # Configuración de la ventana auxiliar
        self.rootAux = ctk.CTkToplevel()                # Crea ventana auxiliar
        self.rootAux.attributes('-topmost', True)       # Posiciona al frente de la pantalla
        self.rootAux.title("Programación de Planta")    # Coloca título de ventana
        self.rootAux.geometry("600x420")                # Dimensiones

        # Configura el tema oscuro
        self.rootAux.configure(bg=grisAzuladoOscuro)            # Fondo oscuro
        ctk.set_appearance_mode("dark")                 # Establece el modo oscuro global

        # Frame para los datos generales
        self.frameDatosGenerales = ctk.CTkFrame(self.rootAux, fg_color=grisAzuladoOscuro)
        self.frameDatosGenerales.pack(expand=True, side="top", fill="both")

        # Etiqueta para datos generales
        self.labelDatosGenerales = ctk.CTkLabel(
            self.frameDatosGenerales,
            text="CHASIS:  " + self.datosGenerales[0] + "\n" + "MODELO-MARCA:  " + self.datosGenerales[2] + "\n" + "FECHA DE INGRESO:  " +self.datosGenerales[1],
            font=textoGrande,
            text_color=blancoHueso,  # Color del texto
            bg_color=grisAzuladoOscuro,   # Color de fondo de la etiqueta
            anchor ="w"
        )
        self.labelDatosGenerales.pack(expand=True, side="top", fill="x", padx=20, pady=20)

         #Crear estilo personalizado para las cabeceras y el cuerpo
        self.styletreeviewInfo = ttk.Style()
        self.styletreeviewInfo.configure("TreeviewInfoVehiculo.Heading", foreground=moradoMedio, font=texto1Bajo, background=grisAzuladoOscuro)
        self.styletreeviewInfo.configure("TreeviewInfoVehiculo", background=grisAzuladoOscuro, foreground=blancoFrio, fieldbackground=grisAzuladoOscuro)
        self.styletreeviewInfo.layout("TreeviewInfoVehiculo", [('Treeview.treearea', {'sticky': 'nswe'})])

        #Crear la treeview
        self.tree = ttk.Treeview(self.rootAux, columns=("ID_PROCESO", "ESTADO", "ID_TECNICO", "INICIO", "FIN", "DURACION", "OBSERVACION"), show='headings',  style="TreeviewInfoVehiculo")
        
        # Definir encabezados en un bucle
        self.encabezados = [
            ("ID_PROCESO", "Id_proceso"),
            ("ESTADO", "Estado"),
            ("ID_TECNICO", "Id_Tecnico"),
            ("INICIO", "Inicio"),
            ("FIN", "Fin"),
            ("DURACION", "Duracion"),
            ("OBSERVACION", "Observacion")
        ]

        for col, texto in self.encabezados:
            self.tree.heading(col, text=texto)
            self.tree.column(col, anchor="w", width=100)

        for registro in self.datosEspecificos:              # Insertar los registros en el Treeview
            self.tree.insert("", "end", values=registro)

        self.tree.pack(expand=True, fill="both")            # Agregar el Treeview a la ventana

        self.buttonCerrar = ctk.CTkButton(self.rootAux, text="Cerrar", font=textoMedio, fg_color=rojoClaro, text_color=moradoOscuro, hover_color=(moradoMedio, blancoFrio))
        self.buttonCerrar.pack(pady=10)

    def asignafuncionBoton(self, funcionCerrar):
        self.buttonCerrar.configure(command=funcionCerrar)
        self.rootAux.mainloop()

class VentanaMuestraInfoHis():
    
    def __init__(self, id_historico, bbdd):
        self.datos = BBDD.leer_historico_completo_porId(bbdd,id_historico)
        print("datos:", self.datos)

        # Configuración de la ventana auxiliar
        self.rootAux = ctk.CTkToplevel()                # Crea ventana auxiliar
        self.rootAux.attributes('-topmost', True)       # Posiciona al frente de la pantalla
        self.rootAux.title("Programación de Planta")    # Coloca título de ventana
        self.rootAux.geometry("400x600")                # Dimensiones

        # Configura el tema oscuro
        self.rootAux.configure(bg=grisAzuladoOscuro)    # Fondo oscuro
        ctk.set_appearance_mode("dark")                 # Establece el modo oscuro global

        self.labeltitulo = ctk.CTkLabel(self.rootAux, text="RESUMEN DE HISTÓRICO", font =textoMedio)
        self.labeltitulo.pack(expand=True, side="top", fill="both")

        # Frame para los datos generales
        self.frameDatos = ctk.CTkFrame(self.rootAux, fg_color = grisMedio)
        self.frameDatos.pack(expand=True, side="top", fill="both", padx  =15, pady=5)

        self.encabezados = [
                            ("ID", "id_proceso"),
                            ("CHASIS", "estado"),
                            ("TECNICO", "tecnico"),
                            ("PROCESO", "proceso"),
                            ("MARCA-MODELO", "modelo_marca"),
                            ("COLOR", "color"),
                            ("INICIO", "inicio"),
                            ("FIN","fin"),
                            ("DURACION","duracion"),
                            ("ESTADO","estado"),
                            ("NOVEDADES","novedades"),
                            ("SUBCONTRATAR","subcontratar"),
                            ("OBSERVACIONES","observaciones"),
                            ("PEDIDO","pedido")
                        ]

        fila = 0
        for titulo, item in zip(self.encabezados, self.datos):
            ctk.CTkLabel(self.frameDatos,
                         text = f"{titulo[0]} : ",
                         font=texto1Medio, 
                         text_color = blancoHueso,
                         anchor="w",
                         bg_color = grisMedio).grid(row = fila, column= 0,
                                                    padx=5, pady=1, sticky = "ew")
            ctk.CTkLabel(self.frameDatos,
                        text = item,
                        font=texto1Medio, 
                        text_color = blancoHueso,
                        anchor="w",
                        bg_color = grisMedio).grid(row = fila, column= 1,
                                                    padx=2, pady=2, sticky = "ew")
            fila+=1

        self.buttonCerrar = ctk.CTkButton(self.rootAux, text="Cerrar", font=textoMedio, fg_color=rojoClaro, text_color=grisOscuro, hover_color = rojoMedio)
        self.buttonCerrar.pack(pady=10)

    def asignafuncionBoton(self, funcionCerrar):

        self.buttonCerrar.configure(command=funcionCerrar)
        self.rootAux.mainloop()

class VentanaCambiarEstadoHist():
    
    def __init__(self, id_historico, bbdd):

        # Configuración de la ventana auxiliar
        self.rootAux = ctk.CTkToplevel()                # Crea ventana auxiliar
        self.rootAux.attributes('-topmost', True)       # Posiciona al frente de la pantalla
        self.rootAux.title("Programación de Planta")    # Coloca título de ventana
        self.rootAux.geometry("400x400")                # Dimensiones

        # Configura el tema oscuro
        self.rootAux.configure(bg=grisAzuladoOscuro)    # Fondo oscuro
        ctk.set_appearance_mode("dark")                 # Establece el modo oscuro global

        self.datos = BBDD.leer_historico_completo_porId(bbdd, id_historico)
        self.labeltitulo = ctk.CTkLabel(self.rootAux, text="CAMBIAR ESTADO", font =textoMedio)
        self.labeltitulo.pack(expand=True, side="top", fill="both")

        self.frameEntradas = ctk.CTkFrame(self.rootAux)
        self.frameEntradas.pack(expand=True, side="bottom", fill="both", pady=10)

        self.labelTecnico = ctk.CTkLabel(self.frameEntradas, text="TECNICO", font=texto1Medio,  anchor="w")
        self.labelTecnico.grid(row=0, column=0, sticky="ew", padx=20, pady=1)
        self.labelProceso = ctk.CTkLabel(self.frameEntradas, text="PROCESO", font=texto1Medio,  anchor="w")
        self.labelProceso.grid(row=1, column=0, sticky="ew", padx=20, pady=1)
        self.labelFechaInicio = ctk.CTkLabel(self.frameEntradas, text="FECHA INICIO", font=texto1Medio,  anchor="w")
        self.labelFechaInicio.grid(row=2, column=0, sticky="ew", padx=20, pady=1)
        self.labelHoraInicio = ctk.CTkLabel(self.frameEntradas, text="HORA INICIO", font=texto1Medio,  anchor="w")
        self.labelHoraInicio.grid(row=2, column=2, sticky="ew", padx=20, pady=1)
        self.labelFechaFin = ctk.CTkLabel(self.frameEntradas, text="FECHA FIN", font=texto1Medio,  anchor="w")
        self.labelFechaFin.grid(row=3, column=0, sticky="ew", padx=20, pady=1)
        self.labelHoraFin = ctk.CTkLabel(self.frameEntradas, text="HORA FIN", font=texto1Medio,  anchor="w")
        self.labelHoraFin.grid(row=3, column=2, sticky="ew", padx=20, pady=1)

        self.labelvalorTecnico = ctk.CTkLabel(self.frameEntradas, text=self.datos[2], font=texto1Medio,  anchor="w")
        self.labelvalorTecnico.grid(row=0, column=1, sticky="ew", padx=20, pady=1)
        self.labelvalorProceso = ctk.CTkLabel(self.frameEntradas, text=self.datos[3], font=texto1Medio,  anchor="w")
        self.labelvalorProceso.grid(row=1, column=1, sticky="ew", padx=20, pady=1)
        self.labelvalorFechaInicio = ctk.CTkLabel(self.frameEntradas, text=self.datos[6], font=texto1Medio,  anchor="w")
        self.labelvalorFechaInicio.grid(row=2, column=1, sticky="ew", padx=20, pady=1)
        self.labelvalorHoraInicio = ctk.CTkLabel(self.frameEntradas, text="HORA INICIO", font=texto1Medio,  anchor="w")
        self.labelvalorHoraInicio.grid(row=2, column=2, sticky="ew", padx=20, pady=1)
        self.labelvalorFechaFin = ctk.CTkLabel(self.frameEntradas, text=self.datos[2], font=texto1Medio,  anchor="w")
        self.labelvalorFechaFin.grid(row=3, column=0, sticky="ew", padx=20, pady=1)
        self.labelvalorHoraFin = ctk.CTkLabel(self.frameEntradas, text="HORA FIN", font=texto1Medio,  anchor="w")
        self.labelvalorHoraFin.grid(row=3, column=2, sticky="ew", padx=20, pady=1)


        self.varEstado   = tk.StringVar(value=self.datos[9])
        self.labelEstado = ctk.CTkLabel(self.frameEntradas, text="ESTADO", font=texto1Medio,  anchor="w")
        self.labelEstado.grid(row=5, column=0, sticky="ew", padx=20, pady=5)
        self.entryEstado  = ctk.CTkOptionMenu (self.frameEntradas, font = numerosMedianos, fg_color= grisAzuladoClaro, width=20, variable=self.varEstado)
        self.entryEstado.grid  (row=5 ,column=1, sticky="ew", pady=5)    

        self.entryEstado.configure(values=["PENDIENTE", "EN EJECUCIÓN", "TERMINADO"])

        self.buttonCancelar = ctk.CTkButton(self.frameEntradas,text="Cancelar", font=texto1Bajo, bg_color=rojoOscuro, command="")   
        self.buttonCancelar.grid(row=6, column=0, padx=22, pady=10)

        self.buttonAgregar = ctk.CTkButton(self.frameEntradas,text="Guardar", font=textoGrande, bg_color=naranjaMedio, command="")    
        self.buttonAgregar.grid(row=6, column=1, padx=22, pady=10)

    def asignafuncion(self, funcionAgregar, funcionCancelar):            #Método para asignar la función al command button de guardar y cancelar desde otro módulo.
        self.buttonAgregar.configure(command = funcionAgregar)
        self.buttonCancelar.configure(command = funcionCancelar)

class VentanaVistaPrevia():
    
    def __init__(self, nombreVentana, df, bbdd):

        self.rootAux = ctk.CTkToplevel()                # Crea ventana auxiliar
        self.rootAux.attributes('-topmost', True)       # Posiciona al frente de la pantalla
        self.rootAux.title("Programación de Planta")    # Coloca título de ventana
        self.rootAux.geometry("600x600")                # Dimensiones

        self.rootAux.configure(bg=grisAzuladoOscuro)    # Fondo oscuro
        ctk.set_appearance_mode("dark")                 # Establece el modo oscuro global

        self.nombreVentana = nombreVentana.upper()
        self.labeltitulo = ctk.CTkLabel(self.rootAux, text=f"{nombreVentana}\nvista previa", font =textoMedio)
        self.labeltitulo.pack(expand=True, side="top", fill="both")

        self.frameTreeview = ctk.CTkFrame(self.rootAux, fg_color=grisAzuladoOscuro)
        self.frameTreeview.pack(expand=True, side="top", fill="both")

        self.encabezados = list(df.columns)

         #Crear estilo personalizado para las cabeceras y el cuerpo
        self.styletreeviewInfo = ttk.Style()
        self.styletreeviewInfo.configure("TreeviewPreviaPedido.Heading", foreground=moradoMedio, font=texto1Bajo, background=grisAzuladoOscuro)
        self.styletreeviewInfo.configure("TreeviewPreviaPedido", background=grisAzuladoOscuro, foreground=blancoFrio, fieldbackground=grisAzuladoOscuro)
        self.styletreeviewInfo.layout("TreeviewPreviaPedido", [('Treeview.treearea', {'sticky': 'nswe'})])

        self.tree = ttk.Treeview(self.frameTreeview, columns=tuple(self.encabezados), show='headings',  style="TreeviewPreviaPedido")

        # Definir encabezados en un bucle
        self.encabezados = [(header, header) for header in self.encabezados]
      
        for col, texto in self.encabezados:
            self.tree.heading(col, text=texto)
            self.tree.column(col, anchor="w", width=100)

        for _, registro in df.iterrows():              # Insertar los registros en el Treeview
            self.tree.insert("", "end", values=list(registro))

        self.tree.pack(expand=True, side = "top", fill="both")            # Agregar el Treeview a la ventana

        self.frameBotones = ctk.CTkFrame(self.rootAux, fg_color=grisAzuladoOscuro)
        self.frameBotones.pack(expand=True, side="bottom", fill="both")

        self.buttonAceptar = ctk.CTkButton(self.frameBotones, text="Aceptar", font=textoMedio, fg_color=rojoClaro, text_color=moradoOscuro, hover_color=(moradoMedio, blancoFrio))
        self.buttonAceptar.grid(row=0 ,column=0, sticky="ew", pady=5)
        self.buttonCancelar = ctk.CTkButton(self.frameBotones, text="Cancelar", font=textoMedio, fg_color=rojoClaro, text_color=moradoOscuro, hover_color=(moradoMedio, blancoFrio))
        self.buttonCancelar.grid(row=0 ,column=1, sticky="ew", pady=5, padx = 20)

    def asignafuncion(self, funcionAceptar, funcionCancelar):               #Método para asignar la función al command button de aceptar y cancelar desde otro módulo.
        self.buttonAceptar.configure(command = funcionAceptar)
        self.buttonCancelar.configure(command = funcionCancelar)

class VentanaVistaPreviaPedido():
        
    def __init__(self, df, bbdd):

        # Configuración de la ventana auxiliar
        self.rootAux = ctk.CTkToplevel()                # Crea ventana auxiliar
        self.rootAux.attributes('-topmost', True)       # Posiciona al frente de la pantalla
        self.rootAux.title("Programación de Planta")    # Coloca título de ventana
        self.rootAux.geometry("400x600")                # Dimensiones

        # Configura el tema oscuro
        self.rootAux.configure(bg=grisAzuladoOscuro)    # Fondo oscuro
        ctk.set_appearance_mode("dark")                 # Establece el modo oscuro global

        self.labeltitulo = ctk.CTkLabel(self.rootAux, text=f"VEHICULOS DE PEDIDO\nvista previa", font =textoMedio)
        self.labeltitulo.pack(expand=True, side="top", fill="both")

        # Frame para los datos generales
        self.frameEntradas = ctk.CTkFrame(self.rootAux, fg_color=grisAzuladoOscuro)
        self.frameEntradas.pack(expand=True, side="top", fill="both")

        self.frameEntradas.grid_columnconfigure(0, weight=1)
        self.frameEntradas.grid_columnconfigure(1, weight=1)

        self.varNombre = tk.StringVar()
        self.labelNombre    = ctk.CTkLabel(self.frameEntradas, text = "NOMBRE", font = texto1Bajo, anchor="w")
        self.labelNombre.grid(row=0,column=0, sticky="ew", padx=20, pady=5)
        self.entryNombre = ctk.CTkEntry   (self.frameEntradas, font = numerosMedianos, width=12, textvariable=self.varNombre)
        self.entryNombre.grid (row=0 ,column=1, sticky="ew", padx=20 , pady=5)

        self.varCliente = tk.StringVar()
        self.labelCliente    = ctk.CTkLabel(self.frameEntradas, text = "DEPENDENCIA/CLIENTE", font = texto1Bajo, anchor="w")
        self.labelCliente.grid(row=1,column=0, sticky="ew", padx=20, pady=5)
        self.entryCliente = ctk.CTkEntry   (self.frameEntradas, font = numerosMedianos, width=12, textvariable=self.varCliente)
        self.entryCliente.grid (row=1 ,column=1, sticky="ew", padx=20 , pady=5)

        self.varFecha_recepcion = tk.StringVar() 
        self.labelFecha_recepcion    = ctk.CTkLabel(self.frameEntradas, text = "FECHA RECEPCION", font = texto1Bajo, anchor="w")
        self.labelFecha_recepcion.grid(row=2,column=0, sticky="ew", padx=20, pady=5)
        self.entryFecha_recepcion = ctk.CTkEntry   (self.frameEntradas, font = numerosMedianos, width=12, textvariable=self.varFecha_recepcion)
        self.entryFecha_recepcion.grid (row=2 ,column=1, sticky="ew", padx=20 , pady=5)
        self.entryFecha_recepcion.bind("<Button-1>", lambda event: self.mostrar_calendario(self.varFecha_recepcion))

        self.varFecha_ingreso = tk.StringVar() 
        self.labelFecha_ingreso    = ctk.CTkLabel(self.frameEntradas, text = "FECHA INGRESO", font = texto1Bajo, anchor="w")
        self.labelFecha_ingreso.grid(row=3,column=0, sticky="ew", padx=20, pady=5)
        self.entryFecha_ingreso = ctk.CTkEntry   (self.frameEntradas, font = numerosMedianos, width=12, textvariable=self.varFecha_ingreso)
        self.entryFecha_ingreso.grid (row=3 ,column=1, sticky="ew", padx=20 , pady=5)
        self.entryFecha_ingreso.bind("<Button-1>", lambda event: self.mostrar_calendario(self.varFecha_ingreso))

        self.varFecha_estimada = tk.StringVar() 
        self.labelFecha_estimada    = ctk.CTkLabel(self.frameEntradas, text = "FECHA ESTIMADA", font = texto1Bajo, anchor="w")
        self.labelFecha_estimada.grid(row=4,column=0, sticky="ew", padx=20, pady=5)
        self.entryFecha_estimada = ctk.CTkEntry   (self.frameEntradas, font = numerosMedianos, width=12, textvariable=self.varFecha_estimada)
        self.entryFecha_estimada.grid (row=4 ,column=1, sticky="ew", padx=20 , pady=5)
        self.entryFecha_estimada.bind("<Button-1>", lambda event: self.mostrar_calendario(self.varFecha_estimada))

        self.varFecha_entrega = tk.StringVar() 
        self.labelFecha_entrega    = ctk.CTkLabel(self.frameEntradas, text = "FECHA ENTREGA", font = texto1Bajo, anchor="w")
        self.labelFecha_entrega.grid(row=5,column=0, sticky="ew", padx=20, pady=5)
        self.entryFecha_entrega = ctk.CTkEntry   (self.frameEntradas, font = numerosMedianos, width=12, textvariable=self.varFecha_entrega)
        self.entryFecha_entrega.grid (row=5 ,column=1, sticky="ew", padx=20 , pady=5)
        self.entryFecha_entrega.bind("<Button-1>", lambda event: self.mostrar_calendario(self.varFecha_entrega))

        # Frame para los datos generales
        self.frameTreeview = ctk.CTkFrame(self.rootAux, fg_color=grisAzuladoOscuro)
        self.frameTreeview.pack(expand=True, side="top", fill="both")

        self.encabezados = list(df.columns)

         #Crear estilo personalizado para las cabeceras y el cuerpo
        self.styletreeviewInfo = ttk.Style()
        self.styletreeviewInfo.configure("TreeviewPreviaPedido.Heading", foreground=moradoMedio, font=texto1Bajo, background=grisAzuladoOscuro)
        self.styletreeviewInfo.configure("TreeviewPreviaPedido", background=grisAzuladoOscuro, foreground=blancoFrio, fieldbackground=grisAzuladoOscuro)
        self.styletreeviewInfo.layout("TreeviewPreviaPedido", [('Treeview.treearea', {'sticky': 'nswe'})])

        self.tree = ttk.Treeview(self.frameTreeview, columns=tuple(self.encabezados), show='headings',  style="TreeviewPreviaPedido")

        # Definir encabezados en un bucle
        self.encabezados = [(header, header) for header in self.encabezados]
      
        for col, texto in self.encabezados:
            self.tree.heading(col, text=texto)
            self.tree.column(col, anchor="w", width=100)

        for _, registro in df.iterrows():              # Insertar los registros en el Treeview
            self.tree.insert("", "end", values=list(registro))

        self.tree.pack(expand=True, side = "top", fill="both")            # Agregar el Treeview a la ventana

        self.frameBotones = ctk.CTkFrame(self.rootAux, fg_color=grisAzuladoOscuro)
        self.frameBotones.pack(expand=True, side="bottom", fill="both")

        self.buttonAceptar = ctk.CTkButton(self.frameBotones, text="Aceptar", font=textoMedio, fg_color=rojoClaro, text_color=moradoOscuro, hover_color=(moradoMedio, blancoFrio))
        self.buttonAceptar.grid(row=0 ,column=0, sticky="ew", pady=5)
        self.buttonCancelar = ctk.CTkButton(self.frameBotones, text="Cancelar", font=textoMedio, fg_color=rojoClaro, text_color=moradoOscuro, hover_color=(moradoMedio, blancoFrio))
        self.buttonCancelar.grid(row=0 ,column=1, sticky="ew", pady=5)

        glo.strVar_newPedido['nombre'] = self.varNombre
        glo.strVar_newPedido['cliente'] = self.varCliente
        glo.strVar_newPedido['fecha_recepcion'] = self.varFecha_recepcion
        glo.strVar_newPedido['fecha_ingreso'] = self.varFecha_entrega
        glo.strVar_newPedido['fecha_estimada'] = self.varFecha_estimada
        glo.strVar_newPedido['fecha_entrega'] = self.varFecha_entrega

    def mostrar_calendario(self, varEntry):
        #Muestra un calendario para seleccionar la fecha
        top = ctk.CTkToplevel(self.rootAux)
        top.title("Seleccionar Fecha")
        top.grab_set()
        top.lift()  # Eleva la ventana Toplevel para que esté al frente
        top.attributes('-topmost', 1)  # También puede asegurar que quede al frente

        cal = Calendar(top, selectmode='day', date_pattern="yyyy-mm-dd")
        cal.pack(pady=20)

        def seleccion_fecha(varEntry):
            varEntry.set(cal.get_date())
            top.destroy()

        btnSeleccionar = tk.Button(top, text="Seleccionar", command = lambda : seleccion_fecha(varEntry))
        btnSeleccionar.pack()

    def asignafuncion(self, funcionAceptar, funcionCancelar):               #Método para asignar la función al command button de aceptar y cancelar desde otro módulo.
        self.buttonAceptar.configure(command = funcionAceptar)
        self.buttonCancelar.configure(command = funcionCancelar)

class VentanaVistaPreviaReferencias():
    
    def __init__(self, df, bbdd):

        # Configuración de la ventana auxiliar
        self.rootAux = ctk.CTkToplevel()                # Crea ventana auxiliar
        self.rootAux.attributes('-topmost', True)       # Posiciona al frente de la pantalla
        self.rootAux.title("Programación de Planta")    # Coloca título de ventana
        self.rootAux.geometry("400x600")                # Dimensiones

        # Configura el tema oscuro
        self.rootAux.configure(bg=grisAzuladoOscuro)    # Fondo oscuro
        ctk.set_appearance_mode("dark")                 # Establece el modo oscuro global

        self.labeltitulo = ctk.CTkLabel(self.rootAux, text=f"REFERENCIAS DE VEHICULOS\nvista previa", font =textoMedio)
        self.labeltitulo.pack(expand=True, side="top", fill="both")


        # Frame para los datos generales
        self.frameOption = ctk.CTkFrame(self.rootAux, fg_color=grisAzuladoOscuro)
        self.frameOption.pack(side="top", fill="both")

        # Configurar peso de las columnas del frame para que se expandan equitativamente
        self.frameOption.grid_columnconfigure(0, weight=1)
        self.frameOption.grid_columnconfigure(1, weight=1)

        # Frame para los datos generales
        self.frameTreeview = ctk.CTkFrame(self.rootAux, fg_color=grisAzuladoOscuro)
        self.frameTreeview.pack(expand=True, side="top", fill="both")

        self.varColumna1 = tk.StringVar()
        self.optionNombreColumna=ctk.CTkOptionMenu(self.frameOption, font = numerosMedianos, fg_color= grisAzuladoClaro, width=20, variable=self.varColumna1)
        self.optionNombreColumna.grid(row=0 ,column=0, sticky="ew", pady=5)
        self.fila = ["REFERENCIA", "MODELO"]
        self.optionNombreColumna.configure(values=self.fila)      # Configurar el OptionMenu con los valores del diccionario
        self.optionNombreColumna.set("REFERENCIA")

        self.varColumna2 = tk.StringVar()
        self.optionNombreColumna=ctk.CTkOptionMenu(self.frameOption, font = numerosMedianos, fg_color= grisAzuladoClaro, width=20, variable=self.varColumna2)
        self.optionNombreColumna.grid(row=0 ,column=1, sticky="ew", pady=5)
        self.fila = ["REFERENCIA", "MODELO"]
        self.optionNombreColumna.configure(values=self.fila)      # Configurar el OptionMenu con los valores del diccionario
        self.optionNombreColumna.set("MODELO")

        self.encabezados = list(df.columns)

         #Crear estilo personalizado para las cabeceras y el cuerpo
        self.styletreeviewInfo = ttk.Style()
        self.styletreeviewInfo.configure("TreeviewPreviaPedido.Heading", foreground=moradoMedio, font=texto1Bajo, background=grisAzuladoOscuro)
        self.styletreeviewInfo.configure("TreeviewPreviaPedido", background=grisAzuladoOscuro, foreground=blancoFrio, fieldbackground=grisAzuladoOscuro)
        self.styletreeviewInfo.layout("TreeviewPreviaPedido", [('Treeview.treearea', {'sticky': 'nswe'})])

        self.tree = ttk.Treeview(self.frameTreeview, columns=tuple(self.encabezados), show='headings',  style="TreeviewPreviaPedido")

        # Definir encabezados en un bucle
        self.encabezados = [(header, header) for header in self.encabezados]
      
        for col, texto in self.encabezados:
            self.tree.heading(col, text=texto)
            self.tree.column(col, anchor="w", width=100)

        for _, registro in df.iterrows():              # Insertar los registros en el Treeview
            self.tree.insert("", "end", values=list(registro))

        self.tree.pack(expand=True, side = "top", fill="both")            # Agregar el Treeview a la ventana

        self.frameBotones = ctk.CTkFrame(self.rootAux, fg_color=grisAzuladoOscuro)
        self.frameBotones.pack(expand=True, side="bottom", fill="both")

        self.buttonAceptar = ctk.CTkButton(self.frameBotones, text="Aceptar", font=textoMedio, fg_color=rojoClaro, text_color=moradoOscuro, hover_color=(moradoMedio, blancoFrio))
        self.buttonAceptar.grid(row=0 ,column=0, sticky="ew", pady=5)
        self.buttonCancelar = ctk.CTkButton(self.frameBotones, text="Cancelar", font=textoMedio, fg_color=rojoClaro, text_color=moradoOscuro, hover_color=(moradoMedio, blancoFrio))
        self.buttonCancelar.grid(row=0 ,column=1, sticky="ew", pady=5, padx = 20)

    def asignafuncion(self, funcionAceptar, funcionCancelar):               #Método para asignar la función al command button de aceptar y cancelar desde otro módulo.
        
        self.buttonAceptar.configure(command = funcionAceptar)
        self.buttonCancelar.configure(command = funcionCancelar)

class VentanaAgregarReferencias():
    def __init__(self, referencias, bbdd):
        self.rootAux = ctk.CTkToplevel()                #crea ventana auxiliar
        self.rootAux.attributes('-topmost', True)       #posiciona al frente de la pantalla
        self.rootAux.title("Programación de Planta")    #coloca titulo de ventana
        self.rootAux.geometry("385x480")                #dimensiones

        self.frameTitulo = ctk.CTkFrame(self.rootAux)
        self.frameTitulo.pack(expand=True, side="top", fill="both")
        self.frameEntradas = ctk.CTkFrame(self.rootAux)
        self.frameEntradas.pack(expand=True, side="bottom", fill="both", pady=10)

        self.referencias = referencias["REFERENCIA"].to_list()
        self.dicReferencias = {}
        self.entReferencias = {}

        self.buttonCancelar = ctk.CTkButton(self.frameEntradas, text="Cancelar", font = texto1Medio,  fg_color = azulClaro, text_color = grisOscuro, hover_color = azulMedio, command="")   
        self.buttonAgregar  = ctk.CTkButton(self.frameEntradas, text="Agregar",  font = textoGrande, fg_color = naranjaClaro, text_color = grisOscuro, hover_color =  naranjaMedio, command="")    

        self.buttonCancelar.grid(row = len(referencias), column=0, padx=22, pady=10)
        self.buttonAgregar.grid (row = len(referencias), column=1, padx=22, pady=10)

    def construyeCamposReferencias(self, referencias, bbdd):

        self.num = 0
        self.frameEntradas.grid_columnconfigure(0, weight=1)  # Columna para labels
        self.frameEntradas.grid_columnconfigure(1, weight=1)  # Columna para entrys
        
        for referencia in referencias:
            self.num += 1
            self.name = f"{referencia}"  # Clave del diccionario con stringVars
            self.varReferencia[self.name] = ctk.StringVar()

            self.entReferencias[self.name] = ctk.CTkLabel(self.frameEntradas, text=f"{referencia}", font=texto1Bajo, text_color=self.colorfuenteLabel, anchor="w", width=12)
            self.entReferencias[self.name].grid(row=self.num, column=0, sticky="ew", padx=20, pady=5)

            self.entReferencias[self.name] = ctk.CTkEntry(self.frameEntradas, font=numerosMedianos, textvariable=glo.strVar_nuevosTiemposVeh[self.name], width=12)
            self.entReferencias[self.name].grid(row=self.num, column=1, sticky="ew", padx=20 , pady=5)

    def asignaFuncion(self, funcionAgregar, funcionCancelar):
        self.buttonAgregar.configure(command = funcionAgregar)
        self.buttonCancelar.configure(command = funcionCancelar)