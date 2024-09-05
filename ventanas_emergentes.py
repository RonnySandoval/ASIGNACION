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

