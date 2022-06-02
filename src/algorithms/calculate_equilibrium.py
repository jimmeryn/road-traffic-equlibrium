""" Calculate Equilibrium Class """
import math
from io import TextIOWrapper

from src.algorithms.algorithm import Algorithm


class CalculateEquilibrium:
    """ Class used to calculate Equilibrium """

    def __init__(
        self,
        algorithm: Algorithm,
        e: float,
        max_iteration_count: int
    ):
        self.algorithm = algorithm
        self.e = e
        self.max_iteration_count = max_iteration_count

    def Run(self, file: TextIOWrapper) -> None:
        iteration_count = 0
        delta_c_max = math.inf
        while (
            delta_c_max > self.e and
            iteration_count < self.max_iteration_count
        ):
            file.write(f"{iteration_count},{delta_c_max}\n")
            iteration_count += 1
            self.algorithm.Iteration()
            delta_c_max = self.algorithm.GetMaxGap()

        file.write(
            f"Iterations,{iteration_count}\n")
        file.write(f"Max_cost_difference,{delta_c_max}\n")

        return self.algorithm.network
