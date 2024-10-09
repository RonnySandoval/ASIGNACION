import CRUD
import fechahora

nombres_procesos = list(map(lambda proceso:proceso.upper(), CRUD.leer_procesos()))      #PROCESOS EN ORDEN SECUENCIAL
orden_procesos = ['SIN PROCESAR'] + nombres_procesos + ['DESPACHO', 'ENTREGADO']        #DIFERENTES DE UN VEHÍCULO

print(nombres_procesos)
print(orden_procesos)


# Modelos de vehículos agrupados por marcas
modelos = list(map(lambda modelo_marca: modelo_marca[1], CRUD.leer_modelos()))



marcas = {
    "NISSAN":   ["ALTIMA","FRONTIER","KICKS","QASHQAI","LEAFT","VERSA","PATHFINDER","XTRAIL",],
    "RENAULT":  ["CAPTUR","KOLEOS","KWID",],
    "BAIC":     ["BJ20","BJ40","D50","NX55","X35","X55","U5P",],
    "FOTON":    ["AUMARK","AUMAN","TUNLAND","VIEW","TOANO",],
    "GEELY":    ["AZKARRA","COOLRAY",],
    "MG":       ["RX8","RX5","MG5","ZS","ONE"]
}


tiempos = {}
for registro_tupla in CRUD.leer_tiempos():
    modelo = registro_tupla[1]
    datos = registro_tupla[2:]
    tiempos[modelo] = []
    tiempos[modelo].extend(list(datos))

"""
#Tiempo de los 5 procesos para cada modelo
tiempos = {
    "ALTIMA":       [0,   60,  60,  30,   15],
    "FRONTIER":     [420, 128, 55,  23,   15],
    "KICKS":        [150, 123, 55,  23,   15],
    "QASHQAI":      [330, 63,  55,  23,   15],
    "LEAFT":        [0,   63,  50,  23,   15],
    "VERSA":        [390, 123, 55,  23,   15],
    "PATHFINDER":   [60,  63,  60,  23,   15],
    "XTRAIL":       [60,  63,  55,  23,   15],
    "CAPTUR":       [60,  60,  60,  30,   15],
    "KOLEOS":       [60,  63,  60,  48,   15],
    "KWID":         [60,  68,  50,  48,   15],
    "BJ20":         [0,   72,  55,  52,   15],
    "BJ40":         [0,   72,  55,  52,   15],
    "D50":          [270, 72,  55,  52,   15],
    "NX55":         [240, 72,  55,  52,   15],
    "X35":          [270, 72,  55,  52,   15],
    "X55":          [0,   72,  55,  52,   15],
    "U5P":          [270, 72,  55,  52,   15],
    "AUMARK":       [0,   365, 120, 300,  15],
    "AUMAN":        [0,   960, 120, 1920, 15],
    "TUNLAND":      [270, 240, 120, 185,  15],
    "VIEW":         [240, 295, 90,  685,  15],
    "TOANO":        [240, 240, 90,  685,  15],
    "AZKARRA":      [0,   72,  55,  22,   15],
    "COOLRAY":      [0,   72,  55,  22,   15],
    "RX8":          [0,   92,  50,  15,   15],
    "RX5":          [0,   210, 50,  15,   15],
    "MG5":          [0,   105, 50,  15,   15],
    "ZS":           [0,   110, 50,  15,   15],
    "ONE":          [0,   200, 50,  15,   15]
}
"""


#FUNCIONES PARA BUSCAR TIEMPOS
def buscar_tiempo(modelo, proceso):         #Devuelve el tiempo de un solo proceso para un modelo dado.
    print(modelo)
    times = tiempos.get(modelo)             # Obtenemos la lista de tiempos para el modelo
    if times is None:
        return None  # Si el modelo no existe en el diccionario

    try:
        indice = nombres_procesos.index(proceso)    # Busca el índice del proceso
        return times[indice]                        # Devuelve el tiempo correspondiente al proceso
    
 
    except ValueError:
        print(f"El modelo {modelo} no existe")
        return None             # Si el proceso no se encuentra en la lista de procesos

def buscar_tiempos(modelo):     #Devuelve una lista con los tiempos de todos los procesos para un modelo dado.
    return tiempos.get(modelo)

class VehiculoBase:             # Son los tipos de vehiculos, es decir los modelos, con sus tiempos de proceso
    def __init__(self, modelo, marca):
        self.modelo = modelo
        self.marca = marca
        self.tiempos_proceso = buscar_tiempos(modelo)

    def obtener_tiempo_proceso(self, proceso):      #Obtiene el tiempo del proceso en cuestion para ese objeto vehiculo
        return buscar_tiempo(self.modelo, proceso)

    def __repr__(self):
        return f"Marca: {self.marca}, Modelo: {self.modelo}, Tiempos {self.tiempos_proceso} \n"    #formato de impresión para cada modelo de vehículo

class Vehiculo(VehiculoBase):               #Es cada vehiculo único que pasa por los procesos de la planta
    def __init__(self, id_chasis, modelo, marca, color, pedido,  fecha, estado='SIN PROCESAR', novedades = "NO"):
        super().__init__(modelo, marca)
        self.color = color
        self.fecha_entrega = fecha
        self.id_chasis = id_chasis
        self.pedido = pedido
        self.estado = estado
        self.novedades = novedades
        self.inicio = 0             #Tiempo en minutos en que el vehículo inicia cierto proceso
        self.fin = 0                #Tiempo en minutos en que el vehículo termina cierto proceso
        self.tecnico_actual= None   #Tecnico que atendió determinaedo proceso del vehículo
        self.plazo = None
        self.historico_estados = [(estado, self.inicio, self.fin, self.tecnico_actual),]  # Guarda la historia de estado, el técnico que atendió cada proceso y sus momentos de inicio y fin de proceso

    def avanzar_estado(self, tecnico):
        # Avanza al siguiente estado del vehículo en el proceso secuencial;
        #solo puede avanzar el estado si se especifica el técnico que lo atenderá
        try:
            self.tecnico_actual = tecnico                                                   #Asigna  al vehículo el técnico pasado por parámetro. El parámetro "tecnico" es un objeto de la clase Tecnico()
            estado_actual = self.estado                                                     #Extrae el ultimo estado en el constructor
            siguiente_estado = orden_procesos[orden_procesos.index(estado_actual) + 1]      #Obtiene el siguiente estado o proceso de la secuencia
            self.estado = siguiente_estado                                                  #Actualiza el estado

            tiempo_proceso = self.obtener_tiempo_proceso(self.estado)   # Obtiene el tiempo de proceso para el estado actual, a partir del metodo de la clase padre VehiculoBase()
            self.inicio=tecnico.comienza                                # Obtiene el tiempo en el que terminó su anterior asignación el técnico en cuestión y actualiza el momento de inicio del vehículo para el proceso actual. El tiempo es un atributo del objeto Tecnico()
            self.fin = tecnico.termina                                  # Calcula el tiempo en que terminará el proceso actual
            self.historico_estados.append((self.estado, self.inicio, self.fin, self.tecnico_actual.nombre))  # Agrega la asignación al histórico de estados del vehículo

        except IndexError:                          # Si no encuentra másprocesos en lista, arrojará un mensaje informando que el vehícuylo estará listo
            print(f"Vehículo {self.id_chasis} ha completado todos los procesos.")

    def __repr__(self):  #Formato de impresión de vehículo
        return f"Vehiculo(chasis: {self.id_chasis},
                Marca: {self.marca}, Modelo: {self.modelo},
                Estado: {self.estado}, Color: {self.color},
                tiempos: {self.tiempos_proceso},
                Resumen: {self.historico_estados},
                Plazo: {self.plazo} \n"

    

personal = []
class Tecnico:                                  # Es cada técnico con nombre e ID
    
    def __init__(self, id_tecnico, nombre, especializacion):

        # Asegurar que el técnico no esté en la lista
        #print(f"{len(personal)} {id_tecnico}")
        if len(personal) != 0:
            if not any(tecnico.id_tecnico == id_tecnico for tecnico in personal):
                self.id_tecnico = id_tecnico
                self.nombre = nombre
                self.especializacion = especializacion
                self.comienza = 0
                self.termina = 0
                self.vehiculo_actual = None
                self.historico_asignacion = []
            else:
                print(f"Técnico con ID {id_tecnico} ya está en la lista.")
                return
        
        else:
            self.id_tecnico = id_tecnico
            self.nombre = nombre
            self.especializacion = especializacion
            self.comienza = 0
            self.termina = 0
            self.vehiculo_actual = None
            self.historico_asignacion = []
        
        personal.append(self)        
        #print(f"se agregó {id_tecnico}")




    def asignar_vehiculo(self, vehiculo, franjaStart):          # Asigna el vehículo al técnico que se pasa por parámetro,
                                                                # actualiza los momentos de inicio, fin y estado y agrega
                                                                # esta infomación al resumen de asignaciones
        #if self.historico_asignacion == []:
        #    self.comienza = fechahora.parseDT(franjaStart)



        try:
            self.vehiculo_actual = vehiculo         # Cambia el vehículo que está atendiendo al que se asignará

            #CASO VEHICULO DEBE ESPERAR AL TÉCNICO
            if  vehiculo.fin <= self.termina:       # Evalua si el momento en que el vehículo a asignar terminó el proceso anterior OCURRE ANTES que el momento en que el técnico terminó la última asignación
            
                tiempo_proceso = vehiculo.obtener_tiempo_proceso(self.especializacion)          # obtiene eltiempo del proceso del vehículo
                self.comienza = self.termina        # Actualiza el momento de inicio (del técnico) del proceso actual al momento de fin (del técnico) del proceso anterior 
                #print(tiempo_proceso)
                self.termina += tiempo_proceso      # Calcula el momento de fin (del tecnico) del proceso actual
                vehiculo.avanzar_estado(self)       # Actualiza el estado usando el método de la clase Vehiculo
                self.historico_asignacion.append((self.vehiculo_actual.id_chasis, self.comienza, self.termina))  # Agrega el nuevo estado con sus caracteríticas al resumen de asignaciones
                return True
            

            #CASO TÉCNICO DEBE ESPERAR AL VEHÍCULO
            elif vehiculo.fin > self.termina:               # Evalua si el momento en que el vehículo a asignar terminó el proceso anterior OCURRE DESPUES que el momento en que el técnico terminó la última asignación

                tiempo_proceso = vehiculo.obtener_tiempo_proceso(self.especializacion)          # obtiene eltiempo del proceso del vehículo
                self.comienza= vehiculo.fin                 # Actualiza el momento de inicio (del técnico) del proceso actual al momento de fin (del vehículo) del proceso anterior 
                self.termina = vehiculo.fin+tiempo_proceso  # Calcula el momento de fin (del tecnico) del proceso actual
                vehiculo.avanzar_estado(self)               # Actualiza el estado usando el método de la clase Vehiculo
                self.historico_asignacion.append((self.vehiculo_actual.id_chasis, self.comienza, self.termina))  # Agrega el nuevo estado con sus caracteríticas al resumen de asignaciones
                return True
            
        except Exception as e:
            print(f"No se ejecutó el método asignar_vehiculo. ****OCURRIÓ UNA EXCEPCIÓN: {e}****") 

        return False


    def __repr__(self):        #Formato de impresión del técnico
        return f"Tecnico(ID: {self.id_tecnico}, 
                 Nombre: {self.nombre}, 
                 Especialización: {self.especializacion}, 
                 Asignaciones: {self.historico_asignacion})
                 \n"


class Pedido:
    def __init__(self, id_pedido, plazo_entrega, vehiculos, estado ="PENDIENTE"):
        self.id_pedido = id_pedido
        self.plazo_entrega = plazo_entrega
        self.vehiculos = vehiculos
        self.estado = estado
        for vehiculo in vehiculos:
            vehiculo.fecha = plazo_entrega
    
    def cambia_estado():
        pass

    def __repr__(self):
        return f"Pedido(ID: {self.id_pedido}, Fecha Entrega: {self.plazo_entrega}, Vehículos: {self.vehiculos}), Estado: {self.estado}"


class OrdenProduccion:
    def __init__(self, vehiculo, proceso, tecnico, inicio, fin, pedido):
        self.chasis         = vehiculo.id_chasis
        self.marca          = vehiculo.marca
        self.modelo         = vehiculo.modelo
        self.color          = vehiculo.color
        self.novedades      = vehiculo.novedades
        self.pedido         = pedido
        self.id_pedido      = pedido
        self.proceso        = proceso
        self.id_tecnico     = tecnico.id_tecnico
        self.nombre_tecnico = tecnico.nombre
        self.especialidad   = tecnico.especializacion
        self.inicio         = inicio
        self.fin            = fin
        self.duracion       = fin-inicio
        self.plazo          = vehiculo.fecha
        self.codigo_orden   = self.codificar_orden()

    def codificar_orden(self):
        chasis = self.chasis
        tecnico = self.nombre_tecnico
        proceso = self.proceso
        self.codigo_orden = str(chasis) +'-' + '-'+ str(tecnico) + '-' + str(proceso)
        return self.codigo_orden

    def almacenar_orden(self):
        datos = (self.codigo_orden,
                 self.chasis,
                 self.marca,
                 self.modelo,
                 self.color,
                 self.novedades,
                 self.pedido,
                 self.id_pedido,
                 self.proceso,
                 self.id_tecnico,
                 self.nombre_tecnico,
                 self.especialidad,
                 self.inicio,
                 self.fin,
                 self.duracion,
                 self.plazo)
        #CODIGO_ORDEN, CHASIS, MARCA, MODELO, COLOR, NOVEDADES, PEDIDO, ID_PEDIDO, PROCESO, ID_TECNICO, NOMBRE_TECNICO, ESPECIALIDAD, INICIO, FIN, DURACION, PLAZO
        CRUD.insertar_orden(*datos)


    def __repr__(self):
        return f"Orden: {self.codigo_orden}, Chasis: {self.chasis},Modelo: {self.modelo}, Marca: {self.marca}, Color: {self.color}, Proceso: {self.proceso}, Id_tecnico: {self.id_tecnico} Tecnico: {self.nombre_tecnico}, Pedido(ID: {self.id_pedido}, Inicio: {self.inicio}, Fin: {self.fin}, Duración: {self.duracion}, Fecha Entrega: {self.plazo}"

######################################################################################################
#########################################METODOS ESTATICOS############################################
######################################################################################################
listaOrdenes = []
def programa_inmediato(pedido, tecnicos, horizonte, franjaStart):

    vehiculos_por_programar = pedido.vehiculos.copy()                   # Extrae una copia de la lista de vehiculos
    contador = 0
    while len(vehiculos_por_programar) > 0:

        tiempos_restantes = list(map(lambda vh: sum(vh.tiempos_proceso), vehiculos_por_programar))  #crea una lista con solo el total de tiempos restante de cada vehiculo
        indice_min_time = tiempos_restantes.index(min(tiempos_restantes))                           #busca el índice con tiempo restante menor
        vehiculo_min_time = vehiculos_por_programar[indice_min_time]                                #busca el vehiculo con tiempo restante menor

        ultimo_estado = vehiculo_min_time.estado                                                    #Extrae el ultimo estado en el constructor del vehiculo seleccionado
        siguiente_estado = orden_procesos[orden_procesos.index(ultimo_estado) + 1]                  #Imprime el siguiente estado o proceso de la secuencia
        print(f"{vehiculo_min_time.id_chasis} necesita {siguiente_estado}")

        tecnicos_disponibles = list(filter(lambda tec: siguiente_estado in tec.especializacion, tecnicos))      # incluye solo aquellos técnicos de la especialidad correcta
        tecnicos_disponibles.sort(key = lambda op: op.termina)                                                  #ordena técnicos por tiempo de menor a mayor

        
        tiempos_disponibles = list(map(lambda operario: operario.termina, tecnicos_disponibles))   #crea una lista solo con los tiempos
        tiempos_disponibles.sort()                                                                 #ordena tiempos de menor a mayor
        print(f"tecnicos disponibles: \n {tecnicos_disponibles}")
        tecnico_min_time = tecnicos_disponibles[0]                                                 #selecciona el tecnico de menor tiempo (el primer elemento de la lista)

        #print(tiempos_disponibles)
        #print(tecnicos_disponibles)


        for times in tiempos_disponibles:                                                          #buscamos en la lista de tiempos de técnicos
            print(f"{times}+{vehiculo_min_time.obtener_tiempo_proceso(siguiente_estado)}")

            asignado = False

            if times + vehiculo_min_time.obtener_tiempo_proceso(siguiente_estado) <= horizonte:    #verificamos que el tiempo asignado no supere el horizonte
                print("OK. Aun no se supera el horizonte")
                tecnico_min_time.asignar_vehiculo(vehiculo_min_time, franjaStart)                               #SE ASIGNA VEHICULO A TÉCNICO desde el método en la clase técnico
                asignado = True
                print(f"asignado = {asignado} {tecnico_min_time.nombre} al vehiculo {vehiculo_min_time.id_chasis} en {siguiente_estado}")
                
                listaOrdenes.append(OrdenProduccion(vehiculo_min_time,
                                                    siguiente_estado, tecnico_min_time,
                                                    vehiculo_min_time.inicio,
                                                    vehiculo_min_time.fin,
                                                    vehiculo_min_time.pedido))
                print(listaOrdenes[-1])
                listaOrdenes[-1].almacenar_orden()
                break
        
        if asignado == False:
            print(f"No se asignó {vehiculo_min_time.id_chasis}")

                
        vehiculos_por_programar.remove(vehiculo_min_time)        #REMOVEMOS DE LA LISTA EL VEHICULO QUE SE ACABA DE ASIGNAR               
        print(f"--------------------------vuelta {contador}")

        contador = contador + 1
    return pedido.vehiculos

#programa_inmediato(pedido_quito06, personal, 700)


def programa_completo(pedido, tecnicos, horizonte):

    vehiculos_por_programar = pedido.vehiculos.copy()                   # Extrae una copia de la lista de vehiculos
    contador = 0
    while len(vehiculos_por_programar) > 0 :

        ind_est_actuales = list(map(lambda vh: orden_procesos.index(vh.estado),vehiculos_por_programar))        # encuentra una lista con los estado actuales de cada vehículo
        print(f"estados: {ind_est_actuales}")
        for vehic in vehiculos_por_programar:                          #bucle para mostrar en consola el resumen de estados de cada vehiculo
            print(vehic)
        


        tiempos_restantes = [
            sum(vh.tiempos_proceso[ind_est:] if ind_est < len(vh.tiempos_proceso)
                else [0,0]) for vh, ind_est in zip(vehiculos_por_programar, ind_est_actuales)
            ]
            #crea una lista con solo el total de tiempos restante de cada vehiculo
        print(tiempos_restantes)


        indice_min_time = tiempos_restantes.index(max(tiempos_restantes))               #busca el índice con tiempo mayor
        vehiculo_min_time = vehiculos_por_programar[indice_min_time]                    #busca el vehiculo con tiempo restante mayor

        ultimo_estado = vehiculo_min_time.estado                                        #Extrae el ultimo estado en el constructor
        siguiente_estado = orden_procesos[orden_procesos.index(ultimo_estado) + 1]      #Obtiene el siguiente estado o proceso de la secuencia
        
        if siguiente_estado == "DESPACHO":
            print(f"<<<<<<<<<Vehiculo {vehiculo_min_time.id_chasis} en despacho>>>>>>>>>")
            vehiculos_por_programar.remove(vehiculo_min_time)
            contador = contador + 1
            continue

        tecnicos_disponibles = list(filter(lambda persona: siguiente_estado in persona.especializacion, tecnicos))      # incluye soloaquellos técnicos de la especialidad correcta
        tecnicos_disponibles.sort(key = lambda op: op.termina)                                                          #ordena técnicos por tiempo de menor a mayor

        tiempos_disponibles = list(map(lambda operario: operario.termina, tecnicos_disponibles))                        #crea una lista solo con los tiempos
        tiempos_disponibles.sort()                                                                                      #ordena tiempos de menor a mayor
        tecnico_min_time = tecnicos_disponibles[0]

        #print(tiempos_disponibles)
        #print(tecnicos_disponibles)


        for times in tiempos_disponibles:                                                               #buscamos en la lista de técnicos
            print(f"{times}+{vehiculo_min_time.obtener_tiempo_proceso(siguiente_estado)}")

            asignado = False

            if times + vehiculo_min_time.obtener_tiempo_proceso(siguiente_estado) <= horizonte:         #verificamos que el tiempo asignado no supere el horizonte
                print("OK. Aun no se supera el horizonte")
                tecnico_min_time.asignar_vehiculo(vehiculo_min_time)                                    #SE ASIGNA VEHICULO A TÉCNICO desde el método en la clase técnico
                asignado = True
                print(f"asignado = {asignado}. Se asignó {vehiculo_min_time.id_chasis} a {tecnico_min_time.id_tecnico} en el proceso {siguiente_estado}\n\n")                
                listaOrdenes.append(OrdenProduccion(vehiculo_min_time, 
                                                    siguiente_estado,
                                                    tecnico_min_time,
                                                    vehiculo_min_time.inicio,
                                                    vehiculo_min_time.fin,
                                                    vehiculo_min_time.pedido))
                print(listaOrdenes[-1])
                listaOrdenes[-1].almacenar_orden()
                break
        
        if asignado == False:
            print(f"No se asignó {vehiculo_min_time.id_chasis}")

        if vehiculo_min_time.estado == 'calidad':
            vehiculos_por_programar.remove(vehiculo_min_time)        #REMOVEMOS DE LA LISTA EL VEHICULO QUE SE ACABA DE ASIGNAR               
        
        print (f"vuelta #{contador}\n---------------------------------")
        contador = contador + 1

    return pedido.vehiculos


def calcular_horizonte(pedido):
    return max(map(lambda vh: vh.fin, pedido.vehiculos))
