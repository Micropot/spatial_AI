import tsp_graph_init


def main():
    MyGraph = tsp_graph_init.Graph("/Users/arthurlamard/Documents/ISEN5/spacial_AI/lieux/graph_5.csv")
    MyGraph.charger_graph()


if __name__ == '__main__':
    main()

