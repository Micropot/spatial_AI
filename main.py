import tsp_graph_init


def main():
    MyGraph = tsp_graph_init.Graph(csv_file=None)
    MyGraph.charger_graph()
    MyGraph.calcul_matrice_cout_od()
    #MyGraph.plus_proche_voisins(lieu=0, voisins=list(range(MyGraph.nb_lieux)))
    #MyGraph.determination_ordre_ppv()
    MyGraph.calcul_distance_route(MyGraph.determination_ordre_ppv())
    #Route aléatoire
    MyRoute = tsp_graph_init.Route(ordre=None)
    print("ordre route aléatoire : ",MyRoute.ordre)
    MyGraph.calcul_distance_route(MyRoute)
if __name__ == '__main__':
    main()
