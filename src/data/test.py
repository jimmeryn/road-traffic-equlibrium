"""
Testing funtion
0 - Exit program
1 - Four Nodes test
2 - Braess test
"""
from time import time

import src.data.data as data
from src.algorithms.b.algorithm_b import AlgorytmB
from src.shared.graph import Graph

DATA_LIST = ['FourNodes', 'SiouxFalls', 'Braess']


def run_test(city_index: int):
    current_city = DATA_LIST[city_index]
    print(f"Importig {current_city} data...")
    [demands, nodes, network] = data.import_data_for_city(current_city)
    print("Data imported.")

    # pylint: disable=no-member
    print("Creating graph...")
    graph = Graph(nodes.values.tolist(), network.values.tolist(), demands)
    print("Graph created.")

    print(f"Test started for {current_city}...")
    start_time = time()
    calculated = AlgorytmB(graph, 3, 0.25).CalculateEquilibrium()
    print(f"Test end after {time() - start_time} sec.")
    print(calculated[1])
    print(calculated[0].GetFlowArray())
    return
