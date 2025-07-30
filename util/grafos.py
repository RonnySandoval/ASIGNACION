import networkx as nx
import matplotlib.pyplot as plt

# Ruta al archivo .txt
archivo = "C:\\NUEVO_PORTATIL\\GITHUB\\ASIGNACION\\utilities\\nombres_archivos.txt"

# Leer y guardar cada línea en una lista, eliminando el salto de línea final
with open(archivo, "r") as f:
    lista_nombres = [linea.strip() for linea in f]

# Mostrar la lista resultante
print(lista_nombres)


# Crear un grafo dirigido
Grafo = nx.DiGraph()

# Agregar nodos
Grafo.add_nodes_from(lista_nombres)

# Agregar aristas dirigidas (de -> hacia)
Grafo.add_edges_from([
    ("main", "controller.mainMenu"),
    ("main", "controller.glo"),
    ("main", "view.estilos"),
    ("main", "view.ventanas_emergentes"),
    ("controller.mainMenu", "controller.mainController"),
    ("controller.mainMenu", "view.estilos"),
    ("controller.mainController", "database.BDcrear"),
    ("controller.mainController", "database.BBDD"),
    ("controller.mainController", "controller.glo"),
    ("controller.mainController", "menu.stepsNuevaPlanta"),
    ("controller.mainController", "menu.ventanaNuevaPlanta"),
    ("controller.mainController", "menu.menu_principal"),
    ("controller.mainController", "view.ventanas_emergentes"),
    ("controller.mainController", "view.root"),
    ("controller.controller", "database.BDcrear"),
    ("controller.controller", "database.BBDD"),
    ("controller.controller", "controller.glo"),
    ("controller.controller", "controller.exception_manejar"),
    ("controller.controller", "menu.stepsNuevaPlanta"),
    ("controller.controller", "menu.ventanaNuevaPlanta"),
    ("controller.controller", "model.model_classPlant"),
    ("controller.controller", "model.model_instancePlant"),
    ("controller.controller", "model.model_callGantt"),
    ("controller.controller", "model.model_datetime"),
    ("controller.controller", "model.model_gantt"),
    ("controller.controller", "view.ventanas_topLevel"),
    ("controller.controller", "view.ventanas_emergentes"),
    ("controller.controller", "view.estilos"),
    ("menu.stepsNuevaPlanta", "view.estilos"),
    ("menu.ventanaNuevaPlanta", "view.ventanas_emergentes"),
    ("menu.ventanaNuevaPlanta", "view.estilos"),
    ("menu.menu_principal", "view.estilos"),
    ("menu.menu_principal", "menu.submenu_nuevo"),
    ("menu.menu_principal", "menu.submenu_editar"),
    ("menu.menu_principal", "menu.submenu_importar"),
    ("menu.menu_principal", "menu.submenu_exportar"),
    ("menu.submenu_editar", "menu.ventanasEliminar"),
    ("menu.submenu_editar", "view.ventanas_topLevel"),
    ("menu.submenu_editar", "controller.controller"),
    ("menu.submenu_editar", "controller.glo"),
    ("menu.submenu_exportar", "view.ventanas_topLevel"),
    ("menu.submenu_exportar", "controller.controller"),
    ("menu.submenu_exportar", "controller.glo"),
    ("menu.submenu_exportar", "database.BBDD"),
    ("menu.submenu_importar", "menu.ventanasImportar"),
    ("menu.submenu_importar", "controller.controller"),
    ("menu.submenu_importar", "controller.controller"),
    ("menu.submenu_nuevo", "view.ventanas_topLevel"),
    ("menu.submenu_nuevo", "view.ventanaNuevoPedido"),
    ("menu.submenu_nuevo", "view.ventanaNuevoTecnico"),
    ("menu.submenu_nuevo", "view,ventanaNuevoProceso"),
    ("menu.submenu_nuevo", "controller.controller"),
    ("menu.submenu_nuevo", "controller.glo"),
    ("", ""),
    
])

# Dibujar el grafo
pos = nx.spring_layout(Grafo)  # Posicionamiento automático
nx.draw(Grafo, pos, with_labels=True, node_size=1500, node_color='lightblue', arrowsize=20, font_size=10)
plt.title("Importaciones de módulos")
plt.show()
