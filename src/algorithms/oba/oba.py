"""OBA Class"""
import math
from typing import Dict

from src.algorithms.algorithm import Algorithm
from src.shared.bush import Bush
from src.shared.network import Network


class OBA(Algorithm):
    """ OBA Class """

    def __init__(self, nodes, networks, demands, error: float) -> None:
        super().__init__(nodes, networks)
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
        main_iterations = 1
        inner_iterations = 1
        for _n in range(1, main_iterations):
            for bush in self.bushes.values():
                self.UpdateRestrictingSubnetwork(bush)
                self.UpdateLinkFlows(bush)

            for _m in range(1, inner_iterations):
                for bush in self.bushes.values():
                    self.UpdateLinkFlows(bush)

    def UpdateRestrictingSubnetwork(self, bush: Bush):
        bush.RemoveUnusedLinks()
        bush.UpdateTopoSort()
        bush.BuildTrees()

        for link in self.network.links.values():
            if self.network.nodes[link.src].pi_max < self.network.nodes[link.dest].pi_max:
                bush.subgraph.links[link.index] = link
                # check if link nodes exists in bush or just dont remove them

        bush.UpdateTopoSort()
        self.FindLastCommonNodes(bush)
        # update data structures

    def UpdateLinkFlows(self, bush):
        k = 0
        while True:
            step_size = math.pow(2, -k)
            delta_x = self.ComputeFlowShift(step_size)
            self.ProjectAndAggregateFlowShifts(delta_x)
            social_pressure = self.CalculateSocialPressure(bush)
            if social_pressure > 0:
                break
            k += 1
        self.ApplyFlowShifts()
        self.UpdateTotalLinkFlowsAndCosts()

    def ComputeFlowShift(self, step_size: float):
        # TODO
        # get route 1 and route 2
        return 0.0

    def ProjectAndAggregateFlowShifts(self, delta_x: float):
        # TODO find last common nodes in Ap
        pass

    def FindLastCommonNodes(self, bush: Bush):
        # TODO
        pass

    def CalculateSocialPressure(self, bush: Bush):
        return 1.0

    def ApplyFlowShifts(self):
        pass

    def UpdateTotalLinkFlowsAndCosts(self):
        pass

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
