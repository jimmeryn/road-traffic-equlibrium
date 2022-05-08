""" BushGraph """
from copy import deepcopy
from typing import Dict, List, Tuple

from src.shared.graph import Graph
from src.shared.link import Link
from src.shared.node import Node
from src.utils.link_utils import create_link_key


class BushGraph:
    """Class implementing sub-graph structure for bush """

    def __init__(self, graph: Graph, originIndex: int) -> None:
        self.graph = graph
        self.originIndex = originIndex
        (nodes, links) = self.GetReachableNodesAndLinks()
        self.nodes = deepcopy(nodes)
        self.links = deepcopy(links)
        self.nodesOrder = self.GetTopoSortedNodesOrder()

    def GetReachableNodesAndLinks(self) -> Tuple[Dict[int, Node], Dict[str, Link]]:
        nodes = self.GetReachableForNode(self.graph.nodes[self.originIndex])
        links = dict()
        for key, link in self.graph.links.items():
            if (
                link.src in nodes and
                link.dest in nodes and
                link.src < link.dest
            ):
                links[key] = link

        return (nodes, links)

    def TopogologicalSortUtil(
        self,
        v: int,
        visited: Dict[int, bool],
        stack: Dict[int, Node]
    ) -> None:
        visited[v] = True
        for key in self.GetNeighbors(v):
            if key not in visited:
                self.TopogologicalSortUtil(key, visited, stack)

        stack[v] = self.graph.nodes[v]

    def TopogologicalSortUtil2(self, v: int, visited: List[int], stack: List[Node]) -> None:
        visited[v - 1] = True
        for i in self.GetNeighbors(v):
            if not visited[i - 1]:
                self.TopogologicalSortUtil2(i, visited, stack)

        stack.insert(0, self.nodes[v].index)

    def GetTopoSortedNodesOrder(self) -> List[int]:
        ordered_nodes = []
        visited = [False] * len(self.nodes)
        self.TopogologicalSortUtil2(self.originIndex, visited, ordered_nodes)

        return ordered_nodes

    def UpdateTopoSort(self):
        self.nodesOrder = self.GetTopoSortedNodesOrder()

    def GetReachableForNode(self, node: Node) -> Dict[int, Node]:
        reachable_nodes = {}
        visited = {}
        self.TopogologicalSortUtil(node.index, visited, reachable_nodes)

        return reachable_nodes

    def GetNeighbors(self, index: int) -> List[int]:
        return list(
            map(
                lambda link: link.dest,
                filter(
                    lambda link: link.src == index,
                    self.graph.links.values()
                )
            )
        )

    def GetIncomingLinks(self, node_index: int) -> List[Link]:
        links = []
        for link in self.links.values():
            if link.dest == node_index:
                links.append(link)
        return links

    def GetLink(self, from_node: int, to_node: int) -> (Link | None):
        return self.links.get(create_link_key(from_node, to_node))
