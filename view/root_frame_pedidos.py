import  tkinter as tk
from    tkinter import ttk
import customtkinter as ctk
import  controller.controller as controller
from    view.estilos import *
import  view.ventanas_emergentes as ventanas_emergentes
import controller.glo as glo
import database.BBDD as BBDD


# Configuración global del estilo de customtkinter
ctk.set_appearance_mode("dark")  # Modo oscuro por defecto
ctk.set_default_color_theme("dark-blue")  # Colores por defecto con tonos azulados


class ContenidoPedidos():

    def __init__(self, contenedor):

        self.frameTablaPedidos = ctk.CTkFrame(contenedor, bg_color=moradoMedio)
        self.frameTablaPedidos.pack(fill="both", expand=True, side="top", padx=5,)

        # Estilo personalizado para Treeview
        self.styletreeviewPedi = ttk.Style()

        # Cambiar el color de fondo y el color de la fuente para Treeview
        self.styletreeviewPedi.configure("TreeviewPedidos", background=grisOscuro, foreground=blancoHueso, rowheight=25, fieldbackground=grisMedio, font=texto1Minimo)

        # Cambiar el color de selección
        self.styletreeviewPedi.map("TreeviewPedidos", background=[("selected",azulClaro)], foreground=[("selected", azulOscuro)])

        self.canvas = ctk.CTkCanvas(self.frameTablaPedidos, bg=grisOscuro)
        self.canvas.pack(side='left', fill='both', expand=True)
        self.frameTablaPedidos.update_idletasks()
        self.canvas.config(width=self.frameTablaPedidos.winfo_width(), height=self.frameTablaPedidos.winfo_height())

class FiltrosPedidos():

    def __init__(self, treePedidos, contenido, bbdd):
    # Crear un frame para los filtros
        self.frame_filtros = tk.Frame(contenido.canvas, bg=grisOscuro)
        self.frame_filtros.pack(fill=tk.X, padx=2, pady=2, side="top")

    # Crear entradas de texto para los filtros
        self.entry_id_pedido = ctk.CTkEntry(self.frame_filtros, fg_color=azulMedio, text_color=blancoHueso)
        self.entry_id_pedido.grid(row=1, column=0, padx=5)
        self.entry_fecha_ingreso = ctk.CTkEntry(self.frame_filtros, fg_color=azulMedio, text_color=blancoHueso)
        self.entry_fecha_ingreso.grid(row=1, column=1, padx=5)
        self.entry_fecha_estimada = ctk.CTkEntry(self.frame_filtros, fg_color=azulMedio, text_color=blancoHueso)
        self.entry_fecha_estimada.grid(row=1, column=2, padx=5)
        self.entry_fecha_entrega = ctk.CTkEntry(self.frame_filtros, fg_color=azulMedio, text_color=blancoHueso)
        self.entry_fecha_entrega.grid(row=1, column=3, padx=5)

        # Configurar el peso de las columnas para que se expandan
        for i in range(4): 
            self.frame_filtros.grid_columnconfigure(i, weight=1)

        # Crear un botón para aplicar los filtros
        self.boton_filtrar = ctk.CTkButton(master=self.frame_filtros, text="Filtro", command=lambda:self.filtrar_datos(treePedidos), width=20,
                                           font=numerosPequeños, hover_color=grisVerdeClaro, fg_color=grisVerdeMedio, corner_radius=15)
        self.boton_filtrar.grid(row=0, column=0, pady=5)
    
        self.boton_actualizar = ctk.CTkButton(master=self.frame_filtros, text="Actualizar", command=lambda:treePedidos.actualizar_tabla(bbdd), width=20,
                                              font=numerosPequeños, hover_color=amarilloMedio, fg_color=amarilloOscuro, corner_radius=15)
        self.boton_actualizar.grid(row=0, column=1, pady=5)

    def filtrar_datos(self, treePedidos):
        treePedidos.tablaPedidos.unbind("<<TreeviewSelect>>")
        # Obtener los criterios de filtro de las entradas
        self.datos             = treePedidos.datos
        filtro_id_pedido       = self.entry_id_pedido.get()
        filtro_fecha_ingreso   = self.entry_fecha_ingreso.get()
        filtro_fecha_estimada  = self.entry_fecha_estimada.get()
        filtro_fecha_entrega   = self.entry_fecha_entrega.get()
        print("datos del contenido de Pedidos: ", self.datos)
        print("Datos de los entry en filtrar_datos:", filtro_id_pedido, filtro_fecha_ingreso, filtro_fecha_estimada, filtro_fecha_entrega)
        # Limpiar la tabla
        for row in treePedidos.tablaPedidos.get_children():
            treePedidos.tablaPedidos.delete(row)
        
        # Agregar datos filtrados a la tabla
        for record in self.datos:
            if (filtro_id_pedido.lower()      in str(record[0]).lower() and
                filtro_fecha_ingreso.lower()  in str(record[1]).lower() and
                filtro_fecha_estimada.lower() in str(record[2]).lower() and
                filtro_fecha_entrega.lower()  in str(record[3]).lower()):

                treePedidos.tablaPedidos.insert(parent='', index='end', iid=record[0], text='', values=record)

            treePedidos.tablaPedidos.bind("<<TreeviewSelect>>")

class TablaPedidos():     #Tabla para pedido
    def __init__(self, contenido, contenedor, laRaiz, bbdd): #Crea latabla y un diccionario con los nombres de los campos

         #Crear estilo personalizado para las cabeceras
        self.styletreeviewPedi = ttk.Style()
        self.styletreeviewPedi.configure("TreeviewPedidos.Heading", foreground=moradoMedio, font=texto1Minimo)
        self.raiz = laRaiz
        #Crear Tabla
        self.styletreeviewPedi.layout("TreeviewPedidos", [('Treeview.treearea', {'sticky': 'nswe'})])
        self.tablaPedidos = ttk.Treeview(contenido.canvas, show="headings", style="TreeviewPedidos")
        self.tablaPedidos["columns"] = ("Id Pedido", "Fecha recepcion", "Fecha ingreso", "Fecha Requerido", "Fecha Entregado")

        # Formatear las columnas
        for col in self.tablaPedidos["columns"]:
            self.tablaPedidos.column(col, anchor=tk.CENTER, width=80)
            self.tablaPedidos.heading(col, text=col, anchor=tk.CENTER)

        #Crear una barra de desplazamiento para la tabla y configurarla
        self.scrollbarTablaPedidos = ttk.Scrollbar(contenido.frameTablaPedidos, orient=tk.VERTICAL, command=self.tablaPedidos.yview)
        self.tablaPedidos.configure(yscrollcommand=self.scrollbarTablaPedidos.set)
        self.tablaPedidos.pack(expand=True, fill="both", side="bottom")
        self.scrollbarTablaPedidos.pack(side='right', fill='y')

        self.pedido_seleccionado = None
        self.llenarTabla(bbdd)

        self.frameBotonesPedidos = ctk.CTkFrame(contenedor, bg_color=moradoMedio)
        self.frameBotonesPedidos.pack(fill="both", side="bottom")
        
        #Botones de programar pedido
        self.botonProgramarTodo = ctk.CTkButton(master=self.frameBotonesPedidos ,text="Programar TODO",
                                                font=textoMedio, hover_color=amarilloOscuro, fg_color=azulOscuro, border_color = blancoFrio,
                                                corner_radius=20, command=lambda:self.programar("completo", bbdd), width=60)
        self.botonProgramarTodo.pack(fill=tk.X, side="left", padx=15, pady=5)

        self.botonProgramarInmediato = ctk.CTkButton(master=self.frameBotonesPedidos, text="Programar INMEDIATO",
                                                     font=textoMedio, hover_color=amarilloOscuro, fg_color=azulOscuro, border_color = blancoFrio,
                                                     corner_radius=20, command=lambda:self.programar("inmediato", bbdd), width=60)
        self.botonProgramarInmediato.pack(fill=tk.X, side="left", padx=15, pady=5)

        self.botonProgramarPorProcesos= ctk.CTkButton(master=self.frameBotonesPedidos, text="Programar POR PROCESOS",
                                                      font=textoMedio, hover_color=amarilloOscuro, fg_color=azulOscuro, border_color = blancoFrio,
                                                     corner_radius=20, command=lambda:self.programar("por procesos", bbdd), width=60)
        self.botonProgramarPorProcesos.pack(fill=tk.X, side="left", padx=15, pady=5)

        self.frameCheckProcesos = ctk.CTkFrame(contenedor, bg_color=moradoMedio)
        self.frameCheckProcesos.pack(fill="both", side="bottom")

        #CHECKBUTTON CON PROCESOS
        self.infoProcesos = BBDD.leer_procesos_completo(bbdd)
        for id in [proceso[0] for proceso in self.infoProcesos]:

            int_name = f"checkIntvar-{id}"                                        # generar el nombre de la IntVar del checkbutton
            self.check_name_proceso = id                                          # nombre del checkbutton
            print(self.check_name_proceso)
            print(glo.intVar_procesos[int_name])
            glo.check_procesos[self.check_name_proceso] = ctk.CTkCheckBox(
                                                                        self.frameCheckProcesos, text=id, 
                                                                        bg_color=grisOscuro, font=texto1Medio, fg_color=grisOscuro,
                                                                        variable=glo.intVar_procesos[int_name])
            glo.check_procesos[self.check_name_proceso].pack(fill=tk.X, side="left", padx=15, pady=5)

    def llenarTabla(self, bbdd):    # Agregar datos a la tabla    
        self.lectura = list(BBDD.leer_pedidos(bbdd))
        self.datos = [(id, rec, ing , est, ent) for id, cli, rec, ing, est, ent, cons  in self.lectura]
        print(self.datos)
        for record in self.datos:
            self.tablaPedidos.insert(parent='', index='end', iid=record[0], text='', values=record)

        def click_fila(event):
            try:
                tabla = event.widget
                filas_seleccionadas = tabla.selection()
                print("filas seleccionadas con click_fila:", filas_seleccionadas)
                datos = tabla.item(filas_seleccionadas[0], "values")
                print(datos)
                pedido = datos[0]
                print(pedido)
                self.pedido_seleccionado = pedido
                glo.pedido_seleccionado = pedido
                glo.stateFrame.tablaDetalles.llenarTabla(bbdd, pedido = pedido)
                            
            except IndexError as e:
                print("Datos actualizados. Pedido No seleccionado")

        #click derecho en información de vehículo       
        def seleccionar_informacion_fila():
            fila = self.tablaPedidos.selection()     #obtener el item seleccionado
            print("Asignar seleccionada")
            if fila:
                valores = self.tablaPedidos.item(fila, 'values')     #obtener los valores de la fila
                print(valores)
                informacion_pedi(valores, bbdd)

        #click derecho en modificar fila
        def seleccionar_exportar_fila():
            fila = self.tablaPedidos.selection()     #obtener el item seleccionado
            print("Modificar seleccionada")
            if fila:
                valores = self.tablaPedidos.item(fila, 'values')     #obtener los valores de la fila
                print(valores)
                exportar_pedi(valores, bbdd)

        #click derecho en modificar fila
        def seleccionar_modificar_fila():
            fila = self.tablaPedidos.selection()     #obtener el item seleccionado
            print("Modificar seleccionada")
            if fila:
                valores = self.tablaPedidos.item(fila, 'values')     #obtener los valores de la fila
                print(valores)
                modificar_pedi(valores, bbdd)

        #click derecho en eliminar fila
        def seleccionar_eliminar_fila():
            fila = self.tablaPedidos.selection()     #obtener el item seleccionado
            print("Eliminar seleccionada")
            if fila:
                valores = self.tablaPedidos.item(fila, 'values')     #obtener los valores de la fila
                print(valores)
                eliminar_pedi(valores, bbdd)       
        
        #CREAR MENU CONTEXTUAL
        self.menu = tk.Menu(self.raiz, tearoff=0)
        self.menu.add_command(label="Información", command = seleccionar_informacion_fila)
        self.menu.add_command(label="Modificar", command = seleccionar_modificar_fila)
        self.menu.add_command(label="Eliminar", command = seleccionar_eliminar_fila)
        
        #Opciones del menú del click derecho

        def informacion_pedi(valores, bbdd):
            id_pedido = valores[0]
            print(f"solicitó información de {id_pedido}")
            controller.ventana_infoPedido(id_pedido, bbdd)

        def modificar_pedi(valores, bbdd):
            id_anterior = valores[0]
            print(f"modificará el chasis {id_anterior}")
            controller.modificar_datos_pedido(id_anterior, bbdd)

        def exportar_pedi(valores, bbdd):
            id_pedido = valores[0]
            print(f"modificará el chasis {id_pedido}")
            controller.exportar_tabla(id_pedido, "pedido", bbdd)

        def eliminar_pedi(valores, bbdd):
            id_pedido = valores[0]
            print(f"Se eliminará {id_pedido}")
            controller.eliminar_pedido_BD(id_pedido, bbdd)

        def mostrar_menu(evento):        # Manejar el evento del clic derecho
            try:
                item_id = self.tablaPedidos.identify_row(evento.y)  # Identificar la fila en la que se hizo click
                self.tablaPedidos.selection_set(item_id)  # Seleccionar la fila

                # Mostrar el menú contextual en la posición del cursor
                self.menu.post(evento.x_root, evento.y_root)
            except:
                pass
        
        
        # Asociar el click derecho al evento
        self.tablaPedidos.bind("<Button-3>", mostrar_menu)
        self.tablaPedidos.bind("<<TreeviewSelect>>", click_fila)

    def actualizar_tabla(self, bbdd):
        # Elimina todos los elementos del Treeview
        for item in self.tablaPedidos.get_children():
            self.tablaPedidos.delete(item)
        
        self.llenarTabla(bbdd)

    def programar(self, tipoPrograma, bbdd):
        pedido = self.pedido_seleccionado
        if pedido == None:
            ventanas_emergentes.messagebox.showerror("Programar vehiculos", "Aún no ha seleccionado un pedido para programar")
            return
        controller.recoge_check_tecnicos() 
        controller.abrirFechayHoraProg(tipoPrograma, pedido, bbdd)
        #ventanas_emergentes.desea_exportar(eventos.nombraArchivoExcel(tipoPrograma))
