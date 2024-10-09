import Mod_clases
import CRUD

# Instancias de todos lo modelos actuales de la planta

ALTIMA = Mod_clases.VehiculoBase('ALTIMA', 'NISSAN')
FRONTIER = Mod_clases.VehiculoBase('FRONTIER', 'NISSAN')
KICKS = Mod_clases.VehiculoBase('KICKS', 'NISSAN')
QASHQAI = Mod_clases.VehiculoBase('QASHQAI', 'NISSAN')
LEAFT = Mod_clases.VehiculoBase('LEAFT', 'NISSAN')
VERSA = Mod_clases.VehiculoBase('VERSA', 'NISSAN')
PATHFINDER = Mod_clases.VehiculoBase('PATHFINDER', 'NISSAN')
XTRAIL = Mod_clases.VehiculoBase('XTRAIL', 'NISSAN')
CAPTUR = Mod_clases.VehiculoBase('CAPTUR', 'RENAULT')
KOLEOS = Mod_clases.VehiculoBase('KOLEOS', 'RENAULT')
KWID = Mod_clases.VehiculoBase('KWID' ,'RENAULT')
BJ20 = Mod_clases.VehiculoBase('BJ20', 'BAIC')
BJ40 = Mod_clases.VehiculoBase('BJ40', 'BAIC')
D50 = Mod_clases.VehiculoBase('D50', 'BAIC')
NX55 = Mod_clases.VehiculoBase('NX55', 'BAIC')
X35 = Mod_clases.VehiculoBase('X35', 'BAIC')
X55 = Mod_clases.VehiculoBase('X55', 'BAICBAIC')
U5P = Mod_clases.VehiculoBase('U5P', 'BAIC')
AUMARK = Mod_clases.VehiculoBase('AUMARK', 'FOTON')
AUMAN = Mod_clases.VehiculoBase('AUMAN', 'FOTON')
TUNLAND = Mod_clases.VehiculoBase('TUNLAND', 'FOTON')
VIEW = Mod_clases.VehiculoBase('VIEW', 'FOTON')
TOANO = Mod_clases.VehiculoBase('TOANO', 'FOTON')
AZKARRA = Mod_clases.VehiculoBase('AZKARRA', 'GEELY')
COOLRAY = Mod_clases.VehiculoBase('COOLRAY', 'GEELY')
RX8 = Mod_clases.VehiculoBase('RX8','MG')
RX5 = Mod_clases.VehiculoBase('RX5','MG')
MG5 = Mod_clases.VehiculoBase('MG5','MG')
ZS = Mod_clases.VehiculoBase('ZS','MG')
ONE = Mod_clases.VehiculoBase('ONE','MG')


#Ejemplos de técnicos
lista_tecnicos = CRUD.leer_tecnicos()
lista_objetos_tecnicos = []
for tecnico in lista_tecnicos:
    lista_objetos_tecnicos.append(Mod_clases.Tecnico(tecnico[0],tecnico[1],tecnico[2]))

"""  
jair_telequinox     = Mod_programador.Tecnico('Ttel01','JAIR', 'telequinox')
osman_telequinox    = Mod_programador.Tecnico('Ttel02','OSMAN', 'telequinox')
brayan_telequinox   = Mod_programador.Tecnico('Ttel03','BRAYAN', 'telequinox')
cristian_PDI        = Mod_programador.Tecnico('Tpdi01','CRISTIAN', 'PDI')
david_PDI           = Mod_programador.Tecnico('Tpdi02','DAVID', 'PDI')
luis_lavado         = Mod_programador.Tecnico('Tlav01','LUIS', 'lavado')
kevin_lavado        = Mod_programador.Tecnico('Tlav02','KEVIN', 'lavado')
jesus_pintura       = Mod_programador.Tecnico('Tpin01','JESUS', 'pintura')
daniel_pintura      = Mod_programador.Tecnico('Tpin02','DANIEL', 'pintura')
victor_calidad      = Mod_programador.Tecnico('Tcal01','VICTOR', 'calidad')
"""


#ejemplos de objetos vehículos únicos.
lista_vehiculos = CRUD.leer_vehiculos()
print(lista_vehiculos[0])

lista_objetos_vehiculos = []
for vehiculo in lista_vehiculos:
    lista_objetos_vehiculos.append(Mod_clases.Vehiculo(id_chasis = vehiculo[0],
                             fecha  = vehiculo[1],
                             marca  = vehiculo[2],
                             modelo = vehiculo[3],
                             color  = vehiculo[4],
                             estado = vehiculo[5],                             
                             pedido = 'quito06',
                             novedades = vehiculo[11]))
    
"""
VHAUK0001=Mod_programador.Vehiculo(id_chasis = 'AUK0001',modelo='AUMARK',pedido='quito06')
VHQAS0002=Mod_programador.Vehiculo(id_chasis = 'QAS0002',modelo='QASHQAI',pedido='quito06')
VHQAS0003=Mod_programador.Vehiculo(id_chasis = 'QAS0003',modelo='QASHQAI',pedido='quito06')
VHXTR0004=Mod_programador.Vehiculo(id_chasis = 'XTR0004',modelo='XTRAIL',pedido='quito06')
VHXTR0005=Mod_programador.Vehiculo(id_chasis = 'XTR0005',modelo='XTRAIL',pedido='quito06')
VHXTR0006=Mod_programador.Vehiculo(id_chasis = 'XTR0006',modelo='XTRAIL',pedido='quito06')
VHXTR0007=Mod_programador.Vehiculo(id_chasis = 'XTR0007',modelo='XTRAIL',pedido='quito06')
VHXTR0008=Mod_programador.Vehiculo(id_chasis = 'XTR0008',modelo='XTRAIL',pedido='quito06')
VHKOL0009=Mod_programador.Vehiculo(id_chasis = 'KOL0009',modelo='KOLEOS',pedido='quito06')
VHBJ40010=Mod_programador.Vehiculo(id_chasis = 'BJ40010',modelo='BJ40',pedido='quito06')
VHX350011=Mod_programador.Vehiculo(id_chasis = 'X350011',modelo='X35',pedido='quito06')
VHX350012=Mod_programador.Vehiculo(id_chasis = 'X350012',modelo='X35',pedido='quito06')
VHVER0013=Mod_programador.Vehiculo(id_chasis = 'VER0013',modelo='VERSA',pedido='quito06')
VHKWI0014=Mod_programador.Vehiculo(id_chasis = 'KIW0014',modelo='KWID',pedido='quito06')
VHTUN0015=Mod_programador.Vehiculo(id_chasis = 'TUN0015',modelo='TUNLAND',pedido='quito06')
VHCAP0016=Mod_programador.Vehiculo(id_chasis = 'CAP0016',modelo='CAPTUR',pedido='quito06')
VHVER0017=Mod_programador.Vehiculo(id_chasis = 'VER0017',modelo='VERSA',pedido='quito06')
VHTOA0018=Mod_programador.Vehiculo(id_chasis = 'TOA0018',modelo='TOANO',pedido='quito06')
VHTOA0019=Mod_programador.Vehiculo(id_chasis = 'TOA0019',modelo='TOANO',pedido='quito06')
VHVIE0020=Mod_programador.Vehiculo(id_chasis = 'VIE0020',modelo='VIEW',pedido='quito06')
VHKIC0021=Mod_programador.Vehiculo(id_chasis = 'KIC0021',modelo='KICKS',pedido='quito06')
VHKIC0022=Mod_programador.Vehiculo(id_chasis = 'KIC0022',modelo='KICKS',pedido='quito06')
VHCOL0023=Mod_programador.Vehiculo(id_chasis = 'COL0023',modelo='COOLRAY',pedido='quito06')
VHAZK0024=Mod_programador.Vehiculo(id_chasis = 'AZK0024',modelo='AZKARRA',pedido='quito06')
VHX550025=Mod_programador.Vehiculo(id_chasis = 'X550025',modelo='X55',pedido='quito06')
VHX550026=Mod_programador.Vehiculo(id_chasis = 'X550026',modelo='X55',pedido='quito06')
VHX550027=Mod_programador.Vehiculo(id_chasis = 'X550027',modelo='X55',pedido='quito06')
VHX550028=Mod_programador.Vehiculo(id_chasis = 'X550028',modelo='X55',pedido='quito06')
"""
#EJEMPLO DE PEDIDO
pedido_quito06 = Mod_clases.Pedido(
                        id_pedido='p_qui06',
                        plazo_entrega = 5000,
                        vehiculos =lista_objetos_vehiculos,
                        estado ="PENDIENTE"
                        )




#Mod_programador.programa_completo(pedido_quito06, Mod_programador.personal, 4000)
#horizonte_calculado = Mod_programador.calcular_horizonte(pedido_quito06)

#print(f"el horizonte es {Mod_programador.calcular_horizonte(pedido_quito06)}")