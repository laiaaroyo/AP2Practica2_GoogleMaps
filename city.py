import networkx as nx
import osmnx as ox
import pickle
import os
from PIL import Image
from buses import *

CityGraph: TypeAlias = nx.Graph
OsmnxGraph: TypeAlias = nx.MultiDiGraph
Path: TypeAlias = list[Coord]

V_CAMINANT: float = 1.5  # m/s
V_DEL_BUS: float = 7.0  # m/s


def get_osmx_graph() -> OsmnxGraph:
    """Retorna un graf de la ciutat de Barcelona amb distancies"""

    g = ox.graph_from_place('Barcelona, Spain', network_type='all') 
    ox.distance.add_edge_lengths(g, precision=3, edges=None)
    return g


def save_osmnx_graph(g: OsmnxGraph, filename: str) -> None:
    """Guarda el graf osmnx g al fitxer filename"""
    fitxer = open(filename, 'wb')
    pickle.dump(g, fitxer)
    fitxer.close()


def load_osmnx_graph(filename: str) -> OsmnxGraph:
    """Retorna el graf osmnx guardat al fitxer filename"""

    assert os.path.exists(filename), 'El fitxer no existeix'
    g = open(filename, 'rb')
    graf = pickle.load(g)
    g.close()

    return graf


def cruilla_mes_propera(g: CityGraph, node: int) -> int:
    """Donada una Parada, retorna la seva Cruilla conectada"""

    for vei in list(g.neighbors(node)):
        if g.nodes[vei]['tipus'] == 'cruilla':
            return vei


def dist_path(g: OsmnxGraph, p: Path) -> int:
    """Donat un camí caminant retorna la distancia en metres"""

    d: float = 0
    for x in range(len(p)-1):
        d += g.edges[(p[x], p[x+1], 0)]['length']
    return d


def time_path(g: CityGraph, p: Path) -> int:
    """Donat un camí retorna el temps que es tarda en recorre'l"""

    t: int = 0
    for x in range(len(p)-1):
        t += g.edges[(p[x], p[x+1])]['temps']
    return t


def build_city_graph(g1: OsmnxGraph, g2: BusesGraph) -> CityGraph:
    """Retorna el graf resultant de la unió del g1 (graf osmns) i g2 (graf de busos)."""

    city_graf = nx.Graph()
    
    # Posem tots els nodes i arestes del graf g1 al nou CityGraph amb les dades que ens interessen amb tipus Cruilla i Carrer
    for node in g1.nodes.data():
        city_graf.add_node(node[0], pos=[node[1]['y'], node[1]['x']], tipus='cruilla')

    for edge in g1.edges.data():
        city_graf.add_edge(edge[0], edge[1], dist=edge[2]['length'], tipus='carrer', temps=edge[2]['length'] // V_CAMINANT)

    # Afegim els nodes del graf g2 (BusesGraph) al nou CityGraph com a tipus Parada
    city_graf.add_nodes_from(g2.nodes.data(), tipus='parada')
        
    # Per cada node Parada, creem una aresta que la uneixi amb la cruilla més propera. Aquesta aresta serà de tipus Cruilla-Parada per diferenciar-la dels Carrers
    distancia = ox.distance.nearest_nodes(g1, [y[1]['pos'][1] for y in g2.nodes.data()], [x[1]['pos'][0] for x in g2.nodes.data()], return_dist=True)
    for x in range(len(distancia[0])):
        city_graf.add_edge(list(g2.nodes)[x], distancia[0][x], dist=distancia[1][x], temps=distancia[1][x]//V_CAMINANT, tipus='cruilla-parada')

    # Per cada aresta al graf g2, creem una nova aresta al CityGraph que tindra com a atribut distància la distància d'anar d'una Parada a una altra pel graf osmnx
    for edge in g2.edges.data():
        path = ox.distance.shortest_path(g1, cruilla_mes_propera(city_graf, edge[0]), cruilla_mes_propera(city_graf, edge[1]), weight='length')
        if path is not None:
            distancia = dist_path(g1, path)
            city_graf.add_edge(edge[0], edge[1], tipus='bus', dist=distancia, temps=distancia//V_DEL_BUS, path=path)
    
    return city_graf


def plot(g: CityGraph, filename: str) -> None: 
    """Desa g com una imatge amb el mapa de la cuitat de fons en l'arxiu filename"""
    
    mapa = staticmap.StaticMap(600, 600)

    # Dibuixem un punt per cada node del graf
    for node in dict(g.nodes).values():
        p = (node['pos'][1], node['pos'][0])
        mapa.add_marker(staticmap.CircleMarker(p, 'red', 1))
    
    # Dibuixem una linia per cada aresta del graf
    for edge in g.edges.data():
        s = g.nodes[edge[0]]['pos'][1], g.nodes[edge[0]]['pos'][0]
        d = g.nodes[edge[1]]['pos'][1], g.nodes[edge[1]]['pos'][0]
        mapa.add_line(staticmap.Line([s, d], 'blue', 1))

    # Guardem la imatge en un fitxer
    imatge = mapa.render()
    imatge.save(filename)


def find_path(ox_g: OsmnxGraph, g: CityGraph, src: Coord, dst: Coord) -> Path:
    """Retorna el camí més curt desde un punt de coordenades src a dst del graf g seegons l'atribut temps"""

    source = ox.nearest_nodes(ox_g, src[1], src[0])
    target = ox.nearest_nodes(ox_g, dst[1], dst[0])
    
    return nx.dijkstra_path(g, source, target, weight='temps')


def show(g: CityGraph) -> None:
    """Mostra g de forma interactiva en una finestra"""

    pos = nx.get_node_attributes(g, 'pos')
    nx.draw(g, node_size=0, pos=pos)
    plt.show()


def plot_path(g: CityGraph, p: Path, filename: str) -> None:
    """Mostra el camí p en l'arxiu filename falta afegir atributs"""
    mapa = staticmap.StaticMap(600,600)

    # Marquem el inici i el destí més grans
    mapa.add_marker(staticmap.CircleMarker(g.nodes[p[0]]['pos'][1], g.nodes[p[0]]['pos'][0], 'red', 4))
    mapa.add_marker(staticmap.CircleMarker(g.nodes[p[-1]]['pos'][1], g.nodes[p[-1]]['pos'][0], 'red', 4))

    # Marquem tots els nodes pels que pasarem
    for punt in p:
        pos = g.nodes[punt]['pos'][1], g.nodes[punt]['pos'][0]
        mapa.add_marker(staticmap.CircleMarker(pos, 'red', 3))
    
    # Marquem totes les arestes per les que pasem
    for x in range(len(p)-1):
        tipus = g.edges[p[x], p[x+1]]['tipus']

        # Els camins caminant els pintem de vermell
        if tipus == 'carrer':
            s = g.nodes[p[x]]['pos'][1], g.nodes[p[x]]['pos'][0]
            d = g.nodes[p[x+1]]['pos'][1], g.nodes[p[x+1]]['pos'][0]
            mapa.add_line(staticmap.Line([s, d], 'red', 2))
        
        # Els camins en bus els pintem de blau
        elif tipus == 'bus':
            p_bus = g.edges[p[x], p[x+1]]['path']
            for y in range(len(p_bus)-1):
                s = g.nodes[p_bus[y]]['pos'][1], g.nodes[p_bus[y]]['pos'][0]
                d = g.nodes[p_bus[y+1]]['pos'][1], g.nodes[p_bus[y+1]]['pos'][0]
                mapa.add_line(staticmap.Line([s, d], 'blue', 2))
            
    # Guardem la imatge en un fitxer
    imatge = mapa.render()
    imatge.save(filename)


def plot_interactive(filename: str) -> None:
    """Donat un archiu, el mostra per pantalla"""

    im = Image.open(filename)
    im.show()
