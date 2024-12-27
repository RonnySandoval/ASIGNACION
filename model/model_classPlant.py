from datetime import datetime
import database.BBDD as BBDD
import model.model_datetime as model_datetime
import controller.glo as glo
import pandas as pd
import random as rnd
import re

nombres_procesos = None
id_procesos = None
orden_procesos = None
modelos = None
tiempos = None
tiemposVH = None
personal = []
listaOrdenes = []

def obtiene_datos_iniciales():
    global nombres_procesos, id_procesos, orden_procesos, modelos, tiempos, tiemposVH

    nombres_procesos = BBDD.leer_procesos_secuencia(glo.base_datos)
    id_procesos = BBDD.obtener_id_procesos_secuencia(glo.base_datos)
    orden_procesos = ['ninguno'] + id_procesos + ['DESPACHO', 'ENTREGADO']
    print("orden de procesos : " , orden_procesos)

    # Modelos de vehículos agrupados por marcas
    modelos = list(map(lambda modelo_marca: modelo_marca[2], BBDD.leer_modelos(glo.base_datos)))
    tiempos = BBDD.leer_tiempos_modelos_df(glo.base_datos)
    tiemposVH = BBDD.leer_tiempos_vehiculos_df(glo.base_datos)
    print(tiempos)

def buscar_tiempo(modelo, proceso):
    #Devuelve el tiempo de un solo proceso para un modelo dado.
    try:
        # Filtra el DataFrame para el modelo dado y obtiene el valor del proceso
        tiempo = tiempos.loc[tiempos['MODELO'] == modelo, proceso].values[0]
        print(f"Tiempo de {modelo} en {proceso} = {tiempo}")
        return int(tiempo)
    
    except IndexError:
        print(f"El modelo {modelo} no existe.")
        return None
    
    except KeyError:
        print(f"El proceso {proceso} no existe en el DataFrame.")
        return None

def buscar_tiempos(modelo):                             #Devuelve una lista con los tiempos de todos los procesos para un modelo dado.
    try:
        id_procesos_filtrados = [col for col in id_procesos if col in tiempos.columns]                  # Filtrar id_procesos para incluir solo los que existen en las columnas del DataFrame

        if id_procesos_filtrados:                                                                       # Verificar que haya al menos una columna válida en id_procesos_filtrado
            tiempos_modelo = tiempos.loc[tiempos['MODELO'] == modelo, id_procesos_filtrados].values[0]  # Si hay columnas válidas, se selecciona
            print("Valores seleccionados:", tiempos_modelo)
        else:
            print("Error: Ninguna de las columnas en id_procesos está en el DataFrame.")                # Si no hay columnas válidas, se imprime un mensaje
        return list(tiempos_modelo)
    
    except IndexError:
        print(f"El modelo {modelo} no existe.")
        return None

def buscar_tiempoVH(chasis, proceso):     #Devuelve el tiempo de un solo proceso para un modelo dado.

    try:
        # Filtra el DataFrame para el modelo dado y obtiene el valor del proceso
        tiempo = tiemposVH.loc[tiemposVH['CHASIS'] == chasis, proceso].values[0]
        print(f"Tiempo de {chasis} en {proceso} = {tiempo}")
        return int(tiempo)
    
    except IndexError:
        print(f"El chasis {chasis} no existe.")
        return None
    
    except KeyError:
        print(f"El proceso {proceso} no existe en el DataFrame.")
        return None

def buscar_tiemposVH(chasis):     #Devuelve una lista con los tiempos de todos los procesos para un modelo dado.
    try:
        # Filtra el DataFrame para el modelo dado y selecciona todas las columnas de procesos
        tiempos_modelo = tiempos.loc[tiempos['MODELO'] == chasis, id_procesos].values[0]
        return tiempos_modelo.tolist()
    
    except IndexError:
        print(f"El modelo {chasis} no existe.")
        return None

class VehiculoBase:             # Son los tipos de vehiculos, es decir los modelos, con sus tiempos de proceso
    def __init__(self, modelo, marca):
        self.modelo = modelo
        self.marca = marca
        self.tiempos_proceso = buscar_tiempos(modelo)
        self.estado_inicial = {'modelo': modelo,
                               'marca': marca,}

    def obtener_tiempo_proceso(self, proceso):          #Obtiene el tiempo del proceso en cuestion para ese objeto vehiculo
        return buscar_tiempo(self.modelo, proceso)

    def reset(self):
        for key, value in self.estado_inicial.items():
            setattr(self, key, value)

        self.tiempos_proceso = buscar_tiempos(self.modelo)

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
        self.libre = None
        self.plazo = None
        self.historico_estados = []  # Guarda la historia de estado, el técnico que atendió cada proceso y sus momentos de inicio y fin de proceso
        self.vueltas = []
        self.estado_inicial = {**self.estado_inicial,  # Estado inicial de la superclase
                               'color': color,
                               'fecha_entrega': fecha,
                               'id_chasis': id_chasis,
                               'pedido': pedido,
                               'estado': estado,
                               'novedades': novedades,
                               'inicio': 0,
                               'fin': 0,
                               'tecnico_actual': None,
                               'libre': None,
                               'plazo': None,
                               'historico_estados': [],
                               'vueltas':[]}

    def reset(self):
        # Ahora restauramos los atributos específicos de Vehiculo
        super().reset()
        for key, value in self.estado_inicial.items():
            setattr(self, key, value)

    def avanzar_estado(self, tecnico, bloques):
        # Avanza al siguiente estado del vehículo en el proceso secuencial;
        #solo puede avanzar el estado si se especifica el técnico que lo atenderá

        if bloques is None:
            siguiente_estado = orden_procesos[orden_procesos.index(self.estado) + 1]      #Obtiene el siguiente estado o proceso de la secuencia
            self.estado = siguiente_estado
            return

        try:
            self.tecnico_actual = tecnico                                                   #Asigna  al vehículo el técnico pasado por parámetro. El parámetro "tecnico" es un objeto de la clase Tecnico()
            estado_actual = self.estado                                                     #Extrae el ultimo estado en el constructor
            siguiente_estado = orden_procesos[orden_procesos.index(estado_actual) + 1]      #Obtiene el siguiente estado o proceso de la secuencia
            self.estado = siguiente_estado                                                  #Actualiza el estado
            #tiempo_proceso = self.obtener_tiempo_proceso(self.estado)   # Obtiene el tiempo de proceso para el estado actual, a partir del metodo de la clase padre VehiculoBase()
            self.inicio =tecnico.comienza                                # Obtiene el tiempo en el que terminó su anterior asignación el técnico en cuestión y actualiza el momento de inicio del vehículo para el proceso actual. El tiempo es un atributo del objeto Tecnico()
            self.fin = tecnico.termina                                  # Calcula el tiempo en que terminará el proceso actual
            self.libre = self.fin
            for bloque in bloques:
                self.historico_estados.append((self.estado, *bloque, self.tecnico_actual.nombre))  # Agrega la asignación al histórico de estados del vehículo

        except IndexError:                          # Si no encuentra másprocesos en lista, arrojará un mensaje informando que el vehícuylo estará listo
            print(f"Vehículo {self.id_chasis} ha completado todos los procesos.")

    def ingresar_a_proceso(self, tecnico, bloques, estado):
        # Avanza al siguiente estado del vehículo en el proceso secuencial;
        #solo puede avanzar el estado si se especifica el técnico que lo atenderá

        if bloques is None:
            self.estado = estado      # Modifica la propiedad estado del vehiculo al proceso especificado
            return

        try:
            self.tecnico_actual = tecnico                                                   #Asigna  al vehículo el técnico pasado por parámetro. El parámetro "tecnico" es un objeto de la clase Tecnico()
            self.estado = estado                                                            #Actualiza el estado
            #tiempo_proceso = self.obtener_tiempo_proceso(self.estado)   # Obtiene el tiempo de proceso para el estado actual, a partir del metodo de la clase padre VehiculoBase()
            self.inicio =tecnico.comienza                                # Obtiene el tiempo en el que terminó su anterior asignación el técnico en cuestión y actualiza el momento de inicio del vehículo para el proceso actual. El tiempo es un atributo del objeto Tecnico()
            self.fin = tecnico.termina                                  # Calcula el tiempo en que terminará el proceso actual
            self.libre = self.fin
            for bloque in bloques:
                self.historico_estados.append((self.estado, *bloque, self.tecnico_actual.nombre))  # Agrega la asignación al histórico de estados del vehículo

        except IndexError:                          # Si no encuentra másprocesos en lista, arrojará un mensaje informando que el vehícuylo estará listo
            print(f"Vehículo {self.id_chasis} ha completado todos los procesos.")

    def obtener_tiempo_proceso_VH(self, proceso):          #Obtiene el tiempo del proceso en cuestion para ese objeto vehiculo
        return buscar_tiempoVH(self.id_chasis, proceso)

    def obtener_historicos(self, bbdd, chasis):
        lectura = BBDD.leer_historico_completo(bbdd, chasis)            #Leer el registro de historicos del vehiculo
        historicos = [(registro[3],                                     #Generar una tupla con cada registro de acuerdo al formato del objeto vheiculo
                    model_datetime.datetime.strptime(registro[6], "%Y-%m-%d %H:%M:%S"),
                    model_datetime.datetime.strptime(registro[7], "%Y-%m-%d %H:%M:%S"),
                    registro[2])
                    for registro in lectura]
        
        historicos_ordenados = sorted(historicos, key=lambda x: x[1])    # Ordenar los históricos por la fecha de inicio (segundo elemento de cada tupla)
        
        if historicos_ordenados:    #solo si hay registros
            for historico in historicos_ordenados:
                print(f"-....-historico en BBDD de {chasis}: {historico}")

                # Actualizar los atributos del vehiculo de acuerdo al ultimo proceso
                self.estado = historico[0]   
                self.inicio = historico[1]
                self.fin = historico[2]
                self.tecnico_actual = historico[3]
                self.historico_estados.append((self.estado, self.inicio, self.fin, self.tecnico_actual))
        else:
            print(f"-....-No hay registros de históricos para el chasis {chasis}")

    def __repr__(self):  #Formato de impresión de vehículo
        return f"""Vehiculo(chasis: {self.id_chasis},
                Marca: {self.marca}, Modelo: {self.modelo},
                Estado: {self.estado}, Color: {self.color},
                tiempos: {self.tiempos_proceso},
                Resumen: {self.historico_estados},
                Plazo: {self.plazo},
                vueltas : {self.vueltas} \n"""
 
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
                self.libre = None
                self.vehiculo_actual = None
                self.historico_asignacion = []
                self.estado_inicial = {         # Guardar el estado inicial
                    'id_tecnico': id_tecnico,
                    'nombre': nombre,
                    'especializacion': especializacion,
                    'comienza': 0,
                    'termina': 0,
                    'libre': None,
                    'vehiculo_actual': None,
                    'historico_asignacion': []
                }
            else:
                print(f"Técnico con ID {id_tecnico} ya está en la lista.")
                return
        
        else:
            self.id_tecnico = id_tecnico
            self.nombre = nombre
            self.especializacion = especializacion
            self.comienza = 0
            self.termina = 0
            self.libre = None
            self.vehiculo_actual = None
            self.historico_asignacion = []
            self.estado_inicial = {         # Guardar el estado inicial
                'id_tecnico': id_tecnico,
                'nombre': nombre,
                'especializacion': especializacion,
                'comienza': 0,
                'termina': 0,
                'libre': None,
                'vehiculo_actual': None,
                'historico_asignacion': []
            }
        
        personal.append(self)        
        #print(f"se agregó {id_tecnico}")

    def reset(self):
        for key, value in self.estado_inicial.items():
            setattr(self, key, value)

    def asignar_vehiculo(self, vehiculo, fechaStart, horaStart):          # Asigna el vehículo al técnico que se pasa por parámetro,
                                                                # actualiza los momentos de inicio, fin y estado y agrega
                                                                # esta infomación al resumen de asignaciones

        try:     #Determinamos si los históricos de vehiculo y técnicos están vacíos o no
            if self.historico_asignacion == []:
                self.comienza = model_datetime.parseDT(fechaStart,horaStart)      # da formato de fecha y hora a la propiedad comienza del tecnico
                self.termina = self.comienza                                 # da formato de fecha y hora a la propiedad termina del tecnico

            if vehiculo.historico_estados == []:
                vehiculo.inicio = model_datetime.parseDT(fechaStart,horaStart)    # da formato de fecha y hora a la propiedad inicio del vehiculo
                vehiculo.fin = vehiculo.inicio                               # da formato de fecha y hora a la propiedad fin del vehiculo

        except Exception as e:
            print(f"Error en la evaluación de historicos. ****OCURRIÓ UNA EXCEPCIÓN: {e}****") 
    


        try:
            self.vehiculo_actual = vehiculo         # Cambia el vehículo que está atendiendo al que se asignará
            tiempo_proceso = vehiculo.obtener_tiempo_proceso(self.especializacion)          # obtiene el tiempo del proceso del vehículo
            
            print(f"último proceso de técnico: {self.comienza, self.termina}, {self.especializacion}")              # último proceso de vehiculo
            print(f"ultima asignación de vehiculo: {vehiculo.inicio, vehiculo.fin}, {vehiculo.estado}")          # ultima asignación de técnico


            #CASO VEHICULO DEBE ESPERAR AL TÉCNICO
            if  vehiculo.fin <= self.termina:       # Evalua si el momento en que el vehículo a asignar terminó el proceso anterior OCURRE ANTES que el momento en que el técnico terminó la última asignación
                print("CASO VEHICULO DEBE ESPERAR AL TÉCNICO")
                self.comienza = self.termina        # Actualiza el momento de inicio (del técnico) del proceso actual al momento de fin (del técnico) del proceso anterior

                bloques = model_datetime.programa_bloques(      #genera los bloques de comienza y termina de acuerdo al tiempo del proceso
                    str(self.comienza.date()),
                    str(self.comienza.time()),
                    tiempo_proceso,
                    am = (glo.turnos.startAM.get(), glo.turnos.endAM.get()),
                    pm = (glo.turnos.startPM.get(), glo.turnos.endPM.get()))
                self.comienza = bloques[0][0]               # Calcula el momento de inicio (del tecnico) del proceso actual
                self.termina =bloques[-1][-1]               # Calcula el momento de fin (del tecnico) del proceso actual
                self.libre = self.termina                  # Calcula el momento en que el técnico está disponible
                vehiculo.avanzar_estado(self, bloques)      # Actualiza el estado usando el método de la clase Vehiculo
                print("Los bloques son", bloques)
                for bloque in bloques:                  
                    self.historico_asignacion.append((self.vehiculo_actual.id_chasis, *bloque))  # Agrega el nuevo estado con sus caracteríticas al resumen de asignaciones
                return True
            

            #CASO TÉCNICO DEBE ESPERAR AL VEHÍCULO
            elif vehiculo.fin > self.termina:               # Evalua si el momento en que el vehículo a asignar terminó el proceso anterior OCURRE DESPUES que el momento en que el técnico terminó la última asignación
                print("CASO TÉCNICO DEBE ESPERAR AL VEHÍCULO")
                self.comienza = vehiculo.fin                # Actualiza el momento de inicio (del técnico) del proceso actual al momento de fin (del vehículo) del proceso anterior               

                bloques = model_datetime.programa_bloques(       #genera los bloques de comienza y termina de acuerdo al tiempo del proceso
                    str(self.comienza.date()),
                    str(self.comienza.time()),
                    tiempo_proceso,
                    am = (glo.turnos.startAM.get(), glo.turnos.endAM.get()),
                    pm = (glo.turnos.startPM.get(), glo.turnos.endPM.get()))
                self.comienza = bloques[0][0]               # Calcula el momento de inicio (del tecnico) del proceso actual
                self.termina = bloques[-1][-1]              # Calcula el momento de fin (del tecnico) del proceso actual
                self.libre   = self.termina                 # Calcula el momento en que el técnico está disponible
                vehiculo.avanzar_estado(self, bloques)      # Actualiza el estado usando el método de la clase Vehiculo
                print("Los bloques son", bloques)
                for bloque in bloques:  
                    self.historico_asignacion.append((self.vehiculo_actual.id_chasis, *bloque))  # Agrega el nuevo estado con sus caracteríticas al resumen de asignaciones
                return True
            
        except Exception as e:
            print(f"No se ejecutó el método asignar_vehiculo. ****OCURRIÓ UNA EXCEPCIÓN: {e}****") 

        return False

    def __repr__(self):        #Formato de impresión del técnico
        return f"""Tecnico(ID: {self.id_tecnico}, Nombre: {self.nombre}, Especialización: {self.especializacion}, Asignaciones: {self.historico_asignacion}), Libre en : {self.libre}\n"""

class Pedido:
    def __init__(self, id_pedido, fecha_recepcion, plazo_entrega, vehiculos, estado ="PENDIENTE"):
        self.id_pedido = id_pedido
        self.fecha_recepcion = fecha_recepcion
        self.plazo_entrega = plazo_entrega
        self.vehiculos = vehiculos
        self.estado = estado

        self.estado_inicial ={
            "id_pedido" : id_pedido,
            "plazo_entrega" : plazo_entrega,
            "vehiculos" : vehiculos,
            "estado" : estado
        }
        for vehiculo in vehiculos:
            vehiculo.fecha = plazo_entrega
    
    def reset(self):
        for key, value in self.estado_inicial.items():
            setattr(self, key, value)

    def cambia_estado():
        pass

    def __repr__(self):
        return f"Pedido(ID: {self.id_pedido}, Fecha Entrega: {self.plazo_entrega}, Vehículos: {self.vehiculos}), Estado: {self.estado}"

class OrdenProduccion:
    def __init__(self, vehiculo, proceso, tecnico, inicio, fin, tiempo_productivo, pedido):
        self.chasis             = vehiculo.id_chasis
        self.marca              = vehiculo.marca
        self.modelo             = vehiculo.modelo
        self.color              = vehiculo.color
        self.novedades          = vehiculo.novedades
        self.pedido             = pedido
        self.proceso            = proceso
        self.id_tecnico         = tecnico.id_tecnico
        self.nombre_tecnico     = tecnico.nombre
        self.inicio             = inicio
        self.fin                = fin
        self.duracion           = (fin-inicio).total_seconds()/60
        self.tiempo_productivo  = tiempo_productivo
        self.plazo              = vehiculo.fecha
        self.codigo_orden       = self.codificar_orden()

    def codificar_orden(self):
        chasis = self.chasis
        tecnico = self.nombre_tecnico
        proceso = self.proceso
        self.codigo_orden = str(chasis)[-4:].upper() + str(tecnico)[-4:].upper() + str(proceso).upper() + f"{rnd.randint(0, 9999):04d}"
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
        #CRUD.insertar_orden(*datos)

    def __repr__(self):
        return f"Orden: {self.codigo_orden}, Chasis: {self.chasis},Modelo: {self.modelo}, Marca: {self.marca}, Color: {self.color}, Proceso: {self.proceso}, Id_tecnico: {self.id_tecnico} Tecnico: {self.nombre_tecnico}, Pedido(ID: {self.pedido}, Inicio: {self.inicio}, Fin: {self.fin}, Duración: {self.duracion}, Fecha Entrega: {self.plazo}"

class ProgramaDeProduccion:
    def __init__(self, ordenes):
        self.ordenes = ordenes
    
    def obtener_horizonte(self):
        pass

    def __repr__(self):
        ordenes_repr = "\n".join([repr(orden) for orden in self.ordenes])        # Crear una representación legible desagregada
        return f"ProgramaDeProduccion:\n{ordenes_repr}"

    def to_dataframe(self):
        data = [vars(orden) for orden in self.ordenes]        # Convertir las órdenes en una lista de diccionarios
        return pd.DataFrame(data)                             # Crear un DataFrame a partir de la lista de diccionarios

######################################################################################################
################################## FUNCIONES PARA SCHEDULING #########################################
######################################################################################################

def programa_inmediato(pedido, tecnicos, horizonte, fechaStart, horaStart):
    print("INICIA EL PROGRAMADOR\n", "pedido", pedido.id_pedido)
    print("VEHICULOS:___________________\n", pedido.vehiculos)
    print("****tecnicos")
    for tecnico in tecnicos:
        if tecnico.libre == None:
            tecnico.libre = model_datetime.parseDT(fechaStart,horaStart)
        print(tecnico)

    vehiculos_por_programar = pedido.vehiculos.copy()                   # Extrae una copia de la lista de vehiculos

    contador = 0
    while len(vehiculos_por_programar) > 0 and contador <=50:
        contador = contador + 1
        print(f"---------------------->inicia vuelta #{contador}<------------------------")

        tiempos_restantes = list(map(lambda vh: sum(vh.tiempos_proceso), vehiculos_por_programar))  #crea una lista con solo el total de tiempos restante de cada vehiculo
        print("****Tiempos restantes", tiempos_restantes)
        
        indice_min_time = tiempos_restantes.index(min(tiempos_restantes))                           #busca el índice con tiempo restante menor
        vehiculo_min_time = vehiculos_por_programar[indice_min_time]                                #busca el vehiculo con tiempo restante menor
        print(f"****seleccionado {vehiculo_min_time} con tiempo mínimo restante de {tiempos_restantes[indice_min_time]}")

        ultimo_estado = vehiculo_min_time.estado                                                    #Extrae el ultimo estado en el constructor del vehiculo seleccionado
        siguiente_estado = orden_procesos[orden_procesos.index(ultimo_estado) + 1]                  #Imprime el siguiente estado o proceso de la secuencia
        print(f"{vehiculo_min_time.id_chasis} necesita {siguiente_estado}")
        tiempo_neto = vehiculo_min_time.obtener_tiempo_proceso_VH(siguiente_estado)

        if tiempo_neto == 0:                         #Avanza al siguiente estado sin asignar el tecnico en caso de tiempo = 0
            vehiculo_min_time.avanzar_estado(tecnico=None, bloques=None)
            print(f"****Tiempo de proceso{siguiente_estado} de {vehiculo_min_time} es 0")
            print (f"-----------------Termina vuelta #{contador}\n-------------------")
            contador = contador + 1
            print("#############################################################")
            continue

        tecnicos_disponibles = list(filter(lambda tec: siguiente_estado in tec.especializacion, tecnicos))    # incluye solo aquellos técnicos de la especialidad correcta
        print("****Tecnicos disponibles para asignar")
        for tecnico in tecnicos_disponibles:
            print(tecnico.id_tecnico)
        tecnicos_disponibles.sort(key = lambda op: op.libre)                                                  #ordena técnicos por tiempo de menor a mayor

        
        tiempos_disponibles = list(map(lambda operario: operario.libre, tecnicos_disponibles))      #crea una lista solo con los tiempos
        tiempos_disponibles.sort()                                                                  #ordena tiempos de menor a mayor
        print(f"****Tecnicos ordenados por disponibilidad para asignar : {tecnicos_disponibles}")                       #ordena tiempos de menor a mayor
        print(f"****tiempos disponibles : {tiempos_disponibles}")
        tecnico_min_time = tecnicos_disponibles[0]                                                 #selecciona el tecnico de menor tiempo (el primer elemento de la lista)
        print("****Tecnico seleccionado:", tecnico_min_time)

        for times in tiempos_disponibles:                                                         #buscamos en la lista de técnicos

            print(f"****El proceso {siguiente_estado} para el chasis {vehiculo_min_time} queda : {times} + {tiempo_neto}")

            asignado = False
            maximaAsignacion = model_datetime.momentoEnd(model_datetime.programa_bloques(fechaStart,
                                                                               horaStart,
                                                                               horizonte ,
                                                                               am   =   (glo.turnos.startAM.get(), glo.turnos.endAM.get()),
                                                                               pm   =   (glo.turnos.startPM.get(), glo.turnos.endPM.get())))
            terminaAsignacion = model_datetime.momentoEnd(model_datetime.programa_bloques(fecha_inicio = str(times.date()),
                                                                                hora_inicio  = str(times.time()),
                                                                                duracion     = tiempo_neto,
                                                                                am   = (glo.turnos.startAM.get(), glo.turnos.endAM.get()),
                                                                                pm   = (glo.turnos.startPM.get(), glo.turnos.endPM.get())
                                                                                )
                                                    )
            print(f"****Se asignará : {times} + {tiempo_neto} = {terminaAsignacion}")

            if terminaAsignacion <= maximaAsignacion:                                              #verificamos que el tiempo asignado no supere el horizonte
                print("OK. Aun no se supera el horizonte")
                tecnico_min_time.asignar_vehiculo(vehiculo_min_time, times.date(), times.time())   #SE ASIGNA VEHICULO A TÉCNICO desde el método en la clase técnico
                asignado = True
                print(f"****ASIGNADO = {asignado}. Se asignó {vehiculo_min_time.id_chasis} a {tecnico_min_time.id_tecnico} en el proceso {siguiente_estado}\n\n")                
                listaOrdenes.append(OrdenProduccion(vehiculo = vehiculo_min_time, 
                                                    proceso  = siguiente_estado,
                                                    tecnico  = tecnico_min_time,
                                                    inicio   = vehiculo_min_time.inicio,
                                                    fin      = vehiculo_min_time.fin,
                                                    tiempo_productivo = tiempo_neto,
                                                    pedido   = vehiculo_min_time.pedido))
                print(f"****Resumen de orden de producción: {listaOrdenes[-1]}")
                #listaOrdenes[-1].almacenar_orden()
                break
        
        if asignado == False:
            print(f"****¡NO se asignó {vehiculo_min_time.id_chasis}!")

                
        vehiculos_por_programar.remove(vehiculo_min_time)        #REMOVEMOS DE LA LISTA EL VEHICULO QUE SE ACABA DE ASIGNAR               
        print (f"------------------Termina vuelta #{contador}---------------------")
        print("#############################################################")
        print("#############################################################")
        print("#############################################################")
        print("#############################################################")

    scheduling = ProgramaDeProduccion(listaOrdenes)
    df_scheduling = scheduling.to_dataframe()
    print(df_scheduling.to_string())
    return {"id"         : reemplazar_caracteres("inmediato_"+ pedido.id_pedido),
            "vehiculos"  : pedido.vehiculos,
            "programa"   : df_scheduling}

def programa_completo(pedido, tecnicos, horizonte, fechaStart, horaStart):
    print("INICIA EL PROGRAMADOR\n", "pedido", pedido.id_pedido)
    print("VEHICULOS:___________________\n", pedido.vehiculos)
    print("****tecnicos")
    for tecnico in tecnicos:
        if tecnico.libre == None:
            tecnico.libre = model_datetime.parseDT(fechaStart,horaStart)
        print(tecnico)

    vehiculos_por_programar = pedido.vehiculos.copy()                   # Extrae una copia de la lista de vehiculos

    contador = 0
    while len(vehiculos_por_programar) > 0  and contador <=200:
        contador = contador + 1
        print(f"---------------------->inicia vuelta #{contador}<------------------------")

        ind_est_actuales = list(map(lambda vh: orden_procesos.index(vh.estado), vehiculos_por_programar))        # encuentra una lista con los estado actuales de cada vehículo
        print(f"****indice de estados: {ind_est_actuales}")
        print("****historicos de vehiculos")
        for vehic in vehiculos_por_programar:                               #bucle para mostrar en consola el resumen de estados de cada vehiculo
            print(f"{vehic.id_chasis}: {vehic.historico_estados}")
        
        tiempos_restantes = [
            sum(vh.tiempos_proceso[ind_est:] if ind_est < len(vh.tiempos_proceso)
                else [0,0]) for vh, ind_est in zip(vehiculos_por_programar, ind_est_actuales)
            ]
            #crea una lista con solo el total de tiempos restante de cada vehiculo
        print("****Tiempos restantes", tiempos_restantes)


        indice_min_time = tiempos_restantes.index(max(tiempos_restantes))               #busca el índice con tiempo mayor
        vehiculo_min_time = vehiculos_por_programar[indice_min_time]                    #busca el vehiculo con tiempo restante mayor
        print(f"****seleccionado {vehiculo_min_time} con tiempo mínimo restante de {tiempos_restantes[indice_min_time]}")
        ultimo_estado = vehiculo_min_time.estado                                        #Extrae el ultimo estado en el constructor

        siguiente_estado = orden_procesos[orden_procesos.index(ultimo_estado) + 1]      #Obtiene el siguiente estado o proceso de la secuencia
        
        if siguiente_estado == "DESPACHO":
            print(f"<<<<<<<<<Vehiculo {vehiculo_min_time.id_chasis} en despacho>>>>>>>>>")
            vehiculos_por_programar.remove(vehiculo_min_time)
            print (f"--------------Termina vuelta #{contador}\n-----------------")
            contador = contador + 1
            print("#############################################################")
            continue
        
        tiempo_neto = vehiculo_min_time.obtener_tiempo_proceso_VH(siguiente_estado)
        if tiempo_neto == 0:                                                        #Avanza al siguiente estado sin asignar el tecnico en caso de tiempo = 0
            vehiculo_min_time.avanzar_estado(tecnico=None, bloques=None)
            print(f"****Tiempo de proceso{siguiente_estado} de {vehiculo_min_time} es 0")
            print (f"--------------Termina vuelta #{contador}\n-----------------")
            contador = contador + 1
            print("#############################################################")
            continue


        tecnicos_disponibles = list(filter(lambda persona: siguiente_estado in persona.especializacion, tecnicos))    # incluye soloaquellos técnicos de la especialidad correcta
        print("****Tecnicos disponibles para asignar")
        for tecnico in tecnicos_disponibles:
            print(tecnico.id_tecnico)
        tecnicos_disponibles.sort(key = lambda op: op.libre)                                                          #ordena técnicos por tiempo de menor a mayor

        tiempos_disponibles = list(map(lambda operario: operario.libre, tecnicos_disponibles))                        #crea una lista solo con los tiempos
        tiempos_disponibles.sort()    
        print(f"****Tecnicos ordenados por disponibilidad para asignar : {tecnicos_disponibles}")                       #ordena tiempos de menor a mayor
        print(f"****tiempos disponibles : {tiempos_disponibles}")
        tecnico_min_time = tecnicos_disponibles[0]                                                                    #selecciona el técnico de time menor
        print("****Tecnico seleccionado:", tecnico_min_time)

        for times in tiempos_disponibles:                                                                             #buscamos en la lista de técnicos
            print(f"****El proceso {siguiente_estado} para el chasis {vehiculo_min_time} queda : {times} + {tiempo_neto}*****")

            asignado = False
            maximaAsignacion = model_datetime.momentoEnd(model_datetime.programa_bloques(fechaStart,
                                                                               horaStart,
                                                                               horizonte,
                                                                               am=(glo.turnos.startAM.get(), glo.turnos.endAM.get()),
                                                                               pm=(glo.turnos.startPM.get(), glo.turnos.endPM.get())))
            terminaAsignacion = model_datetime.momentoEnd(model_datetime.programa_bloques(str(times.date()),
                                                                                str(times.time()),
                                                                                vehiculo_min_time.obtener_tiempo_proceso(siguiente_estado),
                                                                                am = (glo.turnos.startAM.get(), glo.turnos.endAM.get()),
                                                                                pm = (glo.turnos.startPM.get(), glo.turnos.endPM.get())
                                                                                )
                                                    )
            print(f"****Se asignará : {times}+{tiempo_neto}={terminaAsignacion}")


            if terminaAsignacion <= maximaAsignacion:                                               #verificamos que el tiempo asignado no supere el horizonte
                print("     OK. Aun no se supera el horizonte")
                tecnico_min_time.asignar_vehiculo(vehiculo_min_time, times.date(), times.time())    #SE ASIGNA VEHICULO A TÉCNICO desde el método en la clase técnico
                asignado = True
                print(f"****ASIGNADO = {asignado}. Se asignó {vehiculo_min_time.id_chasis} a {tecnico_min_time.id_tecnico} en el proceso {siguiente_estado}\n\n")                
                listaOrdenes.append(OrdenProduccion(vehiculo = vehiculo_min_time, 
                                                    proceso  = siguiente_estado,
                                                    tecnico  = tecnico_min_time,
                                                    inicio   = vehiculo_min_time.inicio,
                                                    fin      = vehiculo_min_time.fin,
                                                    tiempo_productivo = tiempo_neto,
                                                    pedido   = vehiculo_min_time.pedido))
                print(f"****Resumen de orden de producción: {listaOrdenes[-1]}")
                #listaOrdenes[-1].almacenar_orden()
                break
        
        if asignado == False:
            print(f"****¡NO se asignó {vehiculo_min_time.id_chasis}!")

        if vehiculo_min_time.estado == 'calidad':
            vehiculos_por_programar.remove(vehiculo_min_time)        #REMOVEMOS DE LA LISTA EL VEHICULO QUE TERMINÓ TODOS LOS PROCESOS
            print(f"****Se removió {vehiculo_min_time} porque ya completó proceso de CALIDAD")
            continue             
        
        vehiculo_min_time.vueltas.append(f"vuelta #{contador}")

        print (f"------------------Termina vuelta #{contador}---------------------")
        print("##########################################################################################################################")
        print("##########################################################################################################################")

    scheduling = ProgramaDeProduccion(listaOrdenes)
    df_scheduling = scheduling.to_dataframe()
    #df_scheduling.to_excel(f"programa_completo_{pedido.id_pedido}.xlsx", sheet_name="Hoja1", index=False)
    print(df_scheduling.to_string())
    return {"id"         : reemplazar_caracteres("completo_"+ pedido.id_pedido),
            "vehiculos"  : pedido.vehiculos,
            "programa"   : df_scheduling}

def programar_procesos(pedido, tecnicos, procesos, horizonte, fechaStart, horaStart, bbdd):
    """
    Programa los procesos de un pedido asignando técnicos y generando un programa.

    Args:
        pedido (Pedido): Objeto de la clase Pedido que contiene la información del pedido.
        tecnicos (list[Tecnico]): Lista de objetos de la clase Técnico disponibles.
        procesos (list[str]): Lista de nombres de los procesos a programar.
        horizonte (int): Tiempo en minutos del horizonte de programación.
        fechaStart (datetime): Fecha de inicio del programa.
        horaStart (datetime): Hora de inicio del programa.
        bbdd (str): Nombre de la base de datos.

    Returns:
        dict: Diccionario que contiene:
            - `vehiculos_actualizados` (list[Vehiculo]): Lista de objetos Vehículo con los históricos modificados.
            - `programa` (pd.DataFrame): DataFrame con las órdenes generadas en el programa.

    Etapas de la función:
        1. Seleccionar los técnicos que tienen como especialidad los procesos a programar.
        2. Obtener los históricos de los vehículos desde la base de datos.
        3. Obtener los procesos y tiempos desde la base de datos para todos los vehículos.
        4. Iterar sobre cada vehículo en la lista:
            4.1. Obtener un diccionario con los tiempos restantes por chasis.
            4.2. Seleccionar el vehículo con el menor tiempo restante.
        5. Iterar sobre cada proceso a programar:
            5.1. Avanzar el primer proceso de la lista para el vehículo.
            5.2. Asignar el vehículo a un técnico especializado en el proceso.
            5.3. Generar la orden correspondiente.
            5.4. Remover vehículos ya asignados
        6. Generar el programa de producción y convertirlo en un df
    """

    print("INICIA EL PROGRAMADOR\n", "pedido", pedido.id_pedido)
    print("VEHICULOS:___________________\n", pedido.vehiculos)
    print("****tecnicos")

    tecnicos_de_proceso = list(filter(lambda tec: tec.especializacion in procesos, tecnicos))   #selecciona solo a los técnicos que tiene como especialidad el proceso a programar
    for tecnico in tecnicos_de_proceso:
        if tecnico.libre == None:
            tecnico.libre = model_datetime.parseDT(fechaStart,horaStart)                 #Da formato de datetime a la propiedad "libre" de  los objetos Técnico recién inicializados
        print(tecnico)

    vehiculos_por_programar = pedido.vehiculos.copy()                               # Extrae una copia de la lista de vehículos

    for vehiculo in vehiculos_por_programar:                                        # obtiene los historicos de la base de datos y los agrega a la lista en el atributo historico_estados
        vehiculo.obtener_historicos(bbdd, vehiculo.id_chasis)
        print("###-----------------###Vehiculo :", vehiculo.id_chasis,  vehiculo.historico_estados)  

    #vehiculos_por_programar = [vehiculo for vehiculo in vehiculos_por_programar     # Filtrar vehiculos de acuerdo a, si el primer elemento (el estado) de     
    #                            if vehiculo.historico_estados[0] in procesos]       # historico_estados se encuentra en la lista de procesos
     
    todos_los_procesos = list(BBDD.obtener_id_procesos(bbdd))                       # leer los ids de procesos en BD
    todos_los_tiempos = BBDD.leer_tiempos_vehiculos_df(bbdd)                  # obtener un dataframe con los tiempos por vehiculo
    print(todos_los_tiempos)

    contador = 0
    while len(vehiculos_por_programar) > 0 and contador <=50:
        contador += 1
        print(f"---------------------->inicia vuelta #{contador}<------------------------")



        ################################################## CALCULAMOS TIEMPOS RESTANTES ##########################################################
        tiempos_restantes = {}                                          # Crear un diccionario donde se almacenarán las sumas de los tiempos
        for vehiculo in vehiculos_por_programar:                        # Iterar sobre cada vehículo de la
            print(f"vehiculo:  {vehiculo.id_chasis}")
            print(vehiculo.historico_estados)
            procesos_listos = []                                        # crear una lista para el vehiculo de turno donde se agregarán los procesos ya ejecutados, o en ejecución
            
            for estado in vehiculo.historico_estados:                   # Iterar sobre el historico de estados
                print(estado)
                procesos_listos.append(estado[0])                       # agregar cada proceso presente en histórico estados, a la lista
            print(vehiculo.id_chasis, ". procesos listos: ", procesos_listos)

            if vehiculo.id_chasis not in tiempos_restantes:             # Inicializar tiempos_restantes para cada chasis (para poder inicializar el diccionario)
                tiempos_restantes[vehiculo.id_chasis] = 0               

            procesos_faltantes = [proceso for proceso in todos_los_procesos             # verificar cuales procesos no están en la lista de histórico estados
                                    if proceso not in procesos_listos]                  # y crear una lista con estos procesos 
            print(vehiculo.id_chasis, ". procesos faltantes: ", procesos_faltantes)

            for id_proc_faltante in procesos_faltantes:                                                         # Iterar la lista de procesos que están en históricos estados del vehiculo
                clave = todos_los_tiempos.loc[todos_los_tiempos['CHASIS'] == vehiculo.id_chasis].index[0]       # obtener la clave del chasis en el dataframe
                tiempo = todos_los_tiempos.loc[clave, id_proc_faltante]                                         # Obtener el tiempo correspondiente a la clave anterior en el DataFrame
                tiempos_restantes[vehiculo.id_chasis] += int(tiempo)                                                 # agregar al diccionario de tiempos el id_proceso (clave) y el tiempo de proceso (valor)

        
        print("****Tiempos restantes", tiempos_restantes)
        ######################################################################################################################################



        ###################################### SELECCIONAMOS VEHICULO CON TIEMPO RESTANTE MENOR ##############################################
        chasis_min_time = next((key for key, value in tiempos_restantes.items() if value == min(tiempos_restantes.values())), None)     # busca la clave en el diccionario de tiempos restantes, cuyo valor es el tiempo minimo
        vehiculo_min_time = [vehiculo for vehiculo in vehiculos_por_programar   if vehiculo.id_chasis == chasis_min_time][0]            # busca el vehiculo con tiempo restante menor
        print(f"****seleccionado {vehiculo_min_time} con tiempo mínimo restante de {tiempos_restantes[chasis_min_time]}")
        ######################################################################################################################################


        procesos_asignados = 0
        for proceso in procesos:
            print(f"asignará el proceso {proceso}")
            if any(estado[0] == proceso for estado in list(vehiculo_min_time.historico_estados)) == True:                # Comprobamos si el proceso ya fue ejecutado anteriormente
                print(f"{vehiculo_min_time.id_chasis} ya había pasado por {proceso}")
                continue
            
            tiempo_neto = vehiculo_min_time.obtener_tiempo_proceso_VH(proceso)
            if tiempo_neto == 0:                                                            # Comprobamos si el tiempo de proceso es cero
                print(f"****Tiempo de proceso{proceso} de {vehiculo_min_time.id_chasis} es 0")
                vehiculo_min_time.ingresar_a_proceso(tecnico=None, bloques=None, estado = proceso)
                continue
            


            tecnicos_disponibles = list(filter(lambda tec: proceso in tec.especializacion, tecnicos_de_proceso))    # incluye solo aquellos técnicos de la especialidad correcta
            print("****Tecnicos disponibles para asignar")
            for tecnico in tecnicos_disponibles:
                print(tecnico.id_tecnico)
            tecnicos_disponibles.sort(key = lambda operario: operario.libre)

            tiempos_disponibles = list(map(lambda operario: operario.libre, tecnicos_disponibles))      # crea una lista solo con los instantes
            tiempos_disponibles.sort()                                                                  # ordena instantes de menor a mayor
            print(f"****Tecnicos ordenados por disponibilidad para asignar : {tecnicos_disponibles}")
            print(f"****tiempos disponibles : {tiempos_disponibles}")
            tecnico_min_time = tecnicos_disponibles[0]                                                  # selecciona el tecnico de menor tiempo (el primer elemento de la lista)
            print("****Tecnico seleccionado:", tecnico_min_time)
    
       

            for times in tiempos_disponibles:     #buscamos en la lista de técnicos
                print(f"****El proceso {proceso} para el chasis {vehiculo_min_time} queda : {times} + {tiempo_neto}")

                asignado = False
                maximaAsignacion = model_datetime.momentoEnd(model_datetime.programa_bloques(fechaStart,
                                                                                   horaStart,
                                                                                   horizonte ,
                                                                                   am=(glo.turnos.startAM.get(), glo.turnos.endAM.get()), 
                                                                                   pm=(glo.turnos.startPM.get(), glo.turnos.endPM.get())))
                terminaAsignacion = model_datetime.momentoEnd(model_datetime.programa_bloques(
                                                                                    str(times.date()),
                                                                                    str(times.time()),
                                                                                    vehiculo_min_time.obtener_tiempo_proceso(proceso),
                                                                                    am = (glo.turnos.startAM.get(), glo.turnos.endAM.get()),
                                                                                    pm = (glo.turnos.startPM.get(), glo.turnos.endPM.get())
                                                                                    )
                                                        )
                print(f"****Se asignará : {times} + {tiempo_neto} = {terminaAsignacion}")


                if terminaAsignacion <= maximaAsignacion:                          #verificamos que el tiempo asignado no supere el horizonte
                    print("OK. Aun no se supera el horizonte")
                    tecnico_min_time.asignar_vehiculo(vehiculo_min_time, times.date(), times.time())                                    #SE ASIGNA VEHICULO A TÉCNICO desde el método en la clase técnico
                    asignado = True
                    print(f"****ASIGNADO = {asignado}. Se asignó {vehiculo_min_time.id_chasis} a {tecnico_min_time.id_tecnico} en el proceso {proceso}\n\n")                
                    listaOrdenes.append(OrdenProduccion(vehiculo = vehiculo_min_time, 
                                                        proceso  = proceso,
                                                        tecnico  = tecnico_min_time,
                                                        inicio   = vehiculo_min_time.inicio,
                                                        fin      = vehiculo_min_time.fin,
                                                        tiempo_productivo = tiempo_neto,
                                                        pedido   = vehiculo_min_time.pedido))
                    print(f"****Resumen de orden de producción: {listaOrdenes[-1]}")
                    #listaOrdenes[-1].almacenar_orden()
                    break
            
            if asignado == False:
                print(f"****¡NO se asignó {vehiculo_min_time.id_chasis}!")

        if procesos_asignados == 0:
            vehiculos_por_programar.remove(vehiculo_min_time)
            print(f"se removió {vehiculo_min_time.id_chasis} porque ya tenía ejecutados los procesos")
            continue

        vehiculos_por_programar.remove(vehiculo_min_time)        #REMOVEMOS DE LA LISTA EL VEHICULO QUE SE ACABA DE ASIGNAR        
        print(f"se removio {vehiculo_min_time} porque ya tiene asignado los procesos planificados")       
        print (f"------------------Termina vuelta #{contador}---------------------")
        print("##########################################################################################################################")
        print("##########################################################################################################################")
        

    scheduling = ProgramaDeProduccion(listaOrdenes)
    df_scheduling = scheduling.to_dataframe()
    #df_scheduling.to_excel(f"programa_{procesos}_{pedido.id_pedido}.xlsx", sheet_name="Hoja1", index=False)
    print(df_scheduling.to_string())
    return {"id"         : reemplazar_caracteres(f"procesos{procesos}"+ pedido.id_pedido),
            "vehiculos"  : pedido.vehiculos,
            "programa"   : df_scheduling}

def calcular_horizonte(pedido):
    vehiculos_programados = []                       # Lista para almacenar vehículos válidos
    
    for vh in pedido.vehiculos:
        if isinstance(vh.fin, datetime):             # Comprobar si fin es un datetime y agregar a la lista si es válido
            vehiculos_programados.append(vh)
        else:
            print(f"Vehículo con chasis {vh.id_chasis} tiene un fin no válido: {vh.fin}")

    if vehiculos_programados:                        # Si hay vehículos válidos, calcular el horizonte
        return max(vehiculos_programados, key=lambda vh: vh.fin).fin
    else:
        print("No hay vehículos programados válidos.")
        return None

def reemplazar_caracteres(cadena):
    # Usamos expresiones regulares para reemplazar los caracteres no deseados
    cadena_modificada = re.sub(r'''[\[\]{}\'",.]''', '', cadena)
    cadena_final = re.sub(r' ', '', cadena_modificada)
    return cadena_final
