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
        self.links: Dict[str, Link] = dict()
        self.nodes: Dict[int, Node] = dict()
        self.nodesOrder: List[int] = list()

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

    def TopogologicalSortUtil(self, node_index: int, visited: Dict[int, bool], stack: List[int]) -> None:
        visited[node_index] = True
        for neighbor_index in self.GetNeighbors(node_index):
            if neighbor_index not in visited:
                self.TopogologicalSortUtil(neighbor_index, visited, stack)

        stack.insert(0, node_index)

    def GetTopoSortedNodesIndexes(self, node_index: int | None = None) -> List[int]:
        ordered_nodes = []
        visited = {}
        if node_index is not None:
            if node_index == 2:
                pass
            self.TopogologicalSortUtil(node_index, visited, ordered_nodes)
        else:
            for node_index in list(self.nodes):
                if node_index not in visited:
                    self.TopogologicalSortUtil(
                        node_index,
                        visited,
                        ordered_nodes
                    )

        return ordered_nodes

    def UpdateTopoSort(self, node_index: int | None = None):
        self.nodesOrder = self.GetTopoSortedNodesIndexes(node_index)

    def BuildTrees(self, origin_index: int = 1) -> None:
        for node in self.nodes.values():
            node.pi_max = 0
            node.pi_min = math.inf
            node.alpha_max = None
            node.alpha_min = None

        self.nodes[origin_index].pi_min = 0

        for node_index in self.nodesOrder:
            links = self.GetIncomingLinks(node_index)
            dest_node = self.nodes[node_index]
            for link in links:
                src_node = self.nodes[link.src]
                cij = link.cost

                # min distance
                new_cost = src_node.pi_min + cij
                if new_cost < dest_node.pi_min:
                    dest_node.pi_min = new_cost
                    dest_node.alpha_min = link

                # max distance
                new_cost = src_node.pi_max + cij
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

    def BuildMinTree(self, origin_index: int = 1):
        unvisited_nodes = list(self.nodes.keys())
        for node in self.nodes.values():
            node.pi_min = math.inf
            node.alpha_min = None

        self.nodes[origin_index].pi_min = 0

        while unvisited_nodes:
            current_min_node = self.GetCurrentMinNode(unvisited_nodes)
            outcoming_links = self.GetOutcomingLinks(current_min_node.index)
            for link in outcoming_links:
                tentative_value = current_min_node.pi_min + link.cost
                neighbour = self.nodes[link.dest]
                if tentative_value < neighbour.pi_min:
                    neighbour.pi_min = tentative_value
                    neighbour.alpha_min = link

            unvisited_nodes.remove(current_min_node.index)

        return

    def GetCurrentMinNode(self, unvisited_nodes: List[int]):
        current_min_node = None
        for node_index in unvisited_nodes:
            if current_min_node is None:
                current_min_node = self.nodes[node_index]
            elif self.nodes[node_index].pi_min < current_min_node.pi_min:
                current_min_node = self.nodes[node_index]
        return current_min_node
