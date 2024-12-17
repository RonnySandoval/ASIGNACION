import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from estilos import *

"""
# Crear la ventana principal
root = ctk.CTk()
root.title("Gráfico Gantt con CustomTkinter")
root.geometry("800x600")

# Crear un Frame para contener el gráfico
frame = ctk.CTkFrame(root)
frame.pack(fill="both", expand=True, padx=20, pady=20)

# Crear los datos del gráfico de Gantt (tareas, inicio y duración)
tasks = ['Tarea 1', 'Tarea 2', 'Tarea 3']
start_times = [0, 5, 10]  # en unidades de tiempo
durations = [3, 4, 5]  # duración de las tareas en unidades de tiempo
colors = ['red', 'blue', 'green']  # Colores de las barras

# Crear la figura de matplotlib
fig, ax = plt.subplots(figsize=(10, 6))

# Dibujar las barras con broken_barh
for i, (start, duration) in enumerate(zip(start_times, durations)):
    ax.broken_barh([(start, duration)], (i - 0.4, 0.8), facecolors=colors[i])

# Etiquetas y configuración del gráfico
ax.set_yticks(range(len(tasks)))
ax.set_yticklabels(tasks)
ax.set_xlabel('Tiempo')
ax.set_title('Gráfico de Gantt')

# Ajustar el gráfico
ax.grid(True)
"""
# Clase para manejar el gráfico y sus interacciones
class ventanaGantt():
    def __init__(self, master, fig, ax):
        self.master = master  # La ventana principal (root)
        self.fig = fig        # La figura de matplotlib
        self.ax = ax          # Los ejes del gráfico

        # Incrustar el gráfico en el Frame de CustomTkinter
        self.canvas = FigureCanvasTkAgg(fig, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Botón para mostrar/ocultar la rejilla (con estilo de CustomTkinter)
        self.grid_button = ctk.CTkButton(self.master, text="Botón1", command=self.toggle_grid)
        self.grid_button.pack(pady=10)

    # Función para alternar la rejilla en el gráfico
    def toggle_grid(self):
        # Cambiar el estado de la rejilla
        self.ax.grid(not self.ax._axisbelow)  # Cambiar el estado de la rejilla
        self.canvas.draw()

