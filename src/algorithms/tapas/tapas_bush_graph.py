""" TAPAS Bush graph class """
from src.shared.bush_graph import BushGraph
from src.shared.link import Link
from src.shared.network import Network


class TapasBushGraph(BushGraph):
    """ Bush graph for the TAPAS algorithm """

    def __init__(self, network: Network, originIndex: int, demands) -> None:
        super().__init__(network, originIndex, demands)
        self.min_shift = 0.0

    def AddOriginFlowAndCreateLink(self, link: Link, delta_x: float):
        if link.index not in self.links:
            self.links[link.index] = link
        self.AddFlowToBushFlow(link.index, delta_x)
