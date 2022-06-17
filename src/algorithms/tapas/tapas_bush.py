""" TAPAS Bush class """
from typing import List, Set

from src.algorithms.tapas.pas_manager import PasManager
from src.algorithms.tapas.tapas_bush_graph import TapasBushGraph
from src.shared.consts import ZERO_FLOW
from src.shared.link import Link
from src.shared.network import Network


class TapasBush():
    """ Bush for the TAPAS algorithm """

    def __init__(
        self,
        originIndex: int,
        network: Network,
        demands,
        error: float,
        pasManager: PasManager
    ):
        self.originIndex = originIndex
        self.subgraph = TapasBushGraph(network, originIndex, demands)
        self.error = error
        self.m = len(self.subgraph.nodes) - 1
        self.pasManager = pasManager
        self.topo_order = []
        self.clock = 1

    def RemoveCyclicFlows(self):
        while True:
            if not self.TopologicalSort():
                break

    def BuildTrees(self):
        self.subgraph.BuildTrees()

    def Equilibrate(self) -> None:
        self.subgraph.network.BuildMinTree(self.originIndex)
        self.pasManager.RecalculatePASCosts()

        incoming_links_dict = self.subgraph.GetAllIncomingLinks()
        for node_index, node in self.subgraph.nodes.items():
            shortest_path_link = node.alpha_min
            if shortest_path_link is None:
                continue
            incoming_links = incoming_links_dict[node_index]
            for link in incoming_links:
                if (
                    self.subgraph.bush_flow[link.index] <= ZERO_FLOW or
                    link is shortest_path_link
                ):
                    continue
                self.pasManager.CreateNewPAS(self.subgraph, link, node_index)

        for pas in self.pasManager.pasList:
            pas.MoveFlow()

    # Should have one topo sort
    def TopologicalSort(self):
        self.clock = 1
        self.topo_order.clear()
        visited = set()
        explored_links = []
        for node in self.subgraph.nodes.values():
            node.pre = 0
            node.post = 0

        for index in self.subgraph.nodes:
            if index not in visited:
                tmp = self.Explore(index, visited, explored_links)
                if tmp:
                    return True

        return False

    def Explore(self, vertex: int, visited: Set[int], explored_links: List[Link]):
        visited.add(vertex)
        self.PreVisit(vertex)
        links_list = self.subgraph.GetOutcomingLinks(vertex)

        index = -1
        detected = False
        for link in links_list:
            index = link.dest
            if self.subgraph.bush_flow[link.index] > ZERO_FLOW:
                explored_links.append(link)
                if self.subgraph.nodes[index].pre == 0:
                    detected = self.Explore(index, visited, explored_links)
                    if detected:
                        return True
                if self.subgraph.nodes[index].pre > 0 and self.subgraph.nodes[index].post == 0:
                    return self.HandleBackEdge(link, explored_links)
        self.PostVisit(vertex)
        return False

    def HandleBackEdge(self, link: Link, explored_links: List[Link]):
        link_index = link.index
        next_node = link.src
        term_node = link.dest
        next_link = None
        cycle: List[Link] = [link]
        flow = 0.0
        min_flow = self.subgraph.bush_flow[link_index]
        for next_link in explored_links:
            if next_link.dest == next_node:
                flow = self.subgraph.bush_flow[next_link.index]
                cycle.append(next_link)
                if flow < min_flow:
                    min_flow = flow
                next_node = next_link.src
                if next_node == term_node:
                    break

        link_tmp = None
        link_tmp_index = -1
        for link_tmp in cycle:
            link_tmp_index = link_tmp.index
            self.subgraph.AddFlowToBushFlow(link_tmp_index, -min_flow)
            link_tmp.AddFlow(-min_flow)
        return True

    def PreVisit(self, vertex: int):
        self.subgraph.nodes[vertex].pre = self.clock
        self.clock += 1

    def PostVisit(self, vertex: int):
        self.subgraph.nodes[vertex].post = self.clock
        self.clock += 1
        self.topo_order.insert(0, vertex)
