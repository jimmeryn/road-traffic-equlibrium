"""
Testing funtion
0 - Exit program
1 - Four Nodes test
2 - Braess test
"""
from time import time

import src.data.data as data
from src.algorithms.b.algorithm_b import AlgorithmB
from src.algorithms.calculate_equilibrium import CalculateEquilibrium

DATA_LIST = ['FourNodes', 'SiouxFalls', 'Braess']
ALGORITHMS = {
    1: AlgorithmB,
}

MAX_ERROR = 0.25
MAX_ITERATION_COUNT = 100


def run_test(city_index: int, algorithmIndex: int = 1):
    current_city = DATA_LIST[city_index]
    print(current_city)
    print(f"Importing {current_city} data...")
    [demands, nodes, network] = data.import_data_for_city(current_city)
    print("Data imported.")

    print("Creating algorithm and data structures...")
    try:
        algorithm = ALGORITHMS[algorithmIndex](
            nodes.values.tolist(),
            network.values.tolist(),
            demands,
            MAX_ERROR
        )
    except (IndexError, ValueError):
        print("Error during algorithm initialisation...")
    print("Created algorithm.")
    print(f"Test started for {current_city}...")
    start_time = time()
    CalculateEquilibrium(algorithm, MAX_ERROR, MAX_ITERATION_COUNT).Run()
    print(f"Test end after {time() - start_time} sec.")
    return
