"""Algorithm B Class"""
import math
from typing import Tuple

from src.shared.graph import Graph
from src.shared.link import Link


class AlgorytmB:
    """
    Class used to represent B Algorthm

    ...

    Attributes:
    ----------
    graph : Graph
        Graph containing nodes and links
    m : int
        Upper bound on number of arcs on a path — a scalar
    e : float
        Upper bound on max-min path cost differential — a scalar

    Methods:
    -------
    CalculateEquilibrium(A, n, x, c, c_der, m: int, e: float):
        Calculates Equilibrium using B Algorithm - the main procedure,
        swap flow between paths between paths,
        until the max difference between max and min path cost drops to a given level e.
    ShiftFlow()
        Discovering arc-independent max and min paths to each node and transfers flow
        between paths to equalize their costs.
    GetBranchNode(j: int)
        Calculate start node k being the only node p_max and p_min have in common
        (except their shared end node j).
    UpdateTrees(k: int, n: int) -> float
        Updates max and min path potentials (pi_max, pi_min) and pedecessor labels (alpha_max, alpha_min).
    EqualizePathCost(k: int, j: int, x_min, x_max, c_min, c_max, c_der_min, c_der_max, exp_factor)
        Move certain amout of flow (delta_x) from p_max to p_min to equilize costs c_max and c_min (Newton's method).
    GetDeltaXandC(x_min, x_max, c_min, c_max, c_der_min, c_der_max)
        Calculate increment flow (delta_x) and current max and min paths (x_min, x_max) cost difference (delta_c).
    UpdatePathFlow(delta_x: int, k: int, j: int, alpha)
        Update all arcs on a given path by changing their flow (update by delta_x)
        and update costs (k - start node, j - end node).
    """

    def __init__(
        self,
        graph: Graph,
        m: int,
        e: float,
    ):
        self.m = m
        self.e = e
        self.graph = graph
        self.k_hat = 1

    def CalculateEquilibrium(self) -> Tuple[Graph, float]:
        delta_c_max = self.UpdateTrees(1, self.graph.n + 1)
        iteration = 0
        max_iteration_count = 100
        while self.e < delta_c_max and iteration < max_iteration_count:
            iteration += 1
            self.ShiftFlow()
            delta_c_max = self.UpdateTrees(1, self.graph.n + 1)
            self.graph.LogFlow()

        return (self.graph, delta_c_max)

    def ShiftFlow(self):
        for j in range(self.graph.n, 2, -1):
            node = self.graph.nodes[j]
            if node.alpha_max and node.pi_min < node.pi_max:
                [k, *params] = self.GetBranchNode(j)
                if k > 0:
                    self.EqualizeCost(k, j, *params)
                    # TODO create RelabelNodes function
                    # RelabelNodes(k, j)
                    # self.x[j], self.x[k] = self.x[k], self.x[j]
                    self.k_hat = k

    def GetBranchNode(self, j: int):
        ij_min = self.graph.nodes[j].alpha_min
        ij_max = self.graph.nodes[j].alpha_max
        x_min = ij_min.flow
        x_max = ij_max.flow
        c_min = ij_min.cost
        c_max = ij_max.cost
        c_der_min = ij_min.cost_der
        c_der_max = ij_max.cost_der
        m_min = 1
        m_max = 1
        while ij_max.src != ij_min.src:
            while ij_min.src < ij_max.src:
                ij_max = self.graph.nodes[ij_max.src].alpha_max
                x_max = min(x_max, ij_max.flow)

                c_max += ij_max.cost
                c_der_max += ij_max.cost_der
                m_max += 1

            while ij_max.src < ij_min.src:
                ij_min = self.graph.nodes[ij_min.src].alpha_min
                x_min = min(x_min, ij_min.flow)

                c_min += ij_min.cost
                c_der_min += ij_min.cost_der
                m_min += 1

        exp_factor = 1 + math.floor(self.m - max(m_min, m_max) / 2)
        condition = exp_factor * (c_max - c_min) < self.e
        k = 0 if condition else ij_max.src

        return [k, x_min, x_max, c_min, c_max, c_der_min, c_der_max, exp_factor]

    def UpdateTrees(self, k: int, n: int) -> float:
        delta_c_max = 0
        # self.graph.nodes[k].pi_max = 0.0
        # self.graph.nodes[k].alpha_max = None

        for j in range(k + 1, n - 1):
            dest_node = self.graph.nodes[j]
            dest_node.pi_min = math.inf
            dest_node.pi_max = -math.inf
            dest_node.alpha_min = None
            dest_node.alpha_max = None
            for link in self.graph.links.values():
                src_node = self.graph.nodes[link.src]

                # min distance
                new_cost = src_node.pi_min + link.cost
                if new_cost < dest_node.pi_min:
                    dest_node.pi_min = new_cost
                    dest_node.alpha_min = link

                # max distance
                new_cost = src_node.pi_max + link.cost
                if (
                    src_node.alpha_min is not None and
                    link.flow != 0 and
                    new_cost > dest_node.pi_max
                ):
                    dest_node.pi_max = new_cost
                    dest_node.alpha_max = link

            if dest_node.alpha_max is not None:
                delta_c_max = max(
                    self.GetPiDiff(),
                    delta_c_max
                )

        return delta_c_max

    def GetPiDiff(self):
        pi_max_array = map(lambda node: node.pi_max, self.graph.nodes.values())
        pi_min_array = map(lambda node: node.pi_min, self.graph.nodes.values())

        return max(pi_max_array) - min(pi_min_array)

    def EqualizeCost(
        self,
        k: int,
        j: int,
        x_min: int,
        x_max: int,
        c_min: float,
        c_max: float,
        c_der_min: float,
        c_der_max: float,
        exp_factor: int,
    ) -> None:
        [delta_x, delta_c] = self.GetDeltaXandC(
            x_min, x_max, c_min, c_max, c_der_min, c_der_max)
        while self.e < exp_factor * delta_c:
            [
                x_min,
                c_min,
                c_der_min
            ] = self.UpdatePathFlow(delta_x, k, j, "alpha_min")
            [
                x_max,
                c_max,
                c_der_max
            ] = self.UpdatePathFlow(-delta_x, k, j, "alpha_max")
            [
                delta_x,
                delta_c
            ] = self.GetDeltaXandC(x_min, x_max, c_min, c_max, c_der_min, c_der_max)
            self.graph.SetLinksCosts()
        return

    def GetDeltaXandC(
        self,
        x_min: int,
        x_max: int,
        c_min: float,
        c_max: float,
        c_der_min: float,
        c_der_max: float
    ) -> Tuple[int, float]:
        delta_x_max = x_max if c_min < c_max else x_min
        if delta_x_max <= 0:
            return (0, 0.0)
        if c_der_max + c_der_min <= 0:
            delta_x = x_max if c_min <= c_max else -x_min
        else:
            cost = (c_max - c_min) / (c_der_max + c_der_min)
            delta_x = min(delta_x_max, cost)

        return (delta_x, abs(c_max - c_min))

    def UpdatePathFlow(self, delta_x: int, k: int, j: int, alpha_param: str) -> Tuple[int, float, float]:
        x_p = math.inf
        c_p = 0.0
        c_der_p = 0.0
        i = j
        while i != k:
            link: Link | None = self.graph.nodes[i][alpha_param]
            src = link.src
            dest = link.dest
            link.AddFlow(delta_x)
            x_ij = link.flow
            x_p = min(x_p, x_ij)

            c_p += self.graph.GetLink(src, dest).cost
            c_der_p += self.graph.GetLink(src, dest).cost_der
            i = src

        return (x_p, c_p, c_der_p)
