import tsp_graph_init


def main():
    MyGraph = tsp_graph_init.Graph(csv_file=None)
    MyGraph.charger_graph()
    MyGraph.calcul_matrice_cout_od()


if __name__ == '__main__':
    main()

