"""
Main Program
"""
# import src.data.data as data

import src.data.FourNodes.four_nodes as test_data
from src.algorithms.b.b import AlgorytmB

DATA_LIST = ['SiouxFalls']


def main():
    # current_city = DATA_LIST[0]
    # [demands, nodes, network] = data.import_data_for_city(current_city)
    # nodes_count = nodes.count()['node']
    [*params] = test_data.get_data()
    calculated = AlgorytmB(*params).CalculateEquilibrium()
    solution = test_data.get_solution()

    assert calculated[0] == solution[
        0], f"expected Equilibrium to be {solution[0]}, got: {calculated[0]}"
    assert calculated[1] == solution[
        1], f"expected delta_c_max to be {solution[1]}, got: {calculated[1]}"


if __name__ == "__main__":
    main()
