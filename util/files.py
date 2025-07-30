import os

# Ruta de la carpeta raíz (puedes cambiarla por la que necesites)
carpeta_raiz = "C:\\NUEVO_PORTATIL\\GITHUB\\ASIGNACION"

# Archivo de salida
archivo_salida = "nombres_archivos.txt"

# Lista para guardar los nombres compuestos
nombres_completos = []

# Recorrer todas las carpetas y subcarpetas
for carpeta_actual, subcarpetas, archivos in os.walk(carpeta_raiz):
    for archivo in archivos:
        if archivo.endswith(".py"):
            nombre_archivo = os.path.splitext(archivo)[0]
            nombre_carpeta = os.path.basename(carpeta_actual)
            nombre_completo = f"{nombre_carpeta}.{nombre_archivo}"
            nombres_completos.append(nombre_completo)

# Guardar los nombres en un archivo .txt
with open(archivo_salida, "w", encoding="utf-8") as f:
    for nombre in nombres_completos:
        f.write(nombre + "\n")

print(f"Se han guardado {len(nombres_completos)} nombres en '{archivo_salida}'.")