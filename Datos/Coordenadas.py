from math import radians, sin, cos, sqrt, atan2

# COORDENADAS A USAR

"""
Primero usamos Google maps para buscar las coordenadas de cada parada de metro
"""
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


# COORDENADAS COMPLETAS
LISTA_COORDENADAS_COMPLETAS = {
    "LINEA_A": {
        "Carabobo": [-34.62610053364731, -58.455266856364474],
        "Puan": [-34.62353373314256, -58.448689307796165],
        "Primera Junta": [-34.62040330896178, -58.44117541640411],
        "Acoyte": [-34.617827897591006, -58.43570373522767],
        "Rio de Janeiro": [-34.615073181860225, -58.42908179729282],
        "Castro Barros": [-34.6116592227342, -58.42139383355178],
        "Loria": [-34.61067477301032, -58.41488520995769],
        "Plaza Miserere": [-34.609659873855634, -58.40672725350365],
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
        "De Los Incas": [-34.58153925675342, -58.47376015526618],
        "Tronador": [-34.58408786297646, -58.46631270699223],
        "Federico Lacroze": [-34.587133888389175, -58.455142459711595],
        "Dorrego": [-34.59167198229591, -58.44756247499409],
        "Malabia": [-34.599033350690775, -58.43958411232091],
        "Ángel Gallardo": [-34.60212355254462, -58.43106017442186],
        "Medrano": [-34.603132845360776, -58.42118310189165],
        "Carlos Gardel": [-34.60407321067138, -58.411746270772355],
        "Pueyrredón_B": [-34.60453449708696, -58.40539518079814],
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
        "Congreso de Tucamán": [-34.5557799273591, -58.46010399738516],
        "Juramento": [-34.56215927071311, -58.45583392058106],
        "Jose Hernández": [-34.56615596837768, -58.45208060327335],
        "Olleros": [-34.570154610626496, -58.44431800992795],
        "Mtro. Carranza": [-34.575197921759525, -58.43458662356643],
        "Palermo": [-34.57819500778126, -58.425960008126516],
        "Plaza Italia": [-34.58118092699117, -58.4214569752959],
        "Scalabrini Ortiz": [-34.5849601727428, -58.41589282514232],
        "Bulnes": [-34.58822229497502, -58.411255473642484],
        "Aguero": [-34.59156998386249, -58.407145322915845],
        "Pueyrredón_D": [-34.594126963371004, -58.40303517216319],
        "Facultad de Medicina": [-34.5993682836706, -58.3977359491304],
        "Callao_D": [-34.59957140474557, -58.392307158181815],
        "Tribunales": [-34.60176154833913, -58.38456093858365],
        "9 de Julio": [-34.60453888530524, -58.38014065809253],
        "Catedral": [-34.60757221396939, -58.37419688300631],
    },
    "LINEA_E": {
        "Plaza De Los Virreyes": [-34.64287116515874, -58.46121459204399],
        "Varela": [-34.63973761536748, -58.45793156828877],
        "Medalla Milagrosa": [-34.6360831288283, -58.450056602652545],
        "Emilio Mitre": [-34.630936561930646, -58.4418812295682],
        "Jose María Moreno": [-34.627864359519926, -58.433416177903275],
        "Av. La Plata": [-34.62688440896298, -58.426163484695095],
        "Boedo": [-34.62541887571542, -58.41616420949085],
        "General Urquiza": [-34.62458015525477, -58.40927629675371],
        "Jujuy": [-34.62374142635343, -58.402785350874616],
        "Pichincha": [-34.62304099718662, -58.39710097116426],
        "Entre Ríos": [-34.62270550042393, -58.391489789929345],
        "San José": [-34.62224639739259, -58.385224149714155],
        "Independencia_E": [-34.61812318513492, -58.380224512115895],
        "Belgrano": [-34.6128518852584, -58.37787489702144],
        "Bolívar": [-34.60961123829135, -58.37401251606132],
    },
}

"""
Una vez tenemos las coordenadas vamos a aplicar la fórmula de Haversine que nos permite
calcular la distancia entre dos puntos geográficos
"""

def haversine(lat1, lon1, lat2, lon2):
    R = 6371e3  # Radio de la Tierra en metros
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    a = sin(dphi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(dlambda / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

conexiones = []
# Recorrer cada línea y calcular distancias entre estaciones consecutivas
for linea, estaciones in LISTA_COORDENADAS.items():
    estaciones_nombres = list(estaciones.keys())
    for i in range(len(estaciones_nombres) - 1):
        estacion1 = estaciones_nombres[i]
        estacion2 = estaciones_nombres[i + 1]
        coord1 = estaciones[estacion1]  # Coordenadas de la primera estación
        coord2 = estaciones[estacion2]  # Coordenadas de la segunda estación
        # Calcular la distancia entre estaciones consecutivas
        distancia = haversine(coord1[0], coord1[1], coord2[0], coord2[1])
        # Añadir a la lista de conexiones
        conexiones.append((estacion1, estacion2, distancia))

# Mostrar las conexiones calculadas
for conexion in conexiones:
    print(f"{conexion[0]} -> {conexion[1]}: {conexion[2]:.2f}")

# calculamos e imprimimos las distancia entre conexiones de las listas completas
conexiones_completas = []
# Recorrer cada línea y calcular distancias entre estaciones consecutivas
for linea, estaciones in LISTA_COORDENADAS_COMPLETAS.items():
    estaciones_nombres = list(estaciones.keys())
    for i in range(len(estaciones_nombres) - 1):
        estacion1 = estaciones_nombres[i]
        estacion2 = estaciones_nombres[i + 1]
        coord1 = estaciones[estacion1]  # Coordenadas de la primera estación
        coord2 = estaciones[estacion2]  # Coordenadas de la segunda estación
        # Calcular la distancia entre estaciones consecutivas
        distancia = haversine(coord1[0], coord1[1], coord2[0], coord2[1])
        # Añadir a la lista de conexiones
        conexiones_completas.append((estacion1, estacion2, distancia))

print("LINEAS COMPLETAS")
for conexion in conexiones_completas:
    print(f"{conexion[0]} -> {conexion[1]}: {conexion[2]:.2f}")