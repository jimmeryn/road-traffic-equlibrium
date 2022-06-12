""" Graph Class """
import math
from collections import defaultdict
from operator import attrgetter
from typing import Dict, List

from src.shared.graph import Graph
from src.shared.link import Link
from src.shared.node import Node
from src.utils.link_utils import create_link_key


class Network(Graph):
    """
    Class used to store all graph info
    """

    def __init__(self, nodes, links):
        super().__init__()
        self.links = self.CreateLinksDict(links)
        self.nodes = self.CreateNodesDict(nodes)
        self.n: int = int(nodes[-1][0])
        self.outcoming_links_dict = self.GetAllOutcomingLinks()

    def CreateLinksDict(self, links) -> Dict[str, Link]:
        return dict(
            map(lambda link: (
                create_link_key(link[0], link[1]),
                Link(*link)
            ), links)
        )

    def CreateNodesDict(self, nodes) -> Dict[int, Node]:
        return dict(
            map(lambda node: (
                int(node[0]),
                Node(node[0])
            ), nodes)
        )

    def BuildMinTree(self, origin_index: int = 1):
        unvisited_nodes = [*self.nodes]
        for node in self.nodes.values():
            node.pi_min = math.inf
            node.alpha_min = None

        self.nodes[origin_index].pi_min = 0
        current_min_node = self.nodes[origin_index]
        while current_min_node is not None:
            outcoming_links = self.outcoming_links_dict[current_min_node.index]
            for link in outcoming_links:
                tentative_value = current_min_node.pi_min + link.cost
                neighbour = self.nodes[link.dest]
                if tentative_value < neighbour.pi_min:
                    neighbour.pi_min = tentative_value
                    neighbour.alpha_min = link

            unvisited_nodes.remove(current_min_node.index)
            current_min_node = self.GetCurrentMinNode(unvisited_nodes)

        return

    def GetCurrentMinNode(self, unvisited_nodes: List[int]):
        current_min_node = min(
            [self.nodes[i] for i in unvisited_nodes],
            key=attrgetter('pi_min'),
            default=None
        )

        return current_min_node

    def GetAllOutcomingLinks(self) -> Dict[int, List[Link]]:
        all_links = defaultdict(list)
        for link in self.links.values():
            all_links[link.src].append(link)

        return all_links
