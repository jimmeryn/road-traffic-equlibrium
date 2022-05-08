""" Calculate Equilibrium Class """
from src.algorithms.algorithm import Algorithm


class CalculateEquilibrium:
    """ Class used to calculate Equilibrium """

    def __init__(
        self,
        algorithm: Algorithm,
        e: float | int,
        max_iteration_count: int = 100
    ):
        self.algorithm = algorithm
        self.e = e
        self.max_iteration_count = max_iteration_count

    def Run(self) -> None:
        iteration_count = 0
        delta_c_max = self.algorithm.GetMaxGap()
        while (
            delta_c_max > self.e and
            iteration_count < self.max_iteration_count
        ):
            iteration_count += 1
            self.algorithm.Iteration()
            delta_c_max = self.algorithm.GetMaxGap()

        print(f"Algorithm finished after {iteration_count} iterations.")
        print(f"Calculated max cost difference = {delta_c_max}.")
        return self.algorithm.graph
