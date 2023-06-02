import networkx as nx
import osmnx as ox
import pickle
import os
from buses import *
from PIL import Image
import time

#folium, mapa interactivo

CityGraph : TypeAlias = nx.Graph
OsmnxGraph : TypeAlias = nx.MultiDiGraph
Path: TypeAlias = list[Coord]

V_CAMINANT: float = 1.5 #m/s
V_DEL_BUS: float = 7.0 #m/s

def get_osmx_graph() -> OsmnxGraph:
    '''Retorna un graf de la ciutat de Barcelona amb distancies'''
    g = ox.graph_from_place('Barcelona, Spain', network_type='all', simplify=True) 
    ox.distance.add_edge_lengths(g, precision=3, edges=None)
    return g

def save_osmnx_graph(g: OsmnxGraph, filename: str) -> None:
    '''Guarda el graf g al fitxer filename'''
    fitxer = open(filename, 'wb')
    pickle.dump(g, fitxer)
    fitxer.close()

def load_osmnx_graph(filename: str) -> OsmnxGraph:
    '''Retorna el graf guardat al fitxer filename'''
    assert os.path.exists(filename), 'El fitxer no existeix'
    g = open(filename, 'rb')
    graf = pickle.load(g)
    g.close()
    return graf

def cruilla_mes_propera(g: OsmnxGraph, edge: int) -> int:
    """Donada una Parada, retorna la seva Criulla conectada"""
    for vei, atr in dict(g.adj[edge]).items():
            if atr['tipus'] == 'cruilla':
                return vei

def build_city_graph(g1: OsmnxGraph, g2: BusesGraph) -> CityGraph:
    '''Retorna el graf resultant de la unió de g1 i g2.'''
    city_graf = nx.Graph()
    carrers_caminant: list = ['footway', 'pedestrian', 'residential']
    
    #fem que el nou graf tingui tots els nodes i arestes que el graf de la ciutat ara amb les dades que ens interessen.
    for node in g1.nodes.data():
        city_graf.add_node(node[0], pos=[node[1]['y'], node[1]['x']], tipus='cruilla')

    for edge in g1.edges.data():
        #nomes afegim els carrers per anar caminant ja que per on van els busos ho calculem mitjançant el graf OsmnxGraph
        if edge[2]['highway'] in carrers_caminant: 
            city_graf.add_edge(edge[0], edge[1], dist=edge[2]['length'], tipus='carrer', temps=edge[2]['length']/V_CAMINANT) #podria mirar d'afegir nom al carrer

    #afegim els nodes del graf de buses
    city_graf.add_nodes_from(g2.nodes.data(), tipus='parada') 
        
    #per cada node Parada, creem una aresta que la uneixi amb la cruilla més propera
    distancia = ox.distance.nearest_nodes(g1, [y[1]['pos'][1] for y in g2.nodes.data()], [x[1]['pos'][0] for x in g2.nodes.data()], return_dist=True)
    for x in range(len(distancia[0])):
        city_graf.add_edge(list(g2.nodes)[x], distancia[0][x], dist=distancia[1][x], temps=distancia[1][x]/V_CAMINANT, tipus='cruilla-parada')
    
    #per cada aresta Bus, afegim la aresta al city amb la distancia i el temps per anar de la Parada A a la Parada B
    #com que cada parada nomes te una aresta de tipus cruilla-parada, busquem aquesta Cruilla conectada, la distancia i el temps de l'aresta la calculem com el camí més ràpid de parada a parada per carretera
    distancia = ox.distance.shortest_path(g1, [cruilla_mes_propera(city_graf, edge[0]) for edge in g2.edges.data()], [cruilla_mes_propera(city_graf, edge[1]) for edge in g2.edges.data()], weight='length')
    print(distancia)
    '''
    for x in range(len(ditancia))
        city_graf.add_edge(edge[0], edge[1], tipus='bus', dist=distancia, temps=distancia/V_DEL_BUS)
        '''

    return city_graf

def plot(g: CityGraph, filename: str) -> None: 
    '''Desa g com una imatge amb el mapa de la cuitat de fons en l'arxiu filename'''
    
    mapa = staticmap.StaticMap(600,600)

    #Dibuixem un punt per cada node del graf
    for node in dict(g.nodes).values():
        p = (node['pos'][1], node['pos'][0])
        mapa.add_marker(staticmap.CircleMarker(p, 'red', 1))
    
    #Dibuixem una linia per cada aresta del graf
    for edge in g.edges.data():
        s = g.nodes[edge[0]]['pos'][1], g.nodes[edge[0]]['pos'][0]
        d = g.nodes[edge[1]]['pos'][1], g.nodes[edge[1]]['pos'][0]
        mapa.add_line(staticmap.Line([s, d], 'blue', 1))

    #Guardem la imatge en un fitxer
    imatge = mapa.render()
    imatge.save(filename)

def find_path(ox_g: OsmnxGraph, g: CityGraph, src: Coord, dst: Coord) -> tuple[Path, int]:
    'ojo amb la funcio caca aquesta'
    route = nx.shortest_path(g, cruilla_mes_propera(ox_g, src), cruilla_mes_propera(ox_g, dst), weight='temps')
    print(route)
    '''
    fig, ax = ox.plot_graph_route(g, route, route_linewidth=6, node_size=0, bgcolor='k')
    '''

def show(g: CityGraph) -> None: 
    '''Mostra g de forma interactiva en una finestra'''
    pos = nx.get_node_attributes(g, 'pos')
    nx.draw(g, node_size=0, pos=pos)
    plt.show()
    time.sleep(5)

def plot_path(g: CityGraph, p: Path, filename: str) -> None:
    '''Mostra el camí p en l'arxiu filename falta afegir atributs'''
    mapa = staticmap.StaticMap(600,600)
    
    for punt in p:
        mapa.add_marker(staticmap.CircleMarker(punt, 'red', 1))
    
    for x in range(len(p)-1):
        s = p[x]
        d = p[x+1]
        mapa.add_line(staticmap.Line([s, d], 'blue', 1))
    
    #Guardem la imatge en un fitxer
    imatge = mapa.render()
    imatge.save(filename)

def plot_interactive(filename: str) -> None:
    im = Image.open(filename)
    im.show()

def main():
    graf1= get_osmx_graph()
    print('graf de google maps fet')
    graf2= get_buses_graph()
    print('graf de busos fet')
    g1 = build_city_graph(graf1, graf2)
    print('graf de ciutat fet')
    plot(g1, 'finalcity.jpg')
    # g2 = get_buses_graph()
    # show(g2)
    # g3 = build_city_graph(g1, g2)
    # show(g3)

if __name__=="__main__":
    main()
