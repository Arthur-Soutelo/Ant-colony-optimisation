# Arthur SOUTELO ARAUJO

from fourmis_canevas import *
import math
from collections import defaultdict
from collections import Counter
import random
import numpy as np

class Civilisation:
    def __init__(self, nom, ville_nid, ville_food, routes=[], villes=[], fourmis=[]):
        self.__nom = nom 
        self.__ville_nid = ville_nid
        self.__ville_food = ville_food

        self.__routes = routes
        self.__villes = villes
        self.__fourmis = fourmis
        
        self.graph = defaultdict(list)
        self.create_graph_distance()
        self.give_info_all_fourmis()
        
        self.optimum = None
    
    def next_tour(self):
        if self.__ville_food.qte_food != 0:
            for fourmi in self.__fourmis:
                self.give_info_fourmi(fourmi)
                fourmi.faire_un_pas()
            for route in self.__routes:
                route.evaporer_pheromone()
    
    def update_food(self, ville_food):
        self.__ville_food = ville_food
            
    def create_graph_distance(self):
        for i in range(len(self.__routes)):
            ville1 = self.__routes[i].premiere_ville
            ville2 = self.__routes[i].seconde_ville
            route = self.__routes[i]
            self.add_edge_graph(ville1, route)
            self.add_edge_graph(ville2, route)
        # print(self.graph)    
    def add_edge_graph(self,ville,route):
        self.graph[ville].append(route)

    def give_info_fourmi(self,fourmi):
        if isinstance(fourmi.place,Ville):
            fourmi.options = self.graph[fourmi.place]
    def give_info_all_fourmis(self):
        for fourmi in self.__fourmis:
           self.give_info_fourmi(fourmi)
    
    def criteria_stop(self):
        tag_continue = False
        best_paths = []
        for fourmi in self.__fourmis:
            best_paths.append(fourmi.last_path)
        if None in best_paths:
            tag_continue = True
        else:
            count = Counter(best_paths)
            print(count)
            n_times = max(count.values())
            best_distance = min(count.keys())
            n_times_best = count[best_distance]
            best = max(count, key=count.get)
            self.optimum = best
            if n_times_best == n_times:
                tag_continue = False
            else:
                tag_continue = True
        return tag_continue
    
    
    def start_simulation(self):
        tag = self.criteria_stop()
        count=0
        while (tag):
            before = self.optimum
            self.next_tour()
            tag = self.criteria_stop()
            if before == self.optimum:
                count += 1
                if count > 20000:
                    break
    
    def return_path(self):
        villes = []
        print(self.optimum)
        for fourmi in self.__fourmis:
            if fourmi.last_path == self.optimum:
                for place in self.__fourmis[0].path:
                    if isinstance(place,Ville):          
                        villes.append(place)
                return villes


class Fourmi:
    def __init__(self, alpha, beta, gamma, place):
        self.__alpha = alpha 
        self.__beta = beta
        self.__gamma = gamma
        self.porte_food = False
        
        self.place = place
        self.historique = [self.place]
        
        self.last_path = None
        self.path = []
        
        self.options = []
        
        self.vitesse = 5
        self.distance = 0
        
    def __str___(self):
        return (self.__alpha, self.__beta, self.__gamma, self.__porte_food)
    
    def deposer_pheromone(self, route):
        pl_route = route.pheromone
        pl_after = self.__alpha * math.sin(self.__beta * pl_route + self.__gamma)
        route.pheromone = pl_after
    
    def prendre_nourriture(self, ville) : # Prendre la nouriture dans la source de nouriture
        #ville.moins_food()
        self.porte_food = True
        
    def laisser_nourriture(self,ville) : # Laisse la nouriture (dans le nid)
        ville.plus_food()
        self.porte_food = False
        self.effacer_memoire()
        
    def effacer_memoire(self):
        self.historique = [self.place]
        
    def faire_un_pas(self):
        if isinstance(self.place, Route):   # Si fourmi dans une route
            self.deposer_pheromone(self.place)
            self.distance = self.distance + self.vitesse
            if self.porte_food :
                if self.distance >= self.place.longueur:
                    if self.historique[-1] == self.place.premiere_ville:
                        self.place = self.place.premiere_ville
                    elif self.historique[-1] == self.place.seconde_ville:
                        self.place = self.place.seconde_ville
                    self.distance = 0
                    self.historique.pop()    
            else: 
                if self.distance >= self.place.longueur:
                    if self.historique[-1] == self.place.premiere_ville:
                        self.place = self.place.seconde_ville
                    elif self.historique[-1] == self.place.seconde_ville:
                        self.place = self.place.premiere_ville
                    self.distance = 0
                    self.historique.append(self.place)                
                    print('add')
        elif isinstance(self.place,Ville):             # Si fourmi dans une ville
            if self.place.cond == "Food":
                if self.porte_food:
                    self.historique.pop()  
                    self.choix_chemin()
                    self.distance = self.distance + self.vitesse
                    self.deposer_pheromone(self.place)
                else:
                    self.prendre_nourriture(self.place)
                    if self.calculate_path_from_history():
                        self.path = []
                        self.path = self.historique.copy()
                        print("PATH : ")
                        print(self.path)
            elif self.place.cond == "Nid":
                if not(self.porte_food):
                    self.choix_chemin()
                    self.distance = self.distance + self.vitesse
                    self.deposer_pheromone(self.place)
                else:             
                    self.laisser_nourriture(self.place)
                    self.effacer_memoire()
            elif self.place.cond == "Noeud":
                self.choix_chemin()
                self.distance = self.distance + self.vitesse
                self.deposer_pheromone(self.place)

            
    def choix_chemin(self):
        tendances = []     
        if self.porte_food :      
            for route in self.options:
                if self.historique[-1] == route.premiere_ville or self.historique[-1] == route.seconde_ville:
                    self.place = route
        else:
            for route in self.options:
                if len(self.historique)==1:
                    tendances.append(self.get_tendance(route))
                else:
                    last_ville = self.historique[-2]
                    if (last_ville != route.premiere_ville and last_ville != route.seconde_ville):
                        tendances.append(self.get_tendance(route))
                    elif last_ville == route.premiere_ville or last_ville == route.seconde_ville:
                        tendances.append(-10)
            arg = np.argmax(tendances)
            self.place = self.options[arg]        
            
    def get_tendance(self,route):
        q0 = 0.5
        q = random.uniform(0,1)                 # Parametre pour rendre la decision aleatoire
        if q <= q0:                             # Choix de l'équation de tendance basé sur q et qo
            tendance = route.pheromone/(route.longueur**(self.__beta))
        else:
            tendance = (route.pheromone**self.__alpha)/(route.longueur**(self.__beta))
        return tendance
    
    def calculate_path_from_history(self):   # Calculer distance last iteration
        path_actu = 0
        for i in range(len(self.historique)-1):
            ville1 = self.historique[i]
            ville2 = self.historique[i+1]
            dist = self.calculer_distance_entre_villes(ville1, ville2)
            path_actu = path_actu + dist           
        if self.last_path == None:
            self.last_path = path_actu
            return True
        elif path_actu < self.last_path:
            self.last_path = path_actu
            return True
        else:
            return False
                
    def calculer_distance_entre_villes(self,ville1, ville2):
        x1, y1 = ville1.position
        x2, y2 = ville2.position
        return math.floor(math.sqrt((x2 - x1)**2 + (y2 - y1)**2))


class Route:
    def __init__(self, premiere_ville, seconde_ville):
        self.pheromone = 0.2
        self.premiere_ville = premiere_ville
        self.seconde_ville = seconde_ville        
        
        self.__rho_evap = 0.2   # Taux d'évaporation
        
        self.longueur = self.distance(self.premiere_ville.position, self.seconde_ville.position)
        print('longueur : '+str(self.longueur))
   
    def __str__(self):
        return str('Road from '+str(self.premiere_ville) + ' to ' + str(self.seconde_ville)) 
   
    def distance(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return math.floor(math.sqrt((x2 - x1)**2 + (y2 - y1)**2))
    
    def evaporer_pheromone(self):
        self.pheromone = (1 - self.__rho_evap) * self.pheromone

class Ville:
    def __init__(self, position, cond = 'Noeud'):
        self.position = position
        self.qte_food = 0
        self.cond = cond
        
    def __str__(self):
        return str(self.position)
    
    def moins_food(self):
        if self.qte_food > 0 and self.cond == "Food":
            self.qte_food = self.qte_food - 1

    def plus_food(self):
        if self.cond == "Nid":
            self.qte_food = self.qte_food + 1
    
    def start_food(self, qte):
        if self.cond == "Food":
            self.qte_food = qte
        
    
# --------------------------------------------------------
if __name__ == "__main__":
    #fen = FenPrincipale()
    #fen.mainloop()
    
    # ------------------------------------    
    nid = Ville((0,0),"Nid")
    villeA = Ville((50,0))
    villeB = Ville((80,0))
    villeC = Ville((80,100))
    food = Ville((100,100),"Food")
    food.start_food(50)
    
    villes = [nid, villeA, villeB, villeC, food]
    
    route1 = Route(nid, villeA)
    route2 = Route(villeA, villeB)
    route3 = Route(villeB, food)
    route4 = Route(villeB, villeC)
    route5 = Route(villeC, food)
    
    routes = [route1, route2, route3, route4, route5]
    
    a1 = Fourmi(0.1,0.9,0.3,nid)
    a2 = Fourmi(0.2,0.6,0.4,nid)
    a3 = Fourmi(0.6,0.7,0.8,nid)
    a4 = Fourmi(0.1,0.4,0.7,nid)
    a5 = Fourmi(0.2,0.3,0.6,nid)
    fourmis = [a1, a2, a3, a4, a5]
    # ------------------------------------
    
    civ = Civilisation("ECL", nid, food, routes, villes, fourmis)
    
    # for i in range(40):    
    #     print('\n' + str(i)+' :')
    #     print('Place : '+str(a1.place) + '-' + str(a1.distance) + ' // ' + str(a2.place) + '-' + str(a2.distance))
    #     print(a1.porte_food)
    #     civ.next_tour()
    
    # print('\nQte food Nid :')
    # print(nid.qte_food)
    
    
    # print(a1.historique)
    
    civ.start_simulation()
    print(civ.return_path())