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


class ContenidoProgramas():

    def __init__(self, contenedor):

        self.frameTablaProgramas = ctk.CTkFrame(contenedor, bg_color=grisVerdeOscuro)
        self.frameTablaProgramas.pack(fill="both", expand=True, side="left", padx=5,)

        # Estilo personalizado para Treeview
        self.styletreeviewProg = ttk.Style()

        # Cambiar el color de fondo y el color de la fuente para Treeview
        self.styletreeviewProg.configure("TreeviewProgramas", background=grisOscuro, foreground=blancoHueso, rowheight=25, fieldbackground=grisMedio, font=texto1Minimo)

        # Cambiar el color de selección
        self.styletreeviewProg.map("TreeviewProgramas", background=[("selected",verdeClaro)], foreground=[("selected", verdeOscuro)])

        self.canvas = ctk.CTkCanvas(self.frameTablaProgramas, bg=grisOscuro)
        self.canvas.pack(side='left', fill='both', expand=True)
        self.frameTablaProgramas.update_idletasks()
        self.canvas.config(width=self.frameTablaProgramas.winfo_width(), height=self.frameTablaProgramas.winfo_height())

class FiltrosProgramas():

    def __init__(self, treeProgramas, contenido, bbdd):
    # Crear un frame para los filtros
        self.frame_filtros = tk.Frame(contenido.canvas, bg=grisOscuro)
        self.frame_filtros.pack(fill=tk.X, padx=2, pady=2, side="top")

    # Crear entradas de texto para los filtros
        self.entry_id_programa = ctk.CTkEntry(self.frame_filtros, fg_color=verdeMedio, text_color=blancoHueso)
        self.entry_id_programa.grid(row=1, column=0, padx=5)
        self.entry_descricion = ctk.CTkEntry(self.frame_filtros, fg_color=verdeMedio, text_color=blancoHueso)
        self.entry_descricion.grid(row=1, column=1, padx=5)

        # Configurar el peso de las columnas para que se expandan
        for i in range(2): 
            self.frame_filtros.grid_columnconfigure(i, weight=1)

        # Crear un botón para aplicar los filtros
        self.boton_filtrar = ctk.CTkButton(master=self.frame_filtros, text="Filtro", command=lambda:self.filtrar_datos(treeProgramas), width=20,
                                           font=numerosPequeños, hover_color=grisVerdeClaro, fg_color=grisVerdeMedio, corner_radius=15)
        self.boton_filtrar.grid(row=0, column=0, pady=5)
    
        self.boton_actualizar = ctk.CTkButton(master=self.frame_filtros, text="Actualizar", command=lambda:treeProgramas.actualizar_tabla(bbdd), width=20,
                                              font=numerosPequeños, hover_color=amarilloMedio, fg_color=amarilloOscuro, corner_radius=15)
        self.boton_actualizar.grid(row=0, column=1, pady=5)

    def filtrar_datos(self, treeProgramas):
        treeProgramas.tablaProgramas.unbind("<<TreeviewSelect>>")
        # Obtener los criterios de filtro de las entradas
        self.datos             = treeProgramas.datos
        filtro_id_programa       = self.entry_id_programa.get()
        filtro_descripcion   = self.entry_descricion.get()

        print("datos del contenido de Programas: ", self.datos)
        print("Datos de los entry en filtrar_datos:", filtro_id_programa, filtro_descripcion)
        # Limpiar la tabla
        for row in treeProgramas.tablaPedidos.get_children():
            treeProgramas.tablaPedidos.delete(row)
        
        # Agregar datos filtrados a la tabla
        for record in self.datos:
            if (filtro_id_programa.lower()      in str(record[0]).lower() and
                filtro_descripcion.lower()  in str(record[1]).lower()):

                treeProgramas.tablaPedidos.insert(parent='', index='end', iid=record[0], text='', values=record)

            treeProgramas.tablaPedidos.bind("<<TreeviewSelect>>")


class TablaProgramas():     #Tabla para pedido
    def __init__(self, contenido, contenedor, laRaiz, bbdd): #Crea latabla y un diccionario con los nombres de los campos

        self.raiz = laRaiz
         #Crear estilo personalizado para las cabeceras
        self.styletreeviewProg = ttk.Style()
        self.styletreeviewProg.configure("TreeviewProgramas.Heading", foreground=grisVerdeOscuro, font=texto1Minimo)
        
        #Crear Tabla
        self.styletreeviewProg.layout("TreeviewProgramas", [('Treeview.treearea', {'sticky': 'nswe'})])
        self.tablaProgramas = ttk.Treeview(contenido.canvas, show="headings", style="TreeviewProgramas")
        self.tablaProgramas["columns"] = ("Id Programa", "Pedido")

        # Formatear las columnas
        for col in self.tablaProgramas["columns"]:
            self.tablaProgramas.column(col, anchor="w", width=80)
            self.tablaProgramas.heading(col, text=col, anchor=tk.CENTER)

        # Crear un Scrollbar y conectarlo con el Canvas

        #Crear una barra de desplazamiento para la tabla y configurarla
        self.scrollbarTablaProgramas = ttk.Scrollbar(contenido.frameTablaProgramas, orient=tk.VERTICAL, command=self.tablaProgramas.yview)
        self.tablaProgramas.configure(yscrollcommand=self.scrollbarTablaProgramas.set)
        self.tablaProgramas.pack(expand=True, fill="both", side="bottom")
        self.scrollbarTablaProgramas.pack(side='right', fill='y')

        self.programa_seleccionado = None
        self.llenarTabla(bbdd)

        self.frameCheckProcesos = ctk.CTkFrame(contenedor, bg_color=verdeMedio)
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
        self.lectura = list(BBDD.leer_programas(bbdd))
        self.datos = [(id, id_pedido) for id, desc, consec, id_pedido  in self.lectura]
        print(self.datos)
        for record in self.datos:
            self.tablaProgramas.insert(parent='', index='end', iid=record[0], text='', values=record)

        def click_fila(event):
            tabla = event.widget
            filas_seleccionadas = tabla.selection()
            print("filas seleccionadas con click_fila:", filas_seleccionadas)
            datos = tabla.item(filas_seleccionadas[0], "values")
            print(datos)
            programa = datos[0]
            print(programa)
            self.programa_seleccionada = programa
            glo.pedido_seleccionado = programa
            glo.stateFrame.tablaOrdenes.llenarTabla(bbdd, programa = programa)

        #click derecho en información de vehículo       
        def seleccionar_informacion_fila():
            fila = self.tablaProgramas.selection()     #obtener el item seleccionado
            print("Información de programa seleccionada")
            if fila:
                valores = self.tablaProgramas.item(fila, 'values')     #obtener los valores de la fila
                print(valores)
                informacion_programa(valores, bbdd)

        #click derecho en modificar fila
        def seleccionar_gantt_fila():
            fila = self.tablaProgramas.selection()     #obtener el item seleccionado
            print("Gantt de programa seleccionada")
            if fila:
                valores = self.tablaProgramas.item(fila, 'values')     #obtener los valores de la fila
                print(valores)
                gantt_programa(valores, bbdd)

        #click derecho en eliminar fila
        def seleccionar_eliminar_fila():
            fila = self.tablaProgramas.selection()     #obtener el item seleccionado
            print("Eliminar programa seleccionada")
            if fila:
                valores = self.tablaProgramas.item(fila, 'values')     #obtener los valores de la fila
                print(valores)
                eliminar_programa(valores, bbdd)       
        
        #CREAR MENU CONTEXTUAL
        self.menu = tk.Menu(self.raiz, tearoff=0)
        self.menu.add_command(label="Información", command = seleccionar_informacion_fila)
        self.menu.add_command(label="Gantt", command = seleccionar_gantt_fila)
        self.menu.add_command(label="Eliminar", command = seleccionar_eliminar_fila)
        
        #Opciones del menú del click derecho
        def informacion_programa(valores, bbdd):
            id_programa = valores[0]
            print(f"solicitó información de {id_programa}")
            eventos.ventana_infoVehiculo(id_programa, bbdd)
        
        def gantt_programa(valores, bbdd):
            id_programa = valores[0]
            print(f"modificará el chasis {id_programa}")
            eventos.mostrar_gantt_programa(id_programa, bbdd)

        def eliminar_programa(valores, bbdd):
            id_programa = valores[0]
            print(f"Se eliminará {id_programa}")
            eventos.eliminar_programa_BD(id_programa, bbdd)

        def mostrar_menu(evento):        # Manejar el evento del clic derecho
            try:
                item_id = self.tablaProgramas.identify_row(evento.y)  # Identificar la fila en la que se hizo click
                self.tablaProgramas.selection_set(item_id)  # Seleccionar la fila

                # Mostrar el menú contextual en la posición del cursor
                self.menu.post(evento.x_root, evento.y_root)
            except:
                pass
        

        # Asociar el click derecho al evento
        self.tablaProgramas.bind("<Button-3>", mostrar_menu)
        self.tablaProgramas.bind("<<TreeviewSelect>>", click_fila)

    def actualizar_tabla(self, bbdd):
        # Elimina todos los elementos del Treeview
        for item in self.tablaProgramas.get_children():
            self.tablaProgramas.delete(item)
        
        self.llenarTabla(bbdd)
