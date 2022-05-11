"""Algorithm B Class"""
from typing import Dict

from src.algorithms.algorithm import Algorithm
from src.algorithms.b.bush import Bush
from src.shared.network import Network


class AlgorithmB(Algorithm):
    """ Algorithm B Class """

    def __init__(self, nodes, links, demands, error: float) -> None:
        super().__init__(nodes, links)
        self.bushes = self.CreateBushes(demands, self.network, error)

    def CreateBushes(self, demands, network: Network, error: float) -> Dict[int, Bush]:
        bushes: Dict[int, Bush] = {}
        for from_node, demands_array in enumerate(demands):
            from_node_index = from_node + 1
            for to_node, demand in enumerate(demands_array):
                _to_node_index = to_node + 1
                if demand == 0 or from_node_index in bushes:
                    continue
                bushes[from_node_index] = Bush(
                    from_node_index,
                    network,
                    demands_array,
                    error
                )

        return bushes

    def Iteration(self) -> None:
        for bush in self.bushes.values():
            bush.UpdateTopoSort()
            bush.Improve()
            bush.Equilibrate()
            bush.RemoveUnusedLinks()

    def GetMaxGap(self):
        for link in self.network.links.values():
            link.ResetFlow()
        for bush in self.bushes.values():
            for link_key, link in bush.subgraph.links.items():
                self.network.links[link_key].AddFlow(link.flow)
        self.network.BuildTrees()
        return self.network.GetMaxGap()
