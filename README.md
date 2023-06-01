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
- Paquets necessaris: `dataclasses`, `bs4` (BeautifulSoup), `requests`, `yogi`

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

   A més a més, la classe `Billboard' proporciona mètodes per buscar pel·lícules segons diferents criteris, com el nom, el gènere, el director o l'actor. 

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

# Buses
Aquest programa utilitza les dades de l'Àrea Metropolitana de Barcelona per crear un graf representant les parades del bus i les seves connexions. Permet als usuaris calcular la duració del trajecte entre diferents parades i visualitzar les connexions dels busos en un mapa.
## Prerequisits
- Networkx
- Matplotlib.pyplot
- Staticmap
- json
- numpy
- pandas
- request

## Funcionalitat
L'estructura del codi es divideix en: classes de dades,i en llegir les dades per a partir de les dades crear el graf dels busos.
### Classe BusesGraph
Àlies per un graf Networkx que representa la xarxa de busos.
### Classe Coord
Àlies per una tupla de dos valors que representen les coordenades (latitud i longitud).
### Classe `Parada`

Aquesta classe representa una parada i conté els camps següents:
- `nom`: el nom de la parada d'autobús.
- `linies`: una llista de línies de busos que passen per la parada d'autobús.
- `pos`: les coordenades de la parada d'autobús (latitud i longitud).

També proveeix mètodes per afegir línies de bus a la parada.

### Classe `Bus`

Aquesta classe representa totes les característiques de l'autobús i conté els camps següents:
- `v_by_bus`: la velocitat de l'autobús en quilòmetres per hora, que en aquest cas hem suposat, que va a 15 km/h.
- `dist`: la distància entre parada i parada.
- `t_espera`: el temps d'espera a les parades abans de que arribi l'autobús, suposem que és 0.
- `duration`: la duració del trajecte d'autobús.

També proveeix mètodes per calcular la duració del trajecte de bus.


### Funcions

`distance` : retorna la distància entre dos coordenades, utilitzant la fórmula de la distància euclidiana.
`get_buses_graph()`: extreu les dades del bus amb la informació sobre els nodes i l'aresta, i retorna la xarxa de busos utilitzant Networkx.
`show`: dibuixa el graf i ens el mostra en una altra finestra mitjançant Matplotlib, mostrant-nos les parades de bus com a nodes, i les connexions com a arestes.
`plot`: desa una imatge del mapa de la ciutat de Barcelona amb amb la xarxa d'autobusos mitjançant StaticMaps.

### Ús del programa
Per executar el codi, només s'han de cridar a les funcions (prèviament ja hem hagut d'instalar totes les llibreries necessàries):
```python
buses_graph = get_buses_graph()
show(buses_graph)
plot(buses_graph, 'bus_network.png')
```

S'ha de tenir en compte que el planificador de rutes d'autobús es basa en les dades facilitades per l'AMB (Àrea Metropolitana de Barcelona).




### C



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





