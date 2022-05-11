""" BushGraph """
from copy import deepcopy
from typing import Dict, Tuple

from src.shared.graph import Graph
from src.shared.link import Link
from src.shared.network import Network
from src.shared.node import Node


class BushGraph(Graph):
    """Class implementing sub-graph structure for bush """

    def __init__(self, network: Network, originIndex: int) -> None:
        super().__init__()
        self.network = network
        self.originIndex = originIndex
        (nodes, links) = self.GetReachableNodesAndLinks()
        self.nodes = deepcopy(nodes)
        self.links = deepcopy(links)
        self.nodesOrder = self.GetTopoSortedNodesIndexes()

    def GetReachableNodesAndLinks(self) -> Tuple[Dict[int, Node], Dict[str, Link]]:
        nodes = self.network.nodes
        links = dict()
        for key, link in self.network.links.items():
            if (
                link.src in nodes and
                link.dest in nodes and
                link.src < link.dest
            ):
                links[key] = link

        return (nodes, links)
