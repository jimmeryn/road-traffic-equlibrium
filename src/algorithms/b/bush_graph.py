""" BushGraph """
from copy import deepcopy
from typing import Dict, Tuple

from src.shared.graph import Graph
from src.shared.link import Link
from src.shared.network import Network
from src.shared.node import Node
from src.utils.link_utils import create_link_key


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
        self.p2Cont = []

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

    def AddBetterLinks(self) -> bool:
        was_improved = False
        new_link_added = False
        self.p2Cont.clear()
        for link_key, link in self.network.links.items():
            if link_key in self.links:
                continue
            elif self.IsReachable(link) and self.WorthAdding(link):
                if self.AddLink(link, link_key):
                    new_link_added = True
                was_improved = True

        if not was_improved:
            new_link_added = self.AddFromP2()

        return new_link_added

    def IsReachable(self, link: Link) -> bool:
        return link.src in self.nodes and link.dest in self.nodes

    def WorthAdding(self, link: Link) -> bool:
        src_node = self.nodes[link.src]
        dest_node = self.nodes[link.dest]
        if src_node.pi_max + link.cost < dest_node.pi_max:
            self.p2Cont.append(link)
            if src_node.pi_min + link.cost < dest_node.pi_min:
                return True

    def AddFromP2(self):
        added = False
        for link in self.p2Cont:
            if self.AddLink(link):
                added = True
        return added

    def AddLink(self, link: Link, link_key: str | None = None):
        key = link_key if link_key else create_link_key(link.src, link.dest)
        if key in self.links:
            return False
        self.links[key] = link
        src_node_index = link.src
        if src_node_index not in self.nodes:
            src_node = self.network.nodes[src_node_index]
            assert src_node
            self.nodes[src_node_index] = src_node
        dest_node_index = link.dest
        if dest_node_index not in self.nodes:
            dest_node = self.network.nodes[dest_node_index]
            assert src_node
            self.nodes[dest_node_index] = dest_node

        return True

    def TopogologicalSortUtil(self, node_index: int, visited: Dict[int, bool], stack: List[int]) -> None:
        visited[node_index] = True
        for neighbor_index in self.GetNeighbors(node_index):
            if neighbor_index not in visited:
                self.TopogologicalSortUtil(neighbor_index, visited, stack)

        stack.insert(0, node_index)

    def GetTopoSortedNodesIndexes(self) -> List[int]:
        ordered_nodes = []
        visited = {}
        for node_index in list(self.nodes):
            if node_index not in visited:
                self.TopogologicalSortUtil(
                    node_index,
                    visited,
                    ordered_nodes
                )

        return ordered_nodes

    def UpdateTopoSort(self):
        self.nodesOrder = self.GetTopoSortedNodesIndexes()

    def BuildTrees(self) -> None:
        for node in self.nodes.values():
            node.pi_max = 0
            node.pi_min = math.inf
            node.alpha_max = None
            node.alpha_min = None

        self.nodes[self.originIndex].pi_min = 0

        for node_index in self.nodesOrder:
            incoming_links = self.GetIncomingLinks(node_index)
            dest_node = self.nodes[node_index]
            for link in incoming_links:
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
