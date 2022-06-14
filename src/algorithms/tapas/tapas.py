"""TAPAS Class"""
import math
from typing import Dict

from src.algorithms.algorithm import Algorithm
from src.algorithms.tapas.pas_manager import PasManager
from src.algorithms.tapas.tapas_bush import TapasBush
from src.shared.network import Network


class TAPAS(Algorithm):
    """ TAPAS Class """

    def __init__(self, nodes, networks, demands, error: float) -> None:
        super().__init__(nodes, networks)
        self.demands = demands
        self.pasManager = PasManager(self.network)
        self.bushes = self.CreateBushes(
            demands, self.network, error, self.pasManager)

    def CreateBushes(self, demands, network: Network, error: float, pasManager: PasManager) -> Dict[int, TapasBush]:
        bushes: Dict[int, TapasBush] = {}
        for from_node, demands_array in enumerate(demands):
            from_node_index = from_node + 1
            for to_node, demand in enumerate(demands_array):
                _to_node_index = to_node + 1
                if demand == 0 or from_node_index in bushes:
                    continue
                bushes[from_node_index] = TapasBush(
                    from_node_index,
                    network,
                    demands_array,
                    error,
                    pasManager
                )

        return bushes

    def Iteration(self) -> None:
        for bush in self.bushes.values():
            bush.RemoveCyclicFlows()
            bush.Equilibrate()
        self.pasManager.DeleteUnusedPASAndMoveFlow()

    # TODO move get gaps to common file
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
