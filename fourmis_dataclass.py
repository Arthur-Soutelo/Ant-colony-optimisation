# Arthur SOUTELO ARAUJO

from dataclasses import dataclass

@dataclass
class Civilisation:
    nom : str
    ville_nid : bool
    ville_food : bool


@dataclass
class Fourmi:
    alpha : float
    beta : float
    gamma : float
    porte_food : bool

@dataclass
class Route:
    pheromone : int
    longueur : int
    
    

@dataclass
class Ville:
    nom : str
    position : str

if __name__ == "__main__":
    a1 = Fourmi(0.1,0.2,0.3,True)
    print(a1)



    