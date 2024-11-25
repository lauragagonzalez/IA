from math import radians, sin, cos, sqrt, atan2

DISTANCIAS_COMPLETAS = {
    "LINEA_A":[
        ("Carabobo", "Puan", 666.10),
        ("Puan", "Primera Junta", 770.65),
        ("Primera Junta", "Acoyte", 576.81),
        ("Acoyte", "Rio de Janeiro", 678.99),
        ("Rio de Janeiro", "Castro Barros", 799.44),
        ("Castro Barros", "Loria", 605.62),
        ("Loria", "Plaza Miserere", 755.08),
        ("Plaza Miserere", "Alberti", 536.48),
        ("Alberti", "Pasco", 234.71),
        ("Pasco", "Congreso", 519.97),
        ("Congreso", "Sáenz Peña", 549.30),
        ("Sáenz Peña", "Lima", 380.56),
        ("Lima", "Piedras", 360.89),
        ("Piedras", "Perú", 339.32),
        ("Perú", "Plaza de Mayo", 312.92)

    ],
    "LINEA_B": [
        ("De Los Incas", "Tronador", 738.35),
        ("Tronador", "Federico Lacroze", 1077.21),
        ("Federico Lacroze", "Dorrego", 857.96),
        ("Dorrego", "Malabia", 1096.97),
        ("Malabia", "Ángel Gallardo", 852.50),
        ("Ángel Gallardo", "Medrano", 910.95),
        ("Medrano", "Carlos Gardel", 870.01),
        ("Carlos Gardel", "Pueyrredón_B", 583.53),
        ("Pueyrredón_B", "Pasteur", 524.81),
        ("Pasteur", "Callao_B", 664.36),
        ("Callao_B", "Uruguay", 522.25),
        ("Uruguay", "Carlos Pellegrini", 491.78),
        ("Carlos Pellegrini", "Florida", 627.78),
        ("Florida", "Leandro N. Alem", 412.32)
    ],
    "LINEA_C": [
        ("Constitución", "San Juan", 616.99),
        ("San Juan", "Independencia_C", 456.97),
        ("Independencia_C", "Moreno", 632.36),
        ("Moreno", "Avenida de Mayo", 376.04),
        ("Avenida de Mayo", "Diagonal Norte", 475.74),
        ("Diagonal Norte", "Lavalle", 329.50),
        ("Lavalle", "General San Martin", 729.56),
        ("General San Martin", "Retiro", 376.73)
    ],
    "LINEA_D":[
        ("Congreso de Tucamán", "Juramento", 809.99),
        ("Juramento", "Jose Hernández", 561.80),
        ("Jose Hernández", "Olleros", 838.39),
        ("Olleros", "Mtro. Carranza", 1052.78),
        ("Mtro. Carranza", "Palermo", 857.24),
        ("Palermo", "Plaza Italia", 529.33),
        ("Plaza Italia", "Scalabrini Ortiz", 660.35),
        ("Scalabrini Ortiz", "Bulnes", 558.38),
        ("Bulnes", "Aguero", 529.27),
        ("Aguero", "Pueyrredón_D", 471.58),
        ("Pueyrredón_D", "Facultad de Medicina", 758.25),
        ("Facultad de Medicina", "Callao_D", 497.41),
        ("Callao_D", "Tribunales", 749.65),
        ("Tribunales", "9 de Julio", 508.97),
        ("9 de Julio", "Catedral", 640.07)
    ],
    "LINEA_E":[
        ("Plaza De Los Virreyes", "Varela", 460.01),
        ("Varela", "Medalla Milagrosa", 827.15),
        ("Medalla Milagrosa", "Emilio Mitre", 941.79),
        ("Emilio Mitre", "Jose María Moreno", 846.51),
        ("Jose María Moreno", "Av. La Plata", 672.50),
        ("Av. La Plata", "Boedo", 929.33),
        ("Boedo", "General Urquiza", 637.11),
        ("General Urquiza", "Jujuy", 601.21),
        ("Jujuy", "Pichincha", 525.94),
        ("Pichincha", "Entre Ríos", 514.80),
        ("Entre Ríos", "San José", 575.60),
        ("San José", "Independencia_E", 647.70),
        ("Independencia_E", "Belgrano", 624.34),
        ("Belgrano", "Bolívar", 504.77)
    ]
}


#Vamos a calcular la velocidad media de los metros

# calculo de las distancias de cada linea
def distancia_linea(linea) -> float:
    """
    Suma las distancias entre estaciones de una sola linea y devuelve el total.
    :param linea:
    :return:
    """
    distancia_total = 0
    for _, _, distancia in linea:
        distancia_total += distancia
    return distancia_total


def distancias_lineas(lista_lineas) -> list[float]:
    """
    Itera por una lista de lineas y devuelve una lista con sus distancias.
    :param lista_lineas:
    :return:
    """
    distancias = []
    for _, estaciones in lista_lineas:
        distancias.append(distancia_linea(estaciones))
    return distancias


distancias = distancias_lineas(DISTANCIAS_COMPLETAS.items())
print("Lista con distancias de cada linea")
print([f"{dist:.2f}" for dist in distancias])

# ahora calculamos la velocidad media dividiendo las distancias entre lo que tarda el tren en recorrerla

# datos de tiempo (en minutos)
LISTA_TIEMPOS = [
    ("Linea A", 23),
    ("Linea B", 23),
    ("Linea C", 13),
    ("Linea D", 26),
    ("Linea E", 24)
]

def velocidad_media(distancia, tiempo) -> float:
    """
    Calculo de velocidad media en m/s
    """
    tiempo_segundos = tiempo * 60
    velocidad = distancia/tiempo_segundos
    return velocidad


print("Velocidades de cada linea")
velocidades = []
for i in range(len(LISTA_TIEMPOS)):
    velocidad = velocidad_media(distancias[i], LISTA_TIEMPOS[i][1])
    velocidades.append(velocidad)
    print(f"{velocidad:.3f}")

velocidades = {
    "LINEA_A": 5.860,
    "LINEA_B": 7.414,
    "LINEA_C": 5.120,
    "LINEA_D": 6.425,
    "LINEA_E": 6.464,
}


"""
Ahora vamos a calcular el tiempo que tarda entre paradas. luego tendremos en cuenta que hay que añadirle penalizaciones
"""
"""
def calcular_tiempos(distancias, velocidad):
    tiempos = {}
    for linea, paradas in distancias.items():
        tiempos[linea] = []
        for estacion1, estacion2, distancia in paradas:
            velocidad = velocidades[linea]
            tiempo_segundos = distancia/velocidad
            tiempo_minutos = tiempo_segundos / 60
            tiempos[linea].append((estacion1, estacion2, tiempo_minutos))
    return tiempos

tiempos_entre_paradas = calcular_tiempos(DISTANCIAS, velocidades)


for linea, tiempos in tiempos_entre_paradas.items():
    print(f"Tiempos en {linea}:")
    for estacion1, estacion2, tiempo in tiempos:
        print(f" - {estacion1} -> {estacion2}: {tiempo} minutos")
    print()
"""