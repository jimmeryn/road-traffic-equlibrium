"""
Testing funtion
0 - Exit program
1 - Four Nodes test
"""
from time import time

import src.data.data as data
from src.algorithms.b.algorithm_b import AlgorytmB
from src.shared.graph import Graph

DATA_LIST = ['FourNodes', 'SiouxFalls']


def run_test(city_index: int):
    start_time = time()
    print(f"Test started for {DATA_LIST[city_index]}...")

    current_city = DATA_LIST[city_index]
    [demands, nodes, network] = data.import_data_for_city(current_city)

    # pylint: disable=no-member
    graph = Graph(nodes.values.tolist(), network.values.tolist(), demands)

    calculated = AlgorytmB(graph, 3, 0.25).CalculateEquilibrium()
    print(calculated[1])
    print(calculated[0].GetFlowArray())
    print(f"Test end after {time() - start_time} sec.")
    return
