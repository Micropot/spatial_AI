import tsp_graph_init


def main():
    MyGraph = tsp_graph_init.Graph(csv_file=None)
    MyGraph.charger_graph()
    MyGraph.calcul_matrice_cout_od()
    MyGraph.plus_proche_voisins(lieu=0, voisins=list(range(MyGraph.nb_lieux)))


if __name__ == '__main__':
    main()
