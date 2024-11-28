import pandas as pd
import tkinter as tk
from tkinter import messagebox, filedialog
import CRUD
import numpy as np

def desea_guardar(excel):
    respuesta = messagebox.askokcancel("Exportar Programación", "¿Deseas exportar un archivo .xlsx?")
    if respuesta:
        print("Click en Aceptar")

        #seleccionar de carpeta y nombrar archivo
        archivo = filedialog.asksaveasfilename(
            title="Exportar archivo a Excel",
            defaultextension=".xlsx",  # Extensión por defecto del archivo
            filetypes=(("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*")),
            initialfile=excel  # Nombre de archivo inicial sugerido
        )

        if archivo:
            df = CRUD.leer_ordenes_todas()            #leer tabla en BBDD
            df.to_excel(archivo, index=False)         # Guardar los datos en un archivo de Excel           
            print(f"Archivo se guardó en: {archivo}")   

    else:
        print("Click en Cancelar")

def ms_eliminar_tec(id_tecnico, nombre):
    respuesta = messagebox.askokcancel(
        title="Eliminar Eliminar",
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
            f"¡Está a punto de eliminar el Modelo {modelo}!\n\n"
            "Este cambio afectará las tablas MODELOS y TIEMPOS_MODELOS, y es irreversible.\n"
            "Además eliminará todos los registros pertenecientes a los vehiculos con chasis \n"
            f"{chasis}. Esto también afectará las tablas VEHICULOS y TIEMPOS_VEHICULOS."
            "¿Está seguro de que desea eliminarlo todo?"
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

    Por favor, verifique el archivo fuente y las referencias de modelos en la base de Datos. Luego intente cargarlos de nuevo.
    """
    messagebox.showinfo("Modelo no encontrado", mensaje)

def msg_registro_duplicado(dataframe):

    registros = dataframe.to_dict(orient='records')    # Convertir el DataFrame a una lista de diccionarios
    formateado = "\n\n".join([str(registro) for registro in registros])    # Crear el mensaje formateado

    mensaje = f"""
    No se encontró referencia para los siguientes vehículos:

    {formateado}

    Por favor, verifique el archivo fuente y las referencias de modelos en la base de Datos. Luego intente cargarlos de nuevo.
    """
    messagebox.showinfo("Modelo no encontrado", mensaje)