""" Base Algorithm """
from abc import ABC, abstractmethod

from src.shared.network import Network


class Algorithm(ABC):
    """
    Base Algorithm abstract class
    All origin based alogrithms should extend this class
    """

    def __init__(self, nodes, links):
        super().__init__()
        self.network = Network(nodes, links)

    @abstractmethod
    def Iteration(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def GetMaxGap(self) -> None:
        raise NotImplementedError
