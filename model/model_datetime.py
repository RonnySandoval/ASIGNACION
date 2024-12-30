import controller.glo as glo
import pandas as pd
from datetime import datetime, timedelta
import database.BBDD as BBDD

###############################################################################
###############################################################################
from datetime import datetime, timedelta

def parseDT(stringFecha, stringHora):
    fecha_hora_inicio = f"{stringFecha} {stringHora}"                   # Concatenar fecha y hora para crear una cadena completa de fecha y hor
    #print("prueba", datetime.strptime(fecha_hora_inicio, "%Y-%m-%d %H:%M"))
    return datetime.strptime(fecha_hora_inicio, "%Y-%m-%d %H:%M:%S")       # Convertir la fecha y hora de inicio a un objeto datetime

def calcular_hora_final(fecha_inicio, hora_inicio, duracion):

    fecha_hora_inicio = f"{fecha_inicio} {hora_inicio}"                 # Concatenar fecha y hora para crear una cadena completa de fecha y hora
    inicio = datetime.strptime(fecha_hora_inicio, "%Y-%m-%d %H:%M:%S")   # Convertir la fecha y hora de inicio a un objeto datetime
    tiempo_final = inicio + timedelta(minutes=duracion)                 # Sumar los minutos a la hora de inicio
    return inicio, tiempo_final                                         # Retornar ambos objetos datetime

def calcular_hora_finalDT(date_time, duracion):

    inicio = date_time                                    # Asignar datatime al inicio
    tiempo_final = inicio + timedelta(minutes=duracion)   # Sumar los minutos a la hora de inicio
    return tiempo_final                           # Retornar ambos objetos datetime

def separar_fecha_hora(cadena):
    # Convertir la cadena en un objeto datetime
    dt_obj = datetime.strptime(cadena, "%Y-%m-%d %H:%M:%S")
    
    # Extraer la fecha y la hora
    fecha = dt_obj.date()
    hora = dt_obj.time()
    
    return fecha, hora

###############################################################################
###############################################################################
def obtener_dia_semana(fecha):

    dias_semana = {
        "Monday"   : "Lunes",
        "Tuesday"  : "Martes",
        "Wednesday": "Miercoles",
        "Thursday" : "Jueves",
        "Friday"   : "Viernes",
        "Saturday" : "Sabado",
        "Sunday"   : "Domingo"
    }

    #fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")    # Convertir la cadena de fecha en un objeto datetime
    dia_semana_ingles = fecha.date().strftime("%A")        # Obtener el nombre del día de la semana en inglés
    return dias_semana[dia_semana_ingles]                           # Retornar la traducción al español

def siguiente_dia(fecha):
    return fecha  +1

###############################################################################
###############################################################################
def horas_no_laborables(fecha):
    if pd.isna(fecha):
        fecha_ahora = str(datetime.now().date())
    else:
        fecha_ahora = fecha
    # Crear tuplas de cadenas con formato 'YYYY-MM-DD HH:MM:SS'
    madrugada = (
        datetime.strptime(f"{fecha_ahora} 00:00:00", "%Y-%m-%d %H:%M:%S"),
        datetime.strptime(f"{fecha_ahora} {glo.turnos.startAM.get()}:00", "%Y-%m-%d %H:%M:%S")
        )

    mediodia  = (
        datetime.strptime(f"{fecha_ahora} {glo.turnos.endAM.get()}:00", "%Y-%m-%d %H:%M:%S"),
        datetime.strptime(f"{fecha_ahora} {glo.turnos.startPM.get()}:00", "%Y-%m-%d %H:%M:%S")
        )

    noche     = (
        datetime.strptime(f"{fecha_ahora} {glo.turnos.endPM.get()}:00", "%Y-%m-%d %H:%M:%S"),
        datetime.strptime(f"{fecha_ahora} 23:59:00", "%Y-%m-%d %H:%M:%S")
        )

    return {
        "madrugada": madrugada, 
        "mediodia": mediodia, 
        "noche": noche
    }

def horas_laborables(fecha):
    if pd.isna(fecha):
        fecha_ahora = str(datetime.now().date())
    else:
        fecha_ahora = fecha

    # Crear tuplas de cadenas con formato 'YYYY-MM-DD HH:MM:SS'
    manana = (
        datetime.strptime(f"{fecha_ahora} {glo.turnos.startAM.get()}:00", "%Y-%m-%d %H:%M:%S"),
        datetime.strptime(f"{fecha_ahora} {glo.turnos.endAM.get()}:00", "%Y-%m-%d %H:%M:%S")
        )

    tarde  = (
        datetime.strptime(f"{fecha_ahora} {glo.turnos.startPM.get()}:00", "%Y-%m-%d %H:%M:%S"), 
        datetime.strptime(f"{fecha_ahora} {glo.turnos.endPM.get()}:00", "%Y-%m-%d %H:%M:%S")
        )

    return {
        "manana": manana, 
        "tarde": tarde
    }

def define_franja(fecha_hora):
    franjas ={
        glo.turnos.cero           :horas_no_laborables(fecha_hora)["madrugada"][0],
        glo.turnos.startAM.get()  :horas_laborables(fecha_hora)["manana"][0],
        glo.turnos.endAM.get()    :horas_no_laborables(fecha_hora)["mediodia"][0],
        glo.turnos.startPM.get()  :horas_laborables(fecha_hora)["tarde"][0],
        glo.turnos.endPM.get()    :horas_no_laborables(fecha_hora)["noche"][0]
        }
    
    return franjas

###############################################################################
###############################################################################

def progBloqueMadrugada(inicio, duracion, am, pm, bloques):

    fecha_inicio = str(inicio.date())
    fin = calcular_hora_finalDT(inicio, duracion)


    if fin <= define_franja(fecha_inicio)[am[1]]:
        bloques.append((inicio, fin))
        return 0
    
    inicio1 = define_franja(fecha_inicio)[am[0]]
    fin1 = define_franja(fecha_inicio)[am[1]]
    bloques.append((inicio1,fin1))
    return duracion-240

def progBloqueManana(inicio, duracion, am, pm, bloques):

    fecha_inicio = str(inicio.date())
    fin = calcular_hora_finalDT(inicio, duracion)

    if fin <= define_franja(fecha_inicio)[am[1]]:
        bloques.append((inicio, fin))
        return 0

    inicio1 = inicio
    fin1 = define_franja(fecha_inicio)[am[1]]
    bloques.append((inicio1,fin1))
    min_asignados=(int((fin1-inicio1).total_seconds()))/60
    return duracion-min_asignados

def progBloqueMediodia(inicio, duracion, am, pm, bloques):

    fecha_inicio = str(inicio.date())
    inicio = define_franja(fecha_inicio)[pm[0]]
    fin = calcular_hora_finalDT(inicio, duracion)

    if fin <= define_franja(fecha_inicio)[pm[1]]:
        bloques.append((inicio, fin))
        return 0
    
    inicio1 = define_franja(fecha_inicio)[pm[0]]
    fin1 = define_franja(fecha_inicio)[pm[1]]
    bloques.append((inicio1,fin1))
    min_asignados=(int((fin1-inicio1).total_seconds()))/60
    return duracion-min_asignados

def progBloqueTarde(inicio, duracion, am, pm, bloques):
    fecha_inicio = str(inicio.date())
    fin = calcular_hora_finalDT(inicio, duracion)

    if fin <= define_franja(fecha_inicio)[pm[1]]:
        bloques.append((inicio, fin))
        return 0
    
    inicio1 = inicio
    fin1 = define_franja(fecha_inicio)[pm[1]]
    min_asignados=(int((fin1-inicio1).total_seconds()))/60
    bloques.append((inicio1,fin1))
    return duracion-min_asignados

def progBloqueNoche(inicio, duracion, am, pm, bloques):
    next_dia = inicio + timedelta(days=1)
    new_inicio = define_franja(next_dia.date())[am[0]]
    return progBloqueMadrugada(new_inicio, duracion, am, pm, bloques)

def programa_bloques(fecha_inicio, hora_inicio, duracion, am, pm):
    bloques = []
    duracionFaltante = duracion
    dia = fecha_inicio
    momento = datetime.strptime(f"{fecha_inicio} {hora_inicio}", "%Y-%m-%d %H:%M:%S")     # Convertir la fecha y hora de inicio a un objeto datetime
    contador = 0

    while duracion != 0 and contador <=30:
        contador+=1
        #print("------------------------------>vuelta #", contador, ". ", obtener_dia_semana(momento), ". ", momento,"<--------------------------------")
        
        #EVUALUA SI ES FIN DE SEMANA, Y EN CASO AFIRMATIVO LO ACTUALIZA A LUNES
        if obtener_dia_semana(momento) == "Sabado":
                momento = momento + timedelta(days=2)
                momento = define_franja(momento.date())[am[0]]

        if obtener_dia_semana(momento) == "Domingo":
                momento = momento + timedelta(days=1)
                momento = define_franja(momento.date())[am[0]]

        #CASO ANTES DE LAS 8AM
        if momento.time() <  define_franja(dia)[am[0]].time():                    #Evalua si está antes de las 8 am
            #print(f"Entro en CASO ANTES DE LAS 8AM")
            duracionFaltante = progBloqueMadrugada(momento, duracionFaltante, am, pm, bloques)    #Programa un bloque en la mañana y actualiza el tiempo por programar
            if duracionFaltante == 0:                                                          #Determina si terminó antes del mediodía
                #print("retornó en CASO ANTES DE LAS 8AM")
                return bloques                                                              #Rompe el ciclo de ejecución de la función
            momento = define_franja(momento.date())[am[1]]                                  #Actualiza el momento donde terminó a mediodía
            
        #CASO ENTRE 8AM Y 12M
        if momento.time() >= define_franja(dia)[am[0]].time() and momento.time() <  define_franja(fecha_inicio)[am[1]].time():    #Evalua si está durante la mañana.
            #print(f"Entro en CASO ENTRE 8AM Y 12M")
            duracionFaltante = progBloqueManana(momento, duracionFaltante, am, pm, bloques)       #Programa un bloque en la mañana y actualiza el tiempo por programar
            if duracionFaltante == 0:                                                          #Determina si terminó antes del mediodía
                #print("retornó en CASO ENTRE 8AM y 12 M")
                return bloques                                                              #Rompe el ciclo de ejecución de la función
            momento = define_franja(momento.date())[am[1]]                                  #Actualiza el momento donde terminó a mediodía

        #CASO ENTRE LAS 12M Y 2PM
        if momento.time() >= define_franja(dia)[am[1]].time() and momento.time() <  define_franja(fecha_inicio)[pm[0]].time():
            #print(f"Entro en CASO ENTRE LAS 12M Y 2PM")
            duracionFaltante = progBloqueMediodia(momento, duracionFaltante, am, pm, bloques)     #Programa un bloque en la mañana y actualiza el tiempo por programar
            if duracionFaltante == 0:                                                          #Determina si terminó antes del mediodía
                #print("retornó en CASO ENTRE 12M y 2PM")
                return bloques                                                              #Rompe el ciclo de ejecución de la función
            momento = define_franja(momento.date())[pm[1]]                                  #Actualiza el momento donde terminó la tarde
        
        #CASO ENTRE LAS 2PM Y 6PM
        if momento.time() >= define_franja(dia)[pm[0]].time() and momento.time() <  define_franja(fecha_inicio)[pm[1]].time():
            #print(f"Entro en CASO ENTRE LAS 2PM Y 6PM")
            duracionFaltante = progBloqueTarde(momento, duracionFaltante, am, pm, bloques)  #Programa un bloque en la mañana y actualiza el tiempo por programar
            if duracionFaltante == 0:                                                       #Determina si terminó antes del mediodía
                #print("retornó en CASO ENTRE 2PM y 6PM")
                return bloques                                                              #Rompe el ciclo de ejecución de la función
            momento = define_franja(momento.date())[pm[1]]                                  #Actualiza el momento donde terminó en la tarde

        #CASO 6PM y TIEMPO RESTANTE distinto DE 0
        if momento == define_franja(momento.date())[pm[1]] and duracionFaltante !=0:
            #print(f"Entro en CASO 6PM y duracionFaltante!=0")                    
            momento = momento + timedelta(days=1)
            momento = define_franja(momento.date())[am[0]]

        #CASO FIN DE SEMANA
        if obtener_dia_semana(momento) == "Sabado" or obtener_dia_semana(momento)=="Domingo":
            #print("Entró en caso fin de semana")
            continue

        #CASO ENTRE LAS 6PM Y 12PM
        if momento.time() >= define_franja(dia)[pm[1]].time():
            #print(f"Entro en CASO ENTRE LAS 6PM Y 12PM")
            duracionFaltante = progBloqueNoche(momento, duracionFaltante, am, pm, bloques)  #Programa un bloque en la mañana al día siguiente y actualiza el tiempo por programar
            momento = momento + timedelta(days=1)                                           #Actualiza al día siguiente
            momento = define_franja(momento.date())[am[1]]                                  
            if duracionFaltante == 0:
                #print("retornó en CASO DESPUES DE 6PM")                
                return bloques

def momentoEnd (bloques):
    #print("***************final de horizonte: ", bloques[-1][-1], obtener_dia_semana(bloques[-1][-1]) )
    return bloques[-1][-1]

###############################################################################

def definir_bloques(startAM, endAM, startPM, endPM, inicio, fin):
    initDT   = inicio #datetime.datetime.strptime(inicio, "%Y-%m-%d %H:%M:%S")
    finishDT = fin #datetime.datetime.strptime(fin, "%Y-%m-%d %H:%M:%S")
    fecha_inicio = initDT.date()
    hora_inicio  = initDT.time()
    fecha_fin    = finishDT.date()
    hora_fin     = finishDT.time()
    deltaFecha = (fecha_fin - fecha_inicio).days
    
    if (hora_inicio <= endAM)       and    (hora_fin <= endAM):
        if   (deltaFecha == 0):
            return
        elif (deltaFecha == 1):
            print("3 bloques")
            bloques = [concatenar_datetime([hora_inicio, endAM], fecha_inicio), 
                       concatenar_datetime([startPM, endPM],     fecha_inicio),
                       concatenar_datetime([startAM, hora_fin],  fecha_fin)]
        elif (deltaFecha == 2):
            print("5 bloques")
            bloques = [concatenar_datetime([hora_inicio, endAM], fecha_inicio),
                       concatenar_datetime([startPM, endPM],     fecha_inicio),
                       concatenar_datetime([startAM, endAM],     fecha_inicio + timedelta(days=1)),
                       concatenar_datetime([startPM, endPM],     fecha_inicio + timedelta(days=1)),
                       concatenar_datetime([startAM, hora_fin],  fecha_fin)]
        elif (deltaFecha == 3):
            print("7 bloques")
            bloques = [concatenar_datetime([hora_inicio, endAM], fecha_inicio),
                       concatenar_datetime([startPM, endPM],     fecha_inicio),
                       concatenar_datetime([startAM, endAM],     fecha_inicio + timedelta(days=1)),
                       concatenar_datetime([startPM, endPM],     fecha_inicio + timedelta(days=1)),
                       concatenar_datetime([startAM, endAM],     fecha_inicio + timedelta(days=2)),
                       concatenar_datetime([startPM, endPM],     fecha_inicio + timedelta(days=2)),
                       concatenar_datetime([startAM, hora_fin],  fecha_fin)]
        elif (deltaFecha == 4):
            print("9 bloques")
            bloques = [concatenar_datetime([hora_inicio, endAM], fecha_inicio),
                       concatenar_datetime([startPM, endPM],     fecha_inicio),
                       concatenar_datetime([startAM, endAM],     fecha_inicio + timedelta(days=1)),
                       concatenar_datetime([startPM, endPM],     fecha_inicio + timedelta(days=1)),
                       concatenar_datetime([startAM, endAM],     fecha_inicio + timedelta(days=2)),
                       concatenar_datetime([startPM, endPM],     fecha_inicio + timedelta(days=2)),
                       concatenar_datetime([startAM, endAM],     fecha_inicio + timedelta(days=3)),
                       concatenar_datetime([startPM, endPM],     fecha_inicio + timedelta(days=3)),
                       concatenar_datetime([startAM, hora_fin],  fecha_fin)]
        elif (deltaFecha == 5):
            print("9 bloques")
            bloques = [concatenar_datetime([hora_inicio, endAM], fecha_inicio),
                       concatenar_datetime([startPM, endPM],     fecha_inicio),
                       concatenar_datetime([startAM, endAM],     fecha_inicio + timedelta(days=1)),
                       concatenar_datetime([startPM, endPM],     fecha_inicio + timedelta(days=1)),
                       concatenar_datetime([startAM, endAM],     fecha_inicio + timedelta(days=2)),
                       concatenar_datetime([startPM, endPM],     fecha_inicio + timedelta(days=2)),
                       concatenar_datetime([startAM, endAM],     fecha_inicio + timedelta(days=3)),
                       concatenar_datetime([startPM, endPM],     fecha_inicio + timedelta(days=3)),
                       concatenar_datetime([startAM, endAM],     fecha_inicio + timedelta(days=4)),
                       concatenar_datetime([startPM, endPM],     fecha_inicio + timedelta(days=4)),
                       concatenar_datetime([startAM, hora_fin],  fecha_fin)]

    if (hora_inicio >= startPM)     and    (hora_fin >= startPM):
        if   (deltaFecha == 0):
            return
        elif (deltaFecha == 1):
            print("3 bloques")
            bloques = [concatenar_datetime([hora_inicio, endPM], fecha_inicio),
                       concatenar_datetime([startAM, endAM],     fecha_fin),
                       concatenar_datetime([startPM, hora_fin],  fecha_fin)]
        elif (deltaFecha == 2):
            print("5 bloques")
            bloques = [concatenar_datetime([hora_inicio, endPM], fecha_inicio),
                       concatenar_datetime([startAM, endAM],     fecha_inicio + timedelta(days=1)),
                       concatenar_datetime([startPM, endPM],     fecha_inicio + timedelta(days=1)),
                       concatenar_datetime([startAM, endAM],     fecha_fin),
                       concatenar_datetime([startPM, hora_fin],  fecha_fin)]
        elif (deltaFecha == 3):
            print("7 bloques")
            bloques = [concatenar_datetime([hora_inicio, endPM], fecha_inicio),
                       concatenar_datetime([startAM, endAM],     fecha_inicio + timedelta(days=1)),
                       concatenar_datetime([startPM, endPM],     fecha_inicio + timedelta(days=1)),
                       concatenar_datetime([startAM, endAM],     fecha_inicio + timedelta(days=2)),
                       concatenar_datetime([startPM, endPM],     fecha_inicio + timedelta(days=2)),
                       concatenar_datetime([startAM, endAM],     fecha_fin),
                       concatenar_datetime([startPM, hora_fin],  fecha_fin)]
        elif (deltaFecha == 4):
            print("9 bloques")
            bloques = [concatenar_datetime([hora_inicio, endPM], fecha_inicio),
                       concatenar_datetime([startAM, endAM],     fecha_inicio + timedelta(days=1)),
                       concatenar_datetime([startPM, endPM],     fecha_inicio + timedelta(days=1)),
                       concatenar_datetime([startAM, endAM],     fecha_inicio + timedelta(days=2)),
                       concatenar_datetime([startPM, endPM],     fecha_inicio + timedelta(days=2)),
                       concatenar_datetime([startAM, endAM],     fecha_inicio + timedelta(days=3)),
                       concatenar_datetime([startPM, endPM],     fecha_inicio + timedelta(days=3)),
                       concatenar_datetime([startAM, endAM],     fecha_fin),
                       concatenar_datetime([startPM, hora_fin],  fecha_fin)]
        elif (deltaFecha == 5):
            print("11 bloques")
            bloques = [concatenar_datetime([hora_inicio, endPM], fecha_inicio),
                       concatenar_datetime([startAM, endAM],     fecha_inicio + timedelta(days=1)),
                       concatenar_datetime([startPM, endPM],     fecha_inicio + timedelta(days=1)),
                       concatenar_datetime([startAM, endAM],     fecha_inicio + timedelta(days=2)),
                       concatenar_datetime([startPM, endPM],     fecha_inicio + timedelta(days=2)),
                       concatenar_datetime([startAM, endAM],     fecha_inicio + timedelta(days=3)),
                       concatenar_datetime([startPM, endPM],     fecha_inicio + timedelta(days=3)),
                       concatenar_datetime([startAM, endAM],     fecha_inicio + timedelta(days=4)),
                       concatenar_datetime([startPM, endPM],     fecha_inicio + timedelta(days=4)),
                       concatenar_datetime([startAM, endAM],     fecha_fin),
                       concatenar_datetime([startPM, hora_fin],  fecha_fin)]

    if (hora_inicio <= endAM)       and    (hora_fin >= startPM):
        if   (deltaFecha == 0):
            print("2 bloques")
            bloques = [concatenar_datetime([hora_inicio, endAM], fecha_inicio),
                       concatenar_datetime([startPM, hora_fin],  fecha_fin)]
        elif (deltaFecha == 1):
            print("4 bloques")
            bloques = [concatenar_datetime([hora_inicio, endAM], fecha_inicio),
                       concatenar_datetime([startPM, endPM],     fecha_inicio),
                       concatenar_datetime([startAM, endAM],     fecha_fin),
                       concatenar_datetime([startPM, hora_fin],  fecha_fin)]
        elif (deltaFecha == 2):
            print("6 bloques")
            bloques = [concatenar_datetime([hora_inicio, endAM], fecha_inicio),
                       concatenar_datetime([startPM, endPM],     fecha_inicio),
                       concatenar_datetime([startAM, endAM],     fecha_inicio + timedelta(days=1)),
                       concatenar_datetime([startPM, endPM],     fecha_inicio + timedelta(days=1)),
                       concatenar_datetime([startAM, endAM],     fecha_fin),
                       concatenar_datetime([startPM, hora_fin],  fecha_fin)]
        elif (deltaFecha == 3):
            print("8 bloques")
            bloques = [concatenar_datetime([hora_inicio, endAM], fecha_inicio),
                       concatenar_datetime([startPM, endPM],     fecha_inicio),
                       concatenar_datetime([startAM, endAM],     fecha_inicio + timedelta(days=1)),
                       concatenar_datetime([startPM, endPM],     fecha_inicio + timedelta(days=1)),
                       concatenar_datetime([startAM, endAM],     fecha_inicio + timedelta(days=2)),
                       concatenar_datetime([startPM, endPM],     fecha_inicio + timedelta(days=2)),
                       concatenar_datetime([startAM, endAM],     fecha_fin),
                       concatenar_datetime([startPM, hora_fin],  fecha_fin)]
        elif (deltaFecha == 4):
            print("10 bloques")
            bloques = [concatenar_datetime([hora_inicio, endAM], fecha_inicio),
                       concatenar_datetime([startPM, endPM],     fecha_inicio),
                       concatenar_datetime([startAM, endAM],     fecha_inicio + timedelta(days=1)),
                       concatenar_datetime([startPM, endPM],     fecha_inicio + timedelta(days=1)),
                       concatenar_datetime([startAM, endAM],     fecha_inicio + timedelta(days=2)),
                       concatenar_datetime([startPM, endPM],     fecha_inicio + timedelta(days=2)),
                       concatenar_datetime([startAM, endAM],     fecha_inicio + timedelta(days=3)),
                       concatenar_datetime([startPM, endPM],     fecha_inicio + timedelta(days=3)),
                       concatenar_datetime([startAM, endAM],     fecha_fin),
                       concatenar_datetime([startPM, hora_fin],  fecha_fin)]
            
    if (hora_inicio >= startPM)     and    (hora_fin <= endAM):
        if   (deltaFecha == 1):
            print("2 bloques")
            bloques = [concatenar_datetime([hora_inicio, endPM], fecha_inicio),
                       concatenar_datetime([startAM, hora_fin],  fecha_fin)]
        elif (deltaFecha == 2):
            print("4 bloques")
            bloques = [concatenar_datetime([hora_inicio, endPM], fecha_inicio),
                       concatenar_datetime([startAM, endAM],     fecha_inicio + timedelta(days=1)),
                       concatenar_datetime([startPM, endPM],     fecha_inicio + timedelta(days=1)),
                       concatenar_datetime([startAM, hora_fin],  fecha_fin)]
        elif (deltaFecha == 3):
            print("6 bloques")
            bloques = [concatenar_datetime([hora_inicio, endPM], fecha_inicio),
                       concatenar_datetime([startAM, endAM],     fecha_inicio + timedelta(days=1)),
                       concatenar_datetime([startPM, endPM],     fecha_inicio + timedelta(days=1)),
                       concatenar_datetime([startAM, endAM],     fecha_inicio + timedelta(days=2)),
                       concatenar_datetime([startPM, endPM],     fecha_inicio + timedelta(days=2)),
                       concatenar_datetime([startAM, hora_fin],  fecha_fin)]
        elif (deltaFecha == 4):
            print("8 bloques")
            bloques = [concatenar_datetime([hora_inicio, endPM], fecha_inicio),
                       concatenar_datetime([startAM, endAM],     fecha_inicio + timedelta(days=1)),
                       concatenar_datetime([startPM, endPM],     fecha_inicio + timedelta(days=1)),
                       concatenar_datetime([startAM, endAM],     fecha_inicio + timedelta(days=2)),
                       concatenar_datetime([startPM, endPM],     fecha_inicio + timedelta(days=2)),
                       concatenar_datetime([startAM, endAM],     fecha_inicio + timedelta(days=3)),
                       concatenar_datetime([startPM, endPM],     fecha_inicio + timedelta(days=3)),
                       concatenar_datetime([startAM, hora_fin],  fecha_fin)]

    return bloques

def concatenar_datetime(lista_tiempos, fecha):
    """
    Convierte una lista de objetos time y un objeto date en objetos datetime.

    Args:
        lista_tiempos (list): Lista con dos objetos time en formato HH:MM:SS.
        fecha (date): Objeto date en formato AAAA-MM-DD.

    Returns:
        list: Lista con dos objetos datetime en formato AAAA-MM-DD HH:MM:SS.
    """
    datetime_list = []
    for t in lista_tiempos:
        dt = datetime.combine(fecha, t)
        datetime_list.append(dt)
    return datetime_list

class Horarios:
    def __init__(self):
        self.cero    = "00:00"
    
    def set_times(self):
        __, __, self.startAM, self.endAM, self.startPM, self.endPM = BBDD.leer_planta_info(glo.base_datos)
        self.no_AM   = self.no_laboral("no_AM")
        self.no_ME   = self.no_laboral("no_ME")
        self.no_PM   = self.no_laboral("no_PM")

    def no_laboral(self, bloque):
        if bloque == "no_AM":
            start_am_td = timedelta(hours=datetime.strptime(self.startAM, "%H:%M").hour,
                                    minutes=datetime.strptime(self.startAM, "%H:%M").minute)
            midnight_td = timedelta(hours=0, minutes=0)
            self.no_AM = str(start_am_td - midnight_td)

        if bloque == "no_ME":
            end_am_td = timedelta(hours=datetime.strptime(self.endAM, "%H:%M").hour,
                                  minutes=datetime.strptime(self.endAM, "%H:%M").minute)
            start_am_td = timedelta(hours=datetime.strptime(self.startAM, "%H:%M").hour,
                                    minutes=datetime.strptime(self.startAM, "%H:%M").minute)
            self.no_ME = str(end_am_td - start_am_td)

        if bloque == "no_PM":
            end_pm_td = timedelta(hours=datetime.strptime(self.endPM, "%H:%M").hour,
                                  minutes=datetime.strptime(self.endPM, "%H:%M").minute)
            midnight_td = timedelta(hours=24, minutes=0)  # Representa el final del día
            self.no_PM = str(midnight_td - end_pm_td)

glo.turnos = Horarios()




































#ejemplo = programa_bloques("2024-10-10", "22:30", duracion = 1000 ,am=(8,12), pm=(14,18))
#for bloque in ejemplo:
#    print(bloque)
#print(momentoEnd(ejemplo))


#for bloque in programa_bloques("2024-10-07","19:58", duracion = 250 ,am=(8,12), pm=(14,18)):
#    print(bloque)

#print(programa_bloques("2024-10-07","19:58", duracion = 250 ,am=(8,12), pm=(14,18))[-1][-1])


#fecha, hora="2024-10-09", "08:00"
#print("string convertido en datatime", parseDT(fecha,hora))