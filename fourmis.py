# Arthur SOUTELO ARAUJO

from fourmis_canevas import *
import math

class Civilisation:
    def __init__(self, nom, ville_nid, ville_food):
        self.__nom = nom 
        self.__ville_nid = ville_nid
        self.__ville_food = ville_food

        #self.__routes = ... # toutes les routes de l’Environement
        #self.__villes = ... # toutes les villes de l’Environement
        #self.__fourmis = ... # toutes les fourmis dans l’Environement
        #self.__selectionNaturelle = ... # les tours restants avant la prochaine sélection (pour l’algorithme génétique)

    def tour_suivant(self):
        pass

class Fourmi:
    def __init__(self, alpha, beta, gamma):
        self.__alpha = alpha 
        self.__beta = beta
        self.__gamma = gamma
        self.__porte_food = False
    
    def __str___(self):
        return (self.__alpha, self.__beta, self.__gamma, self.__porte_food)
    
    def deposer_pheromone(self, route):
        pl_route = route.pheromone
        pl_after = self.__alpha * math.sin(self.__beta * pl_route + self.__gamma)
        pass
    
    def prendre_nourriture(self, ville) : # Prendre la nouriture dans la source de nouriture
        if ville.moins_food == True:
            self.__porte_food = True
        
    def laisser_nourriture(self,ville) : # Laisse la nouriture (dans le nid)
        ville.plus_food
        self.__porte_food = False
        
    def marcher(self) : # Avancer une étape plus
        pass    

    def choix_chemin(self, ):
        pass

class Route:
    def __init__(self, longueur, premiere_ville, seconde_ville, pheromone = 0):
        self.longueur = longueur
        self.pheromone = pheromone
        self.__premiere_ville = premiere_ville
        self.__seconde_ville = seconde_ville        
        
        self.__rho_evap = 0.5 # Taux d'évaporation
    
    
    def evaporer_pheromone(self):
        self.pheromone = (1 - self.__rho_evap) * self.pheromone

class Ville:
    def __init__(self, position, food=0):
        self.position = position
        self.qte_food = food
        self.cond = 'Noeud'
        
    def moins_food(self):
        if self.qte_food > 0 and self.cond == "Food":
            self.qte_food = self.qte_food - 1
            return True
        else:
            return False
    def plus_food(self):
        if self.cond == "Nid":
            self.qte_food = self.qte_food + 1
        
    
    
        
        
if __name__ == "__main__":
    a1 = Fourmi(0.1,0.2,0.3)
    print(a1)



    