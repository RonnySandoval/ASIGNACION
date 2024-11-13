import  tkinter as tk
from    tkinter import ttk
import customtkinter as ctk
import  eventos as eventos
from    estilos import *
import BBDD

# Configuración global del estilo de customtkinter
ctk.set_appearance_mode("dark")  # Modo oscuro por defecto
ctk.set_default_color_theme("dark-blue")  # Colores por defecto con tonos azulados



class ContenidoHistoricos():
    def __init__(self, contenedor):


        self.frameTablaHistoricos = ctk.CTkFrame(contenedor, bg_color=rojoMedio)
        self.frameTablaHistoricos.pack(fill="both", expand=True, padx=5,)


        # Estilo personalizado para Treeview
        self.styletreeviewHis = ttk.Style()

        # Cambiar el color de fondo y el color de la fuente para Treeview
        self.styletreeviewHis.configure("TreeviewHistoricos", background=grisOscuro, foreground=blancoHueso, rowheight=25, fieldbackground=grisMedio, font=texto1Minimo)

        # Cambiar el color de selección
        self.styletreeviewHis.map("TreeviewHistoricos", background=[("selected", rojoClaro)], foreground=[("selected", rojoOscuro)])

        self.canvas = ctk.CTkCanvas(self.frameTablaHistoricos, bg=grisOscuro)
        self.canvas.pack(side='left', fill='both', expand=True)
        self.frameTablaHistoricos.update_idletasks()
        self.canvas.config(width=self.frameTablaHistoricos.winfo_width(), height=self.frameTablaHistoricos.winfo_height())

class FiltrosHistoricos():
    def __init__(self, historicos, contenido, bbdd):
    # Crear un frame para los filtros
        self.frame_filtros = tk.Frame(contenido.canvas, bg=grisOscuro)
        self.frame_filtros.pack(fill=tk.X, padx=2, pady=2, side="top")

    # Crear entradas de texto para los filtros
        self.entry_id = ctk.CTkEntry(self.frame_filtros, fg_color=rojoOscuro, text_color=blancoHueso)
        self.entry_id.grid(row=1, column=0, padx=5)    
        self.entry_chasis = ctk.CTkEntry(self.frame_filtros, fg_color=rojoOscuro, text_color=blancoHueso)
        self.entry_chasis.grid(row=1, column=1, padx=5)
        self.entry_tecnico = ctk.CTkEntry(self.frame_filtros, fg_color=rojoOscuro, text_color=blancoHueso)
        self.entry_tecnico.grid(row=1, column=2, padx=5)        
        self.entry_proceso = ctk.CTkEntry(self.frame_filtros, fg_color=rojoOscuro, text_color=blancoHueso)
        self.entry_proceso.grid(row=1, column=3, padx=5)
        self.entry_marcamodelo = ctk.CTkEntry(self.frame_filtros, fg_color=rojoOscuro, text_color=blancoHueso)
        self.entry_marcamodelo.grid(row=1, column=4, padx=5)
        self.entry_color = ctk.CTkEntry(self.frame_filtros, fg_color=rojoOscuro, text_color=blancoHueso)
        self.entry_color.grid(row=1, column=5, padx=5)
        self.entry_inicio = ctk.CTkEntry(self.frame_filtros, fg_color=rojoOscuro, text_color=blancoHueso)
        self.entry_inicio.grid(row=1, column=6, padx=5)
        self.entry_fin = ctk.CTkEntry(self.frame_filtros, fg_color=rojoOscuro, text_color=blancoHueso)
        self.entry_fin.grid(row=1, column=7, padx=5)
        self.entry_duracion = ctk.CTkEntry(self.frame_filtros, fg_color=rojoOscuro, text_color=blancoHueso)
        self.entry_duracion.grid(row=1, column=8, padx=5)
        self.entry_estado = ctk.CTkEntry(self.frame_filtros, fg_color=rojoOscuro, text_color=blancoHueso)
        self.entry_estado.grid(row=1, column=9, padx=5)
        self.entry_novedades = ctk.CTkEntry(self.frame_filtros, fg_color=rojoOscuro, text_color=blancoHueso)
        self.entry_novedades.grid(row=1, column=10, padx=5)
        self.entry_observaciones = ctk.CTkEntry(self.frame_filtros, fg_color=rojoOscuro, text_color=blancoHueso)
        self.entry_observaciones.grid(row=1, column=11, padx=5)
        self.entry_subcontratar = ctk.CTkEntry(self.frame_filtros, fg_color=rojoOscuro, text_color=blancoHueso)
        self.entry_subcontratar.grid(row=1, column=12, padx=5)
        self.entry_pedido = ctk.CTkEntry(self.frame_filtros, fg_color=rojoOscuro, text_color=blancoHueso)
        self.entry_pedido.grid(row=1, column=13, padx=5)


        # Configurar el peso de las columnas para que se expandan
        for i in range(14): 
            self.frame_filtros.grid_columnconfigure(i, weight=1)


        # Crear un botón para aplicar los filtros
        self.boton_filtrar = ctk.CTkButton(master=self.frame_filtros, text="Filtro", command=lambda:self.filtrar_datos(historicos), width=20,
                                           font=numerosPequeños, hover_color=grisVerdeClaro, fg_color=grisVerdeMedio, corner_radius=15)
        self.boton_filtrar.grid(row=0, column=0, pady=5)
    
        self.boton_actualizar = ctk.CTkButton(master=self.frame_filtros, text="Actualizar", command=lambda:historicos.actualizar_tabla(bbdd), width=20,
                                              font=numerosPequeños, hover_color=amarilloMedio, fg_color=amarilloOscuro, corner_radius=15)
        self.boton_actualizar.grid(row=0, column=1, pady=5)

    def filtrar_datos(self, historicos):
        # Obtener los criterios de filtro de las entradas
        self.datos          = historicos.datos
        filtro_id     = self.entry_id.get()
        filtro_chasis       = self.entry_chasis.get()
        filtro_tecnico      = self.entry_tecnico.get()
        filtro_proceso      = self.entry_proceso.get()
        filtro_marcamodelo  = self.entry_marcamodelo.get()
        filtro_color        = self.entry_color.get()
        filtro_inicio       = self.entry_inicio.get()
        filtro_fin          = self.entry_fin.get()
        filtro_duracion     = self.entry_duracion.get()
        filtro_estado       = self.entry_estado.get()
        filtro_novedades    = self.entry_novedades.get()
        filtro_observaciones= self.entry_observaciones.get()
        filtro_subcontratar = self.entry_subcontratar.get()
        filtro_pedido       = self.entry_pedido.get()

        # Limpiar la tabla
        for row in historicos.tablaHistoricos.get_children():
            historicos.tablaHistoricos.delete(row)
        
        # Agregar datos filtrados a la tabla
        for record in self.datos:
            if (filtro_id.lower()           in str(record[0]).lower() and
                filtro_chasis.lower()       in str(record[1]).lower() and
                filtro_tecnico.lower()      in record[2].lower() and
                filtro_proceso.lower()      in record[3].lower() and
                filtro_marcamodelo.lower()  in record[4].lower() and
                filtro_color.lower()        in record[5].lower() and
                filtro_inicio.lower()       in record[6].lower() and
                filtro_fin.lower()          in record[7].lower() and
                filtro_duracion.lower()     in str(record[8]).lower() and
                filtro_estado.lower()       in record[9].lower() and
                filtro_novedades.lower()    in record[10].lower() and
                filtro_observaciones.lower()in record[11].lower() and
                filtro_subcontratar.lower() in record[12].lower() and
                filtro_pedido.lower()       in record[13].lower()):

                historicos.tablaHistoricos.insert(parent='', index='end', iid=record[0], text='', values=record)

class TablaHistoricos():        #Tabla para historicos
    def __init__(self, contenido, contenedor, laRaiz, bbdd): #Crea latabla y un diccionario con los nombres de los campos

        self.raiz = laRaiz
         #Crear estilo personalizado para las cabeceras
        self.styletreeviewHis = ttk.Style()
        self.styletreeviewHis.configure("TreeviewHistoricos.Heading", foreground=rojoOscuro, font=texto1Minimo)

        
        #Crear Tabla
        self.styletreeviewHis.layout("TreeviewHistoricos", [('Treeview.treearea', {'sticky': 'nswe'})])
        self.tablaHistoricos = ttk.Treeview(contenido.canvas, show="headings", style="TreeviewHistoricos")
        self.tablaHistoricos["columns"] = ("Id",
                                           "Chasis",
                                           "Tecnico",
                                           "Proceso",
                                           "Marca - Modelo",
                                           "Color",
                                           "Inicio",
                                           "Fin",
                                           "Duracion",
                                           "Estado",
                                           "Novedades",
                                           "Observaciones",
                                           "Subcontratar",
                                           "Pedido")

        # Formatear las columnas
        for col in self.tablaHistoricos["columns"]:
            self.tablaHistoricos.column(col, anchor=tk.CENTER, width=80)
            self.tablaHistoricos.heading(col, text=col, anchor=tk.CENTER)




# Crear un Scrollbar y conectarlo con el Canvas

        #Crear una barra de desplazamiento para la tabla y configurarla
        self.scrollbarTablaHistoricos = ttk.Scrollbar(contenido.frameTablaHistoricos, orient=tk.VERTICAL, command=self.tablaHistoricos.yview)
        self.scrollbarTablaHistoricos.pack(side='right', fill='y')
        self.tablaHistoricos.configure(yscrollcommand=self.scrollbarTablaHistoricos.set)
        self.tablaHistoricos.pack(expand=True, fill="both", side="bottom")

        self.llenarTabla(bbdd)

    def llenarTabla(self, bbdd):    # Agregar datos a la tabla 
        self.datos = BBDD.leer_historicos_completo(bbdd)
        print(self.datos)
        for record in self.datos:
            self.tablaHistoricos.insert(parent='', index='end', iid=record[0], text='', values=record)

        #click derecho en información de vehículo       
        def seleccionar_resumen_fila():
            fila = self.tablaHistoricos.selection()     #obtener el item seleccionado
            print("Asignar seleccionada")
            if fila:
                valores = self.tablaHistoricos.item(fila, 'values')     #obtener los valores de la fila
                print(valores)
                resumen_hist(valores, bbdd)

        #click derecho en asignar vehiculo
        def seleccionar_cambiar_fila():
            fila = self.tablaHistoricos.selection()     #obtener el item seleccionado
            print("Asignar seleccionada")
            if fila:
                valores = self.tablaHistoricos.item(fila, 'values')     #obtener los valores de la fila
                print(valores)
                cambiar_hist(valores, bbdd)

        #click derecho en modificar fila
        def seleccionar_modificar_fila():
            fila = self.tablaHistoricos.selection()     #obtener el item seleccionado
            print("Modificar seleccionada")
            if fila:
                valores = self.tablaHistoricos.item(fila, 'values')     #obtener los valores de la fila
                print(valores)
                modificar_hist(valores, bbdd)

        def seleccionar_anadir_fila():
            fila = self.tablaHistoricos.selection()     #obtener el item seleccionado
            print("Añadir novedad/observación seleccionada")
            if fila:
                valores = self.tablaHistoricos.item(fila, 'values')     #obtener los valores de la fila
                print(valores)
                anadirNovObs_hist(valores)

        #click derecho en eliminar fila
        def seleccionar_eliminar_fila():
            fila = self.tablaHistoricos.selection()     #obtener el item seleccionado
            print("Eliminar seleccionada")
            if fila:
                valores = self.tablaHistoricos.item(fila, 'values')     #obtener los valores de la fila
                print(valores)
                eliminar_hist(valores, bbdd)       
        
        #CREAR MENU CONTEXTUAL
        self.menu = tk.Menu(self.raiz, tearoff=0)
        self.menu.add_command(label="Resumen", command = seleccionar_resumen_fila)
        self.menu.add_command(label="Cambiar Estado", command = seleccionar_cambiar_fila)
        self.menu.add_command(label="Modificar", command = seleccionar_modificar_fila)
        self.menu.add_command(label="Añadir Observación/Novedad", command = seleccionar_anadir_fila)
        self.menu.add_command(label="Eliminar", command = seleccionar_eliminar_fila)
        
        #Opciones del menú del click derecho

        def resumen_hist(valores, bbdd):
            id_historico = valores[0]
            print(f"solicitó información de {valores}")
            eventos.ventanaResumenHistorico(id_historico, bbdd)

        def cambiar_hist(valores, bbdd):
            id_historico = valores[0]
            print(f"cambiará el estado del histórico {valores}")
            eventos.ventanaCambiarEstado(id_historico, bbdd)

        def modificar_hist(valores, bbdd):
            id_anterior = valores[0]
            print(f"modificará el histórico {valores}")
            eventos.ventana_modificarHistorico(id_anterior, bbdd)

        def anadirNovObs_hist(valores):
            id_historico = valores[0]
            print(f"asignará el vehiculo con chasis {valores}")
            eventos.ventana_ObserNoved(valores)
            
        def eliminar_hist(valores, bbdd):
            id_historico = valores[0]
            print(f"Se eliminará el histórico {valores}")
            eventos.ventana_eliminarHistorico(id_historico)


        # Manejar el evento del clic derecho
        def mostrar_menu(evento):
            try:
                item_id = self.tablaHistoricos.identify_row(evento.y)  # Identificar la fila en la que se hizo click
                self.tablaHistoricos.selection_set(item_id)  # Seleccionar la fila

                # Mostrar el menú contextual en la posición del cursor
                self.menu.post(evento.x_root, evento.y_root)
            except:
                pass
        
        
        # Asociar el click derecho al evento
        self.tablaHistoricos.bind("<Button-3>", mostrar_menu)

    def actualizar_tabla(self, bbdd):
        # Elimina todos los elementos del Treeview
        for item in self.tablaHistoricos.get_children():
            self.tablaHistoricos.delete(item)
        
        self.llenarTabla(bbdd)