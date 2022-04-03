"""Algorithm B Class"""
import math
from typing import List, Set, Tuple

from src.shared.link import Link


class AlgorytmB:
    """
    Class used to represent B Algorthm

    ...

    Attributes
    ----------
    A: set[Link]
        set of arcs in acyclic network
    n: int
        highest node number (topologically ordered nodes)
    c: list[float]
        arcs-length cost array
    c_der: list[float]
        arcs-length derivatives array
    m_hat: int
        upper bound on number of arcs on a path—a scalar
    e: float
        upper bound on max-min path cost differential—a scalar
    x: list[int]
        initial arc-flow vector
    pi_max: list[float]
    pi_min: list[float]
    alpha_max: list[Link]
    alpha_min: list[Link]

    Methods
    -------
    CalculateEquilibrium()
        Calculates Equilibrium using B Algorithm - the main procedure,
        swap flow between paths between paths,
        until the max difference between max and min path cost drops to a given level e
    UpdateTrees()
        UpdateTrees
    ShiftFlow()
        ShiftFlow
    GetBranchNode()?
        GetBranchNode
    EqualizePathCost()
        EqualizePathCost
    GetDeltaXandC()
        GetDeltaXandC
    UpdatePathFlow()
        UpdatePathFlow
    ArcCost()
        ArcCost - this method may differ depending on the model
    ArcDerivative()
        ArcDerivative - this method may differ depending on the model
    """

    def __init__(
        self,
        A: Set[Link],
        n: int,
        c: List[List[float]],
        c_der: List[List[float]],
        m_hat: int,
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
        self.m_hat = m_hat
        self.e = e

        self.x = x
        self.pi_max = pi_max
        self.pi_min = pi_min
        self.alpha_max = alpha_max
        self.alpha_min = alpha_min

    def CalculateEquilibrium(self) -> Tuple[List[List[int]], float]:
        delta_c_max = self.UpdateTrees(1, self.n + 1)
        while self.e < delta_c_max:
            k_hat = self.ShiftFlow()
            delta_c_max = self.UpdateTrees(k_hat, self.n + 1)

        return (self.x, delta_c_max)

    def ShiftFlow(self):
        for j in range(self.n, 2, -1):
            if self.alpha_max[j] and self.pi_min[j] < self.pi_max[j]:
                [k, *params] = self.GetBranchNode(j)
                if 0 < k:
                    self.EqualizeCost(k, j, *params)
                    # TODO create RelabelNodes function
                    # RelabelNodes(k, j)
                    k_hat = k
        return k_hat

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

        # Might be error here () do not math in source
        exp_factor = 1 + math.floor(self.m_hat - max(m_min, m_max) / 2)
        condition = exp_factor(c_max - c_min) < self.e
        k = 0 if condition else ij_max.src

        return [k, x_min, x_max, c_min, c_max, c_der_min, c_der_max, exp_factor]

    def UpdateTrees(self, k: int, n: int) -> float:
        delta_c_max = 0.0
        self.pi_max[0] = 0.0
        self.alpha_max[0] = -1.0
        for j in range(k + 1, n - 1):
            self.pi_min[j] = math.inf
            self.pi_max[j] = -math.inf
            self.alpha_min[j] = 0
            self.alpha_max[j] = 0
            for link in self.A:  # for each arc key == i?
                i = link.src  # ij/arc.get("init_node")
                j = link.dest  # ij/arc.get("term_node")
                cij = self.c[i][j]  # self.c.get(i).get(j)
                xij = self.x[i][j]  # self.x.get(i).get(j)
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
                delta_pi = math.inf
                for key in self.pi_max.keys():
                    c = self.pi_max.get(key) - self.pi_min.get(key)
                    delta_pi = c if c < delta_pi else delta_pi

                delta_c_max = max(delta_pi, delta_c_max)
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
        while i != k:
            arc_ij = alpha[i]
            self.x[i][j] = self.x[i][j] + delta_x  # x.getPath(i, j) / set
            x_ij = self.x[i][j]
            x_p = min(x_p, x_ij)

            self.c[i][j] = self.ArcCost(arc_ij, x_ij)
            self.c_der[i][j] = self.ArcDerivative(arc_ij, x_ij)

            c_p = c_p + self.c[i][j]
            c_der_p = c_der_p + self.c_der[i][j]

        return (x_p, c_p, c_der_p)

    # This function may differ on diferent examples
    def ArcCost(self, ij: Link, xij: int) -> float:
        return ij.multip * xij

    # This function may differ on diferent examples
    def ArcDerivative(self, ij: Link, xij: int) -> float:
        return ij.multip
