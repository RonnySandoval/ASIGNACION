import pandas as pd
import math
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.express.colors import qualitative
from dash import Dash, dcc, html, Input, Output
from database import BDcrud, BDmanage as man
    
with man.Database('planta_con_ensamble1.db') as db:
    crud_historicos = BDcrud.HistoricosCrud(db)
    df_historicos = crud_historicos.leer_historicos_graficar_df()
    
    #crud_historicos = BDcrud.OrdenesCrud(db)
    #df_historicos = crud_historicos.leer_ordenes_graficar_programa('inmediato_NISSAN4_4_3')
    #print(df_historicos.to_string())
    pass

# Datos random
df_random = pd.DataFrame([
    # Chasis001
    dict(Item="Chasis001", Task="Juan",   Filters="Ensamble",    Inicio="2024-08-01 08:00", Fin="2024-08-01 08:30"),
    dict(Item="Chasis001", Task="Kevin",  Filters="Telequinox",  Inicio="2024-08-01 08:30", Fin="2024-08-01 10:00"),
    dict(Item="Chasis001", Task="Johan",  Filters="Lavado",      Inicio="2024-08-01 10:10", Fin="2024-08-01 11:00"),
    dict(Item="Chasis001", Task="David",  Filters="Pintura",     Inicio="2024-08-01 11:30", Fin="2024-08-01 14:30"),
    dict(Item="Chasis001", Task="Carlos", Filters="Codigos",     Inicio="2024-08-01 14:15", Fin="2024-08-01 15:45"),
    dict(Item="Chasis001", Task="Lucas",  Filters="Calidad",     Inicio="2024-08-01 16:00", Fin="2024-08-01 17:15"),

    # Chasis002
    dict(Item="Chasis002", Task="Johan",  Filters="Ensamble",    Inicio="2024-08-01 08:10", Fin="2024-08-01 08:45"),
    dict(Item="Chasis002", Task="Lucas",  Filters="Telequinox",  Inicio="2024-08-01 08:50", Fin="2024-08-01 10:20"),
    dict(Item="Chasis002", Task="Kevin",  Filters="Lavado",      Inicio="2024-08-01 10:30", Fin="2024-08-01 11:15"),
    dict(Item="Chasis002", Task="Carlos", Filters="Pintura",     Inicio="2024-08-01 11:45", Fin="2024-08-01 14:00"),
    dict(Item="Chasis002", Task="David",  Filters="Codigos",     Inicio="2024-08-01 14:00", Fin="2024-08-01 15:30"),
    dict(Item="Chasis002", Task="Juan",   Filters="Calidad",     Inicio="2024-08-01 15:45", Fin="2024-08-01 17:00"),

    # Chasis003
    dict(Item="Chasis003", Task="Lucas",  Filters="Ensamble",    Inicio="2024-08-01 08:20", Fin="2024-08-01 08:50"),
    dict(Item="Chasis003", Task="David",  Filters="Telequinox",  Inicio="2024-08-01 08:55", Fin="2024-08-01 10:25"),
    dict(Item="Chasis003", Task="Carlos", Filters="Lavado",      Inicio="2024-08-01 10:30", Fin="2024-08-01 11:10"),
    dict(Item="Chasis003", Task="Juan",   Filters="Pintura",     Inicio="2024-08-01 11:30", Fin="2024-08-01 14:00"),
    dict(Item="Chasis003", Task="Kevin",  Filters="Codigos",     Inicio="2024-08-01 14:10", Fin="2024-08-01 15:40"),
    dict(Item="Chasis003", Task="Johan",  Filters="Calidad",     Inicio="2024-08-01 15:50", Fin="2024-08-01 17:00"),

    # Chasis004
    dict(Item="Chasis004", Task="Carlos", Filters="Ensamble",    Inicio="2024-08-01 08:00", Fin="2024-08-01 08:35"),
    dict(Item="Chasis004", Task="Johan",  Filters="Telequinox",  Inicio="2024-08-01 08:40", Fin="2024-08-01 10:10"),
    dict(Item="Chasis004", Task="Juan",   Filters="Lavado",      Inicio="2024-08-01 10:20", Fin="2024-08-01 11:05"),
    dict(Item="Chasis004", Task="Kevin",  Filters="Pintura",     Inicio="2024-08-01 11:15", Fin="2024-08-01 14:15"),
    dict(Item="Chasis004", Task="Lucas",  Filters="Codigos",     Inicio="2024-08-01 14:25", Fin="2024-08-01 15:50"),
    dict(Item="Chasis004", Task="David",  Filters="Calidad",     Inicio="2024-08-01 16:00", Fin="2024-08-01 17:10"),

    # Chasis005
    dict(Item="Chasis005", Task="Kevin",  Filters="Ensamble",    Inicio="2024-08-01 08:05", Fin="2024-08-01 08:40"),
    dict(Item="Chasis005", Task="Carlos", Filters="Telequinox",  Inicio="2024-08-01 08:45", Fin="2024-08-01 10:15"),
    dict(Item="Chasis005", Task="Lucas",  Filters="Lavado",      Inicio="2024-08-01 10:20", Fin="2024-08-01 11:10"),
    dict(Item="Chasis005", Task="Johan",  Filters="Pintura",     Inicio="2024-08-01 11:30", Fin="2024-08-01 14:10"),
    dict(Item="Chasis005", Task="David",  Filters="Codigos",     Inicio="2024-08-01 14:15", Fin="2024-08-01 15:40"),
    dict(Item="Chasis005", Task="Juan",   Filters="Calidad",     Inicio="2024-08-01 15:50", Fin="2024-08-01 17:05"),
    
    # Chasis004
    dict(Item="Chasis006", Task="Carlos", Filters="Ensamble",    Inicio="2024-08-01 08:00", Fin="2024-08-01 08:35"),
    dict(Item="Chasis006", Task="Johan",  Filters="Telequinox",  Inicio="2024-08-01 08:40", Fin="2024-08-01 10:10"),
    dict(Item="Chasis006", Task="Juan",   Filters="Lavado",      Inicio="2024-08-01 10:20", Fin="2024-08-01 11:05"),
    dict(Item="Chasis006", Task="Kevin",  Filters="Pintura",     Inicio="2024-08-01 11:15", Fin="2024-08-01 14:15"),
    dict(Item="Chasis006", Task="Lucas",  Filters="Codigos",     Inicio="2024-08-01 14:25", Fin="2024-08-01 15:50"),
    dict(Item="Chasis006", Task="David",  Filters="Calidad",     Inicio="2024-08-01 16:00", Fin="2024-08-01 17:10"),

    # Chasis005
    dict(Item="Chasis007", Task="Kevin",  Filters="Ensamble",    Inicio="2024-08-01 08:05", Fin="2024-08-01 08:40"),
    dict(Item="Chasis007", Task="Carlos", Filters="Telequinox",  Inicio="2024-08-01 08:45", Fin="2024-08-01 10:15"),
    dict(Item="Chasis007", Task="Lucas",  Filters="Lavado",      Inicio="2024-08-01 10:20", Fin="2024-08-01 11:10"),
    dict(Item="Chasis007", Task="Johan",  Filters="Pintura",     Inicio="2024-08-01 11:30", Fin="2024-08-01 14:10"),
    dict(Item="Chasis007", Task="David",  Filters="Codigos",     Inicio="2024-08-01 14:15", Fin="2024-08-01 15:40"),
    dict(Item="Chasis007", Task="Juan",   Filters="Calidad",     Inicio="2024-08-01 15:50", Fin="2024-08-01 17:05"),
    
    # Chasis005
    dict(Item="Chasis008", Task="Kevin",  Filters="Ensamble",    Inicio="2024-08-01 08:05", Fin="2024-08-01 08:40"),
    dict(Item="Chasis008", Task="Carlos", Filters="Telequinox",  Inicio="2024-08-01 08:45", Fin="2024-08-01 10:15"),
    dict(Item="Chasis008", Task="Lucas",  Filters="Lavado",      Inicio="2024-08-01 10:20", Fin="2024-08-01 11:10"),
    dict(Item="Chasis008", Task="Johan",  Filters="Pintura",     Inicio="2024-08-01 11:30", Fin="2024-08-01 14:10"),
    dict(Item="Chasis008", Task="David",  Filters="Codigos",     Inicio="2024-08-01 14:15", Fin="2024-08-01 15:40"),
    dict(Item="Chasis008", Task="Juan",   Filters="Calidad",     Inicio="2024-08-01 15:50", Fin="2024-08-01 17:05"),
    
    # Chasis004
    dict(Item="Chasis010", Task="Carlos", Filters="Ensamble",    Inicio="2024-08-01 08:00", Fin="2024-08-01 08:35"),
    dict(Item="Chasis010", Task="Johan",  Filters="Telequinox",  Inicio="2024-08-01 08:40", Fin="2024-08-01 10:10"),
    dict(Item="Chasis010", Task="Juan",   Filters="Lavado",      Inicio="2024-08-01 10:20", Fin="2024-08-01 11:05"),
    dict(Item="Chasis010", Task="Kevin",  Filters="Pintura",     Inicio="2024-08-01 11:15", Fin="2024-08-01 14:15"),
    dict(Item="Chasis010", Task="Lucas",  Filters="Codigos",     Inicio="2024-08-01 14:25", Fin="2024-08-01 15:50"),
    dict(Item="Chasis010", Task="David",  Filters="Calidad",     Inicio="2024-08-01 16:00", Fin="2024-08-01 17:10"),

    # Chasis005
    dict(Item="Chasis010", Task="Kevin",  Filters="Ensamble",    Inicio="2024-08-01 08:05", Fin="2024-08-01 08:40"),
    dict(Item="Chasis010", Task="Carlos", Filters="Telequinox",  Inicio="2024-08-01 08:45", Fin="2024-08-01 10:15"),
    dict(Item="Chasis010", Task="Lucas",  Filters="Lavado",      Inicio="2024-08-01 10:20", Fin="2024-08-01 11:10"),
    dict(Item="Chasis010", Task="Johan",  Filters="Pintura",     Inicio="2024-08-01 11:30", Fin="2024-08-01 14:10"),
    dict(Item="Chasis010", Task="David",  Filters="Codigos",     Inicio="2024-08-01 14:15", Fin="2024-08-01 15:40"),
    dict(Item="Chasis010", Task="Juan",   Filters="Calidad",     Inicio="2024-08-01 15:50", Fin="2024-08-01 17:05"),
    
    dict(Item="Chasis011", Task="Kevin",  Filters="Ensamble",    Inicio="2024-08-01 08:05", Fin="2024-08-01 08:40"),
    dict(Item="Chasis011", Task="Carlos", Filters="Telequinox",  Inicio="2024-08-01 08:45", Fin="2024-08-01 10:15"),
    dict(Item="Chasis011", Task="Lucas",  Filters="Lavado",      Inicio="2024-08-01 10:20", Fin="2024-08-01 11:10"),
    dict(Item="Chasis011", Task="Johan",  Filters="Pintura",     Inicio="2024-08-01 11:30", Fin="2024-08-01 14:10"),
    dict(Item="Chasis011", Task="David",  Filters="Codigos",     Inicio="2024-08-01 14:15", Fin="2024-08-01 15:40"),
    dict(Item="Chasis011", Task="Juan",   Filters="Calidad",     Inicio="2024-08-01 15:50", Fin="2024-08-01 17:05"),
    
    dict(Item="Chasis012", Task="Kevin",  Filters="Ensamble",    Inicio="2024-08-01 08:05", Fin="2024-08-01 08:40"),
    dict(Item="Chasis012", Task="Carlos", Filters="Telequinox",  Inicio="2024-08-01 08:45", Fin="2024-08-01 10:15"),
    dict(Item="Chasis012", Task="Lucas",  Filters="Lavado",      Inicio="2024-08-01 10:20", Fin="2024-08-01 11:10"),
    dict(Item="Chasis012", Task="Johan",  Filters="Pintura",     Inicio="2024-08-01 11:30", Fin="2024-08-01 14:10"),
    dict(Item="Chasis012", Task="David",  Filters="Codigos",     Inicio="2024-08-01 14:15", Fin="2024-08-01 15:40"),
    dict(Item="Chasis012", Task="Juan",   Filters="Calidad",     Inicio="2024-08-01 15:50", Fin="2024-08-01 17:05"),
    
    dict(Item="Chasis013", Task="Kevin",  Filters="Ensamble",    Inicio="2024-08-01 08:05", Fin="2024-08-01 08:40"),
    dict(Item="Chasis013", Task="Carlos", Filters="Telequinox",  Inicio="2024-08-01 08:45", Fin="2024-08-01 10:15"),
    dict(Item="Chasis013", Task="Lucas",  Filters="Lavado",      Inicio="2024-08-01 10:20", Fin="2024-08-01 11:10"),
    dict(Item="Chasis013", Task="Johan",  Filters="Pintura",     Inicio="2024-08-01 11:30", Fin="2024-08-01 14:10"),
    dict(Item="Chasis013", Task="David",  Filters="Codigos",     Inicio="2024-08-01 14:15", Fin="2024-08-01 15:40"),
    dict(Item="Chasis013", Task="Juan",   Filters="Calidad",     Inicio="2024-08-01 15:50", Fin="2024-08-01 17:05"),
])

def flat_df_gantt(df_data, items, tasks, filter1, filter2):

    df = df_data[["CHASIS", "TECNICO", "PROCESO", "ID_MODELO", "INICIO", "FIN"]].copy()
    df["Item"] = df [items]    
    df["Task"] = df [tasks]    
    df["Filter1"] = df[filter1]
    df["Filter2"] = df[filter2]
    df["Inicio"] = pd.to_datetime(df["INICIO"])
    df["Fin"] = pd.to_datetime(df["FIN"])
    df = df[["Item", "Task", "Filter1", "Filter2", "Inicio", "Fin"]]
    
    return df

def plot_gantt(df, items, tasks, filter1, filter2):
    df_data = flat_df_gantt(df, items, tasks, filter1, filter2)
    
    app = Dash(__name__)    # App Dash
    app.layout = html.Div([
        html.H2("Diagrama de Gantt - HISTÓRICOS"),

        html.Div([
            html.Label(f"Filtrar por {filter1}:"),
            dcc.Dropdown(
                id="dropdown-Filter1",
                options=[{"label": t, "value": t} for t in sorted(df_data["Filter1"].unique())],
                value=[], multi=True, placeholder=f"Selecciona {filter1}"
            ),
        ], style={"width": "20%", "display": "inline-block", "margin-right": "2%"}),
        
        html.Div([
            html.Label(f"Filtrar por {filter2}:"),
            dcc.Dropdown(
                id="dropdown-Filter2",
                options=[{"label": t, "value": t} for t in sorted(df_data["Filter2"].unique())],
                value=[], multi=True, placeholder=f"Selecciona {filter2}"
            ),
        ], style={"width": "20%", "display": "inline-block", "margin-right": "2%"}),

        html.Div([
            html.Label(f"Filtrar por {tasks}:"),
            dcc.Dropdown(
                id="dropdown-Task",
                options=[{"label": o, "value": o} for o in sorted(df_data["Task"].unique())],
                value=[], multi=True, placeholder=f"Selecciona {tasks}"
            ),
        ], style={"width": "20%", "display": "inline-block", "margin-right": "2%"}),

        html.Div([
            html.Label(f"Filtrar por {items}:"),
            dcc.Dropdown(
                id="dropdown-Item",
                options=[{"label": o, "value": o} for o in sorted(df_data["Item"].unique())],
                value=[], multi=True, placeholder=f"Selecciona {items}"
            ),
        ], style={"width": "20%", "display": "inline-block", "margin-right": "2%"}),

        html.Div([
            dcc.Graph(id="gantt-grafico")
        ], style={
            "overflowX": "auto",
            "overflowY": "auto",
            "whiteSpace": "nowrap",
            "border": "2px solid gray",
            "padding": "10px",
            "minHeight": "300px"
        }),
    ])

    @app.callback(Output("gantt-grafico", "figure"),
                  Input("dropdown-Filter1", "value"),
                  Input("dropdown-Filter2", "value"),
                  Input("dropdown-Task", "value"),
                  Input("dropdown-Item", "value"))
    def actualizar_gantt(filtro_Filter1, filtro_Filter2, filtro_Task, filtro_Item):
        datos = df_data.copy()
        datos["Text"] = datos["Filter2"] + "<br>" + datos["Task"]

        if filtro_Filter1:
            datos = datos[datos["Filter1"].isin(filtro_Filter1)]
        if filtro_Filter2:
            datos = datos[datos["Filter2"].isin(filtro_Filter2)]
        if filtro_Task:
            datos = datos[datos["Task"].isin(filtro_Task)]
        if filtro_Item:
            datos = datos[datos["Item"].isin(filtro_Item)]
            
        bars = resize(datos)
        h_plot, num_bar = bars["h_plot"], bars["num_bar"]
        
        # Paleta de colores por categoría
        valores_unicos = datos["Filter1"].unique()
        colores_categoria = {
            valor: qualitative.Plotly[i % len(qualitative.Plotly)]
            for i, valor in enumerate(valores_unicos)
}
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.02,
            row_heights=[0.1, 0.9]
        )

        # ---------- Fila 2: Gantt con barras ----------
        for _, row in datos.iterrows():
            fig.add_trace(go.Bar(
                x=[row["Fin"] - row["Inicio"]],
                y=[row["Item"]],
                base=row["Inicio"],
                orientation="h",
                marker_color=colores_categoria[row["Filter1"]],
                hovertemplate=(
                    f"{items}: {row['Item']}<br>"
                    f"{tasks}: {row['Task']}<br>"
                    f"{filter1}: {row['Filter1']}<br>"
                    f"{filter2}: {row['Filter2']}<br>"
                    f"Inicio: {row['Inicio']}<br>"
                    f"Fin: {row['Fin']}<extra></extra>"
                ),
                text=row["Text"],
                textposition="inside"
            ), row=2, col=1)

        # ---------- Fila 1: Eje X como "línea de tiempo" ----------
        fig.add_trace(go.Scatter(
            x=datos["Inicio"].tolist() + datos["Fin"].tolist(),
            y=[None]*len(datos["Inicio"].tolist() + datos["Fin"].tolist()),
            mode="markers",
            marker=dict(opacity=0),
            showlegend=False
        ), row=1, col=1)

        # ---------- Layout ----------
        fig.update_yaxes(
            autorange="reversed",
            fixedrange=True,
            row=2, col=1
        )

        fig.update_xaxes(
            tickformat="%Y-%m-%d",
            row=1, col=1
        )

        fig.update_layout(
            height=h_plot + 60,
            margin={"l": 40, "r": 20, "t": 40, "b": 40},
            showlegend=False,
            template="plotly_dark",
            plot_bgcolor="black",
            paper_bgcolor="black"
        )

        # ---------- Anotación total ----------
        fig.add_annotation(
            text=f"Total: {bars['num_items']} {items}",
            xref="paper", yref="paper",
            x=0.01, y=1.08,
            showarrow=False,
            font=dict(size=14, color="gray")
        )

        return fig
        
    def resize(df):  
        h_disp = 700
        num_items = len(df["Item"].unique())

        if num_items == 0:
            h_plot = 150  # Altura mínima si no hay datos
        elif num_items == 1:
            h_plot = 150  # Altura más cómoda para un solo ítem
        elif num_items <= 5:
            h_plot = num_items * 90
        elif num_items <= 10:
            h_plot = num_items * 70
        elif num_items <= 15:
            h_plot = num_items * 60
        else:
            h_plot = num_items * 50  # Para muchos ítems, más compacto

        return {
            "h_plot": h_plot,
            "num_bar": h_disp / 50,  # Esto ahora es solo informativo
            "num_items": num_items
    }

    
    app.run(debug=True)


"""plot_gantt(df   =df_historicos,
           items="CHASIS",
           tasks="PROCESO",
           filter1="TECNICO",
           filter2="ID_MODELO")"""
plot_gantt(df   =df_historicos,
           items="TECNICO",
           tasks="ID_MODELO",
           filter1="PROCESO",
           filter2="CHASIS")