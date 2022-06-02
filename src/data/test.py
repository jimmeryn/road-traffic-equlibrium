""" Testing funtion """
import os
from time import time

import src.data.data as data
from results.root import ROOT_DIR
from src.algorithms.algorithm import Algorithm
from src.algorithms.b.algorithm_b import AlgorithmB
from src.algorithms.calculate_equilibrium import CalculateEquilibrium
from src.algorithms.oba.oba import OBA
from src.algorithms.tapas.tapas import TAPAS
from src.utils.logger import Logger

DATA_LIST = {
    1: 'FourNodes',
    2: 'Braess',
    3: 'NineNodes',
    4: 'SiouxFalls',
    5: 'ChicagoSketch',
    6: 'SiouxFalls2',
    7: 'SiouxFalls21',
    8: 'SiouxFalls3',
}
ALGORITHMS = {
    1: AlgorithmB,
    2: TAPAS,
    3: OBA,
}


def run_test(
    city_index: int,
    algorithmIndex: int,
    max_error: float | int,
    max_iteration_count: int,
    compare_solution: bool = False
):
    try:
        current_city = DATA_LIST[city_index]
        print(current_city)
        print(f"Importing {current_city} data...")
        (demands, nodes, network, solution) = data.import_data_for_city(current_city)
        print("Data imported.")
    except (IndexError, ValueError):
        print("Error during data importing...")
        return

    print("Creating algorithm and data structures...")
    try:
        algorithm: Algorithm = ALGORITHMS[algorithmIndex](
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
    file_name = f"results-{algorithm.__class__.__name__}-{current_city}.csv"
    full_result_file_name = os.path.join(ROOT_DIR, file_name)
    metadata_file_name = f"data-{algorithm.__class__.__name__}-{current_city}.csv"
    full_metadata_file_name = os.path.join(ROOT_DIR, metadata_file_name)
    with (
        open(full_result_file_name, 'w+', encoding="utf-8") as file,
        open(full_metadata_file_name, 'w+', encoding="utf-8") as data_file
    ):
        start_time = time()
        network = CalculateEquilibrium(
            algorithm,
            max_error,
            max_iteration_count
        ).Run(file, data_file)
        data_file.write(f"Time(sec),{time() - start_time}\n")

    if compare_solution:
        Logger.CompareSolution(solution, network)
        Logger.TestSolution(solution, network)

    print(f"The results are available at: {full_result_file_name}")
    print(f"The metadata is available at: {full_metadata_file_name}")

    return
