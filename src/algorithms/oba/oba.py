"""OBA Class"""
from src.algorithms.algorithm import Algorithm


class OBA(Algorithm):
    """ OBA Class """

    def __init__(self, nodes, networks, demands, error: float) -> None:
        self.graph = None

    def Iteration(self) -> None:
        pass

    def GetMaxGap(self) -> None:
        pass
