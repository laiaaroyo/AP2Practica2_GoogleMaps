# Cinebus!

El projecte gira al voltant d'una cartellera de la ciutat de Barcelona, que mostra una gran varietat de pel·lícules i tota la informació relativa a la projecció d'aquella pel·lícula. Tria una pel·lícula, i et mostrem un mapa interactiu que t'indicarà el recorregut de la primera pel·lícula que es projectarà. T'ensenyem com arribar-hi amb bus i a peu!

## Índex
1. Billboard
2. Buses
3. City
4. Demo


# 1. Billboard
Conjunt de classes i funcions per llegir informació de la cartellera de Barcelona desde la pàgina web "https://www.sensacine.com".

## Requisits

- Python 3.8 o superior
- Paquets necessaris: `dataclasses`, `bs4` (BeautifulSoup), `requests`, `json`, `time`

## Estructura del codi

El codi es divideix en vàries seccions: classes de dades i llegir la informació de la cartellera.

### Classes de dades

1. `Film`: Aquesta classe representa una pel·lícula i conté els següents camps: 
   - `title`: Títol de la pel·lícula.
   - `genre`: Gènere de la pel·lícula.
   - `director`: Director de la pel·lícula.
   - `actors`: Llista d'actors de la pel·lícula.

2. `Cinema`: Aquesta classe representa un cinema i conté els següents camps.
   - `name`: Nom del cinema.
   - `address`: Direcció del cinema.

3. `Projection`: Aquesta classe representa una projecció d'una pel·lícula en un cinema i conté els següents camps:
   - `film`: Objecte de la classe `Film`que representa la pel·lícula projectada.
   - `cinema`: Objete de la classe `Cinema` que representa el cinema on es projecta la pel·lícula.
   - `time`: Tupla que conté l'hora d'inici de la projecció en format (hora,minut).

4. `Billboard`: Aquesta classe representa una cartellera de cine i conté els següents camps.
   - `films`: Llista d'objectes de la classe `Film`, que representa les pel·lícules disponibles a la cartellera.
   - `cinemas`: Llista d'objectes de la classe `Cinema`, que representen els cines disponibles a la cartellera.
   - `projections`: Llista d'objectes de la classe `Projection`, que representen les projeccions de pel·lícules en els cinemes.

   A més a més, la classe `Billboard` proporciona mètodes per buscar pel·lícules segons diferents criteris, com el nom, el gènere, el director o l'actor. 

### Funcions

1. `read`: Aquesta funció és el punt d'entrada principal del programa. Fa la lectura de la cartellera des de la pàgina web "https://www.sensacine.com" i retorna un objecte de la classe `Billboard` amb l'informació obtinguda.

2. `read_list_cinemas`: Aquesta funció llegeix la llista de cinemes disponibles a Barcelona i retorna un diccionari que associa cada cinema amb la seva direcció. 

3. `read_list_films`: Aquesta funció llegeix la llista de pel·lícules disponibles a la cartellera del dia actual des de la pàgina web i retorna un diccionari que associa cada pel·lícula amb les seves característiques principals (títol, gènere, director i actors).

4. `read_list_projections`: Aquesta funció llegeix la llista de projeccions de pel·lícules en els cinemes des de la pàgina web i retorna una llista d'objectes de la classe `Projection`.

### Ús del codi

Per utlitzar el codi, només s'ha de cridar a la funció `read`, que retornarà un objecte de la classe`Billboard`.

```python
billboard = read()
```

Aleshores, es poden realitzar cerques a la cartellera utilitzant els mètodes proporcionats per la classe `Billboard`, com `cerca_peli_per_nom`, `cerca_peli_per_genere`, `cerca_peli_per_director` i `cerca_peli_per_actor`. Aquests mètodeds retornaran llistes de projeccions que coincideixin amb els criteris de cerca especificats.

```python
projections_by_title = billboard.cerca_peli_per_nom("Avengers")
projections_by_genre = billboard.cerca_peli_per_genere("Comedy")
projections_by_director = billboard.cerca_peli_per_director("Christopher Nolan")
projections_by_actor = billboard.cerca_peli_per_actor("Tom Hanks")
```

El codi realitza sol·licituds HTTP a la pàgina web Sensacine.com  per obtenir la informació de la cartellera. Per tant és possible que es produeixin errors de connexió durant l'execució. En cas d'error, el codi tornarà a intenta a demanar la sol·licitud després de 5 segons d'espera.

# 2. Buses
Aquest programa utilitza les dades de l'Àrea Metropolitana de Barcelona per crear un graf representant les parades del bus i les seves connexions. Permet als usuaris calcular la duració del trajecte entre diferents parades i visualitzar les connexions dels busos en un mapa.

## Requisits
- Networkx
- Matplotlib.pyplot
- Staticmap
- json
- numpy
- pandas
- request

## Estructura del codi
L'estructura del codi es divideix en: llegir les dades per a partir de la pàgina web d'AMB i crear el graf dels busos a partir d'aquelles que més ens interessen. I també en crear funcions que ens mostrin el resultat.

### Classe BusesGraph
Àlies per un graf Networkx que representa la xarxa de busos. I on els nodes representen les Parades i les arestes els trajectes entre parades que fan els busos.

### Classe Coord
Àlies per una tupla de dos valors que representen les coordenades (latitud i longitud).

### Funcions

- `distance()` : retorna la distància entre dos coordenades, utilitzant la fórmula de Haversine.
- `get_buses_graph()`: extreu les dades del bus amb la informació sobre els nodes i l'aresta, i retorna el graf que representa la xarxa de busos utilitzant Networkx.
- `show()`: dibuixa el graf i ens el mostra en una altra finestra mitjançant Matplotlib, mostrant-nos les parades de bus com a nodes, i les conexions com a arestes.
- `plot()`: desa com a fitxer amb el nom indicat una imatge del mapa de la ciutat de Barcelona amb la xarxa d'autobusos (és a dir el graf) en les coordenades corresponenets mitjançant StaticMaps.

### Ús del programa
Per executar el codi, només s'han de cridar a les funcions (prèviament ja hem hagut d'instalar totes les llibreries necessàries):
```python
buses_graph = get_buses_graph()
show(buses_graph)
plot(buses_graph, 'bus_network.png')
```

S'ha de tenir en compte que el planificador de rutes d'autobús es basa en les dades facilitades per l'AMB (Àrea Metropolitana de Barcelona).




# City
Aquest mòdul implementa un sistema de navegació de la ciutat mitjançant xarxes de grafs. Combina dades des de la llibreria OSMnx i el graf de busos per representar el graf complet de la ciutat. Els usuaris poden trobar el camí més curt entre dues ubicacions de la ciutat i visualitzar el graf de la ciutat amb el camí. 

## Prerequisits
Paquets necessaris: `networkx`, `osmnx`, `pickle`, `os`, `buses`.

## Funcionalitat

`get_osmx_graph()`
Retorna un graf de la ciutat de Barcelona amb distàncies utilitzant la llibreria OSMnx. Especifica la ubicació (Barcelona,Espanya) i el tipus de xarxa (totes).

`save_osmnx_graph(filename:str) -> OsmnxGraph`
Retorna el graf guardat al fitxer filename. LLegeix les dades del graf amb el mòdul pickle i retorna el graf carregat.

`cruilla_mes_propera(g: OsmnxGraph, node: int) -> int | None`
Donat un node (representada pel seu identificador), retorna el node veí més proper de tipus 'cruïlla'. Itera sobre els nodes adjacents de l'aresta i comprova el seu tipus per trobar el node cruilla més proper. Si no es troba cap node retorna None.

`build_city_graph(g1: OsmnxGraph, g2: BusesGraph) -> CityGraph`
Retorna un graf de la ciutat combinat el graf OSMnx i el graf de busos. Crea un `CityGraph`buit i afegeix nodes i arestes a partir de les dades de g1 i g2. Els nodes de g1 s'afegeixen com a nodes "cruïlla" i les arestes de g1 s'afegeixen com a arestes de "carrer". A més, per cada node 'parada' es crea una aresta per connectar-lo amb el node 'cruilla' més proper. Finalment calcula les distàncies del camí més curt entre els nodes cruilla i els nodes parada mitjançant la funció `ox.shortest_path()`.

`plot(g: CityGraph, filename: str) -> None`
Desa g com una imatge amb el mapa de la cuitat de fons en l'arxiu filename utilitzant la biblioteca `staticmap`

`find_path (ox_g: OsmnxGraph, g: CityGraph, src: Coord, dst: Coord) -> tuple[Path, int]`
Troba el camí més curt entre dues coordenades 'src' i 'dst' del graf de la ciutat g. La funció retorna una tupla que conté el camí com una llista de coordenades i el temps total necessari per recórrer el camí.
Troba la parada d'inici més a prop i la parada de destinació més a prop i calcula el camí més curt del graf entre aquests dos punts.

`show(g: CityGraph) -> None`
Mostra g de forma interactiva en una finestra.

`plot_path(g: CityGraph, p: Path, filename: str) -> None`
Donat el graf de la ciutat 'g', i un camí 'p' (llista de coordenades) i el nom d'un fitxer genera una imatge del graf de la ciutat amb el camí corresponent i el guarda en el fitxer especificat.

`plot_interactive(filename: str) -> None`
Mostra la imatge especificada per el nom del fitxer en una finestra interactiva.

Després tenim també dues funcions que ens ajuden a calcular la distància d'un camí `time_path()`, o el temps que tardem en recorre'l `time_path()`

## Personalització
- Ciutat: el projecte està configurat per utilitzar Barcelona com a ciutat. Podeu especificar la ciutat desitjada en el cas que disposeu d'un `BusesGraph` amb les mateixes característiques de la ciutat escollida.
- Velocitats: la velocitat caminant (`V_CAMINANT`) i la velocitat de l'autobús (`V_DEL_BUS`) es poden ajustar segons el que creieu.

## Ús

```python
    graf1= get_osmx_graph()
    graf2= get_buses_graph()
    
    g_ciutat = build_city_graph(graf1, graf2)
    
    plot(g_ciutat, 'finalcity.jpg')
    
    src: Coord = input('Desde on vols sortir?')
    dst: Coord = input('On vols arribar?')
    path = find_path(graf1, g_ciutat, src, dst)
    
    plot_path(g_ciutat, path, 'cami.jpg')
```
# Demo

Aquest codi representa representa una aplicació de cartellera de pel·lícules. El codi permet als usuaris crear i gestionar una cartellera de pel·lícules, cercar pel·lícules i trobar rutes per arribar a les sales de cinema. 

## Prerequisits
- Python 3.x
- Paquets necessaris: `time`, `geocoder`, `requests`, `billboard`

## Funcionalitat

### Class `Demo`
- La classe `Demo` representa la principal funcionalitat de l'aplicació de la cartellera.
- Contè mètodes per gestionar la cartellera de pel·lícules, cercar pel·lícules i crear grafs per als autobusos i la ciutat i mostrar menús.
- El mètode `executar` és el punt principal del programa i executa el bucle del menú principal.

### Gestionar la cartellera
- `crear_cartellera`: Crea una cartellera tot cridant la funció `read` del modul `billboard`.
- `mostrar_cartellera`: Ensenya el contingut de la cartellera, mostrant els títols de les pel·lícules, gèneres, directors i actors.

### Buscar a la cartellera de pel·lícules 
- `cercar_cartellera`: Demana a l'usuari que seleccioni una opció de cerca i crida als mètodes de cerca corresponents en funció de la selecció.
- `cercar_cartellera_per_nom`: Cerca pel·lícules per títol i mostra els resultats.
- `cercar_cartellera_per_genere`: Cerca pel·lícules per gènere i mostra els resultats.
- `cercar_cartellera_per_directors`: Cerca pel·lícules per director i mostra els resultats.
- `cercar_cartellera_per_actors`: Cerca pel·lícules per actor i mostra els resultats.

### Crear i ensenyar els grafs
- `crear_graf_busos`: Crea el graf de busos.
- `mostrar_graf_busos`: Ensenya el graf de busos.
- `crear_graf_ciutat`: Crea el graf de la ciutat.
- `mostrar_graf_ciutat`: Ensenya el graf de la ciutat.

### Buscar la ruta fins al cinema
- `mostrar_camí_pel·lícula`: Demana a l'usuari que introdueixi la ubicació i l'hora actuals i, a continuació, troba la ruta a la pel·lícula desitjada en funció de l'horari de la pel·lícula.

## Ús
Assegurar-te de tenir totes les llibreries i paquets instal·lats i seguir les opcions de menú que es mostren per interactuar amb l'aplicació.


## Autores

* Clàudia Ibañez
*  Laia Royo





