import time
import requests
from bilboard import *
from buses import *
from city import *
import datetime


class Demo: # Sistema de menús per cercar pel·lícules i indicar el camí per arribar-hi.

    def __init__(self):
        self.billboard = None
        self.graf_busos = None
        self.plot_graf_busos = None
        self.g_maps = None
        self.graf_city = None
        self.plot_graf_city = None


    def mostrar_autors(self) -> None:
        """Funció que imprimeix els autors del projecte."""
        print('Autors del projecte:')
        print(' Laia Royo Rion')
        print(' Clàudia Ibañez Massa')


    def crear_cartellera(self) -> None:
        """Mètode per crear la cartellera de Barcelona. Si s'ha creat amb èxit ho imprimim per pantalla"""
        self.billboard = read()


    def mostrar_cartellera(self) -> None:
        """Mètode per mostrar el contingut de la cartellera (nom de la pel·lícula, gènere, director i actors). 
        Si abans no s'ha creat la cartellera l'hem de crear prèviament"""
        
        if not self.billboard:
            self.crear_cartellera()
        
        print("----- Cartellera -----")
        for film in self.billboard.films:
            print("Title:", film.title)
            print("Genere:", ", ".join(film.genre))
            print("Director:", ", ".join(film.director))
            print("Actors:", ", ".join(film.actors))
            print("----------------------")


    def cercar_cartellera(self) -> list[Projection] | None:
        """Mètode per cercar a la cartellera a través d'un sistema de menús que et permet
        triar quina cerca vols fer. Retorna una llista de projeccions, i si la cerca no es troba a la cartellera
        no retorna res."""

        if not self.billboard:
            self.crear_cartellera()
    
        print("3.1 Cerca per nom de pel·lícula")
        print("3.2 Cerca per gènere")
        print("3.3 Cerca per director")            
        print("3.4 Cerca per actors")

        opcio  = input("Selecciona una opció: ")
        if opcio == "3.1":
            projeccions = self.cercar_cartellera_per_nom()
  
        elif opcio == "3.2":
            projeccions = self.cercar_cartellera_per_genere()
            
        elif opcio == "3.3":
            projeccions = self.cercar_cartellera_per_directors()
            
        elif opcio == "3.4":
            projeccions = self.cercar_cartellera_per_actors()

        if projeccions:   
            resposta = input("Vols que et mostri el camí? ")
            if resposta.lower() == "si":
                self.mostrar_camí_pel·lícula(projeccions)
            
        else:
            print("Opció invàlida!")


    def cercar_cartellera_per_nom(self) -> list[Projection] | None:
        """Mètode per cercar totes les projeccions d'una pel·lícula específica. Sol·licita a l'usuari que introdueixi
        el títol de la pel·lícula i si troba projeccions, imprimeix la informació de cada una, i retorna la llista 
        de projeccions ordenades per hora d'inici. 
        Si no troba projeccions imprimeix un missatge indicant que no s'ha trobat cap pel·lícula."""
        
        if self.billboard:
            nom = input("Introdueix el títol de la pel·lícula que vols cercar: ")
            projeccions = self.billboard.cerca_peli_per_nom(nom)
            
            if projeccions:
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
        plot(self.graf_busos, 'graf_busos.jpg')
        self.plot_graf_busos = 'graf_busos.jpg'
        print("El graf de busos s'ha creat amb èxit!")


    def mostrar_graf_busos(self) -> None:
        """Un cop creat el graf de busos (si no està creat el crea abans) mostra una imatge del graf de busos inserit a la ciutat."""

        if not self.graf_busos:
            self.crear_graf_busos()
        
        plot_interactive(self.plot_graf_busos)


    def crear_graf_ciutat(self) -> None:
        """Crea el graf de la ciutat."""
        self.g_maps = get_osmx_graph()
        print("El graf de l'OpenStreetMaps s'ha creat correctament!")
        
        if self.graf_busos is None:
            self.crear_graf_busos()
       
        self.graf_city = build_city_graph(self.g_maps, self.graf_busos)
        plot(self.graf_city, 'finalcity.jpg')
        self.plot_graf_city = 'finalcity.jpg'

        print("El graf de la ciutat s'ha creat amb èxit!")


    def mostrar_graf_ciutat(self) -> None:
        """Codi per mostrar el graf de la ciutat"""
        
        if self.graf_city is None:
            self.crear_graf_ciutat()
            
        plot_interactive(self.plot_graf_city)


    def obtenir_coordenades(self, direccio:str) -> Coord | None:
        """Donada una direcció retorna les coordenades de l'adreça, retorna una tupla amb la latitud i la longitud."""

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
    
        # Recollim les dades actuals
        print('Introdueix les coordenades en les que et trobes: ')
        lon = input('longitud: ')
        lat = input('latitud: ')
        hora_actual = datetime.datetime.now().time()
        minuts_actuals = hora_actual.hour*60 + hora_actual.minute
        
        # Si encara no hem creat el graf de la ciutat el creem
        if not self.graf_city:
            self.crear_graf_ciutat
        
        temps_per_arribar = 0
        temps_per_projeccio = 0
        idx = 0
        
        # De les projeccions que cumpleixen els requisits de l'usuari, busquem la primera a la que podem arribar-hi
        while temps_per_arribar >= temps_per_projeccio and idx < len(projeccions):
            
            direccio = projeccions[idx].cinema.address
            for x in direccio:
                if x == 'Calle':
                    direccio = direccio.replace('Calle', '')
            
            # Convertim l'adreça a coordenades
            resultat = self.obtenir_coordenades(direccio)

            temps_per_projeccio = minuts_actuals - (projeccions[idx].time[0]*60 + projeccions[idx].time[1])
            
            print(resultat)
            path = find_path(self.g_maps, self.graf_city, [lon, lat], resultat)
            temps_per_arribar = time_path(path)
            
            idx += 1
        
        if temps_per_arribar < temps_per_projeccio:
            # Un avís molt important !
            if temps_per_projeccio - temps_per_arribar <= 5:
                print('Afanyat que sinó no et donarà temps a comprar crispetes! Et sobren menys de 5 minuts')

            # Guardem el camí i l'imprimim per pantalla
            plot_path(self.graf_city, path, 'cami.jpg')
            plot_interactive('cami.jpg')

        else:
            print("No s'han trobat camins vàlids per la teva búsqueda")
            print("Prova-ho amb una altra selecció!")
            self.cercar_cartellera()


    def mostrar_menu(self) -> None:
        """Mostra el menú amb totes les opcions que pot sol·licitar l'usuari."""

        print("----- Mòdul Demo -----")
        print("1. Mostrar autors")
        print("2. Mostrar cartellera")
        print("3. Cercar a la cartellera")
        print("4. Mostrar graf de busos")
        print("5. Mostrar graf de ciutat")
        print("0. Sortir")


def main():
    demo = Demo()
    opcio = None 

    demo.mostrar_menu()
    opcio = input('Selecciona una opció: ')

    while opcio != '0':

        if opcio == "1":
            demo.mostrar_autors()
            time.sleep(2)
        
        elif opcio == "2":
            demo.mostrar_cartellera()
            time.sleep(4)
        
        elif opcio == "3":
            demo.cercar_cartellera()
        
        elif opcio == "4":
            demo.mostrar_graf_busos()
        
        elif opcio == "5":
            print('Perdoneu, aquest procés pot tardar una mica.')
            demo.mostrar_graf_ciutat()
        
        else:
            print("Opció invàlida. Selecciona una opció vàlida inserint un número.")
        
        demo.mostrar_menu()
        opcio = input('Selecciona una opció: ')
                
    print("Gràcies per utilitzar els nostres serveis ! Àdeu ! Fins una altra!")

if __name__=="__main__":
    main()
 
