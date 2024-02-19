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
        # print("self.matrice_od: ", self.matrice_od)

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
            #print("df: ", df)
            for i in range(len(df)):
                self.liste_lieux.append(Lieu(df['x'][i], df['y'][i]))
            # print("self.liste_lieux: ", self.liste_lieux)
            # print("len(self.liste_lieux): ", len(self.liste_lieux))

        else:
            # creation de lieux aleatoires
            for i in range(NB_LIEUX):
                self.liste_lieux.append(Lieu(rd.uniform(0, self.largeur), rd.uniform(0, self.hauteur), str(i)))
            # print("self.liste_lieux", self.liste_lieux)

    def determination_ordre_ppv(self, lieu_actuel):
        ordre = [lieu_actuel]
        voisins = list(range(NB_LIEUX))
        voisins.remove(lieu_actuel)
        while len(voisins) > 0:
            lieu_suivant = self.plus_proche_voisins(lieu_actuel, voisins)
            ordre.append(lieu_suivant)
            lieu_actuel = lieu_suivant
            voisins.remove(lieu_suivant)
        ordre.append(ordre[0])  # Return to the starting point
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
        if self.ordre == other.ordre and self.distance == other.distance:
            return True
        # return self.ordre == other.ordre

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
        for index, lieu in enumerate(self.graph.liste_lieux):
            x, y = lieu.x, lieu.y
            fill_color = "red" if index == 0 else "white"
            # Display the index in the oval
            self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill=fill_color, outline="black")
            self.canvas.create_text(x, y, text=str(index), fill="black")

    def afficher_numero(self, ordre):
        for i, node_index in enumerate(ordre[:-1]):
            lieu = self.graph.liste_lieux[node_index]
            x, y = lieu.x, lieu.y

            # Display the order above the circle
            self.canvas.create_text(x, y - 15, text=str(i), fill="black")

    def afficher_ordre(self, ordre, color):
        for i in range(len(ordre) - 1):
            x1, y1 = self.graph.liste_lieux[ordre[i]].x, self.graph.liste_lieux[ordre[i]].y
            x2, y2 = self.graph.liste_lieux[ordre[i + 1]].x, self.graph.liste_lieux[ordre[i + 1]].y
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2, dash=(4, 4))

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
            self.afficher_ordre(self.ordre, 'gray')
            self.afficher_matrice_cout()
        elif event.char == 'i':
            infos = f"Distance parcourue : {self.distance:.2f}\n"
            self.afficher_infos(infos)
        #pause the program
        elif event.char == 'p':
            time.sleep(5)
    def quitter(self):
        self.fenetre.destroy()

    def executer(self, ordre, best_distance, iterations):
        #self.afficher_lieux()
        #self.afficher_ordre(ordre, 'blue')
        for i in range(len(ordre) - 1):
            self.canvas.delete('all')

            self.afficher_ordre(ordre, 'blue')

            info_text = f"Meilleure distance : {best_distance}\n"
            info_text += f"Iterations : {iterations}\n"

            self.afficher_infos(info_text)
            self.afficher_numero(ordre)
        self.afficher_lieux()
        self.fenetre.update()
        self.fenetre.update_idletasks()
        #self.fenetre.mainloop()


class TSP_GA:
    def __init__(self, graph, population_size, elite_size, mutation_rate, generations):
        self.graph = graph
        self.population_size = population_size
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.population = []
        self.best_route = None
        self.depart = None
        self.pair = []

    def initialiser_population(self):
        self.depart = [self.graph.determination_ordre_ppv(lieu_actuel=i) for i in range(NB_LIEUX)]

        for i in range(len(self.depart)):
            self.depart[i].distance = self.graph.calcul_distance_route(self.depart[i])
            # print(self.depart[i])
            # find 0
            index = self.depart[i].ordre.index(0)
            # print("index: ", index)
            # copy the list from index to the 0 included without the duplicates

            self.depart[i].ordre = self.remove_consecutive_duplicates(
                self.depart[i].ordre[index:] + self.depart[i].ordre[:index + 1])
            self.depart[i].distance = self.graph.calcul_distance_route(self.depart[i])
            # print("self.depart[i]",self.depart[i])
            self.population = self.depart
        for route in self.depart:
            route.distance = self.graph.calcul_distance_route(route)

        # print("self.depart: ", self.depart)
        # print("self.population: ", self.population)
        return self.population

    def selectionner_meilleurs(self):
        self.population = sorted(self.population, reverse=False)
        self.best_route = self.population[:self.elite_size]
        # print("self.best_route: ", self.best_route)
        return self.best_route

    def remove_consecutive_duplicates(self, route_ordre):
        result = [route_ordre[0]]  # Add the first element of the list

        for i in range(1, len(route_ordre)):
            if route_ordre[i] != route_ordre[i - 1]:
                result.append(route_ordre[i])

        return result

    def ox_crossover(self, parent1, parent2):
        #size = len(parent1.ordre)
        # Choose two random crossover points
        point1, point2 = sorted(rd.sample(range(1, NB_LIEUX - 1), 2))
        # print("point1: ", point1)
        # print("point2: ", point2)

        # Initialize the child ordre with a copy of the segment between the crossover points from parent1
        child_ordre = parent1.ordre[point1:point2]

        # Fill in the remaining positions with genes from parent2, preserving order
        remaining_genes = [gene for gene in parent2.ordre if gene not in child_ordre]
        child_ordre.extend(remaining_genes)

        # Create a new route for the child with the modified order
        child_route = Route(ordre=child_ordre)
        child_route.distance = self.graph.calcul_distance_route(child_route)

        return child_route

    def mutation(self, route):
        print("mutation")
        # 2-opt mutation implementation
        # Randomly select two positions in the route
        pos1, pos2 = sorted(rd.sample(range(1, NB_LIEUX - 1), 2))

        # Apply the 2-opt mutation
        route.ordre[pos1:pos2] = route.ordre[pos1:pos2][::-1]
        route.distance = self.graph.calcul_distance_route(route)

        return route



    def run_algo(self):
        #TODO : touche pour afficher ou non les meilleurs routes + pause ?



        year = 0
        unchanged_years = 0
        # Run the genetic algorithm
        self.initialiser_population()
        affichage = Affichage(self.graph, self.population[0].ordre, self.population[0].distance)


        # affichage.afficher_ordre(self.population[0].ordre)
        # affichage.executer(self.population[0].ordre)




        while year < self.generations:
            affichage.fenetre.bind("<Key>", affichage.gerer_touche)
            best = self.selectionner_meilleurs()
            #last_best = best[0]
            # affichage = Affichage(self.graph, self.best_route[0].ordre, self.best_route[0].distance)
            for current, next_element in zip(best, best[1:] + [best[0]]):
                if current != next_element:
                    self.pair.append((current, next_element))
                else:
                    # print("current: ", current)
                    # print("next_element: ", next_element)
                    if rd.random() < self.mutation_rate:
                        mutation = self.mutation(current)
                        # print("mutation: ", mutation)
                        # on ajoute la mutation à la population
                        self.pair.append((current, mutation))

            # print("self.pair: ", self.pair)
            # print('len(self.pair): ', len(self.pair))

            for i in range(len(self.pair)):

                # Create two children from each pair of parents
                for j in range(2):
                    child = self.ox_crossover(self.pair[i][0], self.pair[i][1])

                    self.population.append(child)


            print(f"generation {year} : {best}")
            year += 1

            '''if last_best != best[0]:
                unchanged_years = 0
            else:
                unchanged_years += 1
            print("unchanged_years: ", unchanged_years)

            # Exit if no change for 5 consecutive years
            if unchanged_years >= 10:
                print("No change for 5 consecutive years. Exiting.")
                break'''

            affichage.executer(self.best_route[0].ordre, self.best_route[0].distance, year)
        affichage.fenetre.mainloop()