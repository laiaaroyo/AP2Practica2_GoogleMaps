from dataclasses import dataclass
from datetime import date
from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException
import json
import time
import datetime
import yogi


@dataclass

class Film:
    title: str
    genere: str
    director: str
    actors: list[str]

@dataclass

class Cinema:
    name: str
    address: str

@dataclass

class Projection:
    film: Film
    cinema: Cinema
    time: tuple[int, int]   # hora:minut

@dataclass 

class Billboard:
    films: list[Film]  # pelis disponibles
    cinemas: list[Cinema]  # sales de cine disponible
    projections: list[Projection]  # pelicules en la seva corresponent sala, 
                                    #juntament amb la seva hora de projecció.
    
    def cerca_peli_per_nom(self, keyword:str) -> list[Projection]: 
        """Donat un nom d'una pel·lícula ens retorna una llista de 
        projeccions amb els cinemes que ens mostren la pel·lícula,
        els horaris,.... Si no hi ha cap cerca que coincideixi en cap
        cine retorna una llista buida"""
       
        return [projection for projection in self.projections
                if keyword in projection.film.title]

    def cerca_peli_per_genere(self, genere:str) -> list[Projection]: 
        """Seleccionem les pel·lícules del gènere que ens interessa. Retornem una llista de projeccions"""
        
        return [projection for projection in self.projections
                if genere in projection.film.genere]


    def cerca_peli_per_director(self, director:str) -> list[Projection]:
        """Seleccionem les pel·lícules del director que ens interessa. Retornem una llista de projeccions"""
        
        return [projection for projection in self.projections
                if director in projection.film.director]
    
    def cerca_peli_per_actor(self, actor:str) -> list[Projection]:
        """Donat un actor seleccionem totes les pel·lícules que continguin aquest actor. Retornem una llista
        de projeccions."""

        return [projection for projection in self.projections
                 if actor in projection.film.actors]


def read() -> Billboard | None:

    urls = ['https://www.sensacine.com/cines/cines-en-72480/?page=1',
            'https://www.sensacine.com/cines/cines-en-72480/?page=2',
            'https://www.sensacine.com/cines/cines-en-72480/?page=3']
    
    films : dict[str, Film] = dict()
    cinemes : dict[str, Cinema] = dict()
    projections: list[Projection] = []

    for url in urls:
        while True:
            try:
                response = requests.get(url)
                break
            
            except RequestException:
                print("Hi ha hagut un error:", str(RequestException))
                print("Tornant a intentar en 5 segons...")
                # Esperem 5 segons abans de tornar a provar la petició.
                time.sleep(5)  
        if response:
            contingut = BeautifulSoup(response.content, 'html.parser')
            films = read_list_films(contingut, films)
            cinemes = read_list_cinemas(contingut, cinemes)
            projections = read_list_projections(contingut, cinemes, films, projections)

            return Billboard(list(films.values()), list(cinemes.values()), projections)


def read_list_cinemas(contingut:BeautifulSoup, cinemes:dict[str, Cinema]) -> dict[str, Cinema]: 
    """Llegim totes les sales de cinema que hi ha a Barcelona i fem un diccionari, 
    associant cada cinema amb la seva direcció."""
 
    # llegim tots els cinemes
    sales_cinema : list[str] = []
    sales = contingut.find_all('a', class_='no_underline j_entities')
    for sala in sales:
        sales_cinema.append(sala.text.replace('\n', '').strip()) 
        
    
    # llegim totes les adresses dels cinemes
    adresses = contingut.select('span.lighten:not(.fr.fs11.lighten)')
    idx = 0
    for direccio in adresses:
        cinemes[sales_cinema[idx]] = Cinema(sales_cinema[idx], direccio.text.strip("\n"))
        idx +=1

    return cinemes

    
def read_list_films(contingut:BeautifulSoup, films:dict[str,Film]) -> dict[str,Film]:
    """Llegim totes les pel·lícules disponibles del dia actual, i fem un diccionari, associant
    el nom de cada pel·lícula amb les característiques principals de la pel·lícula."""

    # Seleccionem només les pel·lícules del dia actual
    dia_actual = contingut.find_all('div', class_ = 'tabs_box_pan item-0')
    
    for pelicula_actual in dia_actual:
        data = pelicula_actual.find_all('div', class_='item_resa')
        for entry in data: 
            divs_w = entry.find_all('div', class_ = 'j_w') 
            data_movie = divs_w[0]['data-movie']
            data_movie = json.loads(data_movie)  # convertim en un diccionari
            title = data_movie['title']
            directors = data_movie['directors']
            actors = data_movie['actors']
            genre = data_movie['genre']

            new_film = Film(title, genre, directors, actors)

            # Ens assegurem de no tenir pel·lícules repetides.   
            if new_film not in films.values():
                films[title] = new_film

    return films

            
def read_list_projections(contingut: BeautifulSoup, cinemes:dict[str,Cinema], films:dict[str,Film], projections:list[Projection]) -> list[Projection]:
    """Llegim les hores en què podem visualitzar cada pel·lícula i retornem una llista de projeccions,
    on cada projecció consisteix en la pel·lícula, el cinema en la que la podem veure i l'hora."""

    # Seleccionem només les pel·lícules que estiguin programades per projectar-se el dia actual.
    cines = contingut.find_all('div',class_= 'tabs_box_pan item-0')

    for cine in cines:
        for projeccio in cine:
            div_entry = projeccio.find('div', class_ = 'j_w')
            
            data_movie = div_entry['data-movie']
            data_movie_json = json.loads(data_movie)
            title = data_movie_json['title']
        

            # Seleccionem la pel·lícula segons el títol recuperat
            pelicula_actual = films[title]
                
                
            # Seleccionem el cinema on es pot veure la pel·lícula en funció del nom recuperat
            data_theater = div_entry['data-theater']
            data_theater = json.loads(data_theater)
            name = data_theater['name'].strip()
            cinema_actual = Cinema(name, cinemes[name].address)
        
            # busquem els horaris disponibles per la pel·lícula
            u_items = projeccio.find_all('ul', class_='list_hours')

            for u_item in u_items:
                em_tags = u_item.find_all('em')
    
                # Iterem sobre els horaris extrets
                for em_tag in em_tags:
                    
                    # convertim la cadena en una llista i agafem l'hora d'inici.
                    data_times = em_tag['data-times']
                    data_times = json.loads(data_times)
                    hora_inici = data_times[0]
                    hora, minuts = hora_inici.split(":")
                    time = (int(hora), int(minuts))
   
                    projections.append(Projection(pelicula_actual, cinema_actual,time))
            
    
    return projections










    
 
