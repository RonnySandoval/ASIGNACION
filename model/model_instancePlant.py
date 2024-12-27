import database.BBDD as BBDD
import model.model_classPlant as model_classPlant
import controller.glo as glo


def obtiene_datos_iniciales():
    model_classPlant.personal = []
    pedido = None
    procesos = {}         # INSTANCIAS DE PROCESOS
    objeModelos = {}      # INSTANCIAS DE MODELOS
    objeVehiculos = {}    # INSTANCIAS DE VEHICULOS
    objeTecnicos = {}     # INSTANCIAS DE TECNICOS
    objePedidos = {}      # INSTANCIAS DE PEDIDOS
    tiempos = {}

    print(pedido, procesos, objeModelos, objeVehiculos, objeTecnicos, objePedidos)
    for ids, nombres in zip(BBDD.obtener_id_procesos_secuencia(glo.base_datos), BBDD.leer_procesos_secuencia(glo.base_datos)):
        procesos[nombres] = ids

    for registro in BBDD.leer_modelos_marcas(glo.base_datos):
        objeModelos[registro[1]] = model_classPlant.VehiculoBase(marca=registro[0], modelo=registro[1])

    for vehiculo in BBDD.leer_vehiculos_completos_marcamodelo(glo.base_datos):
        objeVehiculos[vehiculo[0]] = model_classPlant.Vehiculo(
                                id_chasis = vehiculo[0], fecha  = vehiculo[1],
                                marca  = vehiculo[2],    modelo = vehiculo[3],
                                color  = vehiculo[4],    estado = vehiculo[5],
                                novedades = vehiculo[7], pedido = vehiculo[9])

    for tecnico in BBDD.leer_tecnicos(glo.base_datos):
        objeTecnicos[tecnico[0]] = model_classPlant.Tecnico(
                                            id_tecnico=tecnico[0],
                                            nombre=tecnico[1]+" "+tecnico[2],
                                            especializacion=procesos[tecnico[4]])

    for pedido in BBDD.leer_pedidos(glo.base_datos):
        objePedidos[pedido[0]] = model_classPlant.Pedido(
                            id_pedido=pedido[0],  fecha_recepcion=pedido[2], plazo_entrega = pedido[2], estado ="PENDIENTE",
                            vehiculos = [vehiculo for chasis, vehiculo in objeVehiculos.items() if vehiculo.pedido == pedido[0]])

    tiempos["tiempos_mod"]   = BBDD.leer_tiempos_modelos_df(glo.base_datos)
    tiempos["tiempos_veh"] = BBDD.leer_tiempos_vehiculos_df(glo.base_datos)    

    return procesos, objeModelos, objeVehiculos, objeTecnicos, objePedidos, tiempos







    #modelo_clases.programa_por_proceso(objePedidos[0], modelo_clases.personal, ["PDI", "LAV"], 10000, "2024-11-05", "08:45:00", 'planta_manta.db')
    #if objePedidos != []:
    #    pedido = objePedidos[0]
    #horizonte_calculado = modelo_clases.calcular_horizonte(objePedidos[0])

"""
print(f"el horizonte es {horizonte_calculado}")
for vehiculo in objePedidos[0].vehiculos:
    print(vehiculo.id_chasis)
    for estado in vehiculo.historico_estados:
        print(estado)
"""



