import tsp_graph_init


def main():
    MyGraph = tsp_graph_init.Graph(csv_file="/Users/arthurlamard/Documents/ISEN5/spacial_AI/lieux/graph_20.csv")
    MyGraph.charger_graph()
    MyGraph.calcul_matrice_cout_od()
    #MyGraph.plus_proche_voisins(lieu=0, voisins=list(range(MyGraph.nb_lieux)))


    #Route_ppv = MyGraph.determination_ordre_ppv()
    #Route_ppv.distance = MyGraph.calcul_distance_route(Route_ppv)


    #Route aléatoire
    #MyRoute = tsp_graph_init.Route(ordre=None)
    #print("ordre route ppv : ",MyGraph.determination_ordre_ppv())
    #print("ordre route aléatoire : ",MyRoute)
    #MyRoute.distance = MyGraph.calcul_distance_route(MyRoute)
    #print("distance route aléatoire : ",distance)


    #affichage = tsp_graph_init.Affichage(MyGraph, ordre=Route_ppv.ordre, distance=Route_ppv.distance)
    #affichage.executer()


    #print("GRAPH_ppv : ",Route_ppv)
    #print("ROUTE_aléatoire : ",MyRoute)

    algo = tsp_graph_init.TSP_GA(MyGraph, population_size=10, elite_size=5, mutation_rate=0.5, generations=150)
    #algo.initialiser_population()
    #algo.selectionner_meilleurs()
    algo.run_algo()


if __name__ == '__main__':
    main()

