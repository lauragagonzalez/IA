import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import math
import os
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime, timedelta
import webbrowser
import folium
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar

# matplotlib debe usar el backend tkAgg para evitar conflictos con tkinter
matplotlib.use('tkAgg')

# VARIABLES Y DATOS
LISTA_COORDENADAS = {
    "LINEA_A": {
        "Alberti": [-34.60979154021843, -58.40086740463643],
        "Pasco": [-34.609455989895245, -58.39833539938651],
        "Congreso": [-34.608996813572965, -58.39268130286541],
        "Sáenz Peña": [-34.609350026351635, -58.38669461230903],
        "Lima": [-34.60904096524644, -58.382553281561165],
        "Piedras": [-34.60886435838594, -58.37861579874318],
        "Perú": [-34.60857295624564, -58.37492507907565],
        "Plaza de Mayo": [-34.60875839408815, -58.37151330936176],
    },
    "LINEA_B": {
        "Pasteur": [-34.60409382222638, -58.39968610352264],
        "Callao_B": [-34.60434108592872, -58.39243341083207],
        "Uruguay": [-34.60400961150244, -58.38674150304544],
        "Carlos Pellegrini": [-34.60370936151744, -58.381380708823514],
        "Florida": [-34.603244782294965, -58.37454489610343],
        "Leandro N. Alem": [-34.60302925135683, -58.37004749037363],
    },
    "LINEA_C": {
        "Constitución": [-34.62753942668646, -58.38156121435256],
        "San Juan": [-34.622153370728164, -58.37994066311232],
        "Independencia_C": [-34.6180519466846, -58.380256098860485],
        "Moreno": [-34.61237244698663, -58.38060876062811],
        "Avenida de Mayo": [-34.60899098423044, -58.38066790483753],
        "Diagonal Norte": [-34.60482400192541, -58.379488963667214],
        "Lavalle": [-34.60207510706261, -58.37814441867528],
        "General San Martin": [-34.59553840845914, -58.37745834587982],
        "Retiro": [-34.59238671801715, -58.37594819705223],
    },
    "LINEA_D": {
        "Facultad de Medicina": [-34.5993682836706, -58.3977359491304],
        "Callao_D": [-34.59957140474557, -58.392307158181815],
        "Tribunales": [-34.60176154833913, -58.38456093858365],
        "9 de Julio": [-34.60453888530524, -58.38014065809253],
        "Catedral": [-34.60757221396939, -58.37419688300631],
    },
    "LINEA_E": {
        "Pichincha": [-34.62304099718662, -58.39710097116426],
        "Entre Ríos": [-34.62270550042393, -58.391489789929345],
        "San José": [-34.62224639739259, -58.385224149714155],
        "Independencia_E": [-34.61812318513492, -58.380224512115895],
        "Belgrano": [-34.6128518852584, -58.37787489702144],
        "Bolívar": [-34.60961123829135, -58.37401251606132],
    },
}

LINEA_A = {"Alberti", "Pasco", "Congreso", "Sáenz Peña", "Lima", "Piedras", "Perú", "Plaza de Mayo"}
LINEA_B = {"Pasteur", "Callao_B", "Uruguay", "Carlos Pellegrini", "Florida", "Leandro N. Alem"}
LINEA_C = {"Constitución", "San Juan", "Independencia_C", "Moreno", "Avenida de Mayo", "Diagonal Norte", "Lavalle",
           "General San Martin", "Retiro"}
LINEA_D = {"Facultad de Medicina", "Callao_D", "Tribunales", "9 de Julio", "Diagonal Norte", "Catedral"}
LINEA_E = {"Pichincha", "Entre Ríos", "San José", "Independencia_E", "Belgrano", "Bolívar"}
estaciones_linea = [LINEA_A, LINEA_B, LINEA_C, LINEA_D, LINEA_E]

transbordos = [
    ("Lima", "Avenida de Mayo"),                # Línea A <-> Línea C
    ("Perú", "Catedral"),                       # Línea A <-> Línea D
    ("Independencia_C", "Independencia_E"),     # Línea C <-> Línea E
    ("Bolívar", "Perú"),                        # Línea E <-> Línea A
    ("Bolívar", "Catedral"),                    # Línea E <-> Línea D
    ("Diagonal Norte", "Carlos Pellegrini"),    # Línea C <-> Línea B
    ("Carlos Pellegrini", "9 de Julio"),        # Línea B <-> Línea D
    ("9 de Julio", "Diagonal Norte"),           # Línea D <-> Línea C
]

velocidades = {
    "LINEA_A": 5.860,
    "LINEA_B": 7.414,
    "LINEA_C": 5.120,
    "LINEA_D": 6.425,
    "LINEA_E": 6.464,
}

FESTIVOS = [
    "01-01", "24-03", "02-04", "01-05", "25-05", "20-06", "09-07", "17-08",
    "12-10", "20-11", "08-12", "25-12"
]


# FUNCIONES AUXILIARES PARA EL GRAFO
def colorear_nodos(grafo, estaciones):
    color = []
    for node in grafo.nodes:
        if node in estaciones[0]:
            color.append('lightblue')
        elif node in estaciones[1]:
            color.append('red')
        elif node in estaciones[2]:
            color.append('darkblue')
        elif node in estaciones[3]:
            color.append('green')
        elif node in estaciones[4]:
            color.append('purple')
        else:
            color.append('gray')  # Color por defecto si no se encuentra en ninguna línea
    return color


def colorear_edges(grafo, estaciones, transbordos):
    color_edge = []
    for edge in grafo.edges:
        node1, node2 = edge
        if (node1, node2) in transbordos or (node2, node1) in transbordos:
            color_edge.append('yellow')
        elif node1 in estaciones[0] or node2 in estaciones[0]:
            color_edge.append('lightblue')
        elif node1 in estaciones[1] or node2 in estaciones[1]:
            color_edge.append('red')
        elif node1 in estaciones[2] or node2 in estaciones[2]:
            color_edge.append('darkblue')
        elif node1 in estaciones[3] or node2 in estaciones[3]:
            color_edge.append('green')
        elif node1 in estaciones[4] or node2 in estaciones[4]:
            color_edge.append('purple')
        else:
            color_edge.append('gray')  # Color por defecto
    return color_edge


def haversine(lat1, lon1, lat2, lon2) -> float:
    """
    Esta función calcula según la fórmula de Haversine la distancia entre dos puntos geográficos a partir de sus
    coordenadas y teniendo en cuenta la curvatura de la Tierra.
    """
    R = 6371e3  # Radio de la Tierra en metros
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    a = sin(dphi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(dlambda / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def distancia(coordenadas_1, coordenadas_2) -> float:
    """
    Usa la función haversine para calcular la respectiva distancia entre dos coordenadas.
    """
    return haversine(coordenadas_1[0], coordenadas_1[1], coordenadas_2[0], coordenadas_2[1])


# FUNCIONES AUXILIARES PARA ALGORITMO A*
def haversine_h(nodo_actual, nodo_objetivo) -> float:
    """
    Calculo de la distancia entre dos nodos del grafo elegidos (el nodo actual y el nodo destino) con la
    fórmula de haversine.
    """
    pos_actual = G.nodes[nodo_actual]['pos']
    pos_objetivo = G.nodes[nodo_objetivo]['pos']
    lat1 = pos_actual[0]
    lon1 = pos_actual[1]
    lat2 = pos_objetivo[0]
    lon2 = pos_objetivo[1]
    # Convertir de grados a radianes
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    return haversine(lat1, lon1, lat2, lon2)


def tiempo(path, grafo, velocidades) -> float:
    """
    Coge el camino desde el origen al destino y calcula cuanto tarda teniendo en cuenta las velocidades
    de cada linea, y el tiempo por transbordo
    """
    if len(path) == 1:
        return 0
    path_g = grafo.subgraph(path)
    t = 0
    for index in range(len(path) - 1):
        nodo1 = path[index]
        nodo2 = path[index + 1]
        arista = path_g.get_edge_data(nodo1, nodo2)
        line = arista.get("line")
        if line == "transbordo":
            t += 2  # consideramos que se tarda una media de 2 min en realizar un transbordo
        else:
            dist = arista.get("weight", 0)
            velocidad = velocidades.get(line, 0)
            tiempo_trayecto = dist / velocidad
            t += tiempo_trayecto / 60  # lo convertimos en minutos
    return t


def a_estrella(origen_n, destino_n, grafo, velocidades):
    """
    Aplica el algoritmo A* para hallar el camino más corto entre el origen y el destino, devolviendo
    además la longitud de dicho camino.
    """
    camino = nx.astar_path(grafo, origen_n, destino_n, heuristic=haversine_h)
    longitud = nx.astar_path_length(grafo, origen_n, destino_n, heuristic=haversine_h)
    tiempo_trayecto = tiempo(camino, grafo, velocidades)
    return camino, longitud, tiempo_trayecto


def visualizacion(origen_n, destino_n, grafo, velocidades, transbordos):
    """
    Toma un grafo, el origen y destino de la ruta deseada y las velocidades especificas, y crea un grafo mostrando
    la ruta encontrada por el algoritmo A*
    """
    path = a_estrella(origen_n, destino_n, grafo, velocidades)[0]
    path_g = grafo.subgraph(path)
    pos_path = nx.get_node_attributes(grafo, 'pos')
    color_path = colorear_nodos(path_g, estaciones_linea)
    color_edge_path = colorear_edges(path_g, estaciones_linea, transbordos)

    nx.draw(path_g,
            pos=pos_path,
            node_color=color_path,
            with_labels=True,
            edge_color=color_edge_path,
            font_size=5,
            node_size=100)
    plt.show()


# CREACION DEL GRAFO
G = nx.Graph()

# Agregamos nodos con posiciones
for linea, estaciones in LISTA_COORDENADAS.items():
    for estacion, coordenadas in estaciones.items():
        G.add_node(estacion, pos=(coordenadas[0], coordenadas[1]))

# Agregamos aristas entre estaciones con peso determinado por la distancia entre estas
for linea, estaciones in LISTA_COORDENADAS.items():
    estaciones_lista = list(estaciones.keys())
    for i in range(len(estaciones_lista) - 1):
        estacion1 = estaciones_lista[i]
        estacion2 = estaciones_lista[i + 1]
        coord1 = estaciones[estacion1]
        coord2 = estaciones[estacion2]
        G.add_edge(estacion1, estacion2, weight=distancia(coord1, coord2), line=linea)

# Obtener posiciones de los nodos
pos = nx.get_node_attributes(G, 'pos')

# Agregar las aristas entre las estaciones de transbordo
for conexion in transbordos:
    estacion1, estacion2 = conexion
    if estacion1 in G.nodes and estacion2 in G.nodes:
        G.add_edge(estacion1, estacion2, weight=10, line="transbordo")  # Peso de penalizacion 10 metros

# Coloreamos los nodos y las aristas
node_colors = colorear_nodos(G, estaciones_linea)
edge_colors = colorear_edges(G, estaciones_linea, transbordos)

# Dibujar el grafo
plt.figure(figsize=(12, 10))

nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=2)
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=500)
nx.draw_networkx_labels(G, pos, font_size=12)

plt.show()


# EJEMPLOS Y PRUEBAS DEL ALGORITMO A*

# prueba 1: distintas lineas
origen = "Pasteur"
destino = "Plaza de Mayo"
visualizacion(origen, destino, G, velocidades, transbordos)

# prueba 2: de origen al mismo sitio
origen = "Pasteur"
destino = "Pasteur"
visualizacion(origen, destino, G, velocidades, transbordos)

# prueba 3: misma linea
origen = "Constitución"
destino = "Retiro"
visualizacion(origen, destino, G, velocidades, transbordos)


# FUNCIONES AUXILIARES PARA LA INTERFAZ
def es_festivo(fecha):
    """
    Toma una fecha datetime y devuelve un booleano indicando si es festivo o no.
    """
    return fecha.strftime("%d-%m") in FESTIVOS


def horario_metro_operativo(fecha, hora):
    """
    Se toma la fecha y la hora seleccionadas por el usuario y se comprueba si son validas, si lo son se la devolverá
    True, de lo contrario devolverá False, también devolverá un mensaje dependiendo de la situación.
    """
    festivo = es_festivo(fecha)
    dia_semana = fecha.weekday()  # 0=Lunes - 6=Domingo
    if festivo or dia_semana == 6:
        inicio_operativo = datetime.strptime("08:00", "%H:%M").time()
        fin_operativo = datetime.strptime("22:00", "%H:%M").time()
    elif dia_semana == 5:
        inicio_operativo = datetime.strptime("05:00", "%H:%M").time()
        fin_operativo = datetime.strptime("22:30", "%H:%M").time()
    else:
        inicio_operativo = datetime.strptime("05:00", "%H:%M").time()
        fin_operativo = datetime.strptime("22:20", "%H:%M").time()

    if not (inicio_operativo <= hora <= fin_operativo):
        return False, "El servicio de metro no está operativo en el horario seleccionado."
    if datetime.strptime("21:30", "%H:%M").time() <= hora <= fin_operativo:
        return True, "Es posible que el metro cierre pronto."
    return True, ""


def validar_ruta(origen, destino):
    """
    Valida la estacion origen y estacion destino introducidos por el usuario y devuelve un booleano, si hay un error
    con las entradas se devuelve ademas un mensaje de error.
    """
    if not origen or not destino:
        mensaje = "Debe seleccionar tanto la estación de origen como la de destino."
        return False, mensaje
    if origen not in G.nodes or destino not in G.nodes:
        mensaje = "La estación de origen o la estación de destino no existen."
        return False, mensaje
    if origen == destino:
        mensaje = "Ya está en su destino"
        return True, mensaje
    return True, ""


def detectar_transbordos_ruta(ruta):
    """
    Toma una ruta y devuelve una lista de duplas correspondientes a los transbordos de esta.
    """
    transbordos = []
    for index in range(len(ruta) - 1):
        nodo1 = ruta[index]
        nodo2 = ruta[index + 1]
        arista = G.get_edge_data(nodo1, nodo2)
        line = arista.get("line")
        if line == "transbordo":
            transbordos.append((nodo1, nodo2))
    return transbordos


def mostrar_detalles(ruta, distancia_total, tiempo_trayecto, hora_llegada, transbordos):
    """
    Muestra un cuadro de diálogo con los detalles de la ruta calculada.
    """
    detalles = f"Ruta: {' -> '.join(ruta)}\n\n"
    detalles += f"Distancia total: {distancia_total:.2f} metros\n"
    detalles += f"Tiempo estimado: {tiempo_trayecto:.2f} minutos\n"
    detalles += f"Hora estimada de llegada: {hora_llegada.strftime('%H:%M')}\n"

    if transbordos:
        detalles += "\nTransbordos:\n"
        for origen, destino in transbordos:
            detalles += f"  - De {origen} a {destino}\n"

    messagebox.showinfo("Detalles de la ruta", detalles)


def mostrar_mapa(ruta):
    coords = []
    for estacion in ruta:
        found = False
        index = 0
        while index < len(LISTA_COORDENADAS) and not found:
            linea, estaciones = list(LISTA_COORDENADAS.items())[index]
            if estacion in estaciones:
                coords.append(estaciones[estacion])
                found = True
            index += 1
        if not found:
            messagebox.showerror("Error", "No se pudieron encontrar coordenadas para algunas estaciones.")
            return

    inicio_coord = coords[0]
    mapa = folium.Map(location=inicio_coord, zoom_start=14)

    for estacion, coord in zip(ruta, coords):
        folium.Marker(coord, popup=estacion).add_to(mapa)

    folium.PolyLine(coords, color="blue", weight=5).add_to(mapa)

    try:
        mapa.save("ruta_metro.html")
        print("Mapa guardado correctamente como 'ruta_metro.html'.")  # Debug
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el mapa: {e}")
        return

    try:
        file_path = os.path.abspath("ruta_metro.html")
        webbrowser.open(f"file://{file_path}")
        print("Abierto")  # Debug
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el navegador: {e}")
        return


def calcular_ruta():
    """
    Calcula la ruta más corta entre la estación de origen y la de destino.
    Valida las entradas y muestra los resultados en la interfaz gráfica.
    """
    origen_n = estacion_origen.get()
    destino_n = estacion_destino.get()

    ruta_valida, mensaje = validar_ruta(origen_n, destino_n)
    if not ruta_valida:
        messagebox.showerror("Error", mensaje)
        return
    elif mensaje:
        messagebox.showinfo("Aviso", mensaje)

    hora = hora_var.get()
    minuto = minuto_var.get()

    try:
        hora = int(hora)
        minuto = int(minuto)
        fecha_viaje = datetime.strptime(fecha_var.get(), "%d-%m-%Y")
        hora_viaje = datetime.strptime(f"{hora:02d}:{minuto:02d}", "%H:%M").time()

        operativo, mensaje_horario = horario_metro_operativo(fecha_viaje, hora_viaje)
        if not operativo:
            messagebox.showerror("Error", mensaje_horario)
            return
        elif mensaje_horario:
            messagebox.showinfo("Aviso", mensaje_horario)

    except ValueError:
        messagebox.showerror("Error", "Hora o fecha inválida.")
        return

    except Exception as e:
        messagebox.showerror("Error inesperado", f"Ha ocurrido un error inesperado: {str(e)}")
        return

    try:
        ruta, longitud, tiempo_total = a_estrella(origen_n, destino_n, G, velocidades)
        transbordos_ruta = detectar_transbordos_ruta(ruta)
        hora_llegada = datetime.combine(fecha_viaje, hora_viaje) + timedelta(minutes=tiempo_total)

        mostrar_mapa(ruta)
        mostrar_detalles(ruta, longitud, tiempo_total, hora_llegada, transbordos_ruta)

    except nx.NetworkXNoPath:
        messagebox.showerror("Error", "No existe una ruta entre las estaciones seleccionadas.")

    except Exception as e:
        messagebox.showerror("Error inesperado", f"Ha ocurrido un error: {str(e)}")


# CREACION Y DISEÑO DE LA INTERFAZ
ventana = tk.Tk()
ventana.title("Calculadora de rutas de metro")

estacion_origen = tk.StringVar()
estacion_destino = tk.StringVar()
fecha_var = tk.StringVar()
hora_var = tk.StringVar()
minuto_var = tk.StringVar()

# Si el usuario no especifica fecha/hora/minuto estos valores serán los tiempos actuales
fecha_actual = datetime.now()
hora_actual = fecha_actual.hour
minuto_actual = fecha_actual.minute

fecha_var.set(fecha_actual.strftime("%d-%m-%Y"))
hora_var.set(f"{hora_actual:02d}")
minuto_var.set(f"{minuto_actual:02d}")

# Widgets
ttk.Label(ventana, text="Estación de origen:").grid(row=0, column=0, padx=10, pady=10)
origen_menu = ttk.Combobox(ventana, textvariable=estacion_origen, values=list(G.nodes()))
origen_menu.grid(row=0, column=1, padx=10, pady=10)

ttk.Label(ventana, text="Estación de destino:").grid(row=1, column=0, padx=10, pady=10)
destino_menu = ttk.Combobox(ventana, textvariable=estacion_destino, values=list(G.nodes()))
destino_menu.grid(row=1, column=1, padx=10, pady=10)

# Selector de fecha
ttk.Label(ventana, text="Fecha de viaje:").grid(row=2, column=0, padx=10, pady=10)
calendario = Calendar(
    ventana, date_pattern="dd-mm-yyyy",
    textvariable=fecha_var,
    year=fecha_actual.year,
    month=fecha_actual.month,
    day=fecha_actual.day,
    mindate=fecha_actual
)
calendario.grid(row=2, column=1, padx=10, pady=10)

# Selector de hora y minutos
ttk.Label(ventana, text="Hora de salida:").grid(row=3, column=0, padx=10, pady=10)
horas = [f"{h:02d}" for h in range(24)]
minutos = [f"{m:02d}" for m in range(60)]
hora_menu = ttk.Combobox(ventana, textvariable=hora_var, values=horas, width=5, state="readonly")
hora_menu.grid(row=3, column=1, padx=10, pady=5, sticky="w")
minuto_menu = ttk.Combobox(ventana, textvariable=minuto_var, values=minutos, width=5, state="readonly")
minuto_menu.grid(row=3, column=1, padx=10, pady=5, sticky="e")

# Boton de calcular ruta
calcular_btn = ttk.Button(ventana, text="Calcular Ruta", command=calcular_ruta)
calcular_btn.grid(row=4, column=0, columnspan=2, pady=20)

ventana.mainloop()
