""" Calculate Equilibrium Class """
from io import TextIOWrapper

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

    def Run(self, file: TextIOWrapper, data_file: TextIOWrapper) -> None:
        iteration_count = 0
        gaps = self.algorithm.GetGaps()
        data_file.write(f"Bushes,{len(self.algorithm.bushes)}\n")
        data_file.write(f"Nodes,{len(self.algorithm.network.nodes)}\n")
        data_file.write(f"Links,{len(self.algorithm.network.links)}\n")
        while (
            gaps[GAP] > self.e and
            iteration_count < self.max_iteration_count or
            iteration_count <= 0
        ):
            file.write(
                f"{iteration_count},{gaps[1]},{iteration_count},{gaps[0]}\n")
            iteration_count += 1
            self.algorithm.Iteration()
            gaps = self.algorithm.GetGaps()

        data_file.write(
            f"Iterations,{iteration_count}\n")
        data_file.write(f"Rel_gap,{gaps[0]}\n")
        data_file.write(f"Max_cost_difference,{gaps[1]}\n")

        return self.algorithm.network
