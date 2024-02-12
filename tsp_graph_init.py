import numpy as np
import random as rd
import time
import pandas
import tkinter as tk
import csv

# traveling salesman problem with genetic algorithm


class Lieu:
    def __init__(self):
        # cooredonnes du lieu à visiter
        self.x = None
        self.y = None
        # nom du lieu
        self.nom = None

    def distance(self, lieu):
        return np.sqrt((self.x - lieu.x)**2 + (self.y - lieu.y)**2)


class Graph:
    def __init__(self):
        self.largeur = 800
        self.hauteur = 800
        self.liste_lieux = []
        self.nb_lieux = 10
        self.matrice_od = None
        self.plus_proche_voisins = None

    def calcul_matrice_cout_od(self):
        self.matrice_od = np.zeros((self.nb_lieux, self.nb_lieux))
        for i in range(self.nb_lieux):
            for j in range(self.nb_lieux):
                self.matrice_od[i, j] = self.liste_lieux[i].distance(self.liste_lieux[j])

    def plus_proche_voisins(self):
        print("Calcul des plus proches voisins")



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