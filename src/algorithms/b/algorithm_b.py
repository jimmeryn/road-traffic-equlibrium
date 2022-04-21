"""Algorithm B Class"""
import math
from typing import List, Tuple

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
        Upper bound on max-min path cost differential—a scalar

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
        self.k_hat = 0

    def CalculateEquilibrium(self) -> Tuple[List[List[int]], float]:
        delta_c_max = self.UpdateTrees(1, self.graph.n + 1)
        while self.e < delta_c_max:
            self.ShiftFlow()
            delta_c_max = self.UpdateTrees(self.k_hat, self.graph.n + 1)

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
        x_min = self.graph.GetLink(ij_min.src, ij_min.dest).flow
        x_max = self.graph.GetLink(ij_max.src, ij_max.dest).flow
        c_min = self.graph.GetLink(ij_min.src, ij_min.dest).cost
        c_max = self.graph.GetLink(ij_max.src, ij_max.dest).cost
        c_der_min = self.graph.GetLink(ij_min.src, ij_min.dest).cost_der
        c_der_max = self.graph.GetLink(ij_max.src, ij_max.dest).cost_der
        m_min = 1
        m_max = 1
        while ij_max.src != ij_min.src:
            while ij_min.src < ij_max.src:
                ij_max = self.graph.nodes[ij_max.src].alpha_max
                x_max = min(
                    x_max, self.graph.GetLink(ij_max.src, ij_max.dest).flow)

                c_max += self.graph.GetLink(ij_max.src, ij_max.dest).cost
                c_der_max += self.graph.GetLink(ij_max.src,
                                                ij_max.dest).cost_der
                m_max += 1

            while ij_max.src < ij_min.src:
                ij_min = self.graph.nodes[ij_min.src].alpha_min
                x_min = min(
                    x_min, self.graph.GetLink(ij_min.src, ij_min.dest).flow)

                c_min += self.graph.GetLink(ij_min.src, ij_min.dest).cost
                c_der_min += self.graph.GetLink(ij_min.src,
                                                ij_min.dest).cost_der
                m_min += 1

        exp_factor = 1 + math.floor(self.m - max(m_min, m_max) / 2)
        condition = exp_factor * (c_max - c_min) < self.e
        k = 0 if condition else ij_max.src

        return [k, x_min, x_max, c_min, c_max, c_der_min, c_der_max, exp_factor]

    def UpdateTrees(self, k: int, n: int) -> float:
        delta_c_max = 0.0
        self.graph.nodes[k].pi_max = 0.0
        self.graph.nodes[k].alpha_max = None

        for j in range(k + 1, n - 2):
            dest_node = self.graph.nodes[j]
            dest_node.pi_min = math.inf
            dest_node.pi_max = -math.inf
            dest_node.alpha_min = None
            dest_node.alpha_max = None
            for link in self.graph.A.values():
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
                    link.flow > 0 and
                    new_cost > dest_node.pi_max
                ):
                    dest_node.pi_max = new_cost
                    dest_node.alpha_max = link

            if dest_node.alpha_max != 0:
                delta_c_max = max(
                    self.graph.nodes[n - 1].pi_max - self.graph.nodes[n - 1].pi_min, delta_c_max)

        return delta_c_max

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
            self.graph.GetLink(src, dest).flow += delta_x
            x_ij = self.graph.GetLink(src, dest).flow
            x_p = min(x_p, x_ij)

            self.graph.GetLink(src, dest).cost = self.graph.GetLink(
                src, dest).CalculateCost(x_ij)
            self.graph.GetLink(src, dest).cost_der = self.graph.GetLink(
                src, dest).CalculateCostDerivative(x_ij)

            c_p += self.graph.GetLink(src, dest).cost
            c_der_p += self.graph.GetLink(src, dest).cost_der
            i = src

        return (x_p, c_p, c_der_p)
