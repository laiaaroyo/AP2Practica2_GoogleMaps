import networkx as nx
import matplotlib.pyplot as plt
import staticmaps
from typing import TypeAlias
from dataclasses import dataclass
import json
import urllib.request
import numpy as np
import pandas as pd

BusesGraph : TypeAlias = nx.Graph
Coord : TypeAlias = tuple[float, float]

@dataclass
class Parada:
    nom: str
    linies: list[str]
    pos: Coord

    def __init__(self, nom, linia: str, pos: Coord) -> None:
        self.nom = nom
        self.linies = [linia]
        self.pos = pos

    def add_a_line(self, linia: str) -> None:
        self.linies.append(linia)

class Bus:
    v_by_bus: int = 15 #km/h
    dist: float 
    t_espera: int = 0
    duration: float

    def __init__(self, dist: float) -> None:
        self.dist = dist
        self.duration = self.dist*self.v_by_bus

    def revalue(self, newdist: float) -> float:
        '''Recalcula la duracio quan actualitzem la distancia'''
        self.dist = newdist
        self.duration = self.dist*self.v_by_bus
    
    def calculate_duration(self, wait: bool) -> float:
        '''Calcula el que tardara en anar en bus segons si ja estava pujat al bus o l'ha d'esperar'''
        if wait:
            return self.duration + self.t_espera
        return self.duration

def distance(p1: Coord, p2: Coord) -> float:
    '''Donades dies coordenades calcula la distancia entre elles a vol d'ocell'''
    return np.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

def get_buses_graph() -> BusesGraph:
    """Retorna un graf a partir de les dades dels busos de l'AMB."""
    dades_busos_json = urllib.request.urlopen('https://www.ambmobilitat.cat/OpenData/ObtenirDadesAMB.json')
    busos = json.load(dades_busos_json)
    graf: BusesGraph = nx.Graph()
    first = True

    for linia in busos['ObtenirDadesAMBResult']['Linies']['Linia']:
        for parada in linia['Parades']['Parada']:
            if parada['CodAMB'] in dict(graf.nodes):
                dict(graf.nodes)[parada['CodAMB']]['info'].add_a_line(parada['IdLinia'])
            else:
                graf.add_node(parada['CodAMB'], info=Parada(parada['Nom'], parada['IdLinia'], pos=[-parada['UTM_X'], -parada['UTM_Y']]), pos=[-parada['UTM_X'], -parada['UTM_Y']])
                    
            if first:
                first = False

            elif linia == parada['IdLinia'] and parada['CodAMB'] != parada_antiga:
                graf.add_edge(parada['CodAMB'], parada_antiga, info=Bus(distance(dict(graf.nodes)[parada['CodAMB']]['pos'], dict(graf.nodes)[parada_antiga]['pos'])))

            linia = parada['IdLinia']
            parada_antiga = parada['CodAMB']

    return graf

def show(g: BusesGraph) -> None:
    """Mostra el graf"""
    pos = nx.get_node_attributes(g, 'pos')
    nx.draw(g, node_size=0, pos=pos)
    plt.show()

    'o sino'
    '''
    mapa = folium.Map(location=[2.1589900, 41.3887900])
    for p in g.nodes:
        folium.Marker(p['info'].pos, popup = p['info'].nom, tooltip = p['info'].nom).add_to(mapa)
    '''

def plot(g: BusesGraph, nom_fitxer: str) -> None:
    """Desa el graf com una imatge amb el mapa de la ciutat en l'arxiu especificat."""
    'no funciona'
    mapa = (800, 800)
    bbox = g.get_bounding_box() #Area definida amb coordenades
    mapa.add_image(staticmaps.BoundingBox(*bbox), zoom=15)

    for node in g.nodes:
        p = staticmaps.create_latlng(node['info']['pos'][0], node['info']['pos'][1])
        mapa.add_markers(staticmaps.CircleMarker(p, 'red', 5))

    for edge in g.edges:
        s = staticmaps.create_latlng(edge.source['info']['pos'][0], edge.source['info']['pos'][1])
        d = staticmaps.create_latlng(edge.target['info']['pos'][0], edge.target['info']['pos'][1])
        mapa.add_line(staticmaps.Line([s, d], 'blue', 1))

    mapa.save(nom_fitxer)
'''
def main():
    graf = get_buses_graph()
    show(graf)
'''
