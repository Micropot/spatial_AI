import numpy as np
import random as rd
import time
import pandas as pd
import tkinter as tk
import csv

# traveling salesman problem with genetic algorithm
NB_LIEUX = 20


class Lieu:
    def __init__(self, xinit, yinit, nom=""):
        # coordonnes du lieu à visiter
        self.x = xinit
        self.y = yinit
        # nom du lieu
        self.nom = nom

    # calcul la distance entre un point et l'argument de départ
    def distance(self, lieu):
        return np.sqrt((self.x - lieu.x) ** 2 + (self.y - lieu.y) ** 2)

    def __repr__(self):
        return (self.nom + " : " + str(self.x) + " " + str(self.y))


class Graph:
    def __init__(self, csv_file):
        self.largeur = 800
        self.hauteur = 600
        self.liste_lieux = []

        self.matrice_od = None
        self.voisins = None
        self.csv_file = csv_file

    def calcul_matrice_cout_od(self):
        self.matrice_od = np.zeros((NB_LIEUX, NB_LIEUX))
        for i in range(NB_LIEUX):
            for j in range(i + 1, NB_LIEUX):
                self.matrice_od[i, j] = self.liste_lieux[i].distance(self.liste_lieux[j])
                self.matrice_od[j, i] = self.liste_lieux[i].distance(self.liste_lieux[j])
        print("self.matrice_od: ", self.matrice_od)

    def plus_proche_voisins(self, lieu, voisins):
        try:
            voisins.remove(lieu)
        except:
            pass
        ligne = self.matrice_od[lieu, voisins]
        # print("ligne: ", ligne)
        v = voisins[np.argmin(ligne)]
        # print("v: ", v)
        return v

    def charger_graph(self):
        if self.csv_file is not None:
            df = pd.read_csv(self.csv_file)
            print("df: ", df)
            for i in range(len(df)):
                self.liste_lieux.append(Lieu(df['x'][i], df['y'][i]))
            print("self.liste_lieux: ", self.liste_lieux)
            print("len(self.liste_lieux): ", len(self.liste_lieux))

        else:
            # creation de lieux aleatoires
            for i in range(NB_LIEUX):
                self.liste_lieux.append(Lieu(rd.uniform(0, self.largeur), rd.uniform(0, self.hauteur), str(i)))
            print("self.liste_lieux", self.liste_lieux)

    def determination_ordre_ppv(self):
        ordre = [0]
        lieu_actuel = 0
        voisins = list(range(1, NB_LIEUX))
        while len(voisins) > 0:
            lieu_suivant = self.plus_proche_voisins(lieu_actuel, voisins)
            ordre.append(lieu_suivant)
            lieu_actuel = lieu_suivant
            voisins.remove(lieu_suivant)
        ordre.append(0)

        return Route(ordre)

    def calcul_distance_route(self, route):
        distance = 0
        for i in range(0, len(route.ordre) - 1):
            distance += self.matrice_od[route.ordre[i], route.ordre[i + 1]]
        # print("distance: ", distance)
        route.distance = distance
        # print("Route.distance: ", Route.distance)
        return distance


class Route:
    def __init__(self, ordre=None):
        self.distance = None

        if ordre is None:
            # print("Ordre aleatoire:")
            self.ordre = [0]
            self.ordre.extend(rd.sample(range(1, NB_LIEUX), NB_LIEUX - 1))
            self.ordre.append(0)
        else:
            self.ordre = ordre[:]
            if self.ordre[0] != self.ordre[-1]:
                self.ordre.append(ordre[0])

    def __gt__(self, other):
        if self.distance is None or other.distance is None:
            raise ValueError("Distances must be calculated before comparison.")
        return self.distance > other.distance

    def __lt__(self, other):
        if self.distance is None or other.distance is None:
            raise ValueError("Distances must be calculated before comparison.")
        return self.distance < other.distance

    def __neq__(self, other):
        if self.ordre is None or other.ordre is None:
            raise ValueError("Distances must be calculated before comparison.")
        return self.ordre != other.ordre

    def __eq__(self, other):
        if self.ordre is None or other.ordre is None:
            raise ValueError("Distances must be calculated before comparison.")
        return self.ordre == other.ordre

    '''def __le__(self, other):
        if self.distance is None or other.distance is None:
            raise ValueError("Distances must be calculated before comparison.")
        return self.distance <= other.distance'''

    def __repr__(self):
        return f"Ordre : {self.ordre}, Distance : {self.distance}"


class Affichage:
    def __init__(self, graph, ordre, distance):
        self.graph = graph
        self.ordre = ordre
        self.distance = distance
        self.fenetre = tk.Tk()
        self.fenetre.title("Groupe 5 - TSP Genetic Algorithm")

        self.LARGEUR = 800
        self.HAUTEUR = 600

        self.canvas = tk.Canvas(self.fenetre, width=self.LARGEUR, height=self.HAUTEUR, bg="white")
        self.canvas.pack()

        self.texte_info = tk.Text(self.fenetre, height=5, width=50)
        self.texte_info.pack()

        self.fenetre.bind("<Key>", self.gerer_touche)
        self.fenetre.protocol("WM_DELETE_WINDOW", self.quitter)

    def afficher_lieux(self):
        for lieu in self.graph.liste_lieux:
            x, y = lieu.x, lieu.y
            self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="red")
            self.canvas.create_text(x, y, text=lieu.nom, fill="black")

    def afficher_ordre(self, ordre):
        for i in range(len(ordre) - 1):
            x1, y1 = self.graph.liste_lieux[ordre[i]].x, self.graph.liste_lieux[ordre[i]].y
            x2, y2 = self.graph.liste_lieux[ordre[i + 1]].x, self.graph.liste_lieux[ordre[i + 1]].y
            self.canvas.create_line(x1, y1, x2, y2, fill="blue", width=2, dash=(4, 4))

    def afficher_infos(self, infos):
        self.texte_info.delete(1.0, tk.END)
        self.texte_info.insert(tk.END, infos)

    def afficher_matrice_cout(self):
        matrice_cout = self.graph.matrice_od
        texte_matrice = "Matrice de coûts :\n"
        for i in range(len(matrice_cout)):
            for j in range(len(matrice_cout[i])):
                texte_matrice += f"{matrice_cout[i, j]:.2f}\t"
            texte_matrice += "\n"
        self.texte_info.delete(1.0, tk.END)
        self.texte_info.insert(tk.END, texte_matrice)

    def gerer_touche(self, event):
        if event.keysym == "Escape":
            self.quitter()
        elif event.char == 'n':
            self.afficher_ordre(self.ordre)
            self.afficher_matrice_cout()
        elif event.char == 'i':
            infos = f"Distance parcourue : {self.distance:.2f}\n"
            self.afficher_infos(infos)

    def quitter(self):
        self.fenetre.destroy()

    def executer(self):
        self.afficher_lieux()
        self.fenetre.mainloop()


class TSP_GA:
    def __init__(self, graph, population_size, elite_size, mutation_rate, generations):
        self.graph = graph
        self.population_size = population_size
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.population = []

    def initialiser_population(self):
        for i in range(self.population_size):
            self.population.append(Route())
            self.population[i].distance = self.graph.calcul_distance_route(self.population[i])
        print("self.population: ", self.population)
        print("len(self.population): ", len(self.population))

    def selectionner_meilleurs(self):
        self.population = sorted(self.population, reverse=True)
        return self.population[:self.elite_size]
