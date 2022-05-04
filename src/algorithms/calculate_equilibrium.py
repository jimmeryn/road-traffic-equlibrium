""" Calculate Equilibrium Class """
from src.algorithms.algorithm import Algorithm


class CalculateEquilibrium:
    """ Class used to calculate Equilibrium """

    def __init__(
        self,
        algorithm: Algorithm,
        e: float,
        max_iteration_count: int = 100
    ):
        self.algorithm = algorithm
        self.e = e
        self.max_iteration_count = max_iteration_count

    def Run(self) -> None:
        iteration_count = 0
        delta_c_max = self.algorithm.GetMaxGap()
        print(f"\nMAX GAP {delta_c_max}")
        while (
            delta_c_max > self.e and
            iteration_count < self.max_iteration_count
        ):
            print(f"\nMAX GAP {delta_c_max}")
            iteration_count += 1
            self.algorithm.Iteration()
            delta_c_max = self.algorithm.GetMaxGap()

        print(iteration_count)
        return