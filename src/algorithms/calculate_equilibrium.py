""" Calculate Equilibrium Class """
import math

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

    def Run(self) -> None:
        iteration_count = 0
        delta_c_max = math.inf
        while (
            delta_c_max > self.e and
            iteration_count < self.max_iteration_count
        ):
            print(f"Iteration: {iteration_count}, Gap: {delta_c_max}")
            iteration_count += 1
            self.algorithm.Iteration()
            delta_c_max = self.algorithm.GetMaxGap()

        print(f"Algorithm finished after {iteration_count} iterations.")
        print(f"Calculated max cost difference = {delta_c_max}.")

        return self.algorithm.network
