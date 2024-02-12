import numpy as np
import random as rd
import time
import pandas as pd
import tkinter as tk
import csv


# traveling salesman problem with genetic algorithm


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
        self.nb_lieux = 4
        self.matrice_od = None
        self.voisins = None
        self.csv_file = csv_file


    def calcul_matrice_cout_od(self):
        self.matrice_od = np.zeros((self.nb_lieux, self.nb_lieux))
        for i in range(self.nb_lieux):
            for j in range(i+1,self.nb_lieux):
                self.matrice_od[i, j] = self.liste_lieux[i].distance(self.liste_lieux[j])
                self.matrice_od[j, i] = self.liste_lieux[i].distance(self.liste_lieux[j])
        print("self.matrice_od: ", self.matrice_od)

    def plus_proche_voisins(self, lieu, voisins):
        try:
            voisins.remove(lieu)
        except:
            pass
        ligne = self.matrice_od[lieu, voisins]
        print("ligne: ", ligne)
        v = voisins[np.argmin(ligne)]
        print("v: ", v)
        return v

    def charger_graph(self):
        if self.csv_file is not None:
            df = pd.read_csv(self.csv_file)
            for i in range(len(df)):
                self.liste_lieux.append(Lieu(df['x'][i], df['y'][i]))

        else:
            # creation de lieux aleatoires
            for i in range(self.nb_lieux):
                self.liste_lieux.append(Lieu(rd.uniform(0, self.largeur), rd.uniform(0, self.hauteur), str(i)))
        print("self.liste_lieux", type(self.liste_lieux[0]))

    def calcul_distance_route(self):
        ordre = [0]
        lieu_actuel = 0
        voisins = list(range(1, self.nb_lieux))
        while len(voisins) > 0:
            lieu_suivant = self.plus_proche_voisins(lieu_actuel, voisins)
            ordre.append(lieu_suivant)
            lieu_actuel = lieu_suivant
            voisins.remove(lieu_suivant)
        ordre.append(0)
        print("ordre: ", ordre)


class Route:
    def __init__(self):
        self.ordre = None


class Affichage:
    def __init__(self):
        self.graph = Graph()
        self.root = tk.Tk()
        self.root.title("TSP")
        self.canvas = tk.Canvas(self.root, width=self.graph.largeur, height=self.graph.hauteur, bg="white")
        self.canvas.pack()
        self.root.mainloop()
