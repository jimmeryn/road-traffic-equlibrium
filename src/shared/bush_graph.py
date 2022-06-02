""" BushGraph """
import math
from typing import Dict, List, Tuple

from src.shared.consts import ZERO_FLOW
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
        self.demands = demands
        self.bush_flow = self.GetBushFlowDict()
        (nodes, links) = self.GetReachableNodesAndLinks()
        self.nodes = nodes
        self.links = links
        self.nodesOrder = self.GetTopoSortedNodesIndexes()
        self.p2Cont: List[Link] = []
        self.BuildTrees()

    def GetReachableNodesAndLinks(self) -> Tuple[Dict[int, Node], Dict[str, Link]]:
        self.network.BuildMinTree(self.originIndex)
        links: Dict[str, Link] = dict()
        nodes: Dict[int, Node] = dict()
        for key, demand in enumerate(self.demands):
            node_key = key + 1
            link = self.network.nodes[node_key].alpha_min
            while link is not None:
                link.AddFlow(demand)
                self.AddFlowToBushFlow(link.index, demand)
                links[link.index] = link
                link = self.network.nodes[link.src].alpha_min

        # for key, link in links.items():
        #     src_node = self.network.nodes[link.src]
        #     dest_node = self.network.nodes[link.dest]
        #     if key in nodes:
        #         continue
        #     nodes[link.src] = src_node
        #     nodes[link.dest] = dest_node
        nodes = self.network.nodes

        return (nodes, links)

    def GetBushFlowDict(self):
        return dict(
            map(
                lambda link: (link.index, 0.0),
                self.network.links.values()
            )
        )

    def AddFlowToBushFlow(self, link_index: str, flow: float):
        self.bush_flow[link_index] += flow
        if self.bush_flow[link_index] <= ZERO_FLOW:
            self.bush_flow[link_index] = 0.0

    def RemoveEmptyLinks(self):
        for link_key, link in self.links.copy().items():
            if self.bush_flow[link_key] <= ZERO_FLOW and len(self.GetIncomingLinks(link.dest)) > 1:
                del self.links[link_key]

    def AddBetterLinks(self) -> bool:
        was_improved = False
        new_link_added = False
        self.p2Cont.clear()
        for link_key, link in self.network.links.items():
            if link_key in self.links:
                continue
            if self.IsReachable(link) and self.WorthAdding(link):
                if self.AddLink(link):
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

        return False

    def AddFromP2(self):
        added = False
        for link in self.p2Cont:
            if self.AddLink(link):
                added = True
        return added

    def AddLink(self, link: Link):
        if link.index in self.links:
            return False
        src_node_index = link.src
        dest_node_index = link.dest
        # src_node = self.nodes[src_node_index]
        # dest_node = self.nodes[dest_node_index]
        # demand_to = self.GetDemand(dest_node_index)
        self.links[link.index] = link

        if src_node_index not in self.nodes:
            new_node = self.network.nodes[src_node_index]
            self.nodes[src_node_index] = new_node

        if dest_node_index not in self.nodes:
            new_node = self.network.nodes[dest_node_index]
            self.nodes[dest_node_index] = new_node

        return True

    def GetDemand(self, index: int) -> float:
        return self.demands[index - 1] if self.demands.size > index - 1 else 0.0

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
