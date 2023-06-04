import time
import requests
from billboard import *
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
            print("Genere:", ", ".join(film.genere))
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


    def obtenir_coordenades(self, direccio:str) -> Coord:
        """Donada una direcció retorna les coordenades de l'adreça, retorna una tupla amb la latitud i la longitud."""

        equivalencia:dict[str,Coord] = {"Gran Vía de les Corts Catalanes, 385, 08015 Barcelona":(41.37644012709498, 2.1494966562395437) , "Calle Aribau, 8, 08011 Barcelona": (41.38627471324918, 2.162503137010816), 
                        "Rambla de Prat 16, 08012 Barcelona":(41.40185607088032, 2.1516961793420064) , "Paseig de Gracia, 13, 08007 Barcelona": (41.38988140261133, 2.1675482703635613) , 
                        "Carrer de Girona 173-175,08025 Barcelona":(41.399749089154525, 2.164554737011875), "Calle Verdi, 32, 08012 Barcelona": (41.4042920109033, 2.1568431370122014), 
                        "Sta Fé de Nou Mèxic s/n, 08017 Barcelona": (41.39448291172901, 2.1362157744928254),"Avenida Diagonal, 3, 08019 Barcelona":(41.40997594323552, 2.2166893860724706) ,
                        "Passeig Potosí 2 - Centro Comercial La Maquinista, 08030 Barcelona": (41.43973919927414, 2.198296733222233),
                        "Paseo Andreu Nin s/n - Pintor Alzamora, 08016 Barcelona": (41.43845041407611, 2.179690362608926) , "Avenida Diagonal, 208, 08018 Barcelona":(41.40486771581146, 2.190754121672208),
                        "General Mitre, 38-44, 08017 Barcelona": (41.394984391831294, 2.1340233235165305) , "Carrer del Pi, 5, 08002 Barcelona":(41.383370318549254, 2.173896494680645), 
                        "Calle Floridablanca, 135, 08011 Barcelona":(41.38191672257184, 2.162680423515529),
                        "C/ Sant Antoni Maria Claret, 168, 08041 Barcelona":(41.409156105188565, 2.1718909523526544), "Calle Salvador Espriu, 61, 08005 Barcelona":(41.39095680130664, 2.197943708176163) ,
                        "Avenida Diagonal, 508, 08006 Barcelona":(41.39552038735651, 2.153793994681538), "Carrer Béjar, 53, 8014 Barcelona":(41.37757162454815, 2.145023116732765),
                        "Calle Balmes, 422-424, 08022 Barcelona":(41.40739485032398, 2.1385792793423986),
                        "Passeig de Gracia, 13, 08007 Barcelona":(41.38969030251614, 2.1674442658461084), "Carrer de la concordia, 1, 08917 Badalona":(41.44420081834454, 2.2306335388604244), 
                        "Pelai,8":(41.38592831063234, 2.1652820658458003)}
        
        return equivalencia[direccio]


    def mostrar_camí_pel·lícula(self, projeccions: list[Projection]) :
    
        # Recollim les dades actuals
        print('Introdueix les coordenades en les que et trobes: ')
        lon = input('longitud: ')
        lat = input('latitud: ')
        hora_actual = datetime.datetime.now().time()
        minuts_actuals = hora_actual.hour*60 + hora_actual.minute
        
        # Si encara no hem creat el graf de la ciutat el creem
        if not self.graf_city:
            self.crear_graf_ciutat()
        
        temps_per_arribar = 0
        temps_per_projeccio = 0
        idx = 0
        
        # De les projeccions que cumpleixen els requisits de l'usuari, busquem la primera a la que podem arribar-hi
        while temps_per_arribar >= temps_per_projeccio and idx < len(projeccions):
            
            direccio = projeccions[idx].cinema.address
            
            
            # Convertim l'adreça a coordenades
            resultat = self.obtenir_coordenades(direccio)
            print(resultat)
            input()

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
 

    


            

   

    


            
 
