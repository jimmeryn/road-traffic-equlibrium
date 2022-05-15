""" Testing funtion """
from time import time

import src.data.data as data
from src.algorithms.b.algorithm_b import AlgorithmB
from src.algorithms.calculate_equilibrium import CalculateEquilibrium
from src.utils.logger import Logger

# from src.algorithms.oba.oba import OBA
# from src.algorithms.tapas.tapas import TAPAS

DATA_LIST = {
    1: 'FourNodes',
    2: 'Braess',
    3: 'NineNodes',
    4: 'SiouxFalls',
}
ALGORITHMS = {
    1: AlgorithmB,
    # 2: TAPAS,
    # 3: OBA,
}


def run_test(
    city_index: int,
    algorithmIndex: int,
    max_error: float | int,
    max_iteration_count: int
):
    try:
        current_city = DATA_LIST[city_index]
        print(current_city)
        print(f"Importing {current_city} data...")
        (demands, nodes, network, solution) = data.import_data_for_city(current_city)
        print("Data imported.")
    except (IndexError, ValueError):
        print("Error during data importing...")

    print("Creating algorithm and data structures...")
    try:
        algorithm = ALGORITHMS[algorithmIndex](
            nodes.values.tolist(),
            network.values.tolist(),
            demands,
            max_error
        )
    except (IndexError, ValueError) as error:
        print(f"Error during algorithm initialisation...\n{error}\n")
        return
    print("Created algorithm.")
    print(f"Test started for {current_city}...")
    start_time = time()
    network = CalculateEquilibrium(
        algorithm,
        max_error,
        max_iteration_count
    ).Run()
    print(f"Test end after {time() - start_time} sec.")

    Logger.CompareSolution(solution, network)
    Logger.TestSolution(solution, network)
    return
