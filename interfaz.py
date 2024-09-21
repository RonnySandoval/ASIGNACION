import  tkinter as tk
from    tkinter import ttk
import  CRUD as CRUD
import  eventos as eventos
import  re
import  dicc_variables
from    estilos import *
import  Mod_programador
import  Objetos
import  Graficador
import  ventanas_emergentes
import  menu_principal

#####################################################################################################################################################
#####################################################################  RAIZ  ########################################################################
#####################################################################################################################################################


root = tk.Tk()
root.title("Programación de Planta")
root.config(bg=grisAzuladoOscuro)
root.iconbitmap("logo8.ico")
root.geometry("800x600")
root.state('zoomed')

menu_principal.crearMenuPrincipal(root)

# Creación de los frames principales
frameVHyTEC = tk.Frame(root, bg=grisAzuladoMedio)
frameVehiculos = tk.Frame(frameVHyTEC, bg=grisAzuladoMedio)
frameTecnicos = tk.Frame(frameVHyTEC, bg=grisAzuladoMedio)
framePedido = tk.Frame(root, bg=grisAzuladoMedio)

# Posicionar los frames 
frameVHyTEC.pack(expand=True, side="left", fill="both", padx = 3, pady= 3)
frameVehiculos.pack(expand=True, side="top", fill="both", padx = 3, pady= 3)
frameTecnicos.pack(expand=True, side="bottom", fill="both", padx = 3, pady= 3)
framePedido.pack(expand=True, side="right", fill="both", padx = 3, pady= 3)


#####################################################################################################################################################
####################################################### FRAME DE VEHICULOS (ARRIBA)###############################################################
#####################################################################################################################################################


# Crear un Canvas en el frame de Vehículos
canvasVehiculos = tk.Canvas(frameVehiculos, bg=grisAzuladoClaro)
canvasVehiculos.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Crear un Scrollbar y conectarlo con el Canvas
scrollbarVehiculos = tk.Scrollbar(frameVehiculos, orient=tk.VERTICAL, command=canvasVehiculos.yview)
scrollbarVehiculos.pack(side=tk.LEFT, fill=tk.Y)

canvasVehiculos.configure(yscrollcommand=scrollbarVehiculos.set)
canvasVehiculos.bind('<Configure>', lambda e: canvasVehiculos.configure(scrollregion=canvasVehiculos.bbox("all")))

# Crear un frame dentro del Canvas
frameVehiculosInterior = tk.Frame(canvasVehiculos, bg=grisAzuladoClaro)
canvasVehiculos.create_window((0, 0), window=frameVehiculosInterior, anchor="nw")



### Añadir contenido al frame interno ###
#Titulo de marcas
labelVehiculos = tk.Label(frameVehiculosInterior, text="MARCAS - Modelos", font=textoBajo, bg=grisAzuladoClaro, fg=blancoHueso, anchor="w")
labelVehiculos.grid(row=0, column=1, sticky="ew")

#Titulo de tiempos
labelTiemposVehiculos = tk.Label(frameVehiculosInterior, text="Tiempos", font=textoBajo, bg=grisAzuladoClaro, fg=blancoHueso)
labelTiemposVehiculos.grid(row=0, column=2, columnspan=5, sticky="ew")
frameVehiculosInterior.grid_columnconfigure(1, weight=1)


#Botón de crear modelo nuevo
button_CrearModelo = tk.Button(frameVehiculosInterior,text="Crear Modelo", font=textoBajo, bg=grisOscuro, fg=grisClaro,
                               command=eventos.crear_modelo)
button_CrearModelo.grid(row=0, column=7, padx=3)


#Botones de editar modelo
#button_variables_camMod = {}              #Diccionario para almacenar nombres de Botones de editar modelos
for filasCambiarMod in range (1, CRUD.calcula_modelos()+1):
    button_name = f"ButtonAgregar{filasCambiarMod}"
    dicc_variables.button_variables_camMod[button_name] = tk.Button(frameVehiculosInterior,text="Editar", font=textoMinimo, bg=grisAzuladoMedio, fg=blancoHueso,
                                                                    command=lambda varBoton=button_name:eventos.editar_modelo(varBoton))
    dicc_variables.button_variables_camMod[button_name].grid(row=filasCambiarMod, column=0, padx=3)


#label_variables_vehiculos = {}            # Diccionario para almacenar las variables de los Labels y sus textos

#Lee los nombres desde la BBDD y los almacena en variables
for filasVehiculos, textos in zip(range(1, CRUD.calcula_modelos()+1), CRUD.leer_modelos()):                 
    label_name_vehiculo = f"labelVehiculo{filasVehiculos}"
    print(label_name_vehiculo)

    # Crear etiquetas para vehículos con nombres segun BD
    dicc_variables.label_variables_vehiculos[label_name_vehiculo] = tk.Label(frameVehiculosInterior, text=textos[0]+" - "+textos[1],
                                                                             font=texto1Bajo, bg=grisAzuladoClaro, fg=blancoHueso, anchor="w")
    dicc_variables.label_variables_vehiculos[label_name_vehiculo].grid(row=filasVehiculos, column=1, sticky="ew")



# Diccionarios para almacenar las variables y los textos de los entry de tiempos por filas_columnas, ejemplo textExtryTime1_9
#string_variables = {}
#entry_variables = {}

#Crea los campos con los tiempos de proceso 
for columnastimes in range (1,6):

    for filastimes in range (1, CRUD.calcula_modelos()+1):
        #Damos un nombre a la variable objeto
        string_name = f"textExtryTime{filastimes}_{columnastimes}"
        #print(string_name)
        #Relacionamos el nombre a la variable
        dicc_variables.string_variables[string_name] = tk.StringVar()
        #Extraemos el texto del label correspondiente a la marca-modelo
        texto_label = dicc_variables.label_variables_vehiculos[f"labelVehiculo{filastimes}"].cget("text")
        #Filtramos la última palabra: "modelo"
        palabra_modelo = re.search(r'\b(\w+)\b$', texto_label).group(1)

        #Buscamos en BD el tiempo de proceso correspondiente al modelo
        dicc_variables.string_variables[string_name].set(CRUD.leer_tiempo(palabra_modelo, columnastimes + 1))
        entry_name = f"ExtryTime{filastimes}_{columnastimes}"
        #print(entry_name)
        dicc_variables.entry_variables[entry_name] = tk.Entry(frameVehiculosInterior, font=numerosPequeños, width=4, bg=grisAzuladoClaro, fg=blancoHueso,
                                                              textvariable=dicc_variables.string_variables[string_name])
        dicc_variables.entry_variables[entry_name].grid(row=filastimes, column=columnastimes + 1)

button_variables_agregVh = {}
for filasAgregarVH in range (1, CRUD.calcula_modelos()+1):
    button_name = f"ButtonAgregar{filasAgregarVH}"
    button_variables_agregVh[button_name] = tk.Button(frameVehiculosInterior,text="Agregar a Pedido", font=textoMinimo, bg=moradoMedio, fg=blancoHueso,
                                                      command=lambda varBoton=button_name:eventos.agregar_a_pedido(varBoton))
    button_variables_agregVh[button_name].grid(row=filasAgregarVH, column= 7, padx=3)


#######################################################################################################################################################
########################################################## FRAME DE PEDIDOS (DERECHA) ################################################################
#######################################################################################################################################################
frameTablaPedido = tk.Frame(framePedido)
frameTablaPedido.pack(fill="both", expand=True, padx=5,)


# Estilo personalizado para Treeview
styletreeview = ttk.Style()

# Cambiar el color de fondo y el color de la fuente para Treeview
styletreeview.configure("Treeview", background=grisOscuro, foreground=blancoHueso, rowheight=25, fieldbackground=grisMedio, font=texto1Minimo)

# Cambiar el color de selección
styletreeview.map("Treeview", background=[("selected", azulClaro)], foreground=[("selected", moradoOscuro)])


canvas = tk.Canvas(frameTablaPedido, bg=grisOscuro)
canvas.pack(side='left', fill='both', expand=True)
frameTablaPedido.update_idletasks()
canvas.config(width=frameTablaPedido.winfo_width(), height=frameTablaPedido.winfo_height())


class FiltrosPedido():

    def __init__(self,pedido):
    # Crear un frame para los filtros
        self.frame_filtros = tk.Frame(canvas, bg=grisOscuro)
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
    
        self.boton_actualizar = tk.Button(self.frame_filtros, text="Actualizar", command=lambda:pedido1.actualizar_tabla(), font=numerosPequeños, bg=azulOscuro, fg=blancoHueso)
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
    def __init__(self): #Crea latabla y un diccionario con los nombres de los campos


         #Crear estilo personalizado para las cabeceras
        self.styletreeview = ttk.Style()
        self.styletreeview.configure("Treeview.Heading", foreground=moradoMedio, font=texto1Minimo)

        
        #Crear Tabla
        self.tablaPedidos = ttk.Treeview(canvas, show="headings")
        self.tablaPedidos["columns"] = ("Chasis", "Fecha de entrega", "Marca", "Modelo", "Color", "Estado", "Tiempos", "Novedades", "Subcontratar", "Pedido")

        # Formatear las columnas
        for col in self.tablaPedidos["columns"]:
            self.tablaPedidos.column(col, anchor=tk.CENTER, width=80)
            self.tablaPedidos.heading(col, text=col, anchor=tk.CENTER)

        self.tablaPedidos.pack(expand=True, fill="both", padx=5)


# Crear un Scrollbar y conectarlo con el Canvas




        #Crear una barra de desplazamiento para la tabla y configurarla
        self.scrollbarTablaPedido = ttk.Scrollbar(frameTablaPedido, orient=tk.VERTICAL, command=self.tablaPedidos.yview)
        self.scrollbarTablaPedido.pack(side='right', fill='y')
        self.tablaPedidos.configure(yscrollcommand=self.scrollbarTablaPedido.set)
        #self.tablaPedidos.bind('<Configure>', lambda e: self.tablaPedidos.configure(scrollregion=self.tablaPedidos.bbox("all")))



        #empaquetar tabla de pedidos
        self.tablaPedidos.pack(expand=True, fill="both", side="bottom")
        self.llenarTabla()

        #Botones de programar pedido
        self.botonProgramarTodo = tk.Button(framePedido,text="Programar TODO", font=textoGrande, bg=naranjaMedio, fg=blancoHueso, command=self.programar_todo)
        self.botonProgramarTodo.pack()

    #Botones de programar pedido
        self.botonProgramarInmediato = tk.Button(framePedido,text="Programar INMEDIATO", font=textoGrande, bg=naranjaMedio, fg=blancoHueso, command=self.programar_inmediato)
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
        self.menu = tk.Menu(root, tearoff=0)
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





    def actualizar_tabla(self):
        # Elimina todos los elementos del Treeview
        for item in self.tablaPedidos.get_children():
            self.tablaPedidos.delete(item)
        
        self.llenarTabla()




    def programar_todo(self):
        #########GENERAR PROGRAMACIÓN############
        Mod_programador.programa_completo(Objetos.pedido_quito06, Mod_programador.personal, 4000)
        horizonte_calculado = Mod_programador.calcular_horizonte(Objetos.pedido_quito06)
        print(f"el horizonte es {horizonte_calculado}")
       
        #GRAFICAR PROGRAMACIÓN EN GANTT##########
        Graficador.generar_gantt_tecnicos(Mod_programador.personal,horizonte_calculado)
        Graficador.generar_gantt_vehiculos(Objetos.pedido_quito06,horizonte_calculado)

        programa = "programar_todo"
        ventanas_emergentes.desea_guardar(eventos.nombraArchivoExcel(programa))


    def programar_inmediato(self):
        #########GENERAR PROGRAMACIÓN############
        Mod_programador.programa_inmediato(Objetos.pedido_quito06, Mod_programador.personal, 4000)
        horizonte_calculado = Mod_programador.calcular_horizonte(Objetos.pedido_quito06)
        print(f"el horizonte es {horizonte_calculado}")

        #GRAFICAR PROGRAMACIÓN EN GANTT##########
        Graficador.generar_gantt_tecnicos(Mod_programador.personal,horizonte_calculado)
        Graficador.generar_gantt_vehiculos(Objetos.pedido_quito06,horizonte_calculado)

        programa = "programar_inmediato"
        ventanas_emergentes.desea_guardar(eventos.nombraArchivoExcel(programa))





pedido1=TablaPedido()
filtro1=FiltrosPedido(pedido1)



#######################################################################################################################################################
########################################################## FRAME DE TÉCNICOS (ABAJO) ################################################################
#######################################################################################################################################################

# Crear un Canvas en el frame de Tecnicos
canvasTecnicos = tk.Canvas(frameTecnicos, bg=moradoOscuro)
canvasTecnicos.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Crear un Scrollbar y conectarlo con el Canvas
scrollbarTecnicos = tk.Scrollbar(frameTecnicos, orient=tk.VERTICAL, command=canvasTecnicos.yview)
scrollbarTecnicos.pack(side=tk.LEFT, fill=tk.Y)

canvasTecnicos.configure(yscrollcommand=scrollbarTecnicos.set)
canvasTecnicos.bind('<Configure>', lambda e: canvasTecnicos.configure(scrollregion=canvasTecnicos.bbox("all")))

# Crear un frame dentro del Canvas
frameTecnicosInterior = tk.Frame(canvasTecnicos, bg=moradoOscuro)
canvasTecnicos.create_window((0, 0), window=frameTecnicosInterior, anchor="ne")



# Añadir contenido al frame interno

labelIdTecnicos = tk.Label(frameTecnicosInterior, text="ID", font=textoMedio, bg=moradoOscuro, fg=blancoHueso)
labelIdTecnicos.grid(row=0, column=0, sticky="we")

labelTecnicos = tk.Label(frameTecnicosInterior, text="NOMBRE", font=textoMedio, bg=moradoOscuro, fg=blancoHueso)
labelTecnicos.grid(row=0, column=1, sticky="we")

labelAreaTecnicos = tk.Label(frameTecnicosInterior, text="ÁREA", font=textoMedio, bg=moradoOscuro, fg=blancoHueso)
labelAreaTecnicos.grid(row=0, column=2, sticky="we")


#Lee los nombres desde la BBDD y los almacena en variables
fila = 0
for filasTecnicos  in CRUD.leer_tecnicos():
    columna = 0
    for columnasTecnicos in filasTecnicos:
        label_name_tecnico = f"labeltecnico_{fila}_{columna}_{filasTecnicos}_{columnasTecnicos}"
        print(label_name_tecnico)

        # Crear etiquetas para vehículos con nombres segun BD
        dicc_variables.label_variables_tecnicos[label_name_tecnico] = tk.Label(frameTecnicosInterior, text=columnasTecnicos,
                                                                                font=texto1Bajo, bg=moradoOscuro, fg=blancoHueso, anchor="w")
        dicc_variables.label_variables_tecnicos[label_name_tecnico].grid(row = 1 + fila, column = 0 + columna, sticky="ew")
        columna +=1
    fila += 1



#Añadir CHEKLIST para incluir en la programación a los técnicos
int_variables_tecnicos = {}         #Diccionario que tiene los nombres de las variables objeto
check_variables_tecnicos = {}       #Diccionario que tiene los nombre de los checkbutton

for filasCheck in range (1, CRUD.calcula_tecnicos()+1):
    int_name = f"checkName{filasCheck}"
    print(int_name)
    int_variables_tecnicos[int_name] = tk.IntVar(value=1)

    check_name_tecnico = f"checkTecnico{filasCheck}"
    print(check_name_tecnico)
    check_variables_tecnicos[check_name_tecnico] = tk.Checkbutton(frameTecnicosInterior, text="Programar", justify="left", bg=moradoOscuro, font=textoMinimo, fg=grisOscuro, anchor="w",
                                variable=int_variables_tecnicos[int_name],onvalue=1, offvalue=0)
    check_variables_tecnicos[check_name_tecnico].grid(row=filasCheck, column=3, sticky="w")

root.mainloop()