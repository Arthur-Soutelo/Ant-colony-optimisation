from tkinter import *
from tkinter.messagebox import showinfo
import random

class ZoneAffichage(Canvas):
    def __init__(self, parent, w=500, h=400, _bg='white'):  # 500x400 : dessin final !
        self.__w = w
        self.__h = h
        self.liste_noeuds = []
        # Pour avoir un contour pour le Canevas
        self.__fen_parent = parent
        Canvas.__init__(self, parent, width=w, height=h, bg=_bg, relief=RAISED, bd=5)
        
        self.__noeud_start = None
        self.__noeud_end = None 

    def get_dims(self):
        return (self.__w, self.__h)

    # def not_used_keep_dessiner_graphe(self):
    #     for b in self.liste_noeuds:
    #         b.deplacement()
    #     self.after(50, self.dessiner_graphe)  # Important, sinon on fera une seul execution

    def creer_noeud(self, x_centre, y_centre, rayon , col, fill_color="white"):
        noeud = Balle(self, x_centre, y_centre, rayon , col)
        self.pack()
        return noeud
    
    def creer_route(self, x1, y1, x2 , y2):
        route = Route(self, x1, y1, x2 , y2)
        self.pack()
        return route

    def action_pour_un_clique(self, event):
        print("Noeud : (x,y) = ", event.x, event.y)       
        # Placer un noeud à l'endroit cliqué
        self.__fen_parent.placer_un_noeud(event.x, event.y)

    def action_pour_un_clique_droite_start(self, event):
        print("Trace Start : (x,y) = ", event.x, event.y)
        start_x = event.x
        start_y = event.y
        dist = 15
        flag = 0
        print(len(self.liste_noeuds))
        for noeud in self.liste_noeuds:
            x,y = noeud
            if x in range(start_x - dist , start_x + dist) and y in range(start_y - dist , start_y + dist):
                self.__noeud_start = noeud
                print("Noeud Start : (x,y) = ", noeud)
                flag = 1
            elif flag == 0:
                self.__noeud_start = None
        
        
    def action_pour_un_clique_droite_end(self, event):
        print("Trace End: (x,y) = ", event.x, event.y)   
        end_x = event.x
        end_y = event.y
        dist = 15
        flag = 0
        for noeud in self.liste_noeuds:
            x,y = noeud
            if x in range(end_x - dist , end_x + dist) and y in range(end_y - dist , end_y + dist):
                self.__noeud_end = noeud
                print("Noeud End : (x,y) = ", noeud)
                flag = 1
        if flag == 1:
            self.__fen_parent.placer_une_route(self.__noeud_start, self.__noeud_end)
            self.__noeud_end = None
        

    # def not_used_set_coordonnes_du_last_node(self, x_centre, y_centre):
    #     self.__last_node=(x_centre, y_centre)

    def placer_un_noeud_sur_canevas(self, x_centre, y_centre, col=None, fill_color="white"):
        w,h = self.get_dims()
        rayon=10
        if col == None :
            col= random.choice(['green', 'blue', 'red', 'magenta', 'black', 'maroon', 'purple', 'navy', 'dark cyan'])
        node=self.creer_noeud(x_centre, y_centre, rayon , col, fill_color)
        self.update()
        self.__fen_parent.set_coordonnes_du_last_node(x_centre, y_centre)
        return node.get_node_ident()

    def placer_une_route_sur_canevas(self, x1, y1, x2, y2):
        w,h = self.get_dims()
        route = self.creer_route(x1, y1, x2 , y2)
        self.update()
        self.__fen_parent.set_coordonnes_last_route(x1, y1, x2, y2)
        return route.get_route_ident()

class FenPrincipale(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Graphe ACO [Arthur SOUTELO ARAUJO]')
        self.__zoneAffichage = ZoneAffichage(self)
        self.__zoneAffichage.pack()
        # Création des widgets Button
        self.__boutonEffacer = Button(self, text='Undo last node', command=self.undo_last_noeud).pack(side=LEFT, padx=5, pady=5)
        self.__boutonEffacer = Button(self, text='Undo last route', command=self.undo_last_route).pack(side=LEFT, padx=5, pady=5)
        self.__boutonEffacer = Button(self, text='Effacer Tout', command=self.effacer).pack(side=LEFT, padx=5, pady=5)
        self.__boutonQuitter = Button(self, text='Quitter', command=self.destroy).pack(side=LEFT, padx=5, pady=5)
        self.__boutonStart = Button(self, text='Start Simulation').pack(side=RIGHT, padx=5, pady=5)

        self.__zoneAffichage.bind('<Button-1>', self.__zoneAffichage.action_pour_un_clique)
        self.__zoneAffichage.bind('<Button-3>', self.__zoneAffichage.action_pour_un_clique_droite_start)
        self.__zoneAffichage.bind('<ButtonRelease-3>', self.__zoneAffichage.action_pour_un_clique_droite_end)
        
        self.__liste_d_ident_d_objets_crees=[]
        self.__liste_coordonnes_centre_des_nodes=[]
        self.__liste_routes=[]
        self.__liste_coordonnes_routes=[]

        self.placer_noeud_depart()

    def add_a_node_to_your_list(self, noeud) :
        self.__liste_d_ident_d_objets_crees.append(noeud)
        self.__zoneAffichage.liste_noeuds = self.__liste_coordonnes_centre_des_nodes
        
    def add_a_route_to_your_list(self, route) :
        self.__liste_routes.append(route)
        
    def placer_un_noeud(self, x, y):
        node=self.__zoneAffichage.placer_un_noeud_sur_canevas(x,y)
        self.add_a_node_to_your_list(node)
        self.set_coordonnes_du_last_node(x,y)
        self.__liste_coordonnes_centre_des_nodes.append((x,y))
    
    def placer_une_route(self, noeud_start, noeud_end):
        x1,y1 = noeud_start
        x2,y2 = noeud_end
        route = self.__zoneAffichage.placer_une_route_sur_canevas(x1,y1,x2,y2)
        self.add_a_route_to_your_list(route)
        self.set_coordonnes_last_route(x1,y1,x2,y2)
        self.__liste_coordonnes_routes.append((x1,y1,x2,y2))


    def set_coordonnes_du_last_node(self, x_centre, y_centre):
        self.__last_node=(x_centre, y_centre)
    
    def set_coordonnes_last_route(self, x1, y1, x2, y2):
        self.__last_route=(x1, y1, x2, y2)
    
    def get_last_node(self):
        return self.__last_node
    
    def get_last_route(self):
        return self.__last_route

    def placer_noeud_depart(self):
        w,h = self.__zoneAffichage.get_dims()
        x_centre, y_centre=20, h//2
        node= self.__zoneAffichage.placer_un_noeud_sur_canevas(x_centre, y_centre, col="red", fill_color="red")
        self.add_a_node_to_your_list(node)
        self.__liste_coordonnes_centre_des_nodes.append((x_centre, y_centre))

    def undo_last_noeud(self):
        print("Avant undo, liste contient {} elements".format(len(self.__liste_d_ident_d_objets_crees)))
        if len(self.__liste_d_ident_d_objets_crees)==1 :
            print("Peut pas enlever noeud départ")
            return
        x_centre,  y_centre = self.get_last_node()
        last_node=self.__liste_d_ident_d_objets_crees.pop()
        # Pour supprimer, il faut can_id du noeud, pas le noeud lui mm !!
        self.__zoneAffichage.delete(last_node)
        self.__zoneAffichage.update()
        x_last_node,y_last_node = self.__liste_coordonnes_centre_des_nodes.pop()
        self.set_coordonnes_du_last_node(x_last_node,y_last_node)
        print("Après undo, liste contient {} elements".format(len(self.__liste_d_ident_d_objets_crees)))
        
    
    def undo_last_route(self):
        print("Avant undo, liste contient {} elements".format(len(self.__liste_routes)))
        if len(self.__liste_routes)==0 :
            print("Il n'y a plus des routes")
            return
        x1,y1,x2,y2 = self.get_last_route()
        last_route = self.__liste_routes.pop()
        # Pour supprimer, il faut can_id de la route, pas la route lui mm !!
        self.__zoneAffichage.delete(last_route)
        self.__zoneAffichage.update()
        x1,y1,x2,y2 = self.__liste_coordonnes_routes.pop()
        self.set_coordonnes_last_route(x1, y1, x2, y2)
        print("Après undo, liste contient {} elements".format(len(self.__liste_routes)))

    # def ajout_noeud(self):
    #     # Dessin d'un petit cercle
    #     x_centre,  y_centre = self.not_used_generer_un_point_XY_dans_une_bande()
    #     print("(x,y) =", x_centre, ' , ', y_centre)
    #     rayon=10
    #     col= random.choice(['green', 'blue', 'red', 'magenta', 'black', 'purple', 'navy', 'dark cyan'])
    #     self.__zoneAffichage.creer_noeud(x_centre, y_centre, rayon , col)
    #     self.__zoneAffichage.update()
    #     self.__last_node=(x_centre, y_centre)

    # def ajout_route(self):
    #     # Dessin d'une route
    #     print("(x,y) =", x_centre, ' , ', y_centre)
    #     #self.__zoneAffichage.creer_route(x1, y1)
    #     self.__zoneAffichage.update()
    #     #self.__last_node=(x_centre, y_centre)

    def effacer(self):
        self.__zoneAffichage.delete(ALL)
        self.__liste_d_ident_d_objets_crees.clear()
        self.__liste_coordonnes_centre_des_nodes.clear()
        self.__liste_routes.clear()
        self.__liste_coordonnes_routes.clear()
        self.placer_noeud_depart()

    """ INTEGRATION FOURMIS """
    def get_list_routes(self):
        return self.__liste_routes
    def get_list_coordonnes_routes(self):
        return self.__liste_coordonnes_routes


""" F O R M E S"""
class Balle:
    def __init__(self, canvas, cx, cy, rayon, couleur, fill_color="white"):
        self.__cx, self.__cy = cx, cy
        self.__rayon = rayon
        self.__color = couleur
        self.__can = canvas  # Il le faut pour les déplacements
        self.__canid = self.__can.create_oval(cx - rayon, cy - rayon, cx + rayon, cy + rayon, outline=couleur, fill=couleur,width=3)

    def get_node_ident(self):
        return self.__canid
    
    def get_coord(self):
        return (self.__cx, self.__cy)

    # def NoNeed_Here_not_used_generer_un_point_XY_dans_une_bande(self, last_x, last_y):
    #     w,h = self.__can.get_dims()
    #     #last_x, last_y=self.__last_node
    #     delta_x_centre = random.randint(10, 50); delta_y_centre = random.randint(10, 50)
    #     hasard_x=random.randint(0, 1); hasard_y=random.randint(0, 1)
    #     x_centre = last_x+random.randint(10, 50)* 1 if hasard_x else -1
    #     y_centre = last_y+random.randint(10, 50)* 1 if hasard_y else -1
    #     if x_centre < 0 :  x_centre*=-1
    #     if y_centre < 0 :  y_centre*=-1
    #     return (x_centre, y_centre)

    # Un seul déplacement
    # def not_used_keep_deplacement(self):
    #     self.__can.move(self.__canid, 0, 0)

class Route:
    def __init__(self, canvas, x1, y1, x2, y2):
        print(x1,y1,x2,y2)
        self.__x1, self.__y1, self.__x2, self.__y2= x1,y1,x2,y2
        self.__color = "Black"
        self.__can = canvas  # Il le faut pour les déplacements
        self.__canid = self.__can.create_line( self.__x1, self.__y1, self.__x2, self.__y2,width=3)
        
        #self.__textid = self.__can.create_text(abs(self.__x1-self.__x2), abs(self.__y1-self.__y2),fill="black", font=('Helvetica 15 bold'))
        
        self.__noeud_start = None
        self.__noeud_end = None

    def get_route_ident(self):
        return self.__canid
    
# --------------------------------------------------------
if __name__ == "__main__":
    fen = FenPrincipale()
    fen.mainloop()
