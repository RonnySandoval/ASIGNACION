import  tkinter as tk
from    tkinter import ttk
import customtkinter as ctk
import  controller.controller as controller
from    view.estilos import *
import database.BBDD as BBDD

# Configuración global del estilo de customtkinter
ctk.set_appearance_mode("dark")  # Modo oscuro por defecto
ctk.set_default_color_theme("dark-blue")  # Colores por defecto con tonos azulados

class ContenidoOrdenes():

    def __init__(self, contenedor):

        self.frameTablaOrdenes = ctk.CTkFrame(contenedor, bg_color=grisVerdeOscuro)
        self.frameTablaOrdenes.pack(fill="both", expand=True, side="right", padx=5)

        # Estilo personalizado para Treeview
        self.styletreeviewOrdenes = ttk.Style()

        # Cambiar el color de fondo y el color de la fuente para Treeview
        self.styletreeviewOrdenes.configure("TreeviewProgramas", background=grisOscuro, foreground=blancoHueso, rowheight=25, fieldbackground=grisMedio, font=texto1Minimo)

        # Cambiar el color de selección
        self.styletreeviewOrdenes.map("TreeviewProgramas", background=[("selected",verdeClaro)], foreground=[("selected", verdeOscuro)])

        self.canvas = ctk.CTkCanvas(self.frameTablaOrdenes, bg=grisOscuro)
        self.canvas.pack(side='left', fill='both', expand=True)
        self.frameTablaOrdenes.update_idletasks()
        self.canvas.config(width=self.frameTablaOrdenes.winfo_width(), height=self.frameTablaOrdenes.winfo_height())

class FiltrosOrdenes():

    def __init__(self, treeOrdenes, contenido, bbdd):
    # Crear un frame para los filtros
        self.frame_filtros = tk.Frame(contenido.canvas, bg=grisOscuro)
        self.frame_filtros.pack(fill=tk.X, padx=2, pady=2, side="top")

    # Crear entradas de texto para los filtros
        self.entry_codigo = ctk.CTkEntry(self.frame_filtros, fg_color=verdeMedio, text_color=blancoHueso)
        self.entry_codigo.grid(row=1, column=0, padx=5)
        self.entry_chasis = ctk.CTkEntry(self.frame_filtros, fg_color=verdeMedio, text_color=blancoHueso)
        self.entry_chasis.grid(row=1, column=1, padx=5)
        self.entry_tecnico = ctk.CTkEntry(self.frame_filtros, fg_color=verdeMedio, text_color=blancoHueso)
        self.entry_tecnico.grid(row=1, column=2, padx=5)
        self.entry_proceso = ctk.CTkEntry(self.frame_filtros, fg_color=verdeMedio, text_color=blancoHueso)
        self.entry_proceso.grid(row=1, column=3, padx=5)
        self.entry_inicio = ctk.CTkEntry(self.frame_filtros, fg_color=verdeMedio, text_color=blancoHueso)
        self.entry_inicio.grid(row=1, column=4, padx=5)
        self.entry_fin = ctk.CTkEntry(self.frame_filtros, fg_color=verdeMedio, text_color=blancoHueso)
        self.entry_fin.grid(row=1, column=5, padx=5)
        self.entry_timeProd = ctk.CTkEntry(self.frame_filtros, fg_color=verdeMedio, text_color=blancoHueso)
        self.entry_timeProd.grid(row=1, column=6, padx=5)

        # Configurar el peso de las columnas para que se expandan
        for i in range(7): 
            self.frame_filtros.grid_columnconfigure(i, weight=1)


        # Crear un botón para aplicar los filtros
        self.boton_filtrar = ctk.CTkButton(master=self.frame_filtros, text="Filtro", command=lambda:self.filtrar_datos(treeOrdenes), width=20,
                                           font=numerosPequeños, hover_color=grisVerdeClaro, fg_color=grisVerdeMedio, corner_radius=15)
        self.boton_filtrar.grid(row=0, column=0, pady=5)
    
        self.boton_actualizar = ctk.CTkButton(master=self.frame_filtros, text="Actualizar", command=lambda:treeOrdenes.actualizar_tabla(bbdd), width=20,
                                              font=numerosPequeños, hover_color=amarilloMedio, fg_color=amarilloOscuro, corner_radius=15)
        self.boton_actualizar.grid(row=0, column=1, pady=5)

    def filtrar_datos(self, treeOrdenes):

        # Obtener los criterios de filtro de las entradas
        self.datos      = treeOrdenes.datos
        print(self.datos)
        filtro_codigo   = self.entry_codigo.get()
        filtro_chasis   = self.entry_chasis.get()
        filtro_tecnico  = self.entry_tecnico.get()
        filtro_proceso  = self.entry_inicio.get()
        filtro_inicio   = self.entry_proceso.get()
        filtro_fin      = self.entry_proceso.get()
        filtro_timeProd = self.entry_proceso.get()
        
        # Limpiar la tabla
        for row in treeOrdenes.tablaOrdenes.get_children():
            treeOrdenes.tablaOrdenes.delete(row)
        
        # Agregar datos filtrados a la tabla
        for record in self.datos:
            if (filtro_codigo.lower()   in str(record[0]).lower() and
                filtro_chasis.lower()   in str(record[1]).lower() and
                filtro_tecnico.lower()  in str(record[2]).lower() and
                filtro_proceso.lower()  in str(record[3]).lower() and
                filtro_inicio.lower()   in str(record[4]).lower() and
                filtro_fin.lower()      in str(record[5]).lower() and
                filtro_timeProd.lower() in str(record[6]).lower()):

                treeOrdenes.tablaOrdenes.insert(parent='', index='end', iid=record[0], text='', values=record)              

class TablaOrdenes():     #Tabla para pedido
    def __init__(self, contenido, contenedor, laRaiz, bbdd): #Crea latabla y un diccionario con los nombres de los campos

        self.raiz = laRaiz
         #Crear estilo personalizado para las cabeceras
        self.styletreeviewOrdenes = ttk.Style()
        self.styletreeviewOrdenes.configure("TreeviewProgramas.Heading", foreground=grisVerdeOscuro, font=texto1Minimo)
        
        #Crear Tabla
        self.styletreeviewOrdenes.layout("TreeviewProgramas", [('Treeview.treearea', {'sticky': 'nswe'})])
        self.tablaOrdenes = ttk.Treeview(contenido.canvas, show="headings", style="TreeviewProgramas")
        self.tablaOrdenes["columns"] = ("CODIGO", "CHASIS", "TECNICO", "PROCESO", "INICIO", "FIN", "MODELO")

        # Formatear las columnas
        for col in self.tablaOrdenes["columns"]:
            self.tablaOrdenes.column(col, anchor=tk.CENTER, width=80)
            self.tablaOrdenes.heading(col, text=col, anchor=tk.CENTER)

        # Crear un Scrollbar y conectarlo con el Canvas

        #Crear una barra de desplazamiento para la tabla y configurarla
        self.scrollbarTablaOrdenes = ttk.Scrollbar(contenido.frameTablaOrdenes, orient=tk.VERTICAL, command=self.tablaOrdenes.yview)
        self.tablaOrdenes.configure(yscrollcommand=self.scrollbarTablaOrdenes.set)
        self.tablaOrdenes.pack(expand=True, fill="both", side="bottom")
        self.scrollbarTablaOrdenes.pack(side='right', fill='y')
        
        self.llenarTabla(bbdd)

    def llenarTabla(self, bbdd, programa=None):    # Agregar datos a la tabla

        if programa is None:
            self.programaMostrado = list(BBDD.leer_ordenes_completo(bbdd))
            self.datos = [(codigo, chasis, tecnico, proceso, inicio, fin, modelo)
                            for codigo, chasis, inicio, fin, duracion, tiempo_productivo, proceso,
                                observaciones, modelo, color, tecnico
                            in self.programaMostrado]

        if programa is not None:
            self.programaMostrado = list(BBDD.leer_ordenes_por_programa(bbdd, programa))
            self.datos = [(codigo, chasis, tecnico, proceso, inicio, fin, modelo)
                            for codigo, chasis, inicio, fin, duracion, tiempo_productivo, proceso,
                                observaciones, modelo, color, tecnico
                            in self.programaMostrado]
        print(self.datos)

        for item in self.tablaOrdenes.get_children():
            self.tablaOrdenes.delete(item)

        for record in self.datos:
            self.tablaOrdenes.insert(parent='', index='end', iid=record[0], text='', values=record)

        #click derecho en información de vehículo       
        def seleccionar_informacion_fila():
            fila = self.tablaOrdenes.selection()     #obtener el item seleccionado
            print("Resumen de orden seleccionada")
            if fila:
                valores = self.tablaOrdenes.item(fila, 'values')     #obtener los valores de la fila
                print(valores)
                informacion_ord(valores, bbdd)

        #click derecho en asignar vehiculo
        def seleccionar_incluir_fila():
            fila = self.tablaOrdenes.selection()     #obtener el item seleccionado
            print("Incluir orden seleccionada")
            if fila:
                valores = self.tablaOrdenes.item(fila, 'values')     #obtener los valores de la fila
                id_pedido = valores[0]
                print(f"asignará el vehiculo  {valores}")
                print(id_pedido, bbdd)
                incluir_ord(valores, bbdd)

        #click derecho en eliminar fila
        def seleccionar_eliminar_fila():
            fila = self.tablaOrdenes.selection()     #obtener el item seleccionado
            print("Eliminar orden seleccionada")
            if fila:
                valores = self.tablaOrdenes.item(fila, 'values')     #obtener los valores de la fila
                print(valores)
                eliminar_ord(valores, bbdd)       
        
        #CREAR MENU CONTEXTUAL
        self.menu = tk.Menu(self.raiz, tearoff=0)
        self.menu.add_command(label="Resumen", command = seleccionar_informacion_fila)
        self.menu.add_command(label="Incluir en histórico", command = seleccionar_incluir_fila)
        self.menu.add_command(label="Eliminar", command = seleccionar_eliminar_fila)
        
        #Opciones del menú del click derecho
        def informacion_ord(valores, bbdd):
            id_programa = valores[0]
            print(f"solicitó información de {id_programa}")
            controller.ventana_infoOrdenes(id_programa, bbdd)

        def incluir_ord(valores, bbdd):
            id_anterior = valores[0]
            print(f"modificará el chasis {id_anterior}")
            controller.modificar_datos_vehiculo(id_anterior, bbdd)

        def eliminar_ord(valores, bbdd):
            id_programa = valores[0]
            print(f"Se eliminará {id_programa}")
            controller.eliminar_orden(id_programa)

        def mostrar_menu(evento):        # Manejar el evento del clic derecho
            try:
                item_id = self.tablaOrdenes.identify_row(evento.y)  # Identificar la fila en la que se hizo click
                self.tablaOrdenes.selection_set(item_id)  # Seleccionar la fila

                # Mostrar el menú contextual en la posición del cursor
                self.menu.post(evento.x_root, evento.y_root)
            except:
                pass
       
        # Asociar el click derecho al evento
        self.tablaOrdenes.bind("<Button-3>", mostrar_menu)

    def actualizar_tabla(self, bbdd):
        # Elimina todos los elementos del Treeview
        for item in self.tablaOrdenes.get_children():
            self.tablaOrdenes.delete(item)
        
        self.llenarTabla(bbdd)
