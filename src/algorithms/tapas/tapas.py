"""TAPAS Class"""
from src.algorithms.algorithm import Algorithm


class TAPAS(Algorithm):
    """ TAPAS Class """

    def __init__(self, nodes, networks, demands, error: float) -> None:
        super().__init__(nodes, networks)

    def Iteration(self) -> None:
        pass

    def GetMaxGap(self) -> None:
        pass
