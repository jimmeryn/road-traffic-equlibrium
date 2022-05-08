""" Graph Class """
import math
from typing import Dict, List

from src.shared.link import Link
from src.shared.node import Node
from src.utils.link_utils import create_link_key


class Graph:
    """
    Class used to store all graph info
    """

    def __init__(self, nodes, links):
        self.links = self.CreateLinksDict(links)
        self.nodes = self.CreateNodesDict(nodes)
        self.sortedNodes = self.GetTopoSortedNodes()
        self.n: int = int(nodes[-1][0])
        self.BuildTrees()

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

    def GetMaxGap(self) -> float:
        gap = 0
        for node in self.nodes.values():
            if node.pi_max is not None and node.pi_min is not None:
                gap = max(node.pi_max - node.pi_min, gap)
        return gap

    def GetNeighbors(self, index: int) -> List[int]:
        return list(map(lambda link: link.dest, filter(lambda link: link.src == index, self.links.values())))

    def TopogologicalSortUtil(self, v: int, visited: List[int], stack: List[Node]) -> None:
        visited[v - 1] = True
        for i in self.GetNeighbors(v):
            if not visited[i - 1]:
                self.TopogologicalSortUtil(i, visited, stack)

        stack.insert(0, self.nodes[v])

    def GetTopoSortedNodes(self) -> List[Node]:
        ordered_nodes = []
        visited = [False] * len(self.nodes)
        for k in list(self.nodes):
            if not visited[k - 1]:
                self.TopogologicalSortUtil(k, visited, ordered_nodes)

        return ordered_nodes

    def TopoSortNodes(self) -> None:
        self.sortedNodes = self.GetTopoSortedNodes()

    def SetInitialFlows(self, demands) -> None:
        for from_node, demands_array in enumerate(demands):
            for to_node, demand in enumerate(demands_array):
                if demand != 0:
                    link = self.nodes[to_node + 1].alpha_min
                    while link is not None and link.src == from_node + 1:
                        link.AddFlow(demand)
                        link = self.nodes[link.src].alpha_min

    def BuildTrees(self) -> None:
        for i in range(1, self.n + 1):
            self.nodes[i].pi_max = -math.inf
            self.nodes[i].pi_min = math.inf
            self.nodes[i].alpha_max = None
            self.nodes[i].alpha_min = None

        self.nodes[1].pi_max = 0
        self.nodes[1].pi_min = 0

        for _ in range(1, self.n):
            for link in self.links.values():
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

    def GetFlowArray(self) -> List[int]:
        flow_array = []
        for link in self.links.values():
            flow_array.append(link.flow)

        return flow_array

    def RelabelNodes(self, i: int, j: int) -> None:
        self.nodes[i], self.nodes[j] = self.nodes[j], self.nodes[i]
