""" Pas manager """
import math
from typing import Dict, List

from src.algorithms.tapas.pas import Pas
from src.algorithms.tapas.tapas_bush_graph import TapasBushGraph
from src.shared.consts import DIR_TOLERANCE, MU, ZERO_FLOW, V
from src.shared.link import Link
from src.shared.network import Network


class PasManager():
    """ Pas manager class """

    def __init__(self, net: Network) -> None:
        self.network: Network = net
        self.pasList: List[Pas] = []
        self.iteration_number: int = 1
        self.mu = MU
        self.v = V

    def RecalculatePASCosts(self):
        for pas in self.pasList:
            pas.RecalculateCosts()

    def PasExist(self, cheapLink: Link, expLink: Link) -> Pas | None:
        for pas in self.pasList:
            if pas.GetLastExpLink() is expLink and pas.GetLastCheapLink() is cheapLink:
                return pas
        return None

    def CreateExpSegment(self, pas: Pas, checked_links: Dict[int, Link | None], diverge_node: int, node_index: int):
        start = diverge_node
        while start != node_index:
            link = checked_links[start]
            pas.PushBackToExp(link)
            pas.expCost += link.cost
            start = link.dest

    def CreateCheapSegment(self, pas: Pas, diverge_node: int, node_index: int):
        link = self.network.nodes[node_index].alpha_min
        next_dest = link.src
        while link is not None:
            pas.PushFrontToCheap(link)
            next_dest = link.src
            if next_dest == diverge_node:
                return
            link = self.network.nodes[next_dest].alpha_min

    def GetShortestPathNodes(self, graph: TapasBushGraph, node_index: int):
        shortest_path = {node_index}
        link = graph.nodes[node_index].alpha_min
        while link is not None:
            shortest_path.add(link.src)
            link = graph.nodes[link.src].alpha_min

        return shortest_path

    def CreatePas(self, graph: TapasBushGraph, exp_link: Link, node_index: int, check: bool):
        queue = [exp_link]
        checked_nodes = dict.fromkeys(graph.nodes, False)
        checked_links: Dict[int, Link | None] = dict.fromkeys(graph.nodes, None)
        can_stop = False
        shortest_path_nodes = self.GetShortestPathNodes(graph, node_index)
        incoming_links_dict = graph.GetAllIncomingLinks()
        thr = self.v * graph.bush_flow[exp_link.index]
        created = True

        while not can_stop:
            if not queue:
                created = False
                break
            first_in_queue = queue.pop(0)
            checked_links[first_in_queue.src] = first_in_queue

            if first_in_queue.src in shortest_path_nodes:
                diverge_node = first_in_queue.src
                break

            for link in incoming_links_dict[first_in_queue.src]:
                origin_flow = graph.bush_flow[link.index]
                if not check or (check and origin_flow > thr):
                    node_from_index = link.src
                    if origin_flow > ZERO_FLOW and not checked_nodes[node_from_index]:
                        queue.append(link)
                        checked_nodes[node_from_index] = True
                        checked_links[node_from_index] = link

                        if node_from_index in shortest_path_nodes:
                            diverge_node = node_from_index
                            can_stop = True
                            break

            checked_nodes[first_in_queue.src] = 0

        if not created:
            return None

        pas = Pas()
        self.CreateExpSegment(pas, checked_links, diverge_node, node_index)
        self.CreateCheapSegment(pas, diverge_node, node_index)
        if pas.GetCostDiff() < DIR_TOLERANCE:
            del pas
            pas = None
        else:
            pas.AddOrigin(graph)
            self.pasList.append(pas)

        return pas

    def CalculateReducedCost(self, exp_link: Link):
        return self.network.nodes[exp_link.src].pi_min + exp_link.cost - self.network.nodes[exp_link.dest].pi_min

    def CalcThreshold(self):
        return 10.0 * math.pow(10, -self.iteration_number)

    def CreateNewPAS(self, graph: TapasBushGraph, expLink: Link, mergingNodeIndex: int):
        found_pas = self.PasExist(
            self.network.nodes[mergingNodeIndex].alpha_min, expLink)
        is_effective = False
        reduced_cost = self.CalculateReducedCost(expLink)
        exp_index = expLink.index
        red_val = self.mu * reduced_cost
        if found_pas is not None:
            found_pas.AddOrigin(graph)
            is_effective = found_pas.CheckIfEffective(
                red_val, self.v, exp_index, graph)
        else:
            pas_tmp = self.CreatePas(graph, expLink, mergingNodeIndex, False)
            if pas_tmp is not None:
                is_effective = pas_tmp.CheckIfEffective(
                    red_val, self.v, exp_index, graph)

        if reduced_cost > self.CalcThreshold() and not is_effective:
            self.CreatePas(graph, expLink, mergingNodeIndex, True)

    def DeleteUnusedPASAndMoveFlow(self) -> None:
        self.iteration_number += 1

        def filter_pas(pas: Pas):
            pas.MoveFlow()
            return not pas.IsUnused()

        filter(filter_pas, self.pasList)
