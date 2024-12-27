import  tkinter as tk
from    tkinter import ttk
import customtkinter as ctk
import  controller.controller as controller
from    view.estilos import *
import  view.ventanas_emergentes as ventanas_emergentes
import controller.glo as glo
import database.BBDD as BBDD
import re
import pandas as pd


# Configuración global del estilo de customtkinter
ctk.set_appearance_mode("dark")           # Modo oscuro por defecto
ctk.set_default_color_theme("dark-blue")  # Colores por defecto con tonos azulados


class ContenidoDetallePedido():

    def __init__(self, contenedor):

        self.frameTablaDetallePedi = ctk.CTkFrame(contenedor, bg_color=moradoMedio)
        self.frameTablaDetallePedi.pack(fill="both", expand=True, side="top", padx=5)

        # Estilo personalizado para Treeview
        self.styletreeviewDetallePedi = ttk.Style()

        # Cambiar el color de fondo y el color de la fuente para Treeview
        self.styletreeviewDetallePedi.configure("TreeviewPedidos", background=grisOscuro, foreground=blancoHueso, rowheight=25, fieldbackground=grisMedio, font=texto1Minimo)

        # Cambiar el color de selección
        self.styletreeviewDetallePedi.map("TreeviewPedidos", background=[("selected",azulClaro)], foreground=[("selected", azulOscuro)])

        self.canvas = ctk.CTkCanvas(self.frameTablaDetallePedi, bg=grisOscuro)
        self.canvas.pack(side='left', fill='both', expand=True)
        self.frameTablaDetallePedi.update_idletasks()
        self.canvas.config(width=self.frameTablaDetallePedi.winfo_width(), height=self.frameTablaDetallePedi.winfo_height())

class FiltrosDetallePedido():

    def __init__(self, treeVehiPedido, contenido, bbdd):
    # Crear un frame para los filtros
        self.frame_filtros = tk.Frame(contenido.canvas, bg=grisOscuro)
        self.frame_filtros.pack(fill=tk.X, padx=2, pady=2, side="top")

    # Crear entradas de texto para los filtros
        self.entry_chasis = ctk.CTkEntry(self.frame_filtros, fg_color=azulMedio, text_color=blancoHueso)
        self.entry_chasis.grid(row=1, column=0, padx=5)
        self.entry_idModelo = ctk.CTkEntry(self.frame_filtros, fg_color=azulMedio, text_color=blancoHueso)
        self.entry_idModelo.grid(row=1, column=1, padx=5)
        self.entry_color = ctk.CTkEntry(self.frame_filtros, fg_color=azulMedio, text_color=blancoHueso)
        self.entry_color.grid(row=1, column=2, padx=5)
        self.entry_proceso = ctk.CTkEntry(self.frame_filtros, fg_color=azulMedio, text_color=blancoHueso)
        self.entry_proceso.grid(row=1, column=3, padx=5)
        self.entry_estado = ctk.CTkEntry(self.frame_filtros, fg_color=azulMedio, text_color=blancoHueso)
        self.entry_estado.grid(row=1, column=4, padx=5)

        # Configurar el peso de las columnas para que se expandan
        for i in range(5): 
            self.frame_filtros.grid_columnconfigure(i, weight=1)


        # Crear un botón para aplicar los filtros
        self.boton_filtrar = ctk.CTkButton(master=self.frame_filtros, text="Filtro", command=lambda:self.filtrar_datos(treeVehiPedido), width=20,
                                           font=numerosPequeños, hover_color=grisVerdeClaro, fg_color=grisVerdeMedio, corner_radius=15)
        self.boton_filtrar.grid(row=0, column=0, pady=5)
    
        self.boton_actualizar = ctk.CTkButton(master=self.frame_filtros, text="Actualizar", command=lambda:treeVehiPedido.actualizar_tabla(bbdd), width=20,
                                              font=numerosPequeños, hover_color=amarilloMedio, fg_color=amarilloOscuro, corner_radius=15)
        self.boton_actualizar.grid(row=0, column=1, pady=5)

    def filtrar_datos(self, treeVehiPedido):

        # Obtener los criterios de filtro de las entradas
        self.datos      = treeVehiPedido.datos
        print(self.datos)
        filtro_chasis   = self.entry_chasis.get()
        filtro_idModelo = self.entry_idModelo.get()
        filtro_color    = self.entry_color.get()
        filtro_estado   = self.entry_estado.get()
        filtro_proceso   = self.entry_proceso.get()

        # Limpiar la tabla
        for row in treeVehiPedido.tablaDetallePedi.get_children():
            treeVehiPedido.tablaDetallePedi.delete(row)
        
        # Agregar datos filtrados a la tabla
        for record in self.datos:
            if (filtro_chasis.lower() in str(record[0]).lower() and
                filtro_idModelo.lower() in str(record[1]).lower() and
                filtro_color.lower() in str(record[2]).lower() and
                filtro_estado.lower() in str(record[3]).lower() and
                filtro_proceso.lower() in str(record[4]).lower()):

                treeVehiPedido.tablaDetallePedi.insert(parent='', index='end', iid=record[0], text='', values=record)

class TablaDetallePedido():     #Tabla para pedido
    def __init__(self, contenido, contenedor, laRaiz, bbdd): #Crea latabla y un diccionario con los nombres de los campos

        self.raiz = laRaiz
         #Crear estilo personalizado para las cabeceras
        self.styletreeviewDetallePedi = ttk.Style()
        self.styletreeviewDetallePedi.configure("TreeviewPedidos.Heading", foreground=moradoMedio, font=texto1Minimo)
        
        #Crear Tabla
        self.styletreeviewDetallePedi.layout("TreeviewPedidos", [('Treeview.treearea', {'sticky': 'nswe'})])
        self.tablaDetallePedi = ttk.Treeview(contenido.canvas, show="headings", style="TreeviewPedidos")
        self.tablaDetallePedi["columns"] = ("CHASIS", "MARCA-MODELO", "COLOR", "PROCESO", "ESTADO")

        # Formatear las columnas
        for col in self.tablaDetallePedi["columns"]:
            self.tablaDetallePedi.column(col, anchor=tk.CENTER, width=80)
            self.tablaDetallePedi.heading(col, text=col, anchor=tk.CENTER)

        #Crear una barra de desplazamiento para la tabla y configurarla
        self.scrollbarTablaDetallePedi = ttk.Scrollbar(contenido.frameTablaDetallePedi, orient=tk.VERTICAL, command=self.tablaDetallePedi.yview)
        self.tablaDetallePedi.configure(yscrollcommand=self.scrollbarTablaDetallePedi.set)
        self.tablaDetallePedi.pack(expand=True, fill="both", side="bottom")
        self.scrollbarTablaDetallePedi.pack(side='right', fill='y')
        
        self.llenarTabla(bbdd)
        self.construyeCamposHorarios(contenedor, start1="08:00", end1="12:00", start2="14:00", end2="18:00", start3=" ", end3=" ")

    def construyeCamposHorarios(self, contenedor, start1, end1, start2, end2, start3, end3):

        self.frameTurnos = ctk.CTkFrame(contenedor, bg_color=moradoMedio)
        self.frameTurnos.pack(fill="both", side="bottom")

        self.labelTurno1 = ctk.CTkLabel(self.frameTurnos, text="TURNO 1", anchor="center")
        self.labelTurno1.grid(row=0, column=0, columnspan = 4, padx=5)

        self.labelTurno2 = ctk.CTkLabel(self.frameTurnos, text="TURNO 2", anchor="center")
        self.labelTurno2.grid(row=0, column=4, columnspan = 4, padx=5)

        # Configurar columnas: 
        for columna in range(0,7):
            # Las columnas 0 y 5 son las de los extremos (espacio vacío).
            self.frameTurnos.grid_columnconfigure(columna, weight=1)  # Espacio izquierdo

        self.intVarTurnoInicia1 = tk.StringVar(value=start1)
        self.entryTurnoInicia1 = ctk.CTkEntry(self.frameTurnos, textvariable = self.intVarTurnoInicia1, width=60)
        self.entryTurnoInicia1.grid(row=1, column=1, padx=5, pady=5)
        self.entryTurnoInicia1.bind("<FocusOut>", self.validar_hora)

        self.intVarTurnoTermina1 = tk.StringVar(value=end1)
        self.entryTurnoTermina1 = ctk.CTkEntry(self.frameTurnos, textvariable = self.intVarTurnoTermina1, width=60)
        self.entryTurnoTermina1.grid(row=1, column=2, padx=5, pady=5)
        self.entryTurnoTermina1.bind("<FocusOut>", self.validar_hora)

        self.intVarTurnoInicia2 = tk.StringVar(value=start2)
        self.entryTurnoInicia2 = ctk.CTkEntry(self.frameTurnos, textvariable = self.intVarTurnoInicia2, width=60)
        self.entryTurnoInicia2.grid(row=1, column=5, padx=5, pady=5)
        self.entryTurnoInicia2.bind("<FocusOut>", self.validar_hora)

        self.intVarTurnoTermina2 = tk.StringVar(value=end2)
        self.entryTurnoTermina2 = ctk.CTkEntry(self.frameTurnos, textvariable = self.intVarTurnoTermina2, width=60)
        self.entryTurnoTermina2.grid(row=1, column=6, padx=5, pady=5)
        self.entryTurnoTermina2.bind("<FocusOut>", self.validar_hora)

        glo.turnos.startAM = self.intVarTurnoInicia1
        glo.turnos.endAM   = self.intVarTurnoTermina1
        glo.turnos.startPM = self.intVarTurnoInicia2
        glo.turnos.endPM   = self.intVarTurnoTermina2
        
    def llenarTabla(self, bbdd, pedido=None):    # Agregar datos a la tabla

        if pedido is None:
            self.datos = BBDD.leer_vehiculos_completos_df(bbdd)           # leemos el dataframe en la BBDD
        else:
            self.datos = BBDD.leer_vehiculos_por_pedido_df(bbdd, pedido)  # leemos el dataframe en la BBDD
        print(self.datos)

        # Seleccionar solo las columnas necesarias
        columnas_necesarias = ['CHASIS', 'ID_MODELO', 'COLOR', 'NOMBRE_PROCESO', 'ESTADO']
        datos_filtrados = self.datos[columnas_necesarias]

        for item in self.tablaDetallePedi.get_children():
            self.tablaDetallePedi.delete(item)

        # Insertar los datos en la tabla
        for index, row in datos_filtrados.iterrows():
            self.tablaDetallePedi.insert(parent='', index='end', iid=row['CHASIS'], text='', values=row.tolist())

        # Función para obtener el texto del tooltip
        def obtener_texto_tooltip(iid):
            
            valores = self.tablaDetallePedi.item(iid, 'values')
            lecturaHistoricos = BBDD.leer_historico_chasis(bbdd, valores[0])
            lecturaVehiculos  = BBDD.leer_vehiculo_completo(bbdd, valores[0])
            
            if lecturaHistoricos == None:
                return f"Chasis: {valores[1]}\nSin procesos ejecutados"
            
            # Obtener las tuplas (proceso, tiempo, estado)
            procesos_tiempos_estados = []
            for vehiculo in lecturaVehiculos:
                proceso = vehiculo[-2]
                tiempo = vehiculo[-1]
                estado = next((historico[8] for historico in lecturaHistoricos if historico[3] == proceso), "No")
                if estado:
                    procesos_tiempos_estados.append((proceso, tiempo, estado))
        
            mensaje = "".join([f"\n{proceso}: {tiempo}min. {estado}"
                               for proceso, tiempo, estado in procesos_tiempos_estados])
            return f"Chasis: {valores[1]}\nProcesos: {mensaje}"

        # Añadir tooltips a las filas
        controller.Tooltip(self.tablaDetallePedi, obtener_texto_tooltip)

        #click derecho en información de vehículo       
        def seleccionar_informacion_fila():
            fila = self.tablaDetallePedi.selection()     #obtener el item seleccionado
            print("Asignar seleccionada")
            if fila:
                valores = self.tablaDetallePedi.item(fila, 'values')     #obtener los valores de la fila
                print(valores)
                informacion_vh(valores, bbdd)

        #click derecho en asignar vehiculo
        def seleccionar_asignar_fila():
            fila = self.tablaDetallePedi.selection()     #obtener el item seleccionado
            print("Asignar seleccionada")
            if fila:
                valores = self.tablaDetallePedi.item(fila, 'values')     #obtener los valores de la fila
                id_pedido = valores[0]
                print(f"asignará el vehiculo  {valores}")
                print(id_pedido, bbdd)
                controller.ventana_AsignarUnVehiculo(id_pedido, bbdd)

        #click derecho en modificar fila
        def seleccionar_modificar_fila():
            fila = self.tablaDetallePedi.selection()     #obtener el item seleccionado
            print("Modificar seleccionada")
            if fila:
                valores = self.tablaDetallePedi.item(fila, 'values')     #obtener los valores de la fila
                print(valores)
                modificar_vh(valores, bbdd)

        #click derecho en eliminar fila
        def seleccionar_eliminar_fila():
            fila = self.tablaDetallePedi.selection()     #obtener el item seleccionado
            print("Eliminar seleccionada")
            if fila:
                valores = self.tablaDetallePedi.item(fila, 'values')     #obtener los valores de la fila
                print(valores)
                eliminar_vh(valores, bbdd)       
        
        #CREAR MENU CONTEXTUAL
        self.menu = tk.Menu(self.raiz, tearoff=0)
        self.menu.add_command(label="Información", command = seleccionar_informacion_fila)
        self.menu.add_command(label="Asignar", command = seleccionar_asignar_fila)
        self.menu.add_command(label="Modificar", command = seleccionar_modificar_fila)
        self.menu.add_command(label="Eliminar", command = seleccionar_eliminar_fila)
        
        
        #Opciones del menú del click derecho
        def eliminar_vh(valores, bbdd):
            id_pedido = valores[0]
            print(f"Se eliminará {id_pedido}")
            controller.eliminar_VH_pedido(id_pedido)

        def modificar_vh(valores, bbdd):
            id_anterior = valores[0]
            print(f"modificará el chasis {id_anterior}")
            controller.modificar_datos_vehiculo(id_anterior, bbdd)

        def informacion_vh(valores, bbdd):
            id_pedido = valores[0]
            print(f"solicitó información de {id_pedido}")
            controller.ventana_infoVehiculo(id_pedido, bbdd)

        def mostrar_menu(evento):        # Manejar el evento del clic derecho
            try:
                item_id = self.tablaDetallePedi.identify_row(evento.y)  # Identificar la fila en la que se hizo click
                self.tablaDetallePedi.selection_set(item_id)  # Seleccionar la fila

                # Mostrar el menú contextual en la posición del cursor
                self.menu.post(evento.x_root, evento.y_root)
            except:
                pass
        
        
        # Asociar el click derecho al evento
        self.tablaDetallePedi.bind("<Button-3>", mostrar_menu)

    def actualizar_tabla(self, bbdd):
        # Elimina todos los elementos del Treeview
        for item in self.tablaDetallePedi.get_children():
            self.tablaDetallePedi.delete(item)
        
        self.llenarTabla(bbdd)
    
    def validar_hora(self, event):
        """Valida que el formato sea HH:MM en los Entry al perder el foco"""
        entry = event.widget
        texto = entry.get()

        if texto:  # Solo validar si no está vacío
            if not re.match(r'^\d{2}:\d{2}$', texto):  # Valida el formato HH:MM
                ventanas_emergentes.messagebox.showerror("Formato de Hora Inválido", f"'{texto}' no es un formato válido.\nUtilice 'HH:MM'.")
                entry.focus_set()  # Vuelve a enfocar el Entry
                entry.delete(0, tk.END)  # Borra el contenido inválido
