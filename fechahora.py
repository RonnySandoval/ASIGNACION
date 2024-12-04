from datetime import datetime, timedelta

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


#inicio, fin = calcular_hora_final("2024-10-7","15:22", 230)
#print(inicio)
#print(fin)

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

"""
 Ejemplo de uso
fecha = "2024-10-06"
dia_semana = obtener_dia_semana(fecha)
print(f"La fecha {fecha} es un {dia_semana}")
"""
def siguiente_dia(fecha):
    return fecha  +1



###############################################################################
###############################################################################
def horas_no_laborables(fecha):

    # Crear tuplas de cadenas con formato 'YYYY-MM-DD HH:MM:SS'
    madrugada = (
        datetime.strptime(f"{fecha} 00:00:00", "%Y-%m-%d %H:%M:%S"),
        datetime.strptime(f"{fecha} 07:59:00", "%Y-%m-%d %H:%M:%S")
        )

    mediodia  = (
        datetime.strptime(f"{fecha} 12:00:00", "%Y-%m-%d %H:%M:%S"),
        datetime.strptime(f"{fecha} 13:59:00", "%Y-%m-%d %H:%M:%S")
        )

    noche     = (
        datetime.strptime(f"{fecha} 18:00:00", "%Y-%m-%d %H:%M:%S"),
        datetime.strptime(f"{fecha} 23:59:00", "%Y-%m-%d %H:%M:%S")
        )

    return {
        "madrugada": madrugada, 
        "mediodia": mediodia, 
        "noche": noche
    }

def horas_laborables(fecha):

    # Crear tuplas de cadenas con formato 'YYYY-MM-DD HH:MM:SS'
    manana = (
        datetime.strptime(f"{fecha} 08:00:00", "%Y-%m-%d %H:%M:%S"),
        datetime.strptime(f"{fecha} 11:59:00", "%Y-%m-%d %H:%M:%S")
        )

    tarde  = (
        datetime.strptime(f"{fecha} 14:00:00", "%Y-%m-%d %H:%M:%S"), 
        datetime.strptime(f"{fecha} 17:59:00", "%Y-%m-%d %H:%M:%S")
        )

    return {
        "manana": manana, 
        "tarde": tarde
    }


#print(horas_laborables("2024-10-07")["manana"])
#print(horas_no_laborables("2024-10-07")["mediodia"])

def define_franja(fecha_hora):
    franjas ={
        0:horas_no_laborables(fecha_hora)["madrugada"][0],
        8:horas_laborables(fecha_hora)["manana"][0],
        12:horas_no_laborables(fecha_hora)["mediodia"][0],
        14:horas_laborables(fecha_hora)["tarde"][0],
        18:horas_no_laborables(fecha_hora)["noche"][0]
        }
    
    return franjas


#print(define_franja("2024-10-07")[8])



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
        if momento.time() >= define_franja(dia)[am[1]].time() and momento.time() <  define_franja(fecha_inicio)[14].time():
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




#ejemplo = programa_bloques("2024-10-10", "22:30", duracion = 1000 ,am=(8,12), pm=(14,18))
#for bloque in ejemplo:
#    print(bloque)
#print(momentoEnd(ejemplo))

































"""
def programa_bloques(fecha_inicio, hora_inicio, duracion, am, pm):
    bloques = []
    inicio = datetime.strptime(f"{fecha_inicio} {hora_inicio}", "%Y-%m-%d %H:%M")     # Convertir la fecha y hora de inicio a un objeto datetime


    #CASO ANTES DE LAS 8AM
    if inicio.time() <=  define_franja(fecha_inicio)[am[0]].time():             #Evalua si está antes de las 8 am
        inicio = define_franja(fecha_inicio)[am[0]]
        fin = calcular_hora_finalDT(inicio, duracion)

        if fin.time() <= define_franja(fecha_inicio)[am[1]].time():
            bloques.append((inicio, fin))
            return bloques
        
        inicio1 = define_franja(fecha_inicio)[am[0]]
        fin1 = define_franja(fecha_inicio)[am[1]]

        inicio2 = define_franja(fecha_inicio)[pm[0]]
        fin2 = calcular_hora_finalDT(inicio2, duracion-240)
        bloques.append((inicio1,fin1))
        bloques.append((inicio2,fin2))
        return bloques


    #CASO ENTRE 8AM Y 12M
    elif inicio.time() > define_franja(fecha_inicio)[am[0]].time() and inicio.time() <=  define_franja(fecha_inicio)[am[1]].time():
        fin = calcular_hora_finalDT(inicio, duracion)

        if fin.time() <= define_franja(fecha_inicio)[am[1]].time():
            bloques.append((inicio, fin))
            return bloques

        inicio1 = inicio
        fin1 = define_franja(fecha_inicio)[am[1]]
        diferencia=fin1-inicio1
        min_asignados=(int(diferencia.seconds))/60
        inicio2 = define_franja(fecha_inicio)[pm[0]]
        fin2 = calcular_hora_finalDT(inicio2, duracion-min_asignados)
        bloques.append((inicio1,fin1))
        bloques.append((inicio2,fin2))
        return bloques

    #CASO ENTRE LAS 12M Y 2PM
    elif inicio.time() > define_franja(fecha_inicio)[am[1]].time() and inicio.time() <=  define_franja(fecha_inicio)[14].time():
        inicio = define_franja(fecha_inicio)[pm[0]]
        fin = calcular_hora_finalDT(inicio, duracion)

        if fin.time() <= define_franja(fecha_inicio)[pm[1]].time():
            bloques.append((inicio, fin))
            return bloques
        
        inicio1 = define_franja(fecha_inicio)[pm[0]]
        fin1 = define_franja(fecha_inicio)[pm[1]]
        diferencia=fin1-inicio1
        print(diferencia)
        min_asignados=(int(diferencia.seconds))/60
        next_dia =  inicio + timedelta(days=1)
        inicio2 = next_dia.replace(hour=am[0],minute=0,second=0)
        fin2 = calcular_hora_finalDT(inicio2, duracion-240)
        bloques.append((inicio1,fin1))
        bloques.append((inicio2,fin2))
        return bloques
    
    #CASO ENTRE LAS 2PM Y 6PM
    elif inicio.time() > define_franja(fecha_inicio)[pm[0]].time() and inicio.time() <=  define_franja(fecha_inicio)[pm[1]].time():
        fin = calcular_hora_finalDT(inicio, duracion)

        if fin.time() <= define_franja(fecha_inicio)[pm[1]].time():
            bloques.append((inicio, fin))
            return bloques
        
        inicio1 = inicio
        fin1 = define_franja(fecha_inicio)[pm[1]]
        diferencia=fin1-inicio1
        min_asignados=(int(diferencia.seconds))/60

        next_dia =  inicio + timedelta(days=1)
        inicio2 = next_dia.replace(hour = am[0], minute=0,second=0)
        fin2 = calcular_hora_finalDT(inicio2, duracion-min_asignados)
        bloques.append((inicio1,fin1))
        bloques.append((inicio2,fin2))
        return bloques



    #CASO ENTRE LAS 6PM Y 12PM
    elif inicio.time() > define_franja(fecha_inicio)[pm[1]].time():
        inicio = datetime.strptime(f"{fecha_inicio} {hora_inicio}", "%Y-%m-%d %H:%M")     # Convertir la fecha y hora de inicio a un objeto datetime
        next_dia = inicio + timedelta(days=1)
       
        inicio = define_franja(str(next_dia.date()))[am[0]]
        fin = calcular_hora_finalDT(inicio, duracion)

        if fin.time() <= define_franja(fecha_inicio)[am[1]].time():
            bloques.append((inicio, fin))
            return bloques
        
        inicio1 = define_franja(fecha_inicio)[am[0]] + timedelta(days=1)
        fin1 = define_franja(fecha_inicio)[am[1]] + timedelta(days=1)
        diferencia=fin1-inicio1
        min_asignados=(int(diferencia.seconds))/60

        inicio2 = define_franja(fecha_inicio)[pm[0]]+timedelta(days=1)
        fin2 = calcular_hora_finalDT(inicio2, duracion-min_asignados)
        bloques.append((inicio1,fin1))
        bloques.append((inicio2,fin2))
        return bloques
"""


#for bloque in programa_bloques("2024-10-07","19:58", duracion = 250 ,am=(8,12), pm=(14,18)):
#    print(bloque)

#print(programa_bloques("2024-10-07","19:58", duracion = 250 ,am=(8,12), pm=(14,18))[-1][-1])


#fecha, hora="2024-10-09", "08:00"
#print("string convertido en datatime", parseDT(fecha,hora))