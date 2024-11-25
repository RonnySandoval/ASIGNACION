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
strVar_newPedido = {}
cons_newPedido = {}

################################################
###### FRAMES DE CONTENIDOS PRINCIPALES ########
class Contenidos:
    def __init__(self):
        self.contenidoDeModelos = None
        self.contenidoDeTecnicos = None
        self.contenidoProcesos = None
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

        self.contenidoDeHistoricos = None
        self.tablaHistoricos = None
        self.filtroHistoricos = None

        self.contenidoDeReferencias = None

    def __repr__(self):
        return [self.contenidoDeModelos,
                self.contenidoProcesos,
                self.contenidoDeTecnicos,
                self.contenidoDeVehiculos,
                self.tablaVehiculos,
                self.filtroVehiculos,
                self.contenidoDeReferencias]

stateFrame = Contenidos()


base_datos = 'planta_manta.db'


