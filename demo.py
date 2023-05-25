import time
import geocoder
import requests
from billboard import *
hora_actual = datetime.datetime.now().time()

class Demo:
    def __init__(self):
        self.billboard = None

    def mostrar_autors(self):
        print("Autors del projecte:")
        print(" Laia Royo Rion")
        print(" Clàudia Ibañez Massa")


    def crear_cartellera(self):
        self.billboard = read()
        # Codi per crear la cartellera
        print("La cartellera s'ha creat amb èxit!")

    def mostrar_cartellera(self):
        # Codi per mostrar el contingut de la cartellera
        self.crear_cartellera()
        
        if self.billboard:
            print("----- Cartellera -----")
            for film in self.billboard.films:
                print("Title:", film.title)
                print("Genre:", ", ".join(film.genre))
                print("Director:", ", ".join(film.director))
                print("Actors:", ", ".join(film.actors))
                print("----------------------")
  
        else:
            print("La cartellera encara no s'ha creat.")

    def cercar_cartellera(self) -> list[Projection] | None:

        if self.billboard:
    
            print("4.1 Cerca per nom de pel·lícula")
            print("4.2 Cerca per gènere")
            print("4.3 Cerca per director")
            print("4.4 Cerca per actors")
            

            opcio  = input("Selecciona una opció: ")
            if opcio == "4.1":
                self.cercar_cartellera_per_nom()
                
            elif opcio == "4.2":
                self.cercar_cartellera_per_genere()
            
            elif opcio == "4.3":
                self.cercar_cartellera_per_directors()
            
            elif opcio == "4.4":
                self.cercar_cartellera_per_actors()
            
            else:
                print("Opció invàlida!")

        else:
            print("La cartellera encara no s'ha creat.")

    def cercar_cartellera_per_nom(self) -> list[Projection]:
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
            

    def cercar_cartellera_per_genere(self) -> list[Projection]:
        
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

    def cercar_cartellera_per_directors(self) -> list[Projection]:
        
        director = input("Introdueix el nom i cognom del director que vols cercar: ")
        projeccions = self.billboard.cerca_peli_per_director(director)
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

    def cercar_cartellera_per_actors(self) -> list[Projection]:
        
        actor = input("Introdueix l'actor que vols cercar: ")
        projeccions = self.billboard.cerca_peli_per_actor(actor)
        if projeccions:
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

    def crear_graf_busos():
        # Codi per crear el graf de busos
        print("El graf de busos s'ha creat amb èxit!")

    def mostrar_graf_busos():
        # Codi per mostrar el graf de busos
        print("----- Graf de Busos -----")
        # Mostra el graf de busos
        print("--------------------------")

    def crear_graf_ciutat():
        # Codi per crear el graf de la ciutat
        print("El graf de la ciutat s'ha creat amb èxit!")

    def mostrar_graf_ciutat():
        # Codi per mostrar el graf de la ciutat
        print("----- Graf de la Ciutat -----")
        # Mostra el graf de la ciutat
        print("-----------------------------")


    def mostrar_camí_pel·lícula(self):

        projeccions = self.cercar_cartellera()
        lloc = input("Introdueix el lloc actual: ")
        hora_actual = input("Introdueix el moment actual: ")
        
        temps_a_arribar = None
        
        for projeccio in projeccions:
            if hora_actual + temps_a_arribar < projeccio.time:
                adressa_guardada = projeccio.cinema.address
                break

        
        # Convertim l'adreça en coordenades (latitud i longitud)
        coord = self.obtenir_coordenades()

        
        # Codi per obtenir el camí per anar a veure la pel·lícula desitjada
        print("Camí per anar a veure la pel·lícula:")
        print(f"1. {lloc} -> Parada d'autobús -> Cinemes")
        print(f"2. {lloc} -> Peatonal -> Cinemes")

    def obtenir_coordenades(self,direccio:str):

        loc = geocoder.google(direccio)
        print(loc)
        loc.latlng

    
        

    # Funció per mostrar el menú principal
    def mostrar_menu(self):
        print("----- Mòdul Demo -----")
        print("1. Mostrar autors")
        print("2. Crear cartellera")
        print("3. Mostrar cartellera")
        print("4. Cercar a la cartellera")
        print("5. Crear graf de busos")
        print("6. Mostrar graf de busos")
        print("7. Crear graf de ciutat")
        print("8. Mostrar graf de ciutat")
        print("0. Sortir")

    def executar(self):
        opcio = None
        while opcio != "0":
            self.mostrar_menu()
            opcio = input("Selecciona una opció: ")

            if opcio == "1":
                print()
                self.mostrar_autors()
            elif opcio == "2":
                print()
                self.crear_cartellera()
            elif opcio == "3":
                print()
                self.mostrar_cartellera()
            elif opcio == "4":
                print()
                self.crear_cartellera()
                self.cercar_cartellera()
            elif opcio == "0":
                print()
                print("Gràcies per utilitzar els nostres serveis ! Àdeu ! Fins una altra!")
            else:
                print("Opció invàlida. Selecciona una opció vàlida inserint un número.")
            print()

#def main():
    #demo = Demo()
    #demo.executar()

if __name__=="__main__":
    #main()
    loc = geocoder.osm("Paseo Andreu Nin s/n - Pintor Alzamora, 08016 Barcelona")
    print(loc)
    loc.latlng
