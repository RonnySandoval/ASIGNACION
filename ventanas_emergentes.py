import pandas as pd
import tkinter as tk
from tkinter import messagebox, filedialog
import CRUD


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

def msg_eliminar_mod(modelo):
    respuesta = messagebox.askokcancel(
        title="Eliminar Modelo",
        message=(
            f"¡Está a punto de eliminar el Modelo {modelo}!\n\n"
            "Este cambio afectará las tablas MODELOS y TIEMPOS_MODELOS, y es irreversible.\n"
            "¿Está seguro de que desea eliminarlo?"
        )
    )
    if respuesta:
        print("Click en Aceptar")
        return True
    else:
        print("Click en Cancelar")
        return False