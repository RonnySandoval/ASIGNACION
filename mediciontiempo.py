import time
import matplotlib.pyplot as plt

# Función que realiza cálculos y utiliza print
def programa_con_print(n):
    operacion = 0
    for i in range(n):
        operacion = i + i
        print(f"Línea {i}. Acumulado: {operacion}")

# Función para medir el tiempo de ejecución
def medir_tiempo_print(n):
    start = time.time()
    programa_con_print(n)
    end = time.time()
    return end - start

# Configuración de los intervalos
valores_n = range(800, 900, 10)  # De 1000 a 100000 en intervalos de 1000
tiempos = []

# Medir tiempos de ejecución para cada n
for n in valores_n:
    print(f"Ejecutando con {n} prints...")  # Indicación de progreso
    tiempo = medir_tiempo_print(n)
    tiempos.append(tiempo)

# Graficar los resultados
plt.figure(figsize=(10, 6))
plt.plot(valores_n, tiempos, marker='o', label="Tiempo de ejecución")
plt.title("Impacto de la cantidad de prints en el tiempo de ejecución", fontsize=14)
plt.xlabel("Cantidad de prints", fontsize=12)
plt.ylabel("Tiempo de ejecución (segundos)", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.7)
plt.legend(fontsize=12)
plt.show()

