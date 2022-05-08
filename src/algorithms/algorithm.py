""" Base Algorithm """
from abc import ABC, abstractmethod

from src.shared.graph import Graph


class Algorithm(ABC):
    """
    Base Algorithm abstract class
    All origin based alogrithms should extend this class
    """

    def __init__(self, nodes, networks):
        super().__init__()
        self.graph = Graph(nodes, networks)

    @abstractmethod
    def Iteration(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def GetMaxGap(self) -> None:
        raise NotImplementedError
