import matplotlib.pyplot as plt
import networkx as nx

# Crear un gráfico vacío
G = nx.DiGraph()

# Definir los nodos y las relaciones entre ellos (aristas)
# Este ejemplo se basa en un árbol de decisiones para el problema planteado
G.add_edges_from([
    ("Inicio", "Estudio Piloto"),
    ("Estudio Piloto", "Favorable"),
    ("Estudio Piloto", "Desfavorable"),
    ("Favorable", "Planta Grande"),
    ("Favorable", "Planta Pequeña"),
    ("Desfavorable", "No construir"),
    ("Planta Grande", "Mercado Favorable"),
    ("Planta Grande", "Mercado Desfavorable"),
    ("Planta Pequeña", "Mercado Favorable"),
    ("Planta Pequeña", "Mercado Desfavorable")
])

# Posiciones de los nodos para el gráfico (lo hacemos manual para que quede con formato de árbol)
pos = {
    "Inicio": (0, 4),
    "Estudio Piloto": (0, 3),
    "Favorable": (-1, 2),
    "Desfavorable": (1, 2),
    "Planta Grande": (-2, 1),
    "Planta Pequeña": (0, 1),
    "No construir": (2, 1),
    "Mercado Favorable": (-3, 0),
    "Mercado Desfavorable": (-1, 0)
}

# Dibujar los nodos y las aristas
nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_weight='bold', arrows=True)

# Mostrar el gráfico
plt.title("Árbol de Decisiones de Karime")
plt.show()
