from math import radians, sin, cos, sqrt, atan2

DISTANCIAS = {
    #Linea A
    "LINEA_A":[
        ("Alberti", "Pasco", 234.71),
        ("Pasco", "Congreso", 519.97),
        ("Congreso", "Sáenz Peña", 549.30),
        ("Sáenz Peña", "Lima", 380.56),
        ("Lima", "Piedras", 360.89),
        ("Piedras", "Perú", 339.32),
        ("Perú", "Plaza de Mayo", 312.92)
    ],
    "LINEA_B": [
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
        ("Facultad de Medicina", "Callao_D", 497.41),
        ("Callao_D", "Tribunales", 749.65),
        ("Tribunales", "9 de Julio", 508.97),
        ("9 de Julio", "Catedral", 640.07)
    ],
    "LINEA_E":[
        ("Pichincha", "Entre Ríos", 514.80),
        ("Entre Ríos", "San José", 575.60),
        ("San José", "Independencia_E", 647.70),
        ("Independencia_E", "Belgrano", 624.34),
        ("Belgrano", "Bolívar", 504.77)
    ]
}

#Vamos a calcular la velocidad media de los metros
def haversine(lat1, lon1, lat2, lon2) -> float:
    """
    Esta función calcula según la fórmula de Haversine la distancia entre
    dos puntos geográficos a partir de sus coordenadas y teniendo en cuenta
    la curvatura de la Tierra.
    """
    R = 6371e3  # Radio de la Tierra en metros
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    a = sin(dphi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(dlambda / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

"""
Primero calculamos las distancias medias de cada tren
"""
#Linea A
Carabobo = [-34.626318245011326, -58.45600940467113]
Plaza_de_Mayo = [-34.60875839408815, -58.37151330936176]
Ditancia_A = haversine(Carabobo[0], Carabobo[1], Plaza_de_Mayo[0], Plaza_de_Mayo[1])
Tiempo_A = 23*60 #En segundos
VelovidadMedia_A = (Ditancia_A / Tiempo_A )  #m/s

#Linea B
Parque_Chas = [-34.58140914095646, -58.47387976238464]
Leandro_N_Alem = [-34.60302925135683, -58.37004749037363]
Ditancia_B = haversine(Parque_Chas[0], Parque_Chas[1], Leandro_N_Alem[0], Leandro_N_Alem[1])
Tiempo_B = 23*60 #En segundos
VelovidadMedia_B = (Ditancia_B / Tiempo_B )  #m/s

#Linea C
Contitución = [-34.62753942668646, -58.38156121435256]
Retiro = [-34.59238671801715, -58.37594819705223]
Ditancia_C = haversine(Contitución[0], Contitución[1], Retiro[0], Retiro[1])
Tiempo_C = 13*60 #En segundos
VelovidadMedia_C = (Ditancia_C / Tiempo_C )  #m/s

#Linea D
Congreso_tucumán = [-34.55589921320206, -58.46214247768847]
Catedral = [-34.60757221396939, -58.37419688300631]
Ditancia_D = haversine(Congreso_tucumán[0], Congreso_tucumán[1], Catedral[0], Catedral[1])
Tiempo_D = 26*60 #En segundos
VelovidadMedia_D = (Ditancia_D / Tiempo_D )  #m/s

#Linea E
Plaza_virreyes = [-34.64291529882225, -58.46162228932788]
Bolívar = [-34.60961123829135, -58.37401251606132]
Ditancia_E = haversine(Plaza_virreyes[0], Plaza_virreyes[1], Bolívar[0], Bolívar[1])
Tiempo_E = 24*60 #En segundos
VelovidadMedia_E = (Ditancia_E / Tiempo_E )  #m/s


velocidades = {
    "LINEA_A": VelovidadMedia_A,
    "LINEA_B": VelovidadMedia_B,
    "LINEA_C": VelovidadMedia_C,
    "LINEA_D": VelovidadMedia_D,
    "LINEA_E": VelovidadMedia_E,
}

"""
Ahora vamos a calcular el tiempo que tarda entre paradas. luego tendremos en cuenta que hay que añadirle penalizaciones
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