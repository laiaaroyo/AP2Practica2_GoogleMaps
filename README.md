# Project Title

One Paragraph of project description goes here

## Índex
1. Billboard
2. Buses
3. City
4. Demo
5. Bibliografia i llibreries

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
   - `address`: Dirección del cinema.

3. `Projection`: Aquesta classe representa una projecció d'una pel·lícula en un cinema i contiene els següents camps:
   - `film`: Objecte de la classe `Film`que representa la pel·lícula projectada.
   - `cinema`: Objete de la classe `Cinema` que representa el cinema on es projecta la pel·lícula.
   - `time`: Tupla que conté l'hora d'inici de la projecció en format (hora,minut).

4. `Billboard`: Aquesta classe representa una cartellera de cine i conté els següents camps.
   - `films`: Llista d'objectes de la classe 'Film', que representa les pel·lícules disponibles a la cartellera.
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


## Descripció del projecte

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisits

What things you need to install the software and how to install them

```
Give examples
```

### Funcionalitats


## Executar els tests

Explain how to run the automated tests for this system



### And coding style tests

Explain what these tests test and why

```
Give an example
```


## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds



## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc


