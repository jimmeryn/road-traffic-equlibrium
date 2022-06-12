"""Algorithm B Class"""
import math
from typing import Dict

from src.algorithms.algorithm import Algorithm
from src.shared.bush import Bush
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
            if from_node_index in bushes or demands_array.max() == 0:
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

    def GetGaps(self):
        rel_gap = 0
        max_gap = 0

        total_travel_time = 0
        for link in self.network.links.values():
            total_travel_time += link.flow * link.cost

        min_travel_time = 0
        for bush in self.bushes.values():
            bush.BuildTrees()
            self.network.BuildMinTree(bush.originIndex)
            for node_idx, demand in enumerate(bush.subgraph.demands):
                if demand == 0:
                    continue
                node = self.network.nodes[node_idx + 1]
                min_travel_time += demand * node.pi_min
                max_gap = max(max_gap, node.pi_max - node.pi_min)

        rel_gap = 1.0 - min_travel_time / \
            total_travel_time if total_travel_time > 1e-25 else math.inf

        return (rel_gap, max_gap)
