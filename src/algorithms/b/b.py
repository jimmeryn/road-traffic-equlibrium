"""Algorithm B Class"""
import math
from typing import List, Set, Tuple

from src.shared.link import Link

# TODO notes/questions:
# - What is expansion factor - lambda and how to use it
# - What is alpha_max/min -> sometimes it's links sometimes we assign number to it
# - RelabelNodes(k, j) function??


class AlgorytmB:
    """
    Class used to represent B Algorthm

    ...

    Attributes:
    ----------
    A : set[Link]
        Set of arcs in acyclic network
    n : int
        Highest node number (topologically ordered nodes)
    c : list[float]
        Arcs-length cost array
    c_der : list[float]
        Arcs-length derivatives array
    m : int
        Upper bound on number of arcs on a path—a scalar
    e : float
        Upper bound on max-min path cost differential—a scalar
    x : list[int]
        Initial arc-flow vector
    pi_max : list[float]
        Max path potential
    pi_min : list[float]
        Min path potential
    alpha_max : list[Link]
        Max pedecessor labels
    alpha_min : list[Link]
        Min pedecessor labels

    Methods:
    -------
    CalculateEquilibrium(A, n, x, c, c_der, m: int, e: float):
        Calculates Equilibrium using B Algorithm - the main procedure, swap flow between paths between paths, until the max difference between max and min path cost drops to a given level e.
    ShiftFlow()
        Discovering arc-independent max and min paths to each node and transfers flow between paths to equalize their costs.
    GetBranchNode(j: int)
        Calculate start node k being the only node p_max and p_min have in common (except their shared end node j).
    UpdateTrees(k: int, n: int) -> float
        Updates max and min path potentials (pi_max, pi_min) and pedecessor labels (alpha_max, alpha_min).
    EqualizePathCost(k: int, j: int, x_min, x_max, c_min, c_max, c_der_min, c_der_max, exp_factor)
        Move certain amout of flow (delta_x) from p_max to p_min to equilize costs c_max and c_min (Newton's method).
    GetDeltaXandC(x_min, x_max, c_min, c_max, c_der_min, c_der_max)
        Calculate increment flow (delta_x) and current max and min paths (x_min, x_max) cost difference (delta_c).
    UpdatePathFlow(delta_x: int, k: int, j: int, alpha)
        Update all arcs on a given path by changing their flow (update by delta_x) and update costs (k - start node, j - end node).
    ArcCost(arc: Link, flow: int) -> float
        Calculate arc cost at given flow (this method may differ depending on the model)
    ArcDerivative(arc: Link, flow: int) -> float
        Calculate arc derivative at given flow (this method may differ depending on the model)
    """

    def __init__(
        self,
        A: Set[Link],
        n: int,
        c: List[List[float]],
        c_der: List[List[float]],
        m: int,
        e: float,
        x: List[List[int]],
        pi_max: List[float],
        pi_min: List[float],
        alpha_max: List[Link],
        alpha_min: List[Link]
    ):
        self.A = A
        self.n = n
        self.c = c
        self.c_der = c_der
        self.m = m
        self.e = e

        self.x = x
        self.pi_max = pi_max
        self.pi_min = pi_min
        self.alpha_max = alpha_max
        self.alpha_min = alpha_min
        self.k_hat = 0

    def CalculateEquilibrium(self) -> Tuple[List[List[int]], float]:
        delta_c_max = self.UpdateTrees(1, self.n + 1)
        while self.e < delta_c_max:
            self.ShiftFlow()
            delta_c_max = self.UpdateTrees(self.k_hat, self.n + 1)

        return (self.x, delta_c_max)

    def ShiftFlow(self):
        for j in range(self.n, 1, -1):
            if self.alpha_max[j] and self.pi_min[j] < self.pi_max[j]:
                [k, *params] = self.GetBranchNode(j)
                if 0 < k:
                    self.EqualizeCost(k, j, *params)
                    # TODO create RelabelNodes function
                    # RelabelNodes(k, j)
                    self.x[j], self.x[k] = self.x[k], self.x[j]
                    self.k_hat = k

    def GetBranchNode(self, j: int):
        ij_min = self.alpha_min[j]
        ij_max = self.alpha_max[j]
        x_min = self.x[ij_min.src][ij_min.dest]
        x_max = self.x[ij_max.src][ij_max.dest]
        c_min = self.c[ij_min.src][ij_min.dest]
        c_max = self.c[ij_max.src][ij_max.dest]
        c_der_min = self.c_der[ij_min.src][ij_min.dest]
        c_der_max = self.c_der[ij_max.src][ij_max.dest]
        m_min = 1
        m_max = 1
        while ij_max.src != ij_min.src:
            while ij_min.src < ij_max.src:
                ij_max = self.alpha_max[ij_max.src]
                x_max = min(x_max, self.x[ij_max.src][ij_max.dest])

                c_max += self.c[ij_max.src][ij_max.dest]
                c_der_max += self.c_der[ij_max.src][ij_max.dest]
                m_max += 1

            while ij_max.src < ij_min.src:
                ij_min = self.alpha_min[ij_min.src]
                x_min = min(x_min, self.x[ij_min.src][ij_min.dest])

                c_min += self.c[ij_min.src][ij_min.dest]
                c_der_min += self.c_der[ij_min.src][ij_min.dest]
                m_min += 1

        exp_factor = 1 + math.floor(self.m - max(m_min, m_max) / 2)
        condition = exp_factor * (c_max - c_min) < self.e
        k = 0 if condition else ij_max.src

        return [k, x_min, x_max, c_min, c_max, c_der_min, c_der_max, exp_factor]

    def UpdateTrees(self, k: int, n: int) -> float:
        delta_c_max = 0.0
        self.pi_max[0] = 0.0
        self.alpha_max[0] = -1
        for j in range(k + 1, n - 1):
            self.pi_min[j] = math.inf
            self.pi_max[j] = -math.inf
            self.alpha_min[j] = 0
            self.alpha_max[j] = 0
            for link in self.A:
                i = link.src
                j = link.dest
                cij = self.c[i][j]
                xij = self.x[i][j]
                if self.pi_min[i] + cij < self.pi_min[j]:
                    self.pi_min[j] = self.pi_min[i] + cij
                    self.alpha_min[j] = link
                if (
                    self.alpha_min[i] != 0 and
                    xij != 0 and
                    self.pi_max[i] + cij > self.pi_max[j]
                ):
                    self.pi_max[j] = self.pi_max[i] + cij
                    self.alpha_max[j] = link
            if self.alpha_max[j] != 0:
                delta_c_max = max(
                    *[a - b for (a, b) in zip(self.pi_max[k:n],
                                              self.pi_min[k:n])],
                    delta_c_max
                )
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
            ] = self.UpdatePathFlow(delta_x, k, j, self.alpha_min)
            [
                x_max,
                c_max,
                c_der_max
            ] = self.UpdatePathFlow(-delta_x, k, j, self.alpha_max)
            [
                delta_x,
                delta_c
            ] = self.GetDeltaXandC(x_min, x_max, c_min, c_max, c_der_min, c_der_max)
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

    def UpdatePathFlow(self, delta_x: int, k: int, j: int, alpha: list[Link]) -> Tuple[int, float, float]:
        x_p = math.inf
        c_p = 0.0
        c_der_p = 0.0
        i = j
        while i != k:  # i is not changing...
            ij = alpha[i]
            self.x[ij.src][ij.dest] += delta_x
            x_ij = self.x[ij.src][ij.dest]
            x_p = min(x_p, x_ij)

            self.c[ij.src][ij.dest] = self.ArcCost(ij, x_ij)
            self.c_der[ij.src][ij.dest] = self.ArcDerivative(ij, x_ij)

            c_p += self.c[ij.src][ij.dest]
            c_der_p += self.c_der[ij.src][ij.dest]
            i -= 1

        return (x_p, c_p, c_der_p)

    # This function may differ on diferent examples
    def ArcCost(self, ij: Link, xij: int) -> float:
        return ij.multip * xij

    # This function may differ on diferent examples
    def ArcDerivative(self, ij: Link, xij: int) -> float:
        return ij.multip
