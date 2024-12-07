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


class ContenidoDetallePedido():

    def __init__(self, contenedor):

        self.frameTablaDetallePedi = ctk.CTkFrame(contenedor, bg_color=moradoMedio)
        self.frameTablaDetallePedi.pack(fill="both", expand=True, side="right", padx=5)

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

        # Crear un Scrollbar y conectarlo con el Canvas

        #Crear una barra de desplazamiento para la tabla y configurarla
        self.scrollbarTablaDetallePedi = ttk.Scrollbar(contenido.frameTablaDetallePedi, orient=tk.VERTICAL, command=self.tablaDetallePedi.yview)
        self.tablaDetallePedi.configure(yscrollcommand=self.scrollbarTablaDetallePedi.set)
        self.tablaDetallePedi.pack(expand=True, fill="both", side="bottom")
        self.scrollbarTablaDetallePedi.pack(side='right', fill='y')
        
        self.llenarTabla(bbdd)

    def llenarTabla(self, bbdd, pedido=None):    # Agregar datos a la tabla

        if pedido is None:
            self.pedidoMostrado = list(BBDD.leer_vehiculos_completos(bbdd))
            self.datos = [(chasis, modelo, color, proceso, estado)
                            for chasis, fecha, modelo, color, proceso, estado, novedades, subcontratar, pedido
                            in self.pedidoMostrado]

        if pedido is not None:
            self.datos = list(BBDD.leer_vehiculos_por_pedido(bbdd, pedido))

        print(self.datos)

        for item in self.tablaDetallePedi.get_children():
            self.tablaDetallePedi.delete(item)

        for record in self.datos:
            self.tablaDetallePedi.insert(parent='', index='end', iid=record[0], text='', values=record)

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
                eventos.ventana_AsignarUnVehiculo(id_pedido, bbdd)

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
            eventos.eliminar_VH_pedido(id_pedido)

        def modificar_vh(valores, bbdd):
            id_anterior = valores[0]
            print(f"modificará el chasis {id_anterior}")
            eventos.modificar_vehiculo_pedido(id_anterior, bbdd)

        def informacion_vh(valores, bbdd):
            id_pedido = valores[0]
            print(f"solicitó información de {id_pedido}")
            eventos.ventana_infoVehiculo(id_pedido, bbdd)

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
