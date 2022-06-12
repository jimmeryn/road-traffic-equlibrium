""" Graph Class """
import math
from abc import ABC
from collections import defaultdict
from typing import Dict, List

from src.shared.link import Link
from src.shared.node import Node


class Graph(ABC):
    """
    Class used to store all graph info
    """

    def __init__(self):
        self.links: Dict[str, Link] = dict()
        self.nodes: Dict[int, Node] = dict()
        self.nodesOrder: List[int] = list()

    def GetAllNeighbors(self):
        all_neighbors = defaultdict(list)
        for link in self.links:
            [src, dest] = link.split('_')
            all_neighbors[int(src)].append(int(dest))
        return all_neighbors

    def GetIncomingLinks(self, node_index: int) -> List[Link]:
        links = []
        for link in self.links.values():
            if link.dest == node_index:
                links.append(link)

        return links

    def GetAllIncomingLinks(self) -> Dict[int, List[Link]]:
        all_links = defaultdict(list)
        for link in self.links.values():
            all_links[link.dest].append(link)

        return all_links

    def GetAllIncomingLinksLength(self) -> Dict[int, int]:
        all_links = defaultdict(int)
        for link in self.links.values():
            all_links[link.dest] += 1

        return all_links

    def GetAllOutcomingLinks(self) -> Dict[int, List[Link]]:
        all_links = defaultdict(list)
        for link in self.links.values():
            all_links[link.src].append(link)

        return all_links

    def GetOutcomingLinks(self, node_index: int) -> List[Link]:
        links = []
        for link in self.links.values():
            if link.src == node_index:
                links.append(link)

        return links

    def BuildMinTree(self, origin_index: int = 1):
        unvisited_nodes = [*self.nodes]
        for node in self.nodes.values():
            node.pi_min = math.inf
            node.alpha_min = None

        self.nodes[origin_index].pi_min = 0
        outcoming_links_dict = self.GetAllOutcomingLinks()

        while unvisited_nodes:
            current_min_node = self.GetCurrentMinNode(unvisited_nodes)
            outcoming_links = outcoming_links_dict[current_min_node.index]
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
