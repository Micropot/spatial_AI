import tsp_graph_init


def main():
    MyGraph = tsp_graph_init.Graph(csv_file=None)
    MyGraph.charger_graph()
    MyGraph.calcul_matrice_cout_od()
    #MyGraph.plus_proche_voisins(lieu=0, voisins=list(range(MyGraph.nb_lieux)))

    ordre = [0]
    lieu_actuel= 0
    voisins = list(range(1,MyGraph.nb_lieux))
    while len(voisins) > 0:
        lieu_suivant = MyGraph.plus_proche_voisins(lieu_actuel, voisins)
        ordre.append(lieu_suivant)
        lieu_actuel = lieu_suivant
        voisins.remove(lieu_suivant)
    ordre.append(0)
    print("ordre: ", ordre)

if __name__ == '__main__':
    main()
