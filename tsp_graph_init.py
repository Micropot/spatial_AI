import numpy as np
import random as rd
import time
import pandas
import tkinter as tk
import csv


# traveling salesman problem with genetic algorithm


class Lieu:
    def __init__(self, xinit, yinit, nom):
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
        self.nb_lieux = 10
        self.matrice_od = None
        self.plus_proche_voisins = None
        self.csv_file = csv_file


    def calcul_matrice_cout_od(self):
        self.matrice_od = np.zeros((self.nb_lieux, self.nb_lieux))
        for i in range(self.nb_lieux):
            for j in range(self.nb_lieux):
                self.matrice_od[i, j] = self.liste_lieux[i].distance(self.liste_lieux[j])

    def plus_proche_voisins(self):
        print("Calcul des plus proches voisins")

    def charger_graph(self):
        if self.csv_file is not None:
            with open(self.csv_file, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    self.liste_lieux.append(Lieu(int(row[0]), int(row[1]), row[2]))
        else:
            # creation de lieux aleatoires
            for i in range(self.nb_lieux):
                self.liste_lieux.append(Lieu(rd.randint(0, self.largeur), rd.randint(0, self.hauteur), str(i)))


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
