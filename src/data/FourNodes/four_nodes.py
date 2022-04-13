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

    l12 = Link(0, 1, 2)
    l14 = Link(0, 3, 4)
    l23 = Link(1, 2, 1)
    l24 = Link(1, 3, 2)
    l34 = Link(2, 3, 1)
    A = {l12, l14, l23, l24, l34}

    n = 3

    # arc cost
    c = [
        [0.0, 114.0, 0.0, 172.0],
        [0.0, 0.0, 26.0, 62.0],
        [0.0, 0.0, 0.0, 26.0],
        [0.0, 0.0, 0.0, 0.0]
    ]

    c_der = [
        [0.0, 114.0, 0.0, 172.0],
        [0.0, 0.0, 26.0, 62.0],
        [0.0, 0.0, 0.0, 26.0],
        [0.0, 0.0, 0.0, 0.0]
    ]
    m_hat = 3

    e = 0.25

    x = flow

    # min path array
    pi_min = [
        0,
        114,
        140,
        176,
    ]

    # max path array
    pi_max = [
        0,
        114,
        140,
        166,
    ]

    # min predecessor arc array (set of Links) TODO: fix
    alpha_min: dict[int, Link | None] = [
        None,
        l12,
        l23,
        l34,
    ]

    # max predecessor arc array (set of Links) TODO: fix
    alpha_max: dict[int, Link | None] = [
        None,
        l12,
        l23,
        l24,
    ]

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
