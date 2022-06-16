""" Calculate Equilibrium Class """
from io import TextIOWrapper
from time import perf_counter

from src.algorithms.algorithm import Algorithm
from src.shared.consts import GAP


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
        gaps = self.algorithm.GetGaps()
        start_time = perf_counter()
        while (
            gaps[GAP] > self.e and
            iteration_count < self.max_iteration_count or
            iteration_count <= 0
        ):
            file.write(
                f"{iteration_count},{perf_counter() - start_time},{gaps[1]},{gaps[0]}\n")
            iteration_count += 1
            self.algorithm.Iteration()
            gaps = self.algorithm.GetGaps()

        file.write(
            f"{iteration_count},{perf_counter() - start_time},{gaps[1]},{gaps[0]}\n")

        return self.algorithm.network
