import networkx as nx
import matplotlib.pyplot as plt
import staticmap
from typing import TypeAlias
import json
import urllib.request
import numpy as np
import pandas as pd
import math

BusesGraph : TypeAlias = nx.Graph
Coord : TypeAlias = tuple[float, float]

def distance(p1: Coord, p2: Coord) -> float:
    '''Donades dies coordenades calcula la distancia entre elles a vol d'ocell'''
    radi = 6371.0

    # Convertim les coordenades de graus a radians
    lat1_rad = math.radians(p1[0])
    lon1_rad = math.radians(p1[1])
    lat2_rad = math.radians(p2[0])
    lon2_rad = math.radians(p2[1])

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Utilitzem la fòrmula de Haversine
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return radi * c * 1000 #meters

def get_buses_graph() -> BusesGraph:
    """Retorna un graf a partir de les dades dels busos de l'AMB."""
    dades_busos_json = urllib.request.urlopen('https://www.ambmobilitat.cat/OpenData/ObtenirDadesAMB.json')
    busos = json.load(dades_busos_json)
    graf: BusesGraph = nx.Graph()
    first = True
    
    for linia in busos['ObtenirDadesAMBResult']['Linies']['Linia']:
        for parada in linia['Parades']['Parada']:
            # Agafem nomes les parades de Barcelona

            if parada['Municipi'] == 'Barcelona':
                if parada['CodAMB'] in dict(graf.nodes):
                    dict(graf.nodes)[parada['CodAMB']]['linia'].append(parada['IdLinia'])
                else:
                    graf.add_node(parada['CodAMB'], nom=parada['Nom'], linia=[parada['IdLinia']], pos=[parada['UTM_X'], parada['UTM_Y']])
                                                    
                if first:
                    first = False

                elif linia == parada['IdLinia'] and parada['CodAMB'] != parada_antiga:
                    graf.add_edge(parada['CodAMB'], parada_antiga, dist=0, pos1=dict(graf.nodes)[parada['CodAMB']]['pos'], pos2=dict(graf.nodes)[parada_antiga]['pos'])

                linia = parada['IdLinia']
                parada_antiga = parada['CodAMB']

    return graf

def show(g: BusesGraph) -> None:
    """Mostra el graf"""
    pos = nx.get_node_attributes(g, 'pos')
    nx.draw(g, node_size=0, pos=pos)
    plt.show()

def plot(g: BusesGraph, nom_fitxer: str) -> None:
    """Desa el graf com una imatge amb el mapa de la ciutat de fons en l'arxiu especificat."""
    
    mapa = staticmap.StaticMap(800, 800)
    
    for node in dict(g.nodes).values():
        p = (node['pos'][1], node['pos'][0])
        mapa.add_marker(staticmap.CircleMarker(p, 'red', 1))

    for edge in dict(g.edges).values():
        # Si la distancia de l'aresta és de més de 10km, no la volem mostrar ja que tan sols representa les unions entre els dos extrems de linia
        if edge['dist'] < 10000: 
            s = edge['pos2'][1], edge['pos2'][0]
            d = edge['pos1'][1], edge['pos1'][0]
            mapa.add_line(staticmap.Line([s, d], 'blue', 1))

    # Guardem la imatge en un fitxer
    imatge = mapa.render()
    imatge.save(nom_fitxer)
