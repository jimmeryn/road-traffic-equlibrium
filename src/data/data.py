"""Data"""

import os
from ast import literal_eval

import numpy as np
import pandas as pd

PYCACHE = '__pycache__'

COL_DEF: dict[str, int] = {
    "init_node": 0,
    "term_node": 1,
    "capacity": 2,
    "length": 3,
    "free_flow_time": 4,
    "b": 5,
    "power": 6,
    "speed_limit": 7,
    "toll": 8,
    "link_type": 9,
}


def get_root():
    file_path = os.path.realpath(__file__)
    root = os.path.dirname(file_path)

    return root


def get_all_data():
    root = get_root()
    all_folders = [
        x for x in os.listdir(root)[1:]
        if os.path.isdir(os.path.join(root, x))
    ]
    folders = list(
        filter(
            lambda folder_name: (
                folder_name != PYCACHE
            ),
            all_folders
        )
    )

    return folders


def get_network_for_city(city_name: str) -> pd.DataFrame:
    root = get_root()
    netfile = os.path.join(root, city_name, f'{city_name}_net.tntp')
    net = pd.read_csv(netfile, skiprows=8, sep='\t')
    trimmed = [s.strip().lower() for s in net.columns]
    net.columns = trimmed
    # This is an unresolved issue with pandas: https://github.com/PyCQA/pylint/issues/4577
    # pylint: disable=no-member
    net.drop(['~', ';'], axis=1, inplace=True)

    return net


def get_nodes_for_city(city_name: str) -> pd.DataFrame:
    root = get_root()
    nodesfile = os.path.join(root, city_name, f'{city_name}_node.tntp')
    nodes = pd.read_csv(nodesfile, skiprows=0, sep='\t')
    trimmed = [s.strip().lower() for s in nodes.columns]
    nodes.columns = trimmed
    # pylint: disable=no-member
    nodes.drop([';'], axis=1, inplace=True)

    return nodes


def import_matrix(city_name):
    root = get_root()
    tripsfile = os.path.join(root, city_name, f'{city_name}_trips.tntp')
    with open(tripsfile, 'r', encoding='utf-8') as file:
        all_rows = file.read()
        blocks = all_rows.split('Origin')[1:]
        matrix = {}
        for index, _ in enumerate(blocks):
            orig = blocks[index].split('\n')
            dests = orig[1:]
            orig = int(orig[0])

            destination_array = [literal_eval('{'+a.replace(';', ',').replace(' ', '') + '}')
                                 for a in dests]
            destinations = {}
            for i in destination_array:
                destinations = {**destinations, **i}
            matrix[orig] = destinations
        zones = max(matrix.keys())
        mat = np.zeros((zones, zones))
        for i in range(zones):
            for j in range(zones):
                # We map values to a index i-1, as Numpy is base 0
                mat[i, j] = matrix.get(i+1, {}).get(j+1, 0)

        index = np.arange(zones) + 1
        return mat


def import_data_for_city(city_name):
    demands = import_matrix(city_name)
    nodes = get_nodes_for_city(city_name)
    network = get_network_for_city(city_name)

    return [demands, nodes, network]
