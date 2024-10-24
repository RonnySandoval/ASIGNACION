import tkinter as tk
import customtkinter as ctk
from tkcalendar import Calendar
from tkinter import simpledialog
import time
from estilos import grisAzuladoClaro, grisAzuladoMedio, grisAzuladoOscuro, grisMedio, grisOscuro, textoGrande, naranjaOscuro, blancoFrio, amarilloClaro, amarilloMedio, azulOscuro, moradoOscuro, moradoClaro, texto1Bajo, numerosMedianos, naranjaMedio, blancoHueso, azulMedio, moradoMedio, amarilloOscuro, grisVerdeMedio
import datetime
import re
import glo
import BBDD


######################################################################################################
################################### VENTANA PARA AGREGAR Y EDITAR MODELOS ############################
######################################################################################################

class VentanaCreaEdita():
    def __init__(self, accion, bbdd):
        self.accion = accion
        self.rootAux = ctk.CTkToplevel()                #crea ventana auxiliar
        self.rootAux.attributes('-topmost', True)       #posiciona al frente de la pantalla
        self.rootAux.title("Programación de Planta")    #coloca titulo de ventana
        self.rootAux.geometry("385x420")                #dimensiones
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
        self.labelTitulo = ctk.CTkLabel(self.frameTitulo, text=self.titulo + " MODELO", font=textoGrande, text_color=self.colorfuenteLabel, )
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
        self.varMarca.set(datos[0])
        self.varModelo.set(datos[1])
        datos.pop(0)
        datos.pop(0)
        for clave, valor in zip(glo.strVar_nuevosTiemposMod, datos):
            glo.strVar_nuevosTiemposMod[clave].set(valor)

    def asignafuncionBoton(self, funcionGuardar, funcionCancelar):
        self.buttonGuardar.configure(command=funcionGuardar)
        self.buttonCancelar.configure(command=funcionCancelar)
        self.rootAux.mainloop()

###########################################################################################


###########################################################################################

class VentanaGestionaVehiculos():
    def __init__(self, accion, bbdd):
        self.accion = accion
        self.rootAux = ctk.CTkToplevel()                #crea ventana auxiliar
        self.rootAux.attributes('-topmost', True)       #posiciona al frente de la pantalla
        self.rootAux.title("Programación de Planta")    #coloca titulo de ventana
        self.rootAux.geometry("400x700")                #dimensiones
        self.rootAux.resizable(False, False)            #deshabilita la redimension

        self.frameTitulo = ctk.CTkFrame(self.rootAux, fg_color=grisAzuladoMedio, height=10)
        self.frameTitulo.pack(expand=True, side="top", fill = "both")
        self.frameEntradas = ctk.CTkFrame(self.rootAux, fg_color=grisAzuladoMedio)
        self.frameEntradas.pack(expand=True, side="bottom", fill="both")

        self.varChasis = tk.StringVar() 
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
        self.labelNoved.grid(row=12,column=0, sticky="ew", padx=20, pady=5)
        self.entryNoved = ctk.CTkEntry   (self.frameEntradas, font = numerosMedianos, width=12, textvariable=self.varNoved)
        self.entryNoved.grid (row=12,column=1, sticky="ew", padx=20 , pady=5)

        self.labelSubcon  = ctk.CTkLabel(self.frameEntradas, text = "SUBCONTRATAR", font = texto1Bajo, anchor="w")
        self.labelSubcon.grid(row=13,column=0, sticky="ew", padx=20, pady=5)
        self.entrySubcon = ctk.CTkEntry  (self.frameEntradas, font = numerosMedianos, width=12, textvariable=self.varSubcon)
        self.entrySubcon.grid(row=13,column=1, sticky="ew", padx=20 , pady=5)

        self.labelPedido  = ctk.CTkLabel(self.frameEntradas, text = "ID_PEDIDO", font = texto1Bajo, anchor="w")
        self.labelPedido.grid(row=14,column=0, sticky="ew", padx=20, pady=5)
        self.entryPedido = ctk.CTkEntry  (self.frameEntradas, font = numerosMedianos, width=12, textvariable=self.varPedido)
        self.entryPedido.grid(row=14,column=1, sticky="ew", padx=20 , pady=5)


        self.buttonCancelar = ctk.CTkButton(self.frameEntradas,text="Cancelar", font=texto1Bajo, bg_color=grisAzuladoOscuro, command="")   
        self.buttonCancelar.grid(row=15, column=0, padx=22, pady=10)

        if self.accion == "AGREGAR":
            self.buttonAgregar = ctk.CTkButton(self.frameEntradas,text="Agregar", font=textoGrande, bg_color=azulMedio, command="")    
            self.buttonAgregar.grid(row=15, column=1, padx=22, pady=10)

        if self.accion == "MODIFICAR":
            self.buttonAgregar = ctk.CTkButton(self.frameEntradas,text="Reemplazar", font=textoGrande, bg_color=azulMedio, command="")    
            self.buttonAgregar.grid(row=15, column=1, padx=22, pady=10)            


    
    def defineAccionyEstilo(self):
        if self.accion == "AGREGAR":
            self.colorfuenteLabel = blancoFrio
        elif self.accion == "MODIFICAR":
            self.colorfuenteLabel = blancoFrio


    def construyeCamposProcesos(self, bbdd):
    
        self.procesos = BBDD.leer_procesos(bbdd)  # leer BD para obtener una lista con los procesos
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
            self.varMarca.set(datos[0])
            self.varModelo.set(datos[1])
            datos.pop(0)
            datos.pop(0)
            print(datos)

            for clave, valor in zip(glo.strVar_nuevosTiemposMod, datos):
                print("Los valores de tiempos en el modulo ventana_auxiliares son: ", valor)
                glo.strVar_nuevosTiemposVeh[clave].set(valor)


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


    
    def asignafuncionBoton(self, funcionAgregar, funcionCancelar):
        #Método para asignar la función al command button de guardar y cancelar desde otro módulo.
        self.buttonAgregar.configure(command = funcionAgregar)
        self.buttonCancelar.configure(command = funcionCancelar)

        self.rootAux.mainloop()



#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################
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
    def __init__(self, vehiculo):
        self.rootAux = ctk.CTkToplevel()                #crea ventana auxiliar
        self.rootAux.title("Programación de Planta")    #coloca titulo de ventana
        self.rootAux.geometry("385x420")                #dimensiones
        self.rootAux.resizable(False, False)            #deshabilita la redimension

        self.frameTitulo = ctk.CTkFrame(self.rootAux)
        self.frameTitulo.pack(expand=True, side="top", fill="both")
        self.frameEntradas = ctk.CTkFrame(self.rootAux)
        self.frameEntradas.pack(expand=True, side="bottom", fill="both", pady=10)

        self.vehiculo = vehiculo
        self.labelTitulo = ctk.CTkLabel(self.frameTitulo, text="ASIGNAR  " + vehiculo, font=textoGrande)
        self.labelTitulo.pack(expand=True, side="top", fill="x", padx=20, pady=20)

        self.varTecnico = tk.StringVar() 
        self.varProceso = tk.StringVar()
        self.varFecha   = tk.StringVar() 
        self.varHora    = tk.StringVar()

        self.labelTecnico = ctk.CTkLabel(self.frameEntradas, text="TENICO", font=texto1Bajo,  anchor="w")
        self.labelTecnico.grid(row=0, column=0, sticky="ew", padx=20, pady=5)
        self.labelProceso = ctk.CTkLabel(self.frameEntradas, text="PROCESO", font=texto1Bajo,  anchor="w")
        self.labelProceso.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
        self.labelFecha = ctk.CTkLabel(self.frameEntradas, text="FECHA", font=texto1Bajo,  anchor="w")
        self.labelFecha.grid(row=2, column=0, sticky="ew", padx=20, pady=5)
        self.labelHora = ctk.CTkLabel(self.frameEntradas, text="HORA", font=texto1Bajo,  anchor="w")
        self.labelHora.grid(row=3, column=0, sticky="ew", padx=20, pady=5)

        self.entryTecnico = ctk.CTkOptionMenu(self.frameEntradas, font = numerosMedianos, fg_color= grisAzuladoClaro, width=20)
        self.entryProceso = ctk.CTkOptionMenu(self.frameEntradas, font = numerosMedianos, fg_color = grisAzuladoClaro, width=20) 
        self.entryFecha = ctk.CTkEntry       (self.frameEntradas, font = numerosMedianos, fg_color = grisAzuladoClaro, width=20, textvariable=self.varFecha) 
        self.entryHora = ctk.CTkEntry        (self.frameEntradas, font = numerosMedianos, fg_color = grisAzuladoClaro, width=20, textvariable=self.varHora,
                                                validate='focusout', validatecommand=(self.rootAux.register(self.validar_hora), '%P'))  # %P es el valor propuesto

        
        self.entryTecnico.grid (row=0 ,column=1, sticky="ew", pady=5)
        self.entryProceso.grid (row=1 ,column=1, sticky="ew", pady=5)        
        self.entryFecha.grid (row=2 ,column=1, sticky="ew", pady=5)
        self.entryHora.grid (row=3 ,column=1, sticky="ew", pady=5)

        self.entryFecha.bind("<Button-1>", self.mostrar_calendario)
        self.entryHora.bind("<Button-1>", self.seleccionar_hora)

        self.buttonCancelar = ctk.CTkButton(self.frameEntradas, text="Cancelar", font = texto1Bajo,  fg_color = naranjaMedio,  command="")   
        self.buttonAceptar  = ctk.CTkButton(self.frameEntradas, text="Aceptar",  font = textoGrande, fg_color = azulMedio,  command="")
        self.buttonCancelar.grid(row=4, column=0, padx=22, pady=10)  
        self.buttonAceptar.grid(row=4, column=1, padx=22, pady=10)

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