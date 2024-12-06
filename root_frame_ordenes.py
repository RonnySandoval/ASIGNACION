import  tkinter as tk
from    tkinter import ttk
import customtkinter as ctk
import  eventos as eventos
from    estilos import *
import  ventanas_emergentes
import glo
import BBDD


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
        self.entry_chasis = ctk.CTkEntry(self.frame_filtros, fg_color=verdeMedio, text_color=blancoHueso)
        self.entry_chasis.grid(row=1, column=0, padx=5)
        self.entry_idModelo = ctk.CTkEntry(self.frame_filtros, fg_color=verdeMedio, text_color=blancoHueso)
        self.entry_idModelo.grid(row=1, column=1, padx=5)
        self.entry_color = ctk.CTkEntry(self.frame_filtros, fg_color=verdeMedio, text_color=blancoHueso)
        self.entry_color.grid(row=1, column=2, padx=5)
        self.entry_proceso = ctk.CTkEntry(self.frame_filtros, fg_color=verdeMedio, text_color=blancoHueso)
        self.entry_proceso.grid(row=1, column=3, padx=5)
        self.entry_estado = ctk.CTkEntry(self.frame_filtros, fg_color=verdeMedio, text_color=blancoHueso)
        self.entry_estado.grid(row=1, column=4, padx=5)

        # Configurar el peso de las columnas para que se expandan
        for i in range(5): 
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
        filtro_chasis   = self.entry_chasis.get()
        filtro_idModelo = self.entry_idModelo.get()
        filtro_color    = self.entry_color.get()
        filtro_estado   = self.entry_estado.get()
        filtro_proceso   = self.entry_proceso.get()

        # Limpiar la tabla
        for row in treeOrdenes.tablaOrdenes.get_children():
            treeOrdenes.tablaOrdenes.delete(row)
        
        # Agregar datos filtrados a la tabla
        for record in self.datos:
            if (filtro_chasis.lower() in str(record[0]).lower() and
                filtro_idModelo.lower() in str(record[1]).lower() and
                filtro_color.lower() in str(record[2]).lower() and
                filtro_estado.lower() in str(record[3]).lower() and
                filtro_proceso.lower() in str(record[4]).lower()):

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
        self.tablaOrdenes["columns"] = ("CHASIS", "MARCA-MODELO", "COLOR", "PROCESO", "ESTADO")

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
            self.programaMostrado = list(BBDD.leer_vehiculos_completos(bbdd))
            self.datos = [(chasis, modelo, color, proceso, estado)
                            for chasis, fecha, modelo, color, proceso, estado, novedades, subcontratar, pedido
                            in self.programaMostrado]

        if programa is not None:
            self.datos = list(BBDD.leer_ordenes_por_programa(bbdd, programa))
        print(self.datos)

        for item in self.tablaOrdenes.get_children():
            self.tablaOrdenes.delete(item)

        for record in self.datos:
            self.tablaOrdenes.insert(parent='', index='end', iid=record[0], text='', values=record)

        #click derecho en información de vehículo       
        def seleccionar_informacion_fila():
            fila = self.tablaOrdenes.selection()     #obtener el item seleccionado
            print("Asignar seleccionada")
            if fila:
                valores = self.tablaOrdenes.item(fila, 'values')     #obtener los valores de la fila
                print(valores)
                informacion_vh(valores, bbdd)

        #click derecho en asignar vehiculo
        def seleccionar_asignar_fila():
            fila = self.tablaOrdenes.selection()     #obtener el item seleccionado
            print("Asignar seleccionada")
            if fila:
                valores = self.tablaOrdenes.item(fila, 'values')     #obtener los valores de la fila
                id_pedido = valores[0]
                print(f"asignará el vehiculo  {valores}")
                print(id_pedido, bbdd)
                eventos.ventana_AsignarUnVehiculo(id_pedido, bbdd)

        #click derecho en modificar fila
        def seleccionar_modificar_fila():
            fila = self.tablaOrdenes.selection()     #obtener el item seleccionado
            print("Modificar seleccionada")
            if fila:
                valores = self.tablaOrdenes.item(fila, 'values')     #obtener los valores de la fila
                print(valores)
                modificar_vh(valores, bbdd)

        #click derecho en eliminar fila
        def seleccionar_eliminar_fila():
            fila = self.tablaOrdenes.selection()     #obtener el item seleccionado
            print("Eliminar seleccionada")
            if fila:
                valores = self.tablaOrdenes.item(fila, 'values')     #obtener los valores de la fila
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
            id_programa = valores[0]
            print(f"Se eliminará {id_programa}")
            eventos.eliminar_VH_pedido(id_programa)

        def modificar_vh(valores, bbdd):
            id_anterior = valores[0]
            print(f"modificará el chasis {id_anterior}")
            eventos.modificar_vehiculo_pedido(id_anterior, bbdd)

        def informacion_vh(valores, bbdd):
            id_programa = valores[0]
            print(f"solicitó información de {id_programa}")
            eventos.ventana_infoVehiculo(id_programa, bbdd)

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
