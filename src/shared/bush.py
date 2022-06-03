""" Bush Class"""
import math
from typing import List, Literal, Tuple

from src.shared.bush_graph import BushGraph
from src.shared.consts import DIR_TOLERANCE, MULTI_STEP, ZERO_FLOW
from src.shared.link import Link
from src.shared.network import Network


class Bush:
    """ Bush Class """

    def __init__(self, originIndex: int, network: Network, demands, error: float) -> None:
        self.originIndex = originIndex
        self.subgraph = BushGraph(network, originIndex, demands)
        self.error = error
        self.m = len(self.subgraph.nodes) - 1
        self.topoSortUpToDate = True

    def UpdateTopoSort(self):
        if self.topoSortUpToDate:
            return
        self.subgraph.UpdateTopoSort()
        self.topoSortUpToDate = True

    def BuildTrees(self):
        self.subgraph.BuildTrees()

    def RemoveUnusedLinks(self) -> None:
        if self.subgraph.RemoveEmptyLinks():
            self.topoSortUpToDate = False

    def Improve(self):
        self.BuildTrees()
        if self.subgraph.AddBetterLinks():
            self.topoSortUpToDate = False
            self.UpdateTopoSort()
            self.BuildTrees()

    def Equilibrate(self) -> None:
        for node_index in reversed(self.subgraph.nodesOrder):
            self.EqualizeCostNew(node_index)

    def EqualizeCostNew(
        self,
        j: int,
    ) -> None:
        node = self.subgraph.nodes[j]
        if (
            node.alpha_max is None or
            node.alpha_min is None or
            node.pi_max - node.pi_min <= DIR_TOLERANCE
        ):
            return
        min_link = node.alpha_min
        max_link = node.alpha_max
        if min_link is None or max_link is None:
            return
        min_path: List[int] = []
        max_path: List[int] = []
        min_dist = 0
        max_dist = 0
        min_node = min_link.src
        max_node = max_link.src
        if min_node != max_node:
            min_path.append(min_link.index)
            min_dist += min_link.cost
            max_path.append(max_link.index)
            max_dist += max_link.cost
        elif min_link.index != max_link.index:
            min_path.append(min_link)
            min_dist += min_link.cost
            max_path.append(max_link.index)
            max_dist += max_link.cost

        while True:
            if min_node == max_node:
                break
            if self.subgraph.nodesOrder.index(min_node) > self.subgraph.nodesOrder.index(max_node):
                min_link = self.subgraph.nodes[min_node].alpha_min
                if min_link is not None:
                    min_node = min_link.src
                    min_path.append(min_link.index)
                    min_dist += min_link.cost
            else:
                max_link = self.subgraph.nodes[max_node].alpha_max
                if max_link is not None:
                    max_node = max_link.src
                    max_path.append(max_link.index)
                    max_dist += max_link.cost

        if not min_path or not max_path or max_dist - min_dist <= DIR_TOLERANCE:
            return

        min_path_distance = min_dist
        max_path_distance = max_dist

        while True:
            delta_x = self.CalculateFlowStep(
                max_path,
                max_path_distance,
                min_path,
                min_path_distance,
            )
            if delta_x <= ZERO_FLOW:
                break

            min_dist = 0
            for link_index in min_path:
                self.subgraph.links[link_index].AddFlow(delta_x)
                self.subgraph.AddFlowToBushFlow(link_index, delta_x)
                min_dist += self.subgraph.links[link_index].cost

            max_dist = 0
            for link_index in max_path:
                self.subgraph.links[link_index].AddFlow(-delta_x)
                self.subgraph.AddFlowToBushFlow(link_index, -delta_x)
                max_dist += self.subgraph.links[link_index].cost

            if not MULTI_STEP or max_dist <= min_dist:
                break

            min_path_distance = min_dist
            max_path_distance = max_dist

    def CalculateFlowStep(
        self,
        max_path: List[int],
        max_path_distance: List[float],
        min_path: List[int],
        min_path_distance: List[float]
    ):
        delta_x = 0
        distance_diff = max_path_distance - min_path_distance
        der_distance_diff = 0
        if distance_diff > DIR_TOLERANCE:
            for link_index in min_path:
                der_distance_diff += self.subgraph.links[link_index].cost_der
            min_move = math.inf
            o_flow = 0
            for link_index in max_path:
                der_distance_diff += self.subgraph.links[link_index].cost_der
                o_flow = self.subgraph.bush_flow[link_index]
                min_move = min(o_flow, min_move)
            delta_x = min(min_move, distance_diff / der_distance_diff)
        return delta_x

    def EqualizeCost(
        self,
        j: int,
    ) -> None:
        node = self.subgraph.nodes[j]
        if (
            node.alpha_max is None or
            node.alpha_min is None or
            node.pi_max - node.pi_min <= self.error
        ):
            return

        while node.pi_max - node.pi_min > self.error:
            [k, min_node_idx, max_node_idx, *params] = self.GetBranchNode(j)
            if k <= 0:
                return
            delta_x = self.GetDeltaX(*params)
            if delta_x <= ZERO_FLOW:
                return
            self.UpdatePathFlow(delta_x, min_node_idx, 'min')
            self.UpdatePathFlow(-delta_x, max_node_idx, 'max')
            self.BuildTrees()

    def GetBranchNode(self, j: int):
        min_node = self.subgraph.nodes[j]
        min_node_idx = []
        max_node = self.subgraph.nodes[j]
        max_node_idx = []
        c_min = 0
        c_max = 0
        c_der_min = 0
        c_der_max = 0
        x_min = min_node.alpha_min.cost
        x_max = max_node.alpha_max.cost
        while True:
            if min_node.pi_max >= max_node.pi_max:
                min_node_idx.append(min_node.index)
                link = min_node.alpha_min
                min_node = self.subgraph.nodes[link.src]
                c_min += link.cost
                c_der_min += link.cost_der
                x_min = min(x_min, link.flow)
            else:
                max_node_idx.append(max_node.index)
                link = max_node.alpha_max
                max_node = self.subgraph.nodes[link.src]
                c_max += link.cost
                c_der_max += link.cost_der
                x_max = min(x_max, link.flow)

            if min_node == max_node:
                break
        k = min_node.index

        return [k, min_node_idx, max_node_idx, x_min, x_max, c_min, c_max, c_der_min, c_der_max]

    def GetDeltaX(
        self,
        x_min: float,
        x_max: float,
        c_min: float,
        c_max: float,
        c_der_min: float,
        c_der_max: float
    ) -> float:
        delta_x_max = x_max if c_min < c_max else x_min
        if delta_x_max <= 0:
            return 0
        if c_der_max + c_der_min <= 0:
            return x_max if c_min <= c_max else -x_min
        else:
            return min(
                delta_x_max,
                (c_max - c_min) / (c_der_max + c_der_min)
            )

    def UpdatePathFlow(
        self,
        delta_x: float,
        node_array: List[int],
        alpha_param: Literal["min", "max"]
    ) -> Tuple[float, float, float]:
        alpha_param_name = f"alpha_{alpha_param}"
        for i in node_array:
            link: Link = self.subgraph.nodes[i][alpha_param_name]
            link.AddFlow(delta_x)
