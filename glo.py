#FRAME DE MODELOS y TECNICOS
btt_editModelos = {}        # Diccionario para almacenar nombres de Botones de editar modelos
lbl_Modelos = {}            # Diccionario para almacenar las variables de los Labels de modelos y sus textos
lbl_Tecnicos = {}           # Diccionario para almacenar las variables de los Labels de tecnicos y sus textos
lbl_procesos = {}           # Diccionario para almacenar los textos de la tabla del frame de Procesos
lbl_modelProcesos = {}      # Diccionarios para almacenar los textos de los ID procesos para el frame de modelos
strVar_Tiempos = {}         # Diccionarios para almacenar las variables de los entry de tiempos por filas_columnas, ejemplo textExtryTime1_9
ent_Tiempos = {}            # Diccionarios para almacenar los textos de los entry de tiempos por filas_columnas, ejemplo textExtryTime1_9

intVar_tecnicos = {}  # Diccionario que tiene los nombres de las variables objeto de los checkbutton de tecnicos
check_tecnicos = {}  # Diccionario que tiene los nombres de los checkbuttons de tecnicos


#VENTANA CREA-EDITA MODELO
lbl_nuevosTiemposMod = {}        # Diccionario para almacenar los nombres de los label del item tiempo de crear o editar un modelo
ent_nuevosTiemposMod = {}        # Diccionario para almacenar los nombres de los entry del item tiempo de  crear o editar un modelo
strVar_nuevosTiemposMod = {}     # Diccionario para almacenar las variables asociadas a los valores de los entry del item tiempo de  crear o editar un modelo

#VENTANA AGREGA MODELO A VEHICULOS
lbl_nuevosTiemposVeh = {}        # Diccionario para almacenar los nombres de los label del item tiempo de crear o editar un modelo
ent_nuevosTiemposVeh = {}        # Diccionario para almacenar los nombres de los entry del item tiempo de  crear o editar un modelo
strVar_nuevosTiemposVeh = {}     # Diccionario para almacenar las variables asociadas a los valores de los entry del item tiempo de  crear o editar un modelo



################################################
###### FRAMES DE CONTENIDOS PRINCIPALES ########
class Contenidos:
    def __init__(self):
        self.contenidoDeModelos = None
        self.contenidoDeTecnicos = None
        self.contenidoProcesos = None
        self.contenidoDeVehiculos = None
        self.vehiculos = None
        self.filtro = None

    def __repr__(self):
        return [self.contenidoDeModelos, self.contenidoProcesos, self.contenidoDeTecnicos, self.contenidoDeVehiculos, self.vehiculos, self.filtro]

stateFrame = Contenidos()
