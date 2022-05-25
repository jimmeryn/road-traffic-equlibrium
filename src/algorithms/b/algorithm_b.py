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
        self.error = error
        self.demands = demands

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
        gap = 0
        for from_node, demands_array in enumerate(self.demands):
            from_node_index = from_node + 1
            if from_node_index not in self.bushes:
                continue
            bush = self.bushes[from_node_index]
            for to_node, demand in enumerate(demands_array):
                to_node_index = to_node + 1
                if demand == 0:
                    continue
                node = bush.subgraph.nodes[to_node_index]
                gap = max(gap, node.pi_max - node.pi_min)
        return gap

    def IsBushOptimal(self, bush: Bush) -> bool:
        for key, node in bush.subgraph.nodes.items():
            if abs(self.network.nodes[key].pi_min - node.pi_max) > self.error:
                return False
        return True

    def GetNetwork(self):
        for bush in self.bushes.values():
            for key, link in bush.subgraph.links.items():
                self.network.links[key].AddFlow(link.flow)

        return self.network
