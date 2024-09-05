import pandas as pd
import tkinter as tk
from tkinter import messagebox
import CRUD

def desea_guardar(excel):
    respuesta = messagebox.askokcancel("Confirmación", "¿Deseas exportar un archivo .xls?")
    if respuesta:
        print("Click en Aceptar")

        df = CRUD.leer_ordenes_todas()            #leer tabla en BBDD
        df.to_excel(excel, index=False)            # Guardar los datos en un archivo de Excel           
    
    else:
        print("Click en Cancelar")

