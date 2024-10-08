from datetime import datetime, timedelta

###############################################################################
###############################################################################


def parseDT(string):
    return datetime.strptime(string, "%Y-%m-%d %H:%M")


def calcular_hora_final(fecha_inicio, hora_inicio, duracion):

    fecha_hora_inicio = f"{fecha_inicio} {hora_inicio}"                 # Concatenar fecha y hora para crear una cadena completa de fecha y hora
    inicio = datetime.strptime(fecha_hora_inicio, "%Y-%m-%d %H:%M")     # Convertir la fecha y hora de inicio a un objeto datetime
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
        "Wednesday": "Miércoles",
        "Thursday" : "Jueves",
        "Friday"   : "Viernes",
        "Saturday" : "Sábado",
        "Sunday"   : "Domingo"
    }

    fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")    # Convertir la cadena de fecha en un objeto datetime
    dia_semana_ingles = fecha_obj.strftime("%A")        # Obtener el nombre del día de la semana en inglés
    return dias_semana[dia_semana_ingles]               # Retornar la traducción al español


# Ejemplo de uso
#fecha = "2024-10-06"
#dia_semana = obtener_dia_semana(fecha)
#print(f"La fecha {fecha} es un {dia_semana}")

def siguiente_dia(fecha):
    return fecha  +1
    pass


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

def programa_bloques(fecha_inicio, hora_inicio, duracion, am, pm):
    bloques = []
    inicio = datetime.strptime(f"{fecha_inicio} {hora_inicio}", "%Y-%m-%d %H:%M")     # Convertir la fecha y hora de inicio a un objeto datetime


    #CASO ANTES DE LAS 8AM
    if inicio.time() <=  define_franja(fecha_inicio)[am[0]].time():
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



#for bloque in programa_bloques("2024-10-07","19:58", duracion = 250 ,am=(8,12), pm=(14,18)):
    #print(bloque)




#x="2024-10-09 08:00"
#print("string convertido en datatime", parseDT(x))