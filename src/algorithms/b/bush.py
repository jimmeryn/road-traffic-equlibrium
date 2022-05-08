""" Bush Class"""
import math
from typing import Tuple

from src.algorithms.b.bush_graph import BushGraph
from src.shared.graph import Graph
from src.shared.link import Link


class Bush:
    """ Bush Class """

    def __init__(self, originIndex: int, graph: Graph, demands, error: float) -> None:
        self.originIndex = originIndex
        self.subgraph = BushGraph(graph, originIndex)
        self.error = error
        # not sure if this should be calculated or to get this from links list
        self.m = len(self.subgraph.links) - 1
        self.subgraph.UpdateTopoSort()
        self.BuildTrees()
        self.ApplyInitialDemands(demands)

    def UpdateTopoSort(self):
        self.subgraph.UpdateTopoSort()

    def Equilibrate(self) -> None:
        self.UpdateTopoSort()
        for node_index in reversed(self.subgraph.nodesOrder):
            node = self.subgraph.nodes[node_index]
            if node.alpha_max and node.pi_min < node.pi_max:
                [k, *params] = self.GetBranchNode(node_index)
                if k > 0:
                    self.EqualizeCost(k, node_index, *params)

    def GetBranchNode(self, j: int):
        ij_min = self.subgraph.nodes[j].alpha_min
        ij_max = self.subgraph.nodes[j].alpha_max
        x_min = ij_min.flow
        x_max = ij_max.flow
        c_min = ij_min.cost
        c_max = ij_max.cost
        c_der_min = ij_min.cost_der
        c_der_max = ij_max.cost_der
        m_min = 1
        m_max = 1
        while ij_max.src != ij_min.src:
            while ij_min.src < ij_max.src:
                ij_max = self.subgraph.nodes[ij_max.src].alpha_max
                x_max = min(x_max, ij_max.flow)

                c_max += ij_max.cost
                c_der_max += ij_max.cost_der
                m_max += 1

            while ij_max.src < ij_min.src:
                ij_min = self.subgraph.nodes[ij_min.src].alpha_min
                x_min = min(x_min, ij_min.flow)

                c_min += ij_min.cost
                c_der_min += ij_min.cost_der
                m_min += 1

        exp_factor = 1 + math.floor(self.m - max(m_min, m_max) / 2)
        condition = exp_factor * (c_max - c_min) < self.error
        k = 0 if condition else ij_max.src

        return [k, x_min, x_max, c_min, c_max, c_der_min, c_der_max, exp_factor]

    def EqualizeCost(
        self,
        k: int,
        j: int,
        x_min: int,
        x_max: int,
        c_min: float,
        c_max: float,
        c_der_min: float,
        c_der_max: float,
        exp_factor: int,
    ) -> None:
        [delta_x, delta_c] = self.GetDeltaXandC(
            x_min, x_max, c_min, c_max, c_der_min, c_der_max)
        while exp_factor * delta_c > self.error:
            [
                x_min,
                c_min,
                c_der_min
            ] = self.UpdatePathFlow(delta_x, k, j, "alpha_min")
            [
                x_max,
                c_max,
                c_der_max
            ] = self.UpdatePathFlow(-delta_x, k, j, "alpha_max")
            [
                delta_x,
                delta_c
            ] = self.GetDeltaXandC(x_min, x_max, c_min, c_max, c_der_min, c_der_max)
            self.BuildTrees()
        return

    def GetDeltaXandC(
        self,
        x_min: int,
        x_max: int,
        c_min: float,
        c_max: float,
        c_der_min: float,
        c_der_max: float
    ) -> Tuple[int, float]:
        delta_x_max = x_max if c_min < c_max else x_min
        if delta_x_max <= 0:
            return (0, 0.0)
        if c_der_max + c_der_min <= 0:
            delta_x = x_max if c_min <= c_max else -x_min
        else:
            delta_x = min(
                delta_x_max,
                (c_max - c_min) / (c_der_max + c_der_min)
            )

        return (delta_x, abs(c_max - c_min))

    def UpdatePathFlow(self, delta_x: int, k: int, j: int, alpha_param: str) -> Tuple[int, float, float]:
        x_p = math.inf
        c_p = 0.0
        c_der_p = 0.0
        i = j
        while i != k:
            link: Link | None = self.subgraph.nodes[i][alpha_param]
            src = link.src
            dest = link.dest
            link.AddFlow(delta_x)
            x_ij = link.flow
            x_p = min(x_p, x_ij)

            c_p += self.subgraph.GetLink(src, dest).cost
            c_der_p += self.subgraph.GetLink(src, dest).cost_der
            i = src

        return (x_p, c_p, c_der_p)

    def RemoveUnusedLinks(self) -> None:
        pass

    def Improve(self):
        pass

    def ApplyInitialDemands(self, demands):
        for index, demand in enumerate(demands):
            if demand == 0:
                continue
            node_index = index + 1
            origin_node = self.subgraph.nodes[self.originIndex]
            node = self.subgraph.nodes[node_index]
            while True:
                if origin_node == node:
                    break
                node.alpha_min.AddFlow(demand)
                node = self.subgraph.nodes[node.alpha_min.src]

    def BuildTrees(self):
        for node in self.subgraph.nodes.values():
            node.pi_max = 0
            node.pi_min = math.inf
            node.alpha_max = None
            node.alpha_min = None

        self.subgraph.nodes[self.originIndex].pi_min = 0

        for node_index in self.subgraph.nodesOrder:
            incoming_links = self.subgraph.GetIncomingLinks(node_index)
            for link in incoming_links:
                cij = link.cost
                src = link.src
                dest = link.dest
                src_node = self.subgraph.nodes[src]
                dest_node = self.subgraph.nodes[dest]

                # min distance
                new_cost = src_node.pi_min + cij
                if new_cost < dest_node.pi_min:
                    dest_node.pi_min = new_cost
                    dest_node.alpha_min = link

                # max distance
                new_cost = src_node.pi_max + cij
                if new_cost >= dest_node.pi_max:
                    dest_node.pi_max = new_cost
                    dest_node.alpha_max = link

    def BuildTreesDijkstra(self) -> None:
        for node in self.subgraph.nodes.values():
            node.pi_max = 0
            node.pi_min = math.inf
            node.alpha_max = None
            node.alpha_min = None

        self.subgraph.nodes[self.originIndex].pi_min = 0

        for node_index in self.subgraph.nodesOrder:
            incoming_links = self.subgraph.GetIncomingLinks(node_index)
            for link in incoming_links:
                cij = link.cost
                src = link.src
                dest = link.dest
                src_node = self.subgraph.nodes[src]
                dest_node = self.subgraph.nodes[dest]

                # min distance
                new_cost = src_node.pi_min + cij
                if new_cost < dest_node.pi_min:
                    dest_node.pi_min = new_cost
                    dest_node.alpha_min = link

                # max distance
                new_cost = src_node.pi_max + cij
                if new_cost >= dest_node.pi_max:
                    dest_node.pi_max = new_cost
                    dest_node.alpha_max = link
