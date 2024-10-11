import  tkinter as tk
from    tkinter import ttk
import  CRUD as CRUD
import  eventos as eventos
import  re
import  dicc_variables
from    estilos import *
import  Mod_clases
import  Mod_objetos
import  Graficador
import  ventanas_emergentes
import  menu




class ContenidoPedidos():

    def __init__(self, contenedor):


        self.frameTablaPedido = tk.Frame(contenedor)
        self.frameTablaPedido.pack(fill="both", expand=True, padx=5,)


        # Estilo personalizado para Treeview
        self.styletreeview = ttk.Style()

        # Cambiar el color de fondo y el color de la fuente para Treeview
        self.styletreeview.configure("Treeview", background=grisOscuro, foreground=blancoHueso, rowheight=25, fieldbackground=grisMedio, font=texto1Minimo)

        # Cambiar el color de selección
        self.styletreeview.map("Treeview", background=[("selected", azulClaro)], foreground=[("selected", moradoOscuro)])

        self.canvas = tk.Canvas(self.frameTablaPedido, bg=grisOscuro)
        self.canvas.pack(side='left', fill='both', expand=True)
        self.frameTablaPedido.update_idletasks()
        self.canvas.config(width=self.frameTablaPedido.winfo_width(), height=self.frameTablaPedido.winfo_height())


class FiltrosPedido():

    def __init__(self, pedido, contenido):
    # Crear un frame para los filtros
        self.frame_filtros = tk.Frame(contenido.canvas, bg=grisOscuro)
        self.frame_filtros.pack(fill=tk.X, padx=2, pady=2, side="top")

    # Crear entradas de texto para los filtros
        self.entry_chasis = tk.Entry(self.frame_filtros, bg=moradoMedio, fg=blancoHueso)
        self.entry_chasis.grid(row=1, column=0, padx=5)
        self.entry_fecha = tk.Entry(self.frame_filtros, bg=moradoMedio, fg=blancoHueso)
        self.entry_fecha.grid(row=1, column=1, padx=5)
        self.entry_marca = tk.Entry(self.frame_filtros, bg=moradoMedio, fg=blancoHueso)
        self.entry_marca.grid(row=1, column=2, padx=5)
        self.entry_modelo = tk.Entry(self.frame_filtros, bg=moradoMedio, fg=blancoHueso)
        self.entry_modelo.grid(row=1, column=3, padx=5)
        self.entry_color = tk.Entry(self.frame_filtros, bg=moradoMedio, fg=blancoHueso)
        self.entry_color.grid(row=1, column=4, padx=5)
        self.entry_estado = tk.Entry(self.frame_filtros, bg=moradoMedio, fg=blancoHueso)
        self.entry_estado.grid(row=1, column=5, padx=5)
        self.entry_tiempos = tk.Entry(self.frame_filtros, bg=moradoMedio, fg=blancoHueso)
        self.entry_tiempos.grid(row=1, column=6, padx=5)
        self.entry_novedades = tk.Entry(self.frame_filtros, bg=moradoMedio, fg=blancoHueso)
        self.entry_novedades.grid(row=1, column=7, padx=5)
        self.entry_subcontratar = tk.Entry(self.frame_filtros, bg=moradoMedio, fg=blancoHueso)
        self.entry_subcontratar.grid(row=1, column=8, padx=5)
        self.entry_subcontratar = tk.Entry(self.frame_filtros, bg=moradoMedio, fg=blancoHueso)
        self.entry_subcontratar.grid(row=1, column=9, padx=5)

        # Configurar el peso de las columnas para que se expandan
        for i in range(10):  # Suponiendo que hay 9 columnas
            self.frame_filtros.grid_columnconfigure(i, weight=1)


        # Crear un botón para aplicar los filtros
        self.boton_filtrar = tk.Button(self.frame_filtros, text="Filtro", command=lambda:self.filtrar_datos(pedido), font=numerosPequeños, bg=azulOscuro, fg=blancoHueso)
        self.boton_filtrar.grid(row=0, column=0)
    
        self.boton_actualizar = tk.Button(self.frame_filtros, text="Actualizar", command=lambda:pedido.actualizar_tabla(), font=numerosPequeños, bg=azulOscuro, fg=blancoHueso)
        self.boton_actualizar.grid(row=0, column=1)

    def filtrar_datos(self, pedido):
        # Obtener los criterios de filtro de las entradas
        self.datos = pedido.datos
        filtro_chasis = self.entry_chasis.get()
        filtro_fecha = self.entry_fecha.get()
        filtro_marca = self.entry_marca.get()
        filtro_modelo = self.entry_modelo.get()
        filtro_color = self.entry_color.get()
        filtro_estado = self.entry_estado.get()
        filtro_tiempos = self.entry_tiempos.get()
        filtro_novedades = self.entry_novedades.get()
        filtro_subcontratar = self.entry_subcontratar.get()
        
        # Limpiar la tabla
        for row in pedido.tablaPedidos.get_children():
            pedido.tablaPedidos.delete(row)
        
        # Agregar datos filtrados a la tabla
        for record in self.datos:
            if (filtro_chasis.lower() in str(record[0]).lower() and
                filtro_fecha.lower() in record[1].lower() and
                filtro_marca.lower() in str(record[2]).lower() and
                filtro_modelo.lower() in record[3].lower() and
                filtro_color.lower() in record[4].lower() and
                filtro_estado.lower() in record[5].lower() and
                filtro_tiempos.lower() in record[6].lower() and
                filtro_novedades.lower() in record[7].lower() and
                filtro_subcontratar.lower() in record[8].lower()):
                pedido.tablaPedidos.insert(parent='', index='end', iid=record[0], text='', values=record)


#Tabla para pedido
class TablaPedido():
    def __init__(self, contenido, contenedor, laRaiz): #Crea latabla y un diccionario con los nombres de los campos

        self.raiz = laRaiz
         #Crear estilo personalizado para las cabeceras
        self.styletreeview = ttk.Style()
        self.styletreeview.configure("Treeview.Heading", foreground=moradoMedio, font=texto1Minimo)

        
        #Crear Tabla
        self.tablaPedidos = ttk.Treeview(contenido.canvas, show="headings")
        self.tablaPedidos["columns"] = ("Chasis", "Fecha de entrega", "Marca", "Modelo", "Color", "Estado", "Tiempos", "Novedades", "Subcontratar", "Pedido")

        # Formatear las columnas
        for col in self.tablaPedidos["columns"]:
            self.tablaPedidos.column(col, anchor=tk.CENTER, width=80)
            self.tablaPedidos.heading(col, text=col, anchor=tk.CENTER)

        self.tablaPedidos.pack(expand=True, fill="both", padx=5)



# Crear un Scrollbar y conectarlo con el Canvas

        #Crear una barra de desplazamiento para la tabla y configurarla
        self.scrollbarTablaPedido = ttk.Scrollbar(contenido.frameTablaPedido, orient=tk.VERTICAL, command=self.tablaPedidos.yview)
        self.scrollbarTablaPedido.pack(side='right', fill='y')
        self.tablaPedidos.configure(yscrollcommand=self.scrollbarTablaPedido.set)
        #self.tablaPedidos.bind('<Configure>', lambda e: self.tablaPedidos.configure(scrollregion=self.tablaPedidos.bbox("all")))



        #empaquetar tabla de pedidos
        self.tablaPedidos.pack(expand=True, fill="both", side="bottom")
        self.llenarTabla()

        #Botones de programar pedido
        self.botonProgramarTodo = tk.Button(contenedor ,text="Programar TODO", font=textoGrande, bg=naranjaMedio, fg=blancoHueso, command=self.programar_todo)
        self.botonProgramarTodo.pack()

    #Botones de programar pedido
        self.botonProgramarInmediato = tk.Button(contenedor, text="Programar INMEDIATO", font=textoGrande, bg=naranjaMedio, fg=blancoHueso, command=self.programar_inmediato)
        self.botonProgramarInmediato.pack()        
   
   
    # Agregar datos a la tabla        
    def llenarTabla(self):
        self.datos = eventos.leepedidoBBDD()

        if self.datos is not None:
            # Modificamos la lista con datos para que agrupe los tiempos
            for i in range(len(self.datos)):
                registro = self.datos[i]                                                            # Convertir los elementos en las posiciones 6 a 10 a una tupla
                tupla_tiempos = tuple(registro[6:11])                                               # Crear una lista modificable con los elementos excepto los que van a ser reemplazados           
                registro_modificado = list(registro[:6])+ [tupla_tiempos] + list(registro[11:])     # Convertir la tupla a una cadena separada por comas
                registro_modificado[6] = ', '.join(map(str, tupla_tiempos))                         # Actualizar la lista original con el registro modificado
                self.datos[i] = registro_modificado                                                 # Asignar el registro modificado al atributo datos
                print(self.datos[i])

            for record in self.datos:
                self.tablaPedidos.insert(parent='', index='end', iid=record[0], text='', values=record)
        
        #click derecho en modificar fila
        def seleccionar_modificar_fila():
            fila = self.tablaPedidos.selection()     #obtener el item seleccionado
            print("Modificar seleccionada")
            if fila:
                valores = self.tablaPedidos.item(fila, 'values')     #obtener los valores de la fila
                print(valores)
                modificar_vh(valores, fila)

        #click derecho en eliminar fila
        def seleccionar_eliminar_fila():
            fila = self.tablaPedidos.selection()     #obtener el item seleccionado
            print("Eliminar seleccionada")
            if fila:
                valores = self.tablaPedidos.item(fila, 'values')     #obtener los valores de la fila
                print(valores)
                eliminar_vh(valores, fila)       
        
        #CREAR MENU CONTEXTUAL
        self.menu = tk.Menu(self.raiz, tearoff=0)
        self.menu.add_command(label="Modificar", command = seleccionar_modificar_fila)
        self.menu.add_command(label="Eliminar", command = seleccionar_eliminar_fila)
        
        
        #Opciones del menú del click derecho
        def eliminar_vh(valores, item):
            chasis = valores[0]
            print(f"Se eliminará {chasis}")
            eventos.eliminar_VH_pedido(chasis)


        def modificar_vh(valores, item):
            chasis_anterior = valores[0]
            print(f"el primer valor es {chasis_anterior}")
            ventana_auxiliar = eventos.modificar_vehiculo_pedido(chasis_anterior)


        # Manejar el evento del clic derecho
        def mostrar_menu(evento):
            try:
                item_id = self.tablaPedidos.identify_row(evento.y)  # Identificar la fila en la que se hizo click
                self.tablaPedidos.selection_set(item_id)  # Seleccionar la fila

                # Mostrar el menú contextual en la posición del cursor
                self.menu.post(evento.x_root, evento.y_root)
            except:
                pass
        
        
        # Asociar el click derecho al evento
        self.tablaPedidos.bind("<Button-3>", mostrar_menu)





    def actualizar_tabla(self, laRaiz):
        # Elimina todos los elementos del Treeview
        for item in self.tablaPedidos.get_children():
            self.tablaPedidos.delete(item)
        
        self.llenarTabla()




    def programar_todo(self):
        #########GENERAR PROGRAMACIÓN############
        Mod_clases.programa_completo(Mod_objetos.pedido_quito06, Mod_clases.personal, 4000)
        horizonte_calculado = Mod_clases.calcular_horizonte(Mod_objetos.pedido_quito06)
        print(f"el horizonte es {horizonte_calculado}")
       
        #GRAFICAR PROGRAMACIÓN EN GANTT##########
        Graficador.generar_gantt_tecnicos(Mod_clases.personal,horizonte_calculado)
        Graficador.generar_gantt_vehiculos(Mod_objetos.pedido_quito06,horizonte_calculado)

        programa = "programar_todo"
        ventanas_emergentes.desea_guardar(eventos.nombraArchivoExcel(programa))


    def programar_inmediato(self):
        #########GENERAR PROGRAMACIÓN############
        Mod_clases.programa_inmediato(Mod_objetos.pedido_quito06, Mod_clases.personal, 4000, fechaStart="2024-10-09", horaStar="08:00")
        horizonte_calculado = Mod_clases.calcular_horizonte(Mod_objetos.pedido_quito06)
        print(f"el horizonte es {horizonte_calculado}")

        #GRAFICAR PROGRAMACIÓN EN GANTT##########
        Graficador.generar_gantt_tecnicos(Mod_clases.personal,horizonte_calculado)
        Graficador.generar_gantt_vehiculos(Mod_objetos.pedido_quito06,horizonte_calculado)

        programa = "programar_inmediato"
        ventanas_emergentes.desea_guardar(eventos.nombraArchivoExcel(programa))
