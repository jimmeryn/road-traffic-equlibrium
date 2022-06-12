""" Graph Class """
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

    def GetOutcomingLinks(self, node_index: int) -> List[Link]:
        links = []
        for link in self.links.values():
            if link.src == node_index:
                links.append(link)

        return links
