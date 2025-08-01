import plotly.express as px
import plotly.io as pio
import pandas as pd
from dash import Dash, dcc, html, Input, Output

pio.renderers.default = "browser"


# Datos
df = pd.DataFrame([
    # Chasis001
    dict(Item="Chasis001", Task="Juan",   Process="Ensamble",    Start="2024-08-01 08:00", End="2024-08-01 08:30"),
    dict(Item="Chasis001", Task="Kevin",  Process="Telequinox",  Start="2024-08-01 08:30", End="2024-08-01 10:00"),
    dict(Item="Chasis001", Task="Johan",  Process="Lavado",      Start="2024-08-01 10:10", End="2024-08-01 11:00"),
    dict(Item="Chasis001", Task="David",  Process="Pintura",     Start="2024-08-01 11:30", End="2024-08-01 14:30"),
    dict(Item="Chasis001", Task="Carlos", Process="Codigos",     Start="2024-08-01 14:15", End="2024-08-01 15:45"),
    dict(Item="Chasis001", Task="Lucas",  Process="Calidad",     Start="2024-08-01 16:00", End="2024-08-01 17:15"),

    # Chasis002
    dict(Item="Chasis002", Task="Johan",  Process="Ensamble",    Start="2024-08-01 10:10", End="2024-08-01 10:45"),
    dict(Item="Chasis002", Task="Lucas",  Process="Telequinox",  Start="2024-08-01 10:50", End="2024-08-01 11:20"),
    dict(Item="Chasis002", Task="Kevin",  Process="Lavado",      Start="2024-08-01 11:30", End="2024-08-01 12:15"),
    dict(Item="Chasis002", Task="Carlos", Process="Pintura",     Start="2024-08-01 12:45", End="2024-08-01 14:00"),
    dict(Item="Chasis002", Task="David",  Process="Codigos",     Start="2024-08-01 14:00", End="2024-08-01 16:30"),
    dict(Item="Chasis002", Task="Juan",   Process="Calidad",     Start="2024-08-01 16:45", End="2024-08-01 17:00"),

    # Chasis003
    dict(Item="Chasis003", Task="Lucas",  Process="Ensamble",    Start="2024-08-01 10:20", End="2024-08-01 10:50"),
    dict(Item="Chasis003", Task="David",  Process="Telequinox",  Start="2024-08-01 10:55", End="2024-08-01 11:25"),
    dict(Item="Chasis003", Task="Carlos", Process="Lavado",      Start="2024-08-01 11:30", End="2024-08-01 12:10"),
    dict(Item="Chasis003", Task="Juan",   Process="Pintura",     Start="2024-08-01 12:30", End="2024-08-01 14:00"),
    dict(Item="Chasis003", Task="Kevin",  Process="Codigos",     Start="2024-08-01 13:10", End="2024-08-01 15:40"),
    dict(Item="Chasis003", Task="Johan",  Process="Calidad",     Start="2024-08-01 16:50", End="2024-08-01 17:00"),

    # Chasis004
    dict(Item="Chasis004", Task="Carlos", Process="Ensamble",    Start="2024-08-01 09:00", End="2024-08-01 09:35"),
    dict(Item="Chasis004", Task="Johan",  Process="Telequinox",  Start="2024-08-01 10:40", End="2024-08-01 11:10"),
    dict(Item="Chasis004", Task="Juan",   Process="Lavado",      Start="2024-08-01 11:20", End="2024-08-01 12:05"),
    dict(Item="Chasis004", Task="Kevin",  Process="Pintura",     Start="2024-08-01 12:15", End="2024-08-01 13:15"),
    dict(Item="Chasis004", Task="Lucas",  Process="Codigos",     Start="2024-08-01 15:25", End="2024-08-01 15:50"),
    dict(Item="Chasis004", Task="David",  Process="Calidad",     Start="2024-08-01 16:00", End="2024-08-01 17:10"),

    # Chasis005
    dict(Item="Chasis005", Task="Kevin",  Process="Ensamble",    Start="2024-08-01 08:05", End="2024-08-01 08:40"),
    dict(Item="Chasis005", Task="Carlos", Process="Telequinox",  Start="2024-08-01 08:45", End="2024-08-01 10:15"),
    dict(Item="Chasis005", Task="Lucas",  Process="Lavado",      Start="2024-08-01 10:20", End="2024-08-01 11:10"),
    dict(Item="Chasis005", Task="Johan",  Process="Pintura",     Start="2024-08-01 11:30", End="2024-08-01 14:10"),
    dict(Item="Chasis005", Task="David",  Process="Codigos",     Start="2024-08-01 14:15", End="2024-08-01 15:40"),
    dict(Item="Chasis005", Task="Juan",   Process="Calidad",     Start="2024-08-01 15:50", End="2024-08-01 17:05")
])

# Asegurarse de convertir columnas de tiempo
df['Start'] = pd.to_datetime(df['Start'])
df['End'] = pd.to_datetime(df['End'])

fig = px.timeline(
    df, 
    x_start="Start", 
    x_end="End", 
    y="Item", 
    color="Process",  # Puedes cambiar a 'Task' si prefieres filtrar por eso
    hover_data=["Task", "Process"]
)


fig.update_yaxes(autorange="reversed")  # Para que se ordenen de arriba hacia abajo
fig.update_layout(
    title="Diagrama de Gantt por Chasis",
    height=400,
    legend_title="Process",
    template="plotly_dark",
    plot_bgcolor="black",
    paper_bgcolor="black"
)
# Borde blanco en las barras
fig.update_traces(marker_line_color='white', marker_line_width=1.5)
fig.update_layout(bargap=0.5)  # Reduce grosor, parece más suave
fig.show()