""" Bush Class"""
from typing import List, Literal, Tuple

from src.algorithms.b.bush_graph import BushGraph
from src.shared.link import Link
from src.shared.network import Network
from src.shared.node import Node


class Bush:
    """ Bush Class """

    def __init__(self, originIndex: int, network: Network, demands, error: float) -> None:
        self.originIndex = originIndex
        self.subgraph = BushGraph(network, originIndex, demands)
        self.error = error
        self.m = len(self.subgraph.nodes) - 1

    def UpdateTopoSort(self):
        self.subgraph.UpdateTopoSort(self.originIndex)

    def BuildTrees(self):
        self.subgraph.BuildTrees(self.originIndex)

    def RemoveUnusedLinks(self) -> None:
        self.subgraph.RemoveEmptyLinks()

    def Improve(self):
        self.BuildTrees()
        self.subgraph.network.BuildMinTree()
        added_better_links = self.subgraph.AddBetterLinks()
        if added_better_links:
            self.UpdateTopoSort()
            self.BuildTrees()

    def Equilibrate(self) -> None:
        for node_index in reversed(self.subgraph.nodesOrder):
            node = self.subgraph.nodes[node_index]
            if node.alpha_max and node.pi_max - node.pi_min > self.error:
                self.EqualizeCost(node_index, node)

    def EqualizeCost(
        self,
        j: int,
        node: Node
    ) -> None:
        while node.pi_max - node.pi_min > self.error:
            [k, min_node_idx, max_node_idx, *params] = self.GetBranchNode(j)
            if k <= 0:
                break
            delta_x = self.GetDeltaX(*params)
            if delta_x <= 1e-12:
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
