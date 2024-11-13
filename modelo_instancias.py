import CRUD
import BBDD
import modelo_clases
import glo

procesos = {}
for ids, nombres in zip(BBDD.obtener_id_procesos_secuencia(glo.base_datos), BBDD.leer_procesos_secuencia(glo.base_datos)):
    procesos[nombres] = ids

objeModelos = {}        # INSTANCIAS DE MODELOS
for registro in BBDD.leer_modelos_marcas(glo.base_datos):
    objeModelos[registro[1]]=modelo_clases.VehiculoBase(marca=registro[0], modelo=registro[1])

objeVehiculos = []      # INSTANCIAS DE VEHICULOS
for vehiculo in BBDD.leer_vehiculos_completos_marcamodelo(glo.base_datos):
    objeVehiculos.append(modelo_clases.Vehiculo(
                            id_chasis = vehiculo[0], fecha  = vehiculo[1],
                            marca  = vehiculo[2], modelo = vehiculo[3],
                            color  = vehiculo[4], estado = vehiculo[5],
                            novedades = vehiculo[7], pedido = vehiculo[9]))

objeTecnicos = []      # INSTANCIAS DE TECNICOS
for tecnico in BBDD.leer_tecnicos(glo.base_datos):
    objeTecnicos.append(modelo_clases.Tecnico(
                                        id_tecnico=tecnico[0],
                                        nombre=tecnico[1]+" "+tecnico[2],
                                        especializacion=procesos[tecnico[4]])
                                        )

objePedidos = []      # INSTANCIAS DE PEDIDOS
for pedido in BBDD.leer_pedidos(glo.base_datos):
    objePedidos.append(modelo_clases.Pedido(
                        id_pedido=pedido[0],  fecha_recepcion=pedido[2], plazo_entrega = pedido[2], estado ="PENDIENTE",
                        vehiculos = [vehiculo for vehiculo in objeVehiculos if vehiculo.pedido == pedido[0]]))


modelo_clases.programa_por_proceso(objePedidos[0], modelo_clases.personal, ["PDI", "LAV"], 10000, "2024-11-05", "08:45:00", 'planta_manta.db')
pedido = objePedidos[0]
horizonte_calculado = modelo_clases.calcular_horizonte(objePedidos[0])

"""
print(f"el horizonte es {horizonte_calculado}")
for vehiculo in objePedidos[0].vehiculos:
    print(vehiculo.id_chasis)
    for estado in vehiculo.historico_estados:
        print(estado)
"""



