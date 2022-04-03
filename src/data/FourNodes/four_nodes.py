"""
Four nodes - data for testing purpouses
Graph with 4 nodes and 5 edges
"""
from typing import List, Tuple

from src.shared.link import Link


def get_data():
    # Nodes
    nodes = [0, 1, 2, 3]

    # Initial arc Flow (x)
    flow = [
        [0, 57, 0, 43],
        [0, 0, 26, 31],
        [0, 0, 0, 26],
        [0, 0, 0, 0]
    ]

    A = {
        Link(0, 1, 1),
        Link(0, 3, 3),
        Link(1, 2, 0),
        Link(1, 3, 1),
        Link(2, 3, 0),
    }

    n = len(nodes)

    # arc cost
    c = [
        [0, 114, 0, 172],
        [0, 0, 26, 31],
        [0, 0, 0, 26],
        [0, 0, 0, 0]
    ]

    c_der = [
        [0, 114, 0, 172],
        [0, 0, 26, 31],
        [0, 0, 0, 26],
        [0, 0, 0, 0]
    ]
    m_hat = 3

    e = 0.25

    x = flow

    # min path array
    pi_min = {
        0: 0,
        1: 114,
        2: 140,
        3: 176,
    }

    # max path array
    pi_max = {
        0: 0,
        1: 114,
        2: 140,
        3: 166,
    }

    # min predecessor arc array (set of Links) TODO: fix
    alpha_min: dict[int, Link] = {
        0: 0,
        1: 114,
        2: 140,
        3: 176,
    }

    # max predecessor arc array (set of Links) TODO: fix
    alpha_max: dict[int, Link] = {
        0: 0,
        1: 114,
        2: 140,
        3: 176,
    }

    return [
        A,
        n,
        c,
        c_der,
        m_hat,
        e,
        x,
        pi_max,
        pi_min,
        alpha_max,
        alpha_min
    ]


def get_solution() -> Tuple[List[List[int]], float]:
    equilibrium = [[0, 57, 0, 42], [0, 0, 28, 28], [0, 0, 0, 28], [0, 0, 0, 0]]
    delta_c_max = 0.25

    return (equilibrium, delta_c_max)
