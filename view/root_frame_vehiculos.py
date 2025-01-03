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

class ContenidoVehiculos():

    def __init__(self, contenedor):

        self.frameTablaVehiculos = ctk.CTkFrame(contenedor, bg_color=moradoMedio)
        self.frameTablaVehiculos.pack(fill="both", expand=True, padx=5,)


        # Estilo personalizado para Treeview
        self.styletreeviewVeh = ttk.Style()

        # Cambiar el color de fondo y el color de la fuente para Treeview
        self.styletreeviewVeh.configure("TreeviewVehiculos", background=grisOscuro, foreground=blancoHueso, rowheight=25, fieldbackground=grisMedio, font=texto1Minimo)

        # Cambiar el color de selección
        self.styletreeviewVeh.map("TreeviewVehiculos", background=[("selected", moradoClaro)], foreground=[("selected", moradoOscuro)])

        self.canvas = ctk.CTkCanvas(self.frameTablaVehiculos, bg=grisOscuro)
        self.canvas.pack(side='left', fill='both', expand=True)
        self.frameTablaVehiculos.update_idletasks()
        self.canvas.config(width=self.frameTablaVehiculos.winfo_width(), height=self.frameTablaVehiculos.winfo_height())

class FiltrosVehiculos():

    def __init__(self, treeVehiculos, contenido, bbdd):
    # Crear un frame para los filtros
        self.frame_filtros = tk.Frame(contenido.canvas, bg=grisOscuro)
        self.frame_filtros.pack(fill=tk.X, padx=2, pady=2, side="top")

    # Crear entradas de texto para los filtros
        self.entry_chasis = ctk.CTkEntry(self.frame_filtros, fg_color=moradoMedio, text_color=blancoHueso)
        self.entry_chasis.grid(row=1, column=0, padx=5)
        self.entry_fecha = ctk.CTkEntry(self.frame_filtros, fg_color=moradoMedio, text_color=blancoHueso)
        self.entry_fecha.grid(row=1, column=1, padx=5)
        self.entry_marcamodelo = ctk.CTkEntry(self.frame_filtros, fg_color=moradoMedio, text_color=blancoHueso)
        self.entry_marcamodelo.grid(row=1, column=2, padx=5)
        self.entry_color = ctk.CTkEntry(self.frame_filtros, fg_color=moradoMedio, text_color=blancoHueso)
        self.entry_color.grid(row=1, column=3, padx=5)
        self.entry_proceso = ctk.CTkEntry(self.frame_filtros, fg_color=moradoMedio, text_color=blancoHueso)
        self.entry_proceso.grid(row=1, column=4, padx=5)
        self.entry_estado = ctk.CTkEntry(self.frame_filtros, fg_color=moradoMedio, text_color=blancoHueso)
        self.entry_estado.grid(row=1, column=5, padx=5)
        self.entry_novedades = ctk.CTkEntry(self.frame_filtros, fg_color=moradoMedio, text_color=blancoHueso)
        self.entry_novedades.grid(row=1, column=6, padx=5)
        self.entry_subcontratar = ctk.CTkEntry(self.frame_filtros, fg_color=moradoMedio, text_color=blancoHueso)
        self.entry_subcontratar.grid(row=1, column=7, padx=5)
        self.entry_pedido = ctk.CTkEntry(self.frame_filtros, fg_color=moradoMedio, text_color=blancoHueso)
        self.entry_pedido.grid(row=1, column=8, padx=5)

        # Configurar el peso de las columnas para que se expandan
        for i in range(9): 
            self.frame_filtros.grid_columnconfigure(i, weight=1)


        # Crear un botón para aplicar los filtros
        self.boton_filtrar = ctk.CTkButton(master=self.frame_filtros, text="Filtro", command=lambda:self.filtrar_datos(treeVehiculos), width=20,
                                           font=numerosPequeños, hover_color=grisVerdeClaro, fg_color=grisVerdeMedio, corner_radius=15)
        self.boton_filtrar.grid(row=0, column=0, pady=5)
    
        self.boton_actualizar = ctk.CTkButton(master=self.frame_filtros, text="Actualizar", command=lambda:treeVehiculos.actualizar_tabla(bbdd), width=20,
                                              font=numerosPequeños, hover_color=amarilloMedio, fg_color=amarilloOscuro, corner_radius=15)
        self.boton_actualizar.grid(row=0, column=1, pady=5)

    def filtrar_datos(self, treeVehiculos):
        # Obtener los criterios de filtro de las entradas
        self.datos          = treeVehiculos.datos
        filtro_chasis       = self.entry_chasis.get()
        filtro_fecha        = self.entry_fecha.get()
        filtro_marcamodelo  = self.entry_marcamodelo.get()
        filtro_color        = self.entry_color.get()
        filtro_proceso      = self.entry_proceso.get()
        filtro_estado       = self.entry_estado.get()
        filtro_novedades    = self.entry_novedades.get()
        filtro_subcontratar = self.entry_subcontratar.get()
        filtro_pedido       = self.entry_pedido.get()

        # Limpiar la tabla
        for row in treeVehiculos.tablaVehiculos.get_children():
            treeVehiculos.tablaVehiculos.delete(row)
        
        # Agregar datos filtrados a la tabla
        for record in self.datos:
            if (filtro_chasis.lower() in str(record[0]).lower() and
                filtro_fecha.lower() in str(record[1]).lower() and
                filtro_marcamodelo.lower() in str(record[2]).lower() and
                filtro_color.lower() in str(record[3]).lower() and
                filtro_proceso.lower() in str(record[4]).lower() and
                filtro_estado.lower() in str(record[5]).lower() and
                filtro_novedades.lower() in str(record[6]).lower() and
                filtro_subcontratar.lower() in str(record[7]).lower() and
                filtro_pedido.lower() in str(record[8]).lower()):

                treeVehiculos.tablaVehiculos.insert(parent='', index='end', iid=record[0], text='', values=record)

class TablaVehiculos():     #Tabla para pedido
    def __init__(self, contenido, contenedor, laRaiz, bbdd): #Crea latabla y un diccionario con los nombres de los campos

        self.raiz = laRaiz
         #Crear estilo personalizado para las cabeceras
        self.styletreeviewVeh = ttk.Style()
        self.styletreeviewVeh.configure("TreeviewVehiculos.Heading", foreground=moradoMedio, font=texto1Minimo)
        
        #Crear Tabla
        self.styletreeviewVeh.layout("TreeviewVehiculos", [('Treeview.treearea', {'sticky': 'nswe'})])
        print(self.styletreeviewVeh.theme_names())          # Lista los temas disponibles
        print(self.styletreeviewVeh.layout("TreeviewVehiculos"))  # Verifica si el estilo está configurado correctamente
        self.tablaVehiculos = ttk.Treeview(contenido.canvas, show="headings", style="TreeviewVehiculos")
        self.tablaVehiculos["columns"] = ("Chasis", "Fecha de entrega", "Marca - Modelo", "Color", "Proceso", "Estado","Novedades", "Subcontratar", "Pedido")

        # Formatear las columnas
        for col in self.tablaVehiculos["columns"]:
            self.tablaVehiculos.column(col, anchor=tk.CENTER, width=80)
            self.tablaVehiculos.heading(col, text=col, anchor=tk.CENTER)

        #Crear una barra de desplazamiento para la tabla y configurarla
        self.scrollbarTablaVehiculos = ttk.Scrollbar(contenido.frameTablaVehiculos, orient=tk.VERTICAL, command=self.tablaVehiculos.yview)
        self.tablaVehiculos.configure(yscrollcommand=self.scrollbarTablaVehiculos.set)
        self.tablaVehiculos.pack(expand=True, fill="both", side="bottom")
        self.scrollbarTablaVehiculos.pack(side='right', fill='y')
        self.llenarTabla(bbdd)

        self.frameBotonesVehiculos = ctk.CTkFrame(contenedor, bg_color=moradoMedio)
        self.frameBotonesVehiculos.pack(fill="both", side="bottom")

        #Botones de programar pedido
        self.botonProgramarTodo = ctk.CTkButton(master=self.frameBotonesVehiculos ,text="Programar TODO",
                                                font=textoGrande, hover_color=amarilloOscuro, fg_color=naranjaOscuro, border_color = blancoFrio,
                                                corner_radius=20, command=lambda:self.programar("completo", bbdd), width=60)
        self.botonProgramarTodo.pack(fill=tk.X, side="left", padx=15, pady=5)

        self.botonProgramarInmediato = ctk.CTkButton(master=self.frameBotonesVehiculos, text="Programar INMEDIATO",
                                                     font=textoGrande, hover_color=amarilloOscuro, fg_color=naranjaOscuro, border_color = blancoFrio,
                                                     corner_radius=20, command=lambda:self.programar("inmediato", bbdd), width=60)
        self.botonProgramarInmediato.pack(fill=tk.X, side="left", padx=15, pady=5)

        self.botonProgramarPorProcesos= ctk.CTkButton(master=self.frameBotonesVehiculos, text="Programar POR PROCESO",
                                                      font=textoGrande, hover_color=amarilloOscuro, fg_color=naranjaOscuro, border_color = blancoFrio,
                                                     corner_radius=20, command=lambda:self.programar("procesos", bbdd), width=60)
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
        self.datos = BBDD.leer_vehiculos_completos_df(bbdd)
        print(self.datos)
        for index, row in self.datos.iterrows():
            self.tablaVehiculos.insert(parent='', index='end', iid=row['CHASIS'], text='', values=row.tolist())

        # Función para obtener el texto del tooltip
        def obtener_texto_tooltip(iid):
            
            valores = self.tablaVehiculos.item(iid, 'values')
            lecturaRegistros = BBDD.leer_historico_chasis(bbdd, valores[0])
            
            if lecturaRegistros == None:
                return f"Chasis: {valores[0]}\nSin procesos ejecutados"
            
            procesos_estados = [(registro[3], registro[8]) for registro in lecturaRegistros]
            mensaje = "".join([f"\n{proceso}. {estado}" for proceso, estado in procesos_estados])

            return f"Chasis: {valores[0]}\nProcesos: {mensaje}"

        # Añadir tooltips a las filas
        controller.Tooltip(self.tablaVehiculos, obtener_texto_tooltip)

        #click derecho en información de vehículo       
        def seleccionar_informacion_fila():
            fila = self.tablaVehiculos.selection()     #obtener el item seleccionado
            print("Asignar seleccionada")
            if fila:
                valores = self.tablaVehiculos.item(fila, 'values')     #obtener los valores de la fila
                print(valores)
                informacion_vh(valores, bbdd)

        #click derecho en asignar vehiculo
        def seleccionar_asignar_fila():
            fila = self.tablaVehiculos.selection()     #obtener el item seleccionado
            print("Asignar seleccionada")
            if fila:
                valores = self.tablaVehiculos.item(fila, 'values')     #obtener los valores de la fila
                chasis = valores[0]
                print(f"asignará el vehiculo  {valores}")
                print(chasis, bbdd)
                controller.ventana_AsignarUnVehiculo(chasis, bbdd)

        #click derecho en modificar fila
        def seleccionar_modificar_fila():
            fila = self.tablaVehiculos.selection()     #obtener el item seleccionado
            print("Modificar seleccionada")
            if fila:
                valores = self.tablaVehiculos.item(fila, 'values')     #obtener los valores de la fila
                print(valores)
                modificar_vh(valores, bbdd)

        #click derecho en eliminar fila
        def seleccionar_eliminar_fila():
            fila = self.tablaVehiculos.selection()     #obtener el item seleccionado
            print("Eliminar seleccionada")
            if fila:
                valores = self.tablaVehiculos.item(fila, 'values')     #obtener los valores de la fila
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
            chasis = valores[0]
            print(f"Se eliminará {chasis}")
            controller.eliminar_VH_pedido(chasis)

        def modificar_vh(valores, bbdd):
            chasis_anterior = valores[0]
            print(f"modificará el chasis {chasis_anterior}")
            controller.modificar_datos_vehiculo(chasis_anterior, bbdd)

        def informacion_vh(valores, bbdd):
            chasis = valores[0]
            print(f"solicitó información de {chasis}")
            controller.ventana_infoVehiculo(chasis, bbdd)

        def mostrar_menu(evento):        # Manejar el evento del clic derecho
            try:
                item_id = self.tablaVehiculos.identify_row(evento.y)  # Identificar la fila en la que se hizo click
                self.tablaVehiculos.selection_set(item_id)  # Seleccionar la fila

                # Mostrar el menú contextual en la posición del cursor
                self.menu.post(evento.x_root, evento.y_root)
            except:
                pass
        
        # Asociar el click derecho al evento
        self.tablaVehiculos.bind("<Button-3>", mostrar_menu)

    def actualizar_tabla(self, bbdd):
        # Elimina todos los elementos del Treeview
        for item in self.tablaVehiculos.get_children():
            self.tablaVehiculos.delete(item)
        
        self.llenarTabla(bbdd)

    def programar(self, tipoPrograma, bbdd):
        vehiculos = self.vehiculos_seleccionados
        if vehiculos == None:
            ventanas_emergentes.messagebox.showerror("Programar vehiculos", "Aún no has seleccionado vehiculos para programar")
            return
        controller.recoge_check_tecnicos()
        controller.abrirFechayHoraProg(tipoPrograma, bbdd)
        ventanas_emergentes.desea_exportar(controller.nombraArchivoExcel(tipoPrograma))
