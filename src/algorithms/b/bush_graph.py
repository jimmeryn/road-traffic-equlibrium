""" BushGraph """
from copy import deepcopy
from typing import Dict, Tuple

from src.shared.graph import Graph
from src.shared.link import Link
from src.shared.network import Network
from src.shared.node import Node


class BushGraph(Graph):
    """Class implementing sub-graph structure for bush """

    def __init__(self, network: Network, originIndex: int, demands) -> None:
        super().__init__()
        self.network = network
        self.originIndex = originIndex
        (nodes, links) = self.GetReachableNodesAndLinks()
        self.nodes = deepcopy(nodes)
        self.links = deepcopy(links)
        self.nodesOrder = self.GetTopoSortedNodesIndexes(originIndex)
        self.BuildMinTree(originIndex)
        self.ApplyInitialDemands(demands)
        self.BuildTrees(originIndex)

    def GetReachableNodesAndLinks(self) -> Tuple[Dict[int, Node], Dict[str, Link]]:
        network_copy = deepcopy(self.network)
        network_copy.BuildMinTree(self.originIndex)

        links: Dict[str, Link] = dict()
        for key, link in network_copy.links.items():
            src_node_cost = network_copy.nodes[link.src].pi_min
            dest_node_cost = network_copy.nodes[link.dest].pi_min
            if dest_node_cost > src_node_cost:
                links[key] = link

        nodes: Dict[int, Node] = dict()
        for link in links.values():
            src = link.src
            dest = link.dest
            if src not in nodes:
                nodes[src] = network_copy.nodes[src]
            if dest not in nodes:
                nodes[dest] = network_copy.nodes[dest]

        return (nodes, links)

    def ApplyInitialDemands(self, demands):
        origin_node_index = self.nodes[self.originIndex].index
        for index, demand in enumerate(demands):
            if demand == 0:
                continue
            node = self.nodes[index + 1]
            while origin_node_index != node.index:
                node.alpha_min.AddFlow(demand)
                node = self.nodes[node.alpha_min.src]

    def RemoveEmptyLinks(self):
        for link_key, link in self.links.copy().items():
            if link.flow <= 0 and self.GetIncomingLinks(link.dest):
                del self.links[link_key]
