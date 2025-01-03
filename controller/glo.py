#FRAME DE MODELOS y TECNICOS
btt_editModelos = {}        # Diccionario para almacenar nombres de Botones de editar modelos
lbl_Modelos = {}            # Diccionario para almacenar las variables de los Labels de modelos y sus textos
lbl_modelProcesos = {}      # Diccionarios para almacenar los textos de los ID procesos para el frame de modelos
strVar_Tiempos = {}         # Diccionarios para almacenar las variables de los entry de tiempos por filas_columnas, ejemplo textExtryTime1_9
ent_Tiempos = {}            # Diccionarios para almacenar los textos de los entry de tiempos por filas_columnas, ejemplo textExtryTime1_9

lbl_Tecnicos = {}           # Diccionario para almacenar las variables de los Labels de tecnicos y sus textos
lbl_procesos = {}           # Diccionario para almacenar los textos de la tabla del frame de Procesos

btt_editIdModelos = {}        # Diccionario para almacenar nombres de Botones de editar id_modelos en el frame de referencias
lbl_IdModelos = {}            # Diccionario para almacenar las variables de los Labels de id_modelos y sus textos en el frame de referencias
btt_editReferencias = {}        # Diccionario para almacenar nombres de Botones de editar referencias en el frame de referencias
lbl_Referencias = {}            # Diccionario para almacenar las variables de los Labels de referencias y sus textos en el frame de referencias

intVar_tecnicos = {}  # Diccionario que tiene los nombres de las variables objeto de los checkbutton de tecnicos
check_tecnicos = {}  # Diccionario que tiene los nombres de los checkbuttons de tecnicos

intVar_procesos = {}  # Diccionario que tiene los nombres de las variables objeto de los checkbutton de tecnicos
check_procesos = {}  # Diccionario que tiene los nombres de los checkbuttons de tecnicos

#VENTANA CREA-EDITA MODELO
lbl_nuevosTiemposMod = {}        # Diccionario para almacenar los nombres de los label del item tiempo de crear o editar un modelo
ent_nuevosTiemposMod = {}        # Diccionario para almacenar los nombres de los entry del item tiempo de  crear o editar un modelo
strVar_nuevosTiemposMod = {}     # Diccionario para almacenar las variables asociadas a los valores de los entry del item tiempo de  crear o editar un modelo

#VENTANA AGREGA MODELO A VEHICULOS
lbl_nuevosTiemposVeh = {}        # Diccionario para almacenar los nombres de los label del item tiempo de crear o editar un modelo
ent_nuevosTiemposVeh = {}        # Diccionario para almacenar los nombres de los entry del item tiempo de  crear o editar un modelo
strVar_nuevosTiemposVeh = {}     # Diccionario para almacenar las variables asociadas a los valores de los entry del item tiempo de  crear o editar un modelo

#VENTANA PEDIDOS
pedido_seleccionado = None
strVar_newPedido = {}
cons_newPedido = {}

#VARIABLES PARA EVENTOS
actualizar_todo = None          #Función del módulo root y Utilizada por el modulo main
base_datos = None               #cadena de terzo utilizada por los modulos que interacturan con la base de datos, en especial, eventos
gantt = False                   #Variable Boleana para saber si se ha creado un gantt. Utilizada por los modulos gantt y llamar gantt.  
huerfanos = None                #Objeto de Clase Utilizada por el modulo de BDdvalidar, que determina si hayregistros huérfanos en la base de datos
raiz_principal = None           #Objeto de la clase ctk.CTk, utilizada por el modulo main y el modulo eventos
turnos = None                   #Utilizada por los modulos fecha_hora, modelo_clases, eventos, gantt, llamar_gantt

################################################
###### FRAMES DE CONTENIDOS PRINCIPALES ########
class Contenidos:
    def __init__(self):
        self.contenidoDeModelos = None
        self.contenidoDeTecnicos = None
        self.contenidoDeProcesos = None
        self.contenidoTecProc = None

        self.contenidoDeVehiculos = None
        self.tablaVehiculos = None
        self.filtroVehiculos = None

        self.contenidoDePedidos = None
        self.tablaPedidos = None
        self.filtroPedidos = None

        self.contenidoDeDetalles = None
        self.tablaDetalles = None
        self.filtroDetalles = None

        self.contenidoDeProgramas = None
        self.tablaProgramas = None
        self.filtroProgramas = None

        self.contenidoDeOrdenes = None
        self.tablaOrdenes = None
        self.filtroOrdenes = None

        self.contenidoDeHistoricos = None
        self.tablaHistoricos = None
        self.filtroHistoricos = None

        self.contenidoDeReferencias = None

        self.contenidoGraficos = None

    def __repr__(self):
        return [self.contenidoDeModelos,
                self.contenidoDeProcesos,
                self.contenidoDeTecnicos,
                self.contenidoDeVehiculos,
                self.tablaVehiculos,
                self.filtroVehiculos,
                self.contenidoDePedidos,
                self.tablaPedidos,
                self.filtroPedidos,
                self.contenidoDeDetalles,
                self.tablaDetalles,
                self.filtroDetalles,
                self.contenidoDeProgramas,
                self.tablaProgramas,
                self.filtroProgramas,
                self.contenidoDeOrdenes,
                self.tablaOrdenes,
                self.filtroOrdenes,
                self.contenidoDeHistoricos,
                self.tablaHistoricos,
                self.filtroHistoricos,
                self.contenidoDeReferencias]

class ProgramaPlanta:
    def __init__(self):
        self.procesos = None 
        self.tecnicos = None
        self.modelos = None
        self.vehiculos = None
        self.pedidos = None
        self.referencias = None
        self.gantt = None

stateFrame = Contenidos()
scheduling = ProgramaPlanta()

