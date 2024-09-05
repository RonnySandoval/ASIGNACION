import tkinter
import eventos


def registrarPedidosdeBBDD(tabla):
    tabla.datos = eventos.leepedidoBBDD()

    if tabla.datos is not None:
        # Modificamos la lista con datos para que agrupe los tiempos
        for i in range(len(tabla.datos)):
            registro = tabla.datos[i]                                                            # Convertir los elementos en las posiciones 6 a 10 a una tupla
            tupla_tiempos = tuple(registro[6:11])                                               # Crear una lista modificable con los elementos excepto los que van a ser reemplazados           
            registro_modificado = list(registro[:6])+ [tupla_tiempos] + list(registro[11:])     # Convertir la tupla a una cadena separada por comas
            registro_modificado[6] = ', '.join(map(str, tupla_tiempos))                         # Actualizar la lista original con el registro modificado
            tabla.datos[i] = registro_modificado                                                 # Asignar el registro modificado al atributo datos
            print(tabla.datos[i])

        for record in tabla.datos:
            tabla.tablaPedidos.insert(parent='', index='end', iid=record[0], text='', values=record)





"""self.datos = eventos.leepedidoBBDD()


"""