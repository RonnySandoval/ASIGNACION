import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import customtkinter as ctk

import view.estilos as estilos

"""
class VentanaStepProcesos():
    def __init__(self, datosStep1):

        self.rootAux = ctk.CTkToplevel()
        self.rootAux.title("Crear Nueva Planta")
        self.rootAux.config(background = estilos.grisOscuro)
        self.rootAux.iconbitmap("logo5.ico")
        self.rootAux.geometry("850x500")
        self.rootAux.lift()  # Eleva la ventana Toplevel para que esté al frente
        self.rootAux.attributes('-topmost', 1)  # También puede asegurar que quede al frente

        self.frameTitulo = ctk.CTkFrame(self.rootAux, fg_color = estilos.grisOscuro)
        self.frameTitulo.pack(expand=True, side="top", fill="both")
        self.frameEntradas = ctk.CTkFrame(self.rootAux, fg_color=estilos.grisOscuro)
        self.frameEntradas.pack(expand=True, side="bottom", fill="both", pady=10, padx=10)

        self.labelTitulo = ctk.CTkLabel(self.frameTitulo,   text = f"Definir procesos para\nPlanta {datosStep1["nombre"]}",
                                               font = estilos.textoMedio, text_color = estilos.blancoFrio, bg_color = estilos.grisOscuro)
        self.labelTitulo.pack(expand=True, side="top", fill="both")

        self.labelNombre        = ctk.CTkLabel(self.frameEntradas,   text = "Nombre",      font = estilos.textoMedio, text_color = estilos.blancoFrio, bg_color = estilos.grisOscuro)
        self.labelId            = ctk.CTkLabel(self.frameEntradas,   text = "Id Proceso",  font = estilos.textoMedio, text_color = estilos.blancoFrio, bg_color = estilos.grisOscuro)
        self.labelDescripcion   = ctk.CTkLabel(self.frameEntradas,   text = "Descripción", font = estilos.textoMedio, text_color = estilos.blancoFrio, bg_color = estilos.grisOscuro)
        self.labelSecuencia     = ctk.CTkLabel(self.frameEntradas,   text = "Secuencia",   font = estilos.textoMedio, text_color = estilos.blancoFrio, bg_color = estilos.grisOscuro)

        self.labelNombre     .grid(row=0, column=1, sticky="ew", padx=20, pady=5)
        self.labelId         .grid(row=0, column=2, sticky="ew", padx=20, pady=5)
        self.labelDescripcion.grid(row=0, column=3, sticky="ew", padx=20, pady=5)
        self.labelSecuencia  .grid(row=0, column=4, sticky="ew", padx=20, pady=5)

        try:
            self.cantidadProcesos = int(datosStep1["cantidadProcesos"])
        except Exception as e:
            print("ocurrió una excepción al crear el formulario de procesos:" , e)
            self.cantidadProcesos = 1
        self.dicc_Entry_Procesos     = {}
        self.dicc_StringVar_Procesos = {}
        self.encabezados = ["nombre","id","descripcion","secuencia"]
        self.genera_formulario()

        self.buttonAtras      = ctk.CTkButton(self.frameEntradas, text="Atrás",     font = estilos.textoGrande, text_color = estilos.blancoFrio,
                                              fg_color = estilos.rojoMedio,         hover_color = estilos.rojoOscuro, corner_radius=25, command="")  
        self.buttonCancelar   = ctk.CTkButton(self.frameEntradas, text="Cancelar",  font = estilos.texto1Bajo, text_color = estilos.blancoFrio,
                                              fg_color = estilos.naranjaMedio,      hover_color = estilos.naranjaOscuro, corner_radius=25, command="")   
        self.buttonCargar  = ctk.CTkButton(self.frameEntradas, text="Cargar",       font = estilos.texto1Bajo, text_color = estilos.blancoFrio,
                                              fg_color = estilos.azulMedio,         hover_color = estilos.azulOscuro, corner_radius=25, command="")
        self.buttonSiguiente  = ctk.CTkButton(self.frameEntradas, text="Siguiente", font = estilos.textoGrande, text_color = estilos.blancoFrio,
                                              fg_color = estilos.grisVerdeMedio,     hover_color = estilos.grisVerdeOscuro, corner_radius=25, command="")

        self.buttonAtras.grid    (row= self.cantidadProcesos + 2, column=1, pady=25)
        self.buttonCancelar.grid (row= self.cantidadProcesos + 2, column=2, pady=25)
        self.buttonCargar.grid   (row= self.cantidadProcesos + 2, column=3, pady=25)   
        self.buttonSiguiente.grid(row= self.cantidadProcesos + 2, column=4, pady=25)

    def genera_formulario(self):
        for fila in (range (1, self.cantidadProcesos+1)):

            for columna in self.encabezados:
                ctk.CTkLabel(self.frameEntradas,
                            text = "Proceso",
                            font = estilos.textoMedio,
                            text_color = estilos.blancoFrio,
                            bg_color = estilos.grisOscuro).grid(row=fila,
                                                                column=0,
                                                                sticky="ew",
                                                                padx=20,
                                                                pady=5)
                
                string_name = f"text_Fila{fila}_Columna{columna}"                  # Damos un nombre a la variable objeto
                self.dicc_StringVar_Procesos[string_name] = tk.StringVar()         # Relacionamos el nombre a la variable en el diccionario de StringVar
                entry_name = string_name                                            # Damos un nombre al entry 
                print(entry_name, self.dicc_StringVar_Procesos[string_name])

                self.dicc_StringVar_Procesos[entry_name] = ctk.CTkEntry(self.frameEntradas, font=estilos.textoMedio, width=50, bg_color=estilos.grisOscuro,
                                                                    textvariable=self.dicc_StringVar_Procesos[string_name])
                self.dicc_StringVar_Procesos[entry_name].grid(row=fila, column = self.encabezados.index(columna) + 1, sticky="nsew", padx=2, pady=2)

    def genera_df_datos(self):
        for clave, valor in self.dicc_StringVar_Procesos.items(): print(clave, " : ", valor.get())

        dicc_para_dataframe = {}
        for key, value in self.dicc_StringVar_Procesos.items():          # Extraer fila y columna
            fila = int(key.split("Fila")[1].split("_")[0])
            columna = key.split("Columna")[1]
            
            if fila not in dicc_para_dataframe:                 # Agregar valor al diccionario procesado
                dicc_para_dataframe[fila] = {}
            dicc_para_dataframe[fila][columna] = value.get()

        self.df = pd.DataFrame.from_dict(dicc_para_dataframe, orient='index')  # Crear el DataFrame
        print(self.df)
        return self.df

    def asignafuncion(self, funcionAtras, funcionCargar, funcionCancelar, funcionSiguiente):               #Método para asignar la función al command button de aceptar y cancelar desde otro módulo.

        self.buttonAtras.configure(command = funcionAtras)
        self.buttonCargar.configure(command = funcionCargar)       
        self.buttonCancelar.configure(command = funcionCancelar)
        self.buttonSiguiente.configure(command = funcionSiguiente)

class VentanaStepTecnicos():       #Ventana para crear o editar modelos
    def __init__(self, datosStep1, datosStep2):

        self.rootAux = ctk.CTkToplevel()
        self.rootAux.title("Crear Nuevo Tecnico")
        self.rootAux.config(background = estilos.grisOscuro)
        self.rootAux.iconbitmap("logo5.ico")
        self.rootAux.lift()  # Eleva la ventana Toplevel para que esté al frente
        self.rootAux.attributes('-topmost', 1)  # También puede asegurar que quede al frente

        self.frameTitulo = ctk.CTkFrame(self.rootAux, fg_color=estilos.grisOscuro)
        self.frameTitulo.pack(expand=True, side="top", fill="both", padx=10)
        self.frameCuerpo = ctk.CTkFrame(self.rootAux, fg_color=estilos.grisOscuro)
        self.frameCuerpo.pack(expand=True, side="bottom", fill="both", padx=10)
        self.frameEntradas = ctk.CTkFrame(self.frameCuerpo, fg_color=estilos.grisOscuro)
        self.frameEntradas.pack(expand=True, side="left", fill="both", pady=10, padx=10)
        self.frameBotones = ctk.CTkFrame(self.frameCuerpo, fg_color=estilos.grisOscuro)
        self.frameBotones.pack(expand=True, side="right", fill="both", pady=10)

        # variables objeto para los entry. Deben ser parte del constructor, para poder usarlas en sus métodos
        self.varNombre         = tk.StringVar()
        self.varApellido       = tk.StringVar()
        self.varDocumento      = tk.StringVar()

        #LABEL PARA TITULO Y CAMPOS
        self.labelTitulo          = ctk.CTkLabel(self.frameTitulo,   text = "CREAR NUEVO TÉCNICO", font = estilos.textoGrande, text_color = estilos.blancoHueso, fg_color=estilos.grisOscuro)
        self.labelNombre          = ctk.CTkLabel(self.frameEntradas, text = "Nombre",              font = estilos.texto1Medio, text_color = estilos.blancoHueso, fg_color=estilos.grisOscuro, anchor="w")
        self.labelApellido        = ctk.CTkLabel(self.frameEntradas, text = "Apellido",            font = estilos.texto1Medio, text_color = estilos.blancoHueso, fg_color=estilos.grisOscuro, anchor="w")
        self.labelDocumento       = ctk.CTkLabel(self.frameEntradas, text = "Documento",           font = estilos.texto1Medio, text_color = estilos.blancoHueso, fg_color=estilos.grisOscuro, anchor="w")
        self.labelEspecialidades  = ctk.CTkLabel(self.frameEntradas, text = "Especialidades",      font = estilos.texto1Medio, text_color = estilos.blancoHueso, fg_color=estilos.grisOscuro, anchor="w")

        self.labelTitulo.pack           (expand=True, side="top", fill="x", padx=20, pady=20)
        self.labelNombre.grid           (row=1, column=0, sticky="ew", padx=5, pady=5)
        self.labelApellido.grid         (row=2, column=0, sticky="ew", padx=5, pady=5)
        self.labelDocumento.grid        (row=3, column=0, sticky="ew", padx=5, pady=5)
        self.labelEspecialidades.grid   (row=4, column=0, sticky="ew", padx=5, pady=5)

        #ENTRY PARA CAMPOS
        self.entryNombre = ctk.CTkEntry      (self.frameEntradas, font = estilos.numerosMedianos, text_color = estilos.blancoHueso, fg_color=estilos.grisOscuro, width=150, textvariable=self.varNombre)
        self.entryApellido = ctk.CTkEntry    (self.frameEntradas, font = estilos.numerosMedianos, text_color = estilos.blancoHueso, fg_color=estilos.grisOscuro, width=150, textvariable=self.varApellido)
        self.entryDocumento = ctk.CTkEntry   (self.frameEntradas, font = estilos.numerosMedianos, text_color = estilos.blancoHueso, fg_color=estilos.grisOscuro, width=150, textvariable=self.varDocumento)

        self.entryNombre.grid       (row=1, column=1, sticky="ew", pady=5)
        self.entryApellido.grid     (row=2, column=1, sticky="ew", pady=5)    
        self.entryDocumento.grid    (row=3, column=1, sticky="ew", pady=5)


        self.df_procesos =  datosStep2
        print(self.df_procesos)
        self.cantidadProcesos = int(datosStep1["cantidadProcesos"])
        self.dicc_Option_especialidades    = {}
        self.dicc_StringVar_especialidades = {}
        self.genera_desplegables()

        self.buttonAgregar    = ctk.CTkButton(self.frameEntradas, text="Agregar Técnico",    font = estilos.textoGrande, text_color = estilos.grisOscuro,
                                              fg_color = estilos.blancoFrio,        hover_color = estilos.grisClaro, corner_radius=25, command="") 
        self.buttonAtras      = ctk.CTkButton(self.frameBotones, text="Atrás",     font = estilos.textoGrande, text_color = estilos.blancoFrio, 
                                              fg_color = estilos.rojoMedio,         hover_color = estilos.rojoOscuro, corner_radius=25, command="")  
        self.buttonCancelar   = ctk.CTkButton(self.frameBotones, text="Cancelar",  font = estilos.texto1Bajo, text_color = estilos.blancoFrio, 
                                              fg_color = estilos.naranjaMedio,      hover_color = estilos.naranjaOscuro, corner_radius=25, command="")   
        self.buttonCargar     = ctk.CTkButton(self.frameBotones, text="Cargar",    font = estilos.texto1Bajo, text_color = estilos.blancoFrio, 
                                              fg_color = estilos.azulMedio,         hover_color = estilos.azulOscuro, corner_radius=25, command="")
        self.buttonSiguiente  = ctk.CTkButton(self.frameBotones, text="Siguiente", font = estilos.textoGrande, text_color = estilos.blancoFrio, 
                                              fg_color = estilos.verdeMedio,    hover_color = estilos.verdeOscuro, corner_radius=25, command="")

        self.buttonAgregar.grid   (row = 0, column=0, columnspan = 2, sticky = "nsew", padx=5, pady=10)
        self.buttonAtras.grid    (row = 0, column=2, pady=15, padx=5)
        self.buttonCancelar.grid (row = 1, column=2, pady=15, padx=5)
        self.buttonCargar.grid   (row = 2, column=2, pady=15, padx=5)   
        self.buttonSiguiente.grid(row = 3, column=2, pady=15, padx=5)

    def genera_desplegables(self):
        for fila in (range (1, self.cantidadProcesos+1)):
            
            string_name = f"text_fila{fila}"                                   # Damos un nombre a la variable objeto
            self.dicc_StringVar_especialidades[string_name] = tk.StringVar()         # Relacionamos el nombre a la variable en el diccionario de StringVar
            entry_name = string_name                                                 # Damos un nombre al OptionMenu
            print(entry_name, self.dicc_StringVar_especialidades[string_name])

            self.dicc_StringVar_especialidades[entry_name] = ctk.CTkOptionMenu(self.frameEntradas, font=estilos.texto1Medio, bg_color=estilos.grisOscuro,
                                                                variable=self.dicc_StringVar_especialidades[string_name], anchor ="center")
            self.dicc_StringVar_especialidades[entry_name].grid(row= 3 + fila, column = 1, padx=2, pady=5)

            self.dicc_StringVar_especialidades[entry_name].configure(values = self.df_procesos["nombre"].tolist())

    def genera_df_datos(self):
        for clave, valor in self.dicc_StringVar_Procesos.items(): print(clave, " : ", valor.get())

        dicc_para_dataframe = {}
        for key, value in self.dicc_StringVar_Procesos.items():          # Extraer fila y columna
            fila = int(key.split("Fila")[1].split("_")[0])
            columna = key.split("Columna")[1]
            
            if fila not in dicc_para_dataframe:                 # Agregar valor al diccionario procesado
                dicc_para_dataframe[fila] = {}
            dicc_para_dataframe[fila][columna] = value.get()

        self.df = pd.DataFrame.from_dict(dicc_para_dataframe, orient='index')  # Crear el DataFrame
        print(self.df)

    def asignafuncion(self, funcionAgregar, funcionAtras, funcionCargar, funcionCancelar, funcionSiguiente):               #Método para asignar la función al command button de aceptar y cancelar desde otro módulo.

        self.buttonAgregar.configure  (command = funcionAgregar)
        self.buttonAtras.configure   (command = funcionAtras)
        self.buttonCancelar.configure(command = funcionCargar)       
        self.buttonCargar.configure  (command = funcionCancelar)
        self.buttonSiguiente.configure(command = funcionSiguiente)
"""

class VentanaCargar():

    def __init__(self, info):
        self.rootAux = ctk.CTkToplevel()                #crea ventana auxiliar
        self.rootAux.title(f"Cargar {info}")          #coloca titulo de ventana
        self.rootAux.geometry("500x360")                #dimensiones
        self.rootAux.resizable(False, False)            #deshabilita la redimension
        self.rootAux.lift()  # Eleva la ventana Toplevel para que esté al frente

        self.frameTitulo = ctk.CTkFrame(self.rootAux)
        self.frameTitulo.pack(side="top", fill="both")
        self.frameEntradas = ctk.CTkFrame(self.rootAux)
        self.frameEntradas.pack(side="bottom", fill="both", pady=10)

        self.labelTitulo = ctk.CTkLabel(self.frameTitulo, text=f"CARGAR {info} DESDE EXCEL", font=estilos.textoGrande)
        self.labelTitulo.pack(expand=True, side="top", fill="x", padx=20, pady=5)

        self.varSaltarFila = tk.StringVar() 
        self.labelSaltarFila = ctk.CTkLabel(self.frameEntradas, text="Saltar filas", font=estilos.texto1Medio,  anchor="w")
        self.labelSaltarFila.grid(row=0, column=0, sticky="ew", padx=20, pady=5)
        self.OptionSaltarFila = ctk.CTkOptionMenu(self.frameEntradas, font = estilos.numerosMedianos, fg_color= estilos.grisAzuladoClaro, width=20, variable=self.varSaltarFila)
        self.OptionSaltarFila.grid(row=0 ,column=1, sticky="ew", pady=5)
        self.fila = ["0","1","2","3","4","5","6","7","8","9","10"]
        self.OptionSaltarFila.configure(values=self.fila)      # Configurar el OptionMenu con los valores del diccionario
        self.OptionSaltarFila.set("0")

        self.varEncabezadoFila = tk.StringVar() 
        self.labelEncabezadoFila = ctk.CTkLabel(self.frameEntradas, text="Fila de Encabezados", font=estilos.texto1Medio,  anchor="w")
        self.labelEncabezadoFila.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
        self.OptionEncabezadoFila = ctk.CTkOptionMenu(self.frameEntradas, font = estilos.numerosMedianos, fg_color= estilos.grisAzuladoClaro, width=20, variable=self.varSaltarFila)
        self.OptionEncabezadoFila.grid(row=1, column=1, sticky="ew", pady=5)
        self.fila = ["0","1","2","3","4","5","6","7","8","9","10"]
        self.OptionEncabezadoFila.configure(values=self.fila)      # Configurar el OptionMenu con los valores del diccionario
        self.OptionEncabezadoFila.set("1")

        self.varColumnas = tk.StringVar() 
        self.labelColumnas = ctk.CTkLabel(self.frameEntradas, text="Rango de Columnas", font=estilos.texto1Medio,  anchor="w")
        self.labelColumnas.grid(row=2, column=0, sticky="ew", padx=20, pady=5)
        self.entryColumnas = ctk.CTkEntry(self.frameEntradas, font = estilos.numerosMedianos, fg_color= estilos.grisAzuladoClaro, width=20, textvariable=self.varColumnas)
        self.entryColumnas.grid(row=2, column=1, sticky="ew", pady=5)
        self.define_columnas(info)

        self.buttonCargar  = ctk.CTkButton(self.frameEntradas, text="Seleccionar Archivo",  font = estilos.textoGrande,
                                           fg_color = estilos.grisVerdeMedio,  hover_color = estilos.grisVerdeOscuro,
                                           command = self.seleccionarArchivo)
        self.buttonCargar.grid(row=4, column=0, padx=22, pady=15)

        self.ruta = ""
        self.labelruta = ctk.CTkLabel(self.frameEntradas, text= self.ruta, font=estilos.texto1Bajo,  anchor="w")
        self.labelruta.grid(row=5, columnspan=2, sticky="ew", padx=20, pady=2)


        self.buttonAceptar = ctk.CTkButton(self.frameEntradas, text="Aceptar", font = estilos.textoMedio,  fg_color = estilos.azulMedio,  command="")
        self.buttonAceptar.grid(row=6, column=0, padx=22, pady=5)  
        self.buttonCancelar = ctk.CTkButton(self.frameEntradas, text="Cancelar", font = estilos.texto1Bajo,  fg_color = estilos.naranjaMedio,  command="")
        self.buttonCancelar.grid(row=6, column=1, padx=22, pady=5)  

    def define_columnas(self, info):

        if info == "procesos":
            self.varColumnas.set("A:D")
        elif info == "tecnicos":
            self.varColumnas.set("A:D")
        elif info == "modelos":
            self.varColumnas.set("A:B")
        elif info == "referencias":
            self.varColumnas.set("A:B")
        else:
            self.varColumnas.set("")

    def seleccionarArchivo(self):
        self.ruta = askopenfilename(
                                title="Seleccionar archivo Excel",
                                filetypes=[("Archivos Excel", "*.xlsx *.xls")]
                                )
        self.labelruta.configure(text=self.ruta)
        return self.ruta
        
    def asignafuncion(self, funcionAceptar, funcionCancelar):               #Método para asignar la función al command button de aceptar y cancelar desde otro módulo.
        self.buttonAceptar.configure(command = funcionAceptar)
        self.buttonCancelar.configure(command = funcionCancelar)

class VentanaPreviewLoad():
    
    def __init__(self, dict_df):

        # Configuración de la ventana auxiliar
        self.rootAux = ctk.CTkToplevel()                # Crea ventana auxiliar
        self.rootAux.attributes('-topmost', True)       # Posiciona al frente de la pantalla
        self.rootAux.title("Programación de Planta")    # Coloca título de ventana
        self.rootAux.geometry("400x600")
        # Configura el tema oscuro
        self.rootAux.configure(bg=estilos.grisAzuladoOscuro)    # Fondo oscuro
        ctk.set_appearance_mode("dark")                 # Establece el modo oscuro global

        self.labeltitulo = ctk.CTkLabel(self.rootAux, text=f"Vista previa de Planta", font =estilos.textoMedio)
        self.labeltitulo.pack(side="top", fill="both")

        self.frameTablas = ctk.CTkFrame(self.rootAux, fg_color=estilos.grisAzuladoOscuro)
        self.frameTablas.pack(expand=True, side="top", fill="both")

        # Contenedor principal: Canvas para soportar scroll
        self.canvas = ctk.CTkCanvas(self.frameTablas, bg="#2C3E50", highlightthickness=0)  # Canvas para scroll
        self.scrollbar_y = ttk.Scrollbar(self.frameTablas, orient="vertical", command=self.canvas.yview)
        self.scrollbar_x = ttk.Scrollbar(self.frameTablas, orient="horizontal", command=self.canvas.xview)

        self.canvas.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        self.scrollbar_y.pack(side="right", fill="y")
        self.scrollbar_x.pack(side="bottom", fill="x")
        self.canvas.pack(fill="both", expand=True)

        # Frame interno dentro del canvas (contenedor de los widgets)
        self.frame_scrollable = ctk.CTkFrame(self.canvas, fg_color="#2C3E50")
        self.frame_scrollable.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.frame_scrollable)

        # Frame para cada tabla
        self.frameTreeviewProcesos = ctk.CTkFrame(self.frame_scrollable, fg_color=estilos.grisAzuladoOscuro)
        self.frameTreeviewProcesos.pack(expand=True, side="top", fill="both")

        self.frameTreeviewTecnicos = ctk.CTkFrame(self.frame_scrollable, fg_color=estilos.grisAzuladoOscuro)
        self.frameTreeviewTecnicos.pack(expand=True, side="top", fill="both")

        self.frameTreeviewModelos = ctk.CTkFrame(self.frame_scrollable, fg_color=estilos.grisAzuladoOscuro)
        self.frameTreeviewModelos.pack(expand=True, side="top", fill="both")

        self.frameTreeviewReferencias = ctk.CTkFrame(self.frame_scrollable, fg_color=estilos.grisAzuladoOscuro)
        self.frameTreeviewReferencias.pack(expand=True, side="top", fill="both")

        self.frameTreeviewTiempos = ctk.CTkFrame(self.frame_scrollable, fg_color=estilos.grisAzuladoOscuro)
        self.frameTreeviewTiempos.pack(expand=True, side="top", fill="both")

         #Crear estilo personalizado para las cabeceras y el cuerpo
        self.styletreeviewInfo = ttk.Style()
        self.styletreeviewInfo.configure("TreeviewPrevia.Heading", foreground=estilos.moradoMedio, font=estilos.texto1Bajo, background=estilos.grisAzuladoOscuro)
        self.styletreeviewInfo.configure("TreeviewPrevia", background=estilos.grisOscuro, foreground=estilos.blancoFrio, fieldbackground=estilos.grisAzuladoOscuro)
        self.styletreeviewInfo.layout("TreeviewPrevia", [('Treeview.treearea', {'sticky': 'nswe'})])

        self.crear_treeview(self.frameTreeviewProcesos, dict_df["PROCESOS"])
        self.crear_treeview(self.frameTreeviewTecnicos, dict_df["TECNICOS"])
        self.crear_treeview(self.frameTreeviewModelos, dict_df["MARCAS_MODELOS"])
        self.crear_treeview(self.frameTreeviewReferencias, dict_df["MODELOS_REFERENCIAS"])
        self.crear_treeview(self.frameTreeviewTiempos, dict_df["TIEMPOS_MODELOS"])

        self.frameBotones = ctk.CTkFrame(self.rootAux, fg_color=estilos.grisAzuladoOscuro)
        self.frameBotones.pack(side="bottom", fill="both")

        self.buttonAceptar = ctk.CTkButton(self.frameBotones, text="Aceptar", font=estilos.textoMedio, fg_color=estilos.rojoClaro,
                                           text_color=estilos.moradoOscuro, hover_color=(estilos.moradoMedio, estilos.blancoFrio), anchor="center")
        self.buttonAceptar.grid(row=0 ,column=0, sticky="ew", pady=5)
        self.buttonCancelar = ctk.CTkButton(self.frameBotones, text="Cancelar", font=estilos.textoMedio, fg_color=estilos.rojoClaro,
                                            text_color=estilos.moradoOscuro, hover_color=(estilos.moradoMedio, estilos.blancoFrio), anchor="center")
        self.buttonCancelar.grid(row=0 ,column=1, sticky="ew", pady=5, padx = 20)

    def crear_treeview(self, frame, dataframe):
        """
        Crea un Treeview a partir de un DataFrame en un frame de tkinter.
            ->argm. frame: El contenedor donde se colocará el Treeview.
            ->argm. dataframe: El DataFrame de pandas con los datos para el Treeview.
        """

        # Crear el Treeview
        tree = ttk.Treeview(frame, show="headings",  style="TreeviewPrevia")
        tree.pack(fill=tk.BOTH, expand=True)

        # Configurar las columnas en el Treeview
        tree["columns"] = list(dataframe.columns)
        
        # Configurar encabezados y ancho de columnas
        for col in dataframe.columns:
            tree.heading(col, text=col)  # Títulos de las columnas
            tree.column(col, width=100, anchor=tk.W)  # Ancho de cada columna

        # Insertar filas en el Treeview
        for _, row in dataframe.iterrows():
            tree.insert("", tk.END, values=list(row))
    
    def asignafuncion(self, funcionAceptar, funcionCancelar):               #Método para asignar la función al command button de aceptar y cancelar desde otro módulo.
        self.buttonAceptar.configure(command = funcionAceptar)
        self.buttonCancelar.configure(command = funcionCancelar)
