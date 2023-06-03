import time
import geocoder
import requests
from bs4 import BeautifulSoup
import geocoder
import networkx as nx

from billboard import *
from buses import *


class Demo: # sistema de menús per cercar pel·lícules i indicar el camí per arribar-hi.
    def __init__(self):
        self.billboard = None
        self.graf_busos = None
        self.graf_city = None

    def mostrar_autors(self) -> None:
        """Funció que imprimeix els autors del projecte."""
        print("Autors del projecte:")
        print(" Laia Royo Rion")
        print(" Clàudia Ibañez Massa")

    def crear_cartellera(self) -> None:
        """Mètode per crear la cartellera de Barcelona. Si s'ha creat amb èxit ho imprimim per pantalla """
        self.billboard = read()
        # Codi per crear la cartellera
        print("La cartellera s'ha creat amb èxit!")

    def mostrar_cartellera(self) -> None:
        """Mètode per mostrar el contingut de la cartellera (nom pel·lícula, gènere, director i actors). 
        Si abans no s'ha creat la cartellera l'hem de crear prèviament."""
        
        if not self.billboard:
            self.crear_cartellera()
        else:
            print("----- Cartellera -----")
            for film in self.billboard.films:
                print("Title:", film.title)
                print("Genere:", ", ".join(film.genere))
                print("Director:", ", ".join(film.director))
                print("Actors:", ", ".join(film.actors))
                print("----------------------")

    def cercar_cartellera(self) -> list[Projection] | None:
        """Mètode per cercar a la cartellera a través d'un sistema de menús que et permet
        triar quina cerca vols fer. Retorna una llista de projeccions, i si la cerca no es troba a la cartellera
        no retorna res."""

        if self.billboard:
    
            print("3.1 Cerca per nom de pel·lícula")
            print("3.2 Cerca per gènere")
            print("3.3 Cerca per director")
            print("3.4 Cerca per actors")
            

            opcio  = input("Selecciona una opció: ")
            if opcio == "3.1":
                projeccions = self.cercar_cartellera_per_nom()
                resposta = input("Vols que et mostri el camí? ")
                if resposta == "Si":
                    if projeccions:
                        self.mostrar_camí_pel·lícula(projeccions)
  
            elif opcio == "3.2":
                projeccions = self.cercar_cartellera_per_genere()
                resposta= input("Vols que et mostri el camí? " )
                if resposta == "Si":
                    if projeccions:
                        self.mostrar_camí_pel·lícula(projeccions)
            
            elif opcio == "3.3":
                projeccions = self.cercar_cartellera_per_directors()
                resposta = input("Vols que et mostri el camí? ")
                if resposta == "Si":
                    if projeccions:
                        self.mostrar_camí_pel·lícula(projeccions)
            
            elif opcio == "3.4":
                projeccions = self.cercar_cartellera_per_actors()
                resposta = input("Vols que et mostri el camí? ")
                if resposta == "Si":
                    if projeccions:
                        self.mostrar_camí_pel·lícula(projeccions)
            
            else:
                print("Opció invàlida!")

        else:
            print("La cartellera encara no s'ha creat.")

    def cercar_cartellera_per_nom(self) -> list[Projection] | None:
        """Mètode per cercar totes les projeccions d'una pel·lícula específica. Sol·licita a l'usuari que introdueixi
        el títol de la pel·lícula i si troba projeccions, imprimeix la informació de cada una, i retorna la llista 
        de projeccions ordenades per hora d'inici. 
        Si no troba projeccions imprimeix un missatge indicant que no s'ha trobat cap pel·lícula."""
        
        if self.billboard:
            print("Introdueix el títol de la pel·lícula que vols cercar: ",end="")
            nom = yogi.read(str)
            projeccions = self.billboard.cerca_peli_per_nom(nom)
            if len(projeccions) > 0:
                print("Resultats de la cerca:")
                for projection in projeccions:
                    print("Títol:", projection.film.title)
                    print("Cinema:", projection.cinema.name)
                    print("Direcció:", projection.cinema.address)
                    print("Hora:", projection.time[0],":",projection.time[1])
                    print("----------------------")
                return sorted(projeccions, key = lambda x: (x.time[0],x.time[1]))

            else:
                print("No s'ha trobat cap pel·lícula que coincideixi amb la cerca.")
            

    def cercar_cartellera_per_genere(self) -> list[Projection] | None:
        """Realitza una búsqueda a la cartellera per gènere de pel·lícula. Retorna una llista de projeccions
        ordenades per hora d'inci."""
        
        if self.billboard:
            genere = input("Introdueix el gènere de la pel·lícula que t'interessa cercar: ")
            projeccions = self.billboard.cerca_peli_per_genere(genere)
            if projeccions:
                print("Resultats de la cerca:")
                for projection in projeccions:
                    print("Títol:", projection.film.title)
                    print("Cinema:", projection.cinema.name)
                    print("Direcció:", projection.cinema.address)
                    print("Hora:", projection.time[0],":",projection.time[1])
                    print("----------------------")
                return sorted(projeccions, key = lambda x: (x.time[0], x.time[1]))
                

            else:
                print("No s'ha trobat cap pel·lícula")

    def cercar_cartellera_per_directors(self) -> list[Projection] | None:
        """Realitza una cerca a la cartellera per director de la pel·lícula. Retorna una llista de projeccions
        ordenades per hora d'inici."""
        
        if self.billboard:
            director = input("Introdueix el nom i cognom del director que vols cercar: ")
            projeccions = self.billboard.cerca_peli_per_director(director)
            if len(projeccions) > 0:
                print("Resultats de la cerca:")
                for projection in projeccions:
                    print("Títol:", projection.film.title)
                    print("Cinema:", projection.cinema.name)
                    print("Direcció:", projection.cinema.address)
                    print("Hora:", projection.time[0],":",projection.time[1])
                    print("----------------------")
                return sorted(projeccions, key = lambda x: (x.time[0], x.time[1]))
            else:
                print("No s'ha trobat cap pel·lícula")

    def cercar_cartellera_per_actors(self) -> list[Projection] | None:
        """Realitza una cerca a la cartellera per actor de la pel·lícula. Retorna una llista 
        de projeccions ordenades per hora d'inici."""
        if self.billboard:
            actor = input("Introdueix l'actor que vols cercar: ")
            projeccions = self.billboard.cerca_peli_per_actor(actor)
            if len(projeccions) > 0:
                print("Resultats de la cerca:")
                for projection in projeccions:
                    print("Títol:", projection.film.title)
                    print("Cinema:", projection.cinema.name)
                    print("Direcció:", projection.cinema.address)
                    print("Hora:", projection.time[0],":",projection.time[1])
                    print("----------------------")
                return sorted(projeccions,key = lambda x: (x.time[0], x.time[1]))
            else:
                print("No s'ha trobat cap pel·lícula")

    def crear_graf_busos(self) -> None:
        """Utilitza el mòdul buses per crear el graf de busos i desar-lo en una imatge en format .jpg. """
       
        self.graf_busos = get_buses_graph() 
        plot(self.graf_busos, "graf_busos.jpg")
        print("El graf de busos s'ha creat amb èxit!")

    def mostrar_graf_busos(self) -> None:
        """Un cop creat el graf de busos (si no està creat el crea abans) mostra una
        imatge del graf de busos inserit a la ciutat."""
        
        print("----- Graf de Busos -----")

        if self.graf_busos is None:
            self.crear_graf_busos()
        
        plot_interactive()

        
        print("--------------------------")

    def crear_graf_ciutat(self) -> None:
        """Crea el graf de la ciutat."""
        g1 = get_osmx_graph()
        print("El graf de l'OpenStreetMaps s'ha creat correctament!")
        
        if self.graf_busos is None:
            self.crear_graf_busos()
        g2 = self.graf_busos()
        
       
        self.graf_city = build_city_graph(g1, g2)
        print("El graf de la ciutat s'ha creat amb èxit!")
        show(self.graf_city)

    def mostrar_graf_ciutat(self) -> None:
        # Codi per mostrar el graf de la ciutat
        print("----- Graf de la Ciutat -----")
        
        if self.graf_city is None:
            self.crear_graf_ciutat()

        plot(self.graf_city, 'finalcity.jpg')


        print("-----------------------------")

    def obtenir_coordenades(self,direccio:str) -> tuple[int,int] | None:
        """Donada una direcció retorna les coordenades de l'adreça, retorna una tupla
        amb la latitud i la longitud."""

        url = f"https://nominatim.openstreetmap.org/search?q={direccio}&format=json"
        intents = 0
        
        while intents < 3:
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                
                if data:
                    latitud = data[0]['lat']
                    longitud = data[0]['lon']
                    return (latitud, longitud)
            
            print("No s'ha trobat la direcció. Tornant a intentar en 3 segons...")
            intents +=1
            time.sleep(3)


    def mostrar_camí_pel·lícula(self, projeccions: list[Projection]) :
       

        lloc = input("Introdueix el lloc actual: ")
        
        temps_a_arribar = 0
        hora_actual = datetime.datetime.now().time()
        
        idx = 0
        
        hora_que_arribem = self.sumar_hores(hora_actual,temps_a_arribar)
        # Passem a minuts l'hora en què comença la pel·lícula.
        hora_projeccio = projeccions[idx].time[0] * 60 + projeccions[idx].time[1]
        
        while hora_que_arribem > hora_projeccio:
            idx+=1
            hora_que_arribem = self.sumar_hores(hora_actual,temps_a_arribar)
            hora_projeccio = projeccions[idx].time[0] * 60 + projeccions[idx].time[1]
        
        
    
        direccio = projeccions[idx].cinema.address
        if "Calle" in direccio:
            direccio = direccio.replace("Calle", "")
        
        # Convertim l'adreça a coordenades
        resultat = self.obtenir_coordenades(direccio)
        if resultat is not None:
            latitud,longitud = resultat
        
        if hora_projeccio - hora_que_arribem <= 5:
            print("Alerta! Afanya't o sino no et donarà temps a comprar palomitas!")

        # Codi per obtenir el camí per anar a veure la pel·lícula desitjada
        print("Camí per anar a veure la pel·lícula:")
        print(f"1. {lloc} -> Parada d'autobús -> Cinemes")
        print(f"2. {lloc} -> Peatonal -> Cinemes")

    
    def sumar_hores(self,hora_actual:datetime.datetime, temps_a_arribar:int):

        # Seleccionem només les hores i els minuts d'hora actual i ho passem a minuts
        #Sumem el temps que tardem a arribar fins al cinema

        hores = hora_actual.hour
        minuts = hora_actual.minute
        total_minuts = hores * 60 + minuts

        return (total_minuts + temps_a_arribar)


    # Funció per mostrar el menú principal
    def mostrar_menu(self) -> None:
        """Mostra el menú amb totes les opcions que pot sol·licitar l'usuari."""
        print("----- Mòdul Demo -----")
        print("1. Mostrar autors")
        print("2. Mostrar cartellera")
        print("3. Cercar a la cartellera")
        print("4. Mostrar graf de busos")
        print("5. Mostrar graf de ciutat")
        print("0. Sortir")

    def executar(self) -> None:
        """Executa el programa principal del sistema de gestió de la cartellera. Mostra un menú d'opcions
        i demana a l'usuari que seleccioni una opció. Depenent de l'opció seleccionada, es crida una funció o una altra.
        El bucle es repeteix fins que l'usuari selecciona l'opció `0` per sortir del programa. """
        
        opcio = None 
        cartellera = read()
        if cartellera:
            while opcio != "0":
                self.mostrar_menu()
                opcio = input("Selecciona una opció: ")
                if opcio == "1":
                    print()
                    self.mostrar_autors()
                elif opcio == "2":
                    print()
                    self.mostrar_cartellera()
                elif opcio == "3":
                    print()
                    self.crear_cartellera()
                    self.cercar_cartellera()
                elif opcio == "4":
                    self.mostrar_graf_busos()
                elif opcio == "5":
                    self.mostrar_graf_ciutat()

                elif opcio == "0":
                    print()
                    print("Gràcies per utilitzar els nostres serveis ! Àdeu ! Fins una altra!")
                else:
                    print("Opció invàlida. Selecciona una opció vàlida inserint un número.")
                print()

def main():
    demo = Demo()
    demo.executar()


if __name__=="__main__":
    main()
    
   

    


            

