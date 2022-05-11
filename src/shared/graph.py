""" Graph Class """
import math
from abc import ABC
from typing import Dict, List

from src.shared.link import Link
from src.shared.node import Node
from src.utils.link_utils import create_link_key


class Graph(ABC):
    """
    Class used to store all graph info
    """

    def __init__(self):
        self.links: Dict[str, Link]
        self.nodes: Dict[int, Node]
        self.nodesOrder: List[int]

    def GetMaxGap(self) -> float:
        gap = 0
        for node in self.nodes.values():
            if node.pi_max is not None and node.pi_min is not None:
                gap = max(node.pi_max - node.pi_min, gap)
        return gap

    def GetNeighbors(self, index: int) -> List[int]:
        return list(
            map(
                lambda link: link.dest,
                filter(
                    lambda link: link.src == index,
                    self.links.values()
                )
            )
        )

    def TopogologicalSortUtil(self, node_index: int, visited: List[int], stack: List[int]) -> None:
        visited[node_index - 1] = True
        for neighbor_index in self.GetNeighbors(node_index):
            if not visited[neighbor_index - 1]:
                self.TopogologicalSortUtil(neighbor_index, visited, stack)

        stack.insert(0, self.nodes[node_index].index)

    def GetTopoSortedNodesIndexes(self, node_index: int | None = None) -> List[int]:
        ordered_nodes = []
        visited = [False] * len(self.nodes)
        if node_index is not None:
            self.TopogologicalSortUtil(node_index, visited, ordered_nodes)
        else:
            for node_index in list(self.nodes):
                if not visited[node_index - 1]:
                    self.TopogologicalSortUtil(
                        node_index,
                        visited,
                        ordered_nodes
                    )

        return ordered_nodes

    def UpdateTopoSort(self):
        self.nodesOrder = self.GetTopoSortedNodesIndexes()

    def BuildTrees(self, origin_index: int = 1) -> None:
        for node in self.nodes.values():
            node.pi_max = -math.inf
            node.pi_min = math.inf
            node.alpha_max = None
            node.alpha_min = None

        self.nodes[origin_index].pi_min = 0
        self.nodes[origin_index].pi_max = 0

        for node_index in self.nodesOrder:
            for link in self.GetOutcomingLinks(node_index):
                cij = link.cost
                src = link.src
                dest = link.dest
                src_node = self.nodes[src]
                dest_node = self.nodes[dest]

                # min distance
                new_cost = src_node.pi_min + \
                    cij if src_node.pi_min != math.inf else cij
                if new_cost < dest_node.pi_min:
                    dest_node.pi_min = new_cost
                    dest_node.alpha_min = link

                # max distance
                new_cost = src_node.pi_max + \
                    cij if src_node.pi_max != -math.inf else cij
                if new_cost > dest_node.pi_max:
                    dest_node.pi_max = new_cost
                    dest_node.alpha_max = link

    def GetLink(self, from_node: int, to_node: int) -> (Link | None):
        return self.links.get(create_link_key(from_node, to_node))

    def GetIncomingLinks(self, node_index: int) -> List[Link]:
        links = []
        for link in self.links.values():
            if link.dest == node_index:
                links.append(link)

        return links

    def GetOutcomingLinks(self, node_index: int) -> List[Link]:
        links = []
        for link in self.links.values():
            if link.src == node_index:
                links.append(link)

        return links
