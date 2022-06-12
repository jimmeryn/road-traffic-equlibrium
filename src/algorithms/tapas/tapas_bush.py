""" TAPAS Bush class """
from src.algorithms.tapas.pas_manager import PasManager
from src.algorithms.tapas.tapas_bush_graph import TapasBushGraph
from src.shared.consts import ZERO_FLOW
from src.shared.network import Network


class TapasBush():
    """ Bush for the TAPAS algorithm """

    def __init__(
        self,
        originIndex: int,
        network: Network,
        demands,
        error: float,
        pasManager: PasManager
    ):
        self.originIndex = originIndex
        self.subgraph = TapasBushGraph(network, originIndex, demands)
        self.error = error
        self.m = len(self.subgraph.nodes) - 1
        self.pasManager = pasManager
        self.exploredLinks = []

    def RemoveCyclicFlows(self):
        while True:
            self.exploredLinks.clear()
            # need to find cycles in topo sort since pas can be cyclic
            if not False:  # topologicalSort() -> boolean:
                break

    def BuildTrees(self):
        self.subgraph.BuildTrees()

    def RemoveUnusedLinks(self) -> None:
        self.subgraph.RemoveEmptyLinks()

    def Equilibrate(self) -> None:
        self.subgraph.network.BuildMinTree(self.originIndex)
        self.pasManager.RecalculatePASCosts()

        incoming_links_dict = self.subgraph.GetAllIncomingLinks()
        for node_index, node in self.subgraph.nodes.items():
            shortest_path_link = node.alpha_min
            if shortest_path_link is None:
                continue
            for link in incoming_links_dict[node_index]:
                if (
                    self.subgraph.bush_flow[link.index] <= ZERO_FLOW or
                    link is shortest_path_link
                ):
                    continue
                self.pasManager.CreateNewPAS(self.subgraph, link, node_index)

        flow_was_moved = False
        for pas in self.pasManager.pasSet.values():
            if pas.MoveFlow():
                flow_was_moved = True

        return flow_was_moved
