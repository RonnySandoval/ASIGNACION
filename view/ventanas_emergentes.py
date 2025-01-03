from tkinter import messagebox, filedialog

def desea_exportar(nombreExcel, nombreVentana, df):
    respuesta = messagebox.askokcancel(f"Exportar {nombreVentana}", "¿Deseas exportar a un archivo .xlsx?")
    if respuesta:
        print("Click en Aceptar")

        #seleccionar de carpeta y nombrar archivo
        archivo = filedialog.asksaveasfilename(
            title="Exportar archivo a Excel",
            defaultextension=".xlsx",  # Extensión por defecto del archivo
            filetypes=(("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*")),
            initialfile=nombreExcel  # Nombre de archivo inicial sugerido
        )

        if archivo:
            df.to_excel(archivo, index=False)           # Guardar los datos en un archivo de Excel           
            print(f"Archivo se guardó en: {archivo}")   

    else:
        print("Click en Cancelar")

def msg_eliminar_his(id_historico):
    respuesta = messagebox.askokcancel(
        title="Eliminar Histórico",
        message=f"¡Está a punto de eliminar el registro Histórico {id_historico}!\n"
        "Este cambio afectará la tabla HISTÓRICOS, y es irreversible.\n"
        "¿Seguro desea eliminarlo?"
    )
    if respuesta:
        print("Click en Aceptar")
        return "Aceptar"
    else:
        print("Click en Cancelar")
        return "Cancelar"
    
def msg_eliminar_tec(id_tecnico, nombre):
    respuesta = messagebox.askokcancel(
        title="Eliminar Técnico",
        message=f"¡Está a punto de eliminar el técnico {nombre} con id: {id_tecnico}!\n"
        "Este cambio afectará las tablas TECNICOS y TECNICOS_ESPECIALIDAD, y es irreversible.\n"
        "¿Seguro desea eliminarlo?"
    )
    if respuesta:
        print("Click en Aceptar")
        return "Aceptar"
    else:
        print("Click en Cancelar")
        return "Cancelar"

def msg_eliminar_ped(id):
    respuesta = messagebox.askokcancel(
        title="Eliminar Pedido",
        message=f"¡Está a punto de eliminar el pedido {id}!\n"
        "Este cambio afectará las tablas de PEDIDOS, VEHICULO, TIEMPOS_VEHICULO, PROGRAMAS Y ÓRDENES y es irreversible.\n"
        "¿Seguro desea eliminar todos los registros implicados?"
    )
    if respuesta:
        print("Click en Aceptar")
        return "Aceptar"
    else:
        print("Click en Cancelar")
        return "Cancelar"

def msg_eliminar_prog(id):
    respuesta = messagebox.askokcancel(
        title="Eliminar Programa",
        message=f"¡Está a punto de eliminar el programa {id} y todas las órdenes de este!\n"
        "Este cambio afectará las tablas de PROGRAMAS y de ÓRDENES, y es irreversible.\n"
        "¿Seguro desea eliminarlo?"
    )
    if respuesta:
        print("Click en Aceptar")
        return "Aceptar"
    else:
        print("Click en Cancelar")
        return "Cancelar"

def msg_eliminar_proc(nombre):
    respuesta = messagebox.askokcancel(
        title="Eliminar Proceso",
        message=f"¡Está a punto de eliminar el proceso {nombre}!\n"
        "Este cambio afectará las tablas de PROCESOS, TÉCNICOS_PROCESOS y de TIEMPOS_MODELOS, y es irreversible.\n"
        "(Los registros de vehiculos, históricos y programas no se verán afectados).\n"
        "¿Seguro desea eliminarlo?"
    )
    if respuesta:
        print("Click en Aceptar")
        return "Aceptar"
    else:
        print("Click en Cancelar")
        return "Cancelar"
    
def msg_eliminar_veh(chasis):
    respuesta = messagebox.askokcancel(
        title="Eliminar Vehículo",
        message=f"¡Está a punto de eliminar el Vehículo {chasis}!\n"
        "Este cambio afectará las tablas VEHICULOS y TIEMPOS_VEHICULOS, y es irreversible.\n"
        "¿Seguro desea eliminarlo?"
    )
    if respuesta:
        print("Click en Aceptar")
        return "Aceptar"
    else:
        print("Click en Cancelar")
        return "Cancelar"

def msg_eliminar_mod(modelo, vehiculos):
    chasis = [vehiculo[0] for vehiculo in vehiculos]
    respuesta = messagebox.askokcancel(
        title="Eliminar Modelo",
        message=(
            f"¡Está a punto de eliminar el Modelo {modelo}!\n\n"+
            "Este cambio afectará las tablas MODELOS y TIEMPOS_MODELOS, y es irreversible.\n"+
            "Además eliminará todos los registros pertenecientes a los vehiculos con chasis \n"+
            f"{chasis}. Esto también afectará las tablas VEHICULOS y TIEMPOS_VEHICULOS."+
            "(Los registros de histórico y programas no se verán afectados).\n\n"+
            "¿Está seguro de que desea eliminarlo todo?"
        )
    )
    if respuesta:
        print("Click en Aceptar")
        return "Aceptar"
    else:
        print("Click en Cancelar")
        return "Cancelar"

def msg_eliminar_ref(referencia, modelo):
    respuesta = messagebox.askokcancel(
        title="Eliminar Referencia",
        message=(
            f"¡Está a punto de eliminar la referencia {referencia} del modelo {modelo}!\n\n"+
            "Este cambio es irreversible.\n"+
            "(Los registros de histórico, vehiculos y programas No se verán afectados).\n\n"+
            "¿Está seguro de que desea eliminarla?"
        )
    )
    if respuesta:
        print("Click en Aceptar")
        return "Aceptar"
    else:
        print("Click en Cancelar")
        return "Cancelar"

def msg_registro_nulo(dataframe):

    registros = dataframe.to_dict(orient='records')    # Convertir el DataFrame a una lista de diccionarios
    formateado = "\n\n".join([str(registro) for registro in registros])    # Crear el mensaje formateado

    mensaje = f"""
    No se encontró referencia para los siguientes vehículos:

    {formateado}

    ¿Desea agregar más referencias para los vehículos no encontrados?
    En caso contrario, verifique el archivo fuente y las referencias de modelos en la base de Datos.
    Luego intente cargarlos de nuevo.
    """
    return messagebox.askquestion("Referencia no encontrada", mensaje, )

def msg_registro_duplicado(dataframe):

    registros = dataframe.to_dict(orient='records')    # Convertir el DataFrame a una lista de diccionarios
    formateado = "\n\n".join([str(registro) for registro in registros])    # Crear el mensaje formateado

    mensaje = f"""
    No se encontró referencia para los siguientes vehículos:

    {formateado}

    Por favor, verifique el archivo fuente y las referencias de modelos en la base de Datos. Luego intente cargarlos de nuevo.
    """
    messagebox.showinfo("Modelo no encontrado", mensaje)