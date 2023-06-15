# Arthur SOUTELO ARAUJO

from tkinter import *
from tkinter.messagebox import showinfo
import random
from fourmis import *

class ZoneAffichage(Canvas):
    def __init__(self, parent,frame, w=700, h=600, _bg='white'):  # 500x400 : dessin final !
        self.__w = w
        self.__h = h
        self.liste_noeuds = []
        # Pour avoir un contour pour le Canevas
        self.__fen_parent = parent
        Canvas.__init__(self, frame, width=w, height=h, bg=_bg, relief=RAISED, bd=5)
        
        self.__noeud_start = None
        self.__noeud_end = None 

    def get_dims(self):
        return (self.__w, self.__h)

    def creer_noeud(self, x_centre, y_centre, rayon , col, fill_color="white"):
        noeud = Balle(self, x_centre, y_centre, rayon , col)
        self.pack()
        return noeud
    
    def creer_route(self, x1, y1, x2 , y2):
        route = Line(self, x1, y1, x2 , y2)
        self.pack()
        return route

    def action_pour_un_clique(self, event):
        type_noeud = self.__fen_parent.type_noeud
        if type_noeud == 'Nid':
            print("Nid : (x,y) = ", event.x, event.y)       
            self.__fen_parent.placer_noeud_depart(event.x, event.y)
        elif type_noeud == "Food":
            print("Food : (x,y) = ", event.x, event.y)       
            self.__fen_parent.placer_noeud_food(event.x, event.y)
        else:
            print("Noeud : (x,y) = ", event.x, event.y)       
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
        

    def placer_un_noeud_sur_canevas(self, x_centre, y_centre, col=None, fill_color="white"):
        w,h = self.get_dims()
        rayon=10
        if col == None :
            col= 'black'
        node=self.creer_noeud(x_centre, y_centre, rayon , col, fill_color)
        self.update()
        self.__fen_parent.set_coordonnes_du_last_node(x_centre, y_centre)
        return node

    def placer_une_route_sur_canevas(self, x1, y1, x2, y2):
        w,h = self.get_dims()
        route = self.creer_route(x1, y1, x2 , y2)
        self.update()
        self.__fen_parent.set_coordonnes_last_route(x1, y1, x2, y2)
        return route

class FenPrincipale(Tk):
    def __init__(self):
        self.type_noeud = "Noeud"
        
        Tk.__init__(self)
        self.title('Graphe ACO [Arthur SOUTELO ARAUJO et Gabriel BELTRAMI]')
        
        self.__Frame0 = Frame(self, width=100, height=100)
        self.__Frame11 = Frame(self.__Frame0, width=300, height=1000)
        self.__Frame12 = Frame(self.__Frame0, width=300, height=1000)
        self.__Frame2 = Frame(self.__Frame0, width=300, height=1000)
        self.Frame3 = Frame(self, width=3000, height=2000, bg="green")
        
        self.__zoneAffichage = ZoneAffichage(self, self.Frame3)
        self.__zoneAffichage.pack()
        
        self.__title = Label(self.__Frame0, text = "Ant Colony Optimization")
        self.__title.config(font =("Courier", 15), relief="groove",height=3,width=25)
        self.__text0 = Label(self.__Frame2, text = "Placer :                     ")
        self.__text0.config(font =("Courier", 13))
        self.__text = Label(self.__Frame11, text = "Effacer :                    ")
        self.__text.config(font =("Courier", 13))
        
        self.__Frame0.pack(side=LEFT, padx=0, pady=10)
        self.__title.pack(side=TOP, padx=0, pady=10)
        self.__Frame2.pack(side=TOP, padx=0, pady=60)
        self.__text0.pack(side=TOP, padx=0, pady=10)
        self.__Frame11.pack(side=TOP, padx=0, pady=60)
        self.__text.pack(side=TOP, padx=0, pady=10)
        self.__Frame12.pack(side=TOP, padx=0, pady=30)
        self.Frame3.pack(side=LEFT, padx=0, pady=10)
        
        # Création des widgets Button
        self.__boutonEffacer1 = Button(self.__Frame11, text='Undo last node', command=self.undo_last_noeud,width=12, height=2).pack(side=LEFT, padx=5, pady=5)
        self.__boutonEffacer2 = Button(self.__Frame11, text='Undo last route', command=self.undo_last_route,width=12, height=2).pack(side=LEFT, padx=5, pady=5)
        self.__boutonEffacer3 = Button(self.__Frame11, text='Effacer Tout', command=self.effacer,width=12, height=2).pack(side=LEFT, padx=5, pady=5)
        self.__boutonQuitter = Button(self.__Frame12, text='Quitter', command=self.destroy,width=10, height=2).pack(side=LEFT, padx=20, pady=5)
        self.__boutonStart = Button(self.__Frame12, text='Start Simulation', command=self.start,width=25, height=2).pack(side=RIGHT, padx=5, pady=5)
        
        self.__boutonNoeud = Button(self.__Frame2, text='Nid', command=self.add_nid,width=12, height=2).pack(side=LEFT, padx=5, pady=5)
        self.__boutonNoeud = Button(self.__Frame2, text='Noeud', command=self.add_noeud,width=12, height=2).pack(side=LEFT, padx=5, pady=5)
        self.__boutonFood = Button(self.__Frame2, text='Food', command=self.add_food,width=12, height=2).pack(side=LEFT, padx=5, pady=5)

        self.__zoneAffichage.bind('<Button-1>', self.__zoneAffichage.action_pour_un_clique)
        self.__zoneAffichage.bind('<Button-3>', self.__zoneAffichage.action_pour_un_clique_droite_start)
        self.__zoneAffichage.bind('<ButtonRelease-3>', self.__zoneAffichage.action_pour_un_clique_droite_end)
        
     
        #self.__canvas = ZoneAffichage(self,800,700,'white')
        #self.__canvas.pack(side=TOP, padx=5,pady=5)
        
        self.__liste_noeuds=[]
        self.__liste_coordonnes_centre_des_nodes=[]
        self.__liste_routes=[]
        self.__liste_coordonnes_routes=[]
        
        self.__Nid = None
        self.__Food = None
        
    def add_nid(self): 
        self.type_noeud = "Nid"
    def add_food(self):
        self.type_noeud = "Food"
    def add_noeud(self):
        self.type_noeud = "Noeud"

    def add_a_node_to_your_list(self, noeud) :
        self.__liste_noeuds.append(noeud)
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
        self.__liste_coordonnes_routes.append([x1,y1,x2,y2])

    def set_coordonnes_du_last_node(self, x_centre, y_centre):
        self.__last_node=(x_centre, y_centre)
    
    def set_coordonnes_last_route(self, x1, y1, x2, y2):
        self.__last_route=(x1, y1, x2, y2)
    
    def get_last_node(self):
        return self.__last_node
    
    def get_last_route(self):
        return self.__last_route

    def placer_noeud_depart(self, x, y):
        if self.__Nid == None:
            self.__Nid = self.__zoneAffichage.placer_un_noeud_sur_canevas(x, y, col="red", fill_color="red")
            self.add_a_node_to_your_list(self.__Nid)
            self.set_coordonnes_du_last_node(x,y)
            self.__liste_coordonnes_centre_des_nodes.append((x,y))
        else:
            print("Il existe un Nid déjà")
            
    def placer_noeud_food(self, x, y):
        if self.__Food == None:
            self.__Food = self.__zoneAffichage.placer_un_noeud_sur_canevas(x, y, col="blue", fill_color="blue")
            self.add_a_node_to_your_list(self.__Food)
            self.set_coordonnes_du_last_node(x,y)
            self.__liste_coordonnes_centre_des_nodes.append((x,y))
        else:
            print("Il existe un noeud Food déjà")

    def undo_last_noeud(self):
        print("Avant undo, liste contient {} elements".format(len(self.__liste_noeuds)))
        if len(self.__liste_noeuds)==0 :
            print("Peut pas enlever")
            return
        x_centre,  y_centre = self.get_last_node()
        last_node = self.__liste_noeuds.pop()
        if last_node.get_node_ident() == self.__Nid:
            self.__Nid = None
        elif last_node.get_node_ident() == self.__Food:
            self.__Food = None
        # Pour supprimer, il faut can_id du noeud, pas le noeud lui mm !!
        self.__zoneAffichage.delete(last_node.get_node_ident())
        self.__zoneAffichage.update()
        x_last_node,y_last_node = self.__liste_coordonnes_centre_des_nodes.pop()
        self.set_coordonnes_du_last_node(x_last_node,y_last_node)
        print("Après undo, liste contient {} elements".format(len(self.__liste_noeuds)))
    
    def undo_last_route(self):
        print("Avant undo, liste contient {} elements".format(len(self.__liste_routes)))
        if len(self.__liste_routes)==0 :
            print("Il n'y a plus des routes")
            return
        x1,y1,x2,y2 = self.get_last_route()
        last_route = self.__liste_routes.pop()
        # Pour supprimer, il faut can_id de la route, pas la route lui mm !!
        self.__zoneAffichage.delete(last_route.get_route_ident())
        self.__zoneAffichage.update()
        x1,y1,x2,y2 = self.__liste_coordonnes_routes.pop()
        self.set_coordonnes_last_route(x1, y1, x2, y2)
        print("Après undo, liste contient {} elements".format(len(self.__liste_routes)))

    def effacer(self):
        self.__zoneAffichage.delete(ALL)
        self.__liste_noeuds.clear()
        self.__liste_coordonnes_centre_des_nodes.clear()
        self.__liste_routes.clear()
        self.__liste_coordonnes_routes.clear()

    """ INTEGRATION FOURMIS """
    def create_fourmis(self,number, place):
        fourmis = []
        for i in range(number):
            alpha = random.uniform(0,1)
            beta =  random.uniform(0,1)
            gamma = random.uniform(0,1)
            fourmi = Fourmi(alpha, beta, gamma, place)
            fourmis.append(fourmi)
        return fourmis

    def color_all_roads_black(self):
        for route in self.__liste_routes:
            self.__zoneAffichage.itemconfig(route.get_route_ident(), fill = "Black")

    def color_roads(self, path, routes):
        print("COLOR")
        print(path)
        roads = []
        for k in range(len(path)-1):
            for j in range(k+1,len(path)):
                pos1 = path[k].position
                pos2 = path[j].position
                for i in range(len(self.__liste_coordonnes_routes)):
                    coord1 = (self.__liste_coordonnes_routes[i][0],self.__liste_coordonnes_routes[i][1])
                    coord2 = (self.__liste_coordonnes_routes[i][2],self.__liste_coordonnes_routes[i][3])
                    if coord1 == pos1 and coord2 == pos2:
                        self.__zoneAffichage.itemconfig(self.__liste_routes[i].get_route_ident(), fill = "Red")
                    elif coord2 == pos1 and coord1 == pos2:
                        self.__zoneAffichage.itemconfig(self.__liste_routes[i].get_route_ident(), fill = "Red")

    def start(self):    # Start simulation # appelle fourmis.py
        nid = Ville(self.__Nid.get_coord(),"Nid")
        food = Ville(self.__Food.get_coord(),"Food")
        food.start_food(20000)
        
        fourmis = self.create_fourmis(23,nid)
        routes = []
        villes = []
        
        #order list
        for i in range(len(self.__liste_coordonnes_centre_des_nodes)):
            if self.__liste_coordonnes_centre_des_nodes[i] == self.__Nid.get_coord():
                self.__liste_coordonnes_centre_des_nodes.pop(i)
                self.__liste_coordonnes_centre_des_nodes.append(self.__Nid.get_coord())
            elif self.__liste_coordonnes_centre_des_nodes[i] == self.__Food.get_coord():
                self.__liste_coordonnes_centre_des_nodes.pop(i)
                self.__liste_coordonnes_centre_des_nodes.append(self.__Food.get_coord())
                
        for coord in self.__liste_coordonnes_centre_des_nodes:
            if coord != self.__Nid.get_coord() and coord != self.__Food.get_coord():
                villes.append(Ville(coord))
        villes.append(nid)
        villes.append(food)        
        
        print("NOMBRE DE VILLES :")
        print(len(villes))
        print("Liste DE VILLES :")
        print(self.__liste_coordonnes_centre_des_nodes)
        
        print("Liste DE Routes :")
        print(self.__liste_coordonnes_routes)
        for coords in self.__liste_coordonnes_routes:
            coord1 = (coords[0],coords[1])
            coord2 = (coords[2],coords[3])
            premiere_ville = None
            seconde_ville = None
            for i in range(len(self.__liste_coordonnes_centre_des_nodes)):
                if self.__liste_coordonnes_centre_des_nodes[i] == coord1:
                    premiere_ville = villes[i]
                elif self.__liste_coordonnes_centre_des_nodes[i] == coord2:
                    seconde_ville = villes[i]
                    
            print(premiere_ville.position)
            print(seconde_ville.position)
            routes.append(Route(premiere_ville, seconde_ville))
            
        print("ROUTES :")
        for i in range(len(routes)):
            print(routes[i].longueur)
        
        civ = Civilisation("Civilisation X", nid, food, routes, villes, fourmis)

        self.color_all_roads_black()
        civ.start_simulation()
        self.color_roads(civ.return_path(),routes)
        

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

class Line:
    def __init__(self, canvas, x1, y1, x2, y2):
        print(x1,y1,x2,y2)
        self.__x1, self.__y1, self.__x2, self.__y2= x1,y1,x2,y2
        self.__color = "Black"
        self.__can = canvas  # Il le faut pour les déplacements
        self.__canid = self.__can.create_line( self.__x1, self.__y1, self.__x2, self.__y2,width=3)
        
        taille = math.floor(math.sqrt((x2 - x1)**2 + (y2 - y1)**2))
        self.__textid = self.__can.create_text((self.__x1+self.__x2)/2, (self.__y1+self.__y2)/2 +20, text = taille)
        
        #self.qtPhe = 0
        #self.__label = self.__can.create_text((self.__x1+self.__x2)/2, (self.__y1+self.__y2)/2 - 20, text = math.floor(self.qtPhe*10))
        
        self.noeud_start = (x1, y1)
        self.noeud_end = (x2, y2)

    def get_route_ident(self):
        return self.__canid
    
    def get_pos(self):
        return ((self.__x1, self.__y1),(self.__x2, self.__y2))

    
# --------------------------------------------------------
if __name__ == "__main__":
    fen = FenPrincipale()
    fen.mainloop()
