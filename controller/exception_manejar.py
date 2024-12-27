import logging
import traceback
from tkinter import messagebox

logging.basicConfig(
    filename="errores.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def capturar_excepcion(e, contexto=""):
    mensaje = f"Error inesperdo en {contexto}: {e}\n{traceback.format_exc()}"
    logging.error(mensaje)
    messagebox.showerror("____ERROR INESPERADO____", f"Error en {contexto}: {str(e)}")
    print(mensaje)

def manejar_errores(contexto):
    def decorador(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                capturar_excepcion(e, contexto)
        return wrapper
    return decorador

