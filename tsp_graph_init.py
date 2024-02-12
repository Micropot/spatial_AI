import numpy as np
import random as rd
import time
import pandas
import tkinter as tk
import csv

# traveling salesman problem with genetic algorithm


class Lieu:
    def __init__(self):

        self.x = None
        self.y = None


class Graph:
    def __init__(self):
        self.largeur = 800
        self.hauteur = 800



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