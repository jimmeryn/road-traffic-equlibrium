""" Bush Class"""
import math
from typing import Tuple

from src.algorithms.b.bush_graph import BushGraph
from src.shared.link import Link
from src.shared.network import Network


class Bush:
    """ Bush Class """

    def __init__(self, originIndex: int, network: Network, demands, error: float) -> None:
        self.originIndex = originIndex
        self.p2Cont = []
        self.error = error
        # not sure if this should be calculated or to get this from links list
        self.m = len(self.subgraph.links) - 1
        self.UpdateTopoSort()
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
        iteration_count = 0
        while exp_factor * delta_c > self.error and iteration_count < 100:
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
            iteration_count += 1
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

    def UpdatePathFlow(
        self,
        delta_x: int,
        k: int,
        j: int,
        alpha_param: str
    ) -> Tuple[int, float, float]:
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

    def BuildTrees(self):
        self.subgraph.BuildTrees(self.originIndex)

    def RemoveUnusedLinks(self) -> None:
        self.subgraph.RemoveEmptyLinks()

    def Improve(self):
        self.BuildTrees()
        added_better_links = self.AddBetterLinks()
        if added_better_links:
            self.UpdateTopoSort()
            self.BuildTrees()

    # TODO: Probably should move this 3 metods to the BushGraph class
    def AddBetterLinks(self) -> bool:
        was_improved = False
        new_link_added = False
        self.p2Cont.clear()
        for link_key, link in self.subgraph.network.links.items():
            if link_key in self.subgraph.links:
                continue
            elif self.IsReachable(link) and self.WorthAdding(link):
                if self.AddLink(link, link_key):
                    new_link_added = True
                was_improved = True

        if not was_improved:
            new_link_added = self.AddFromP2()

        return new_link_added

    def IsReachable(self, link: Link) -> bool:
        return self.subgraph.nodes[link.src] and self.subgraph.nodes[link.dest]

    def WorthAdding(self, link: Link) -> bool:
        link_cost = link.cost
        src_node = self.subgraph.nodes[link.src]
        dest_node = self.subgraph.nodes[link.dest]
        if src_node.pi_max + link_cost < dest_node.pi_max:
            self.p2Cont.append(link)
            if link_cost + src_node.pi_min < dest_node.pi_min:
                return True

    def AddFromP2(self):
        added = False
        for link in self.p2Cont:
            if self.AddLink(link):
                added = True
        return added

    def AddLink(self, link: Link, link_key: str | None = None):
        key = link_key if link_key else create_link_key(link.src, link.dest)
        if key in self.subgraph.links:
            return False
        self.subgraph.links[key] = link
        src_node_index = link.src
        if src_node_index not in self.subgraph.nodes:
            src_node = self.subgraph.network.nodes[src_node_index]
            assert src_node
            self.subgraph.nodes[src_node_index] = src_node
        dest_node_index = link.dest
        if dest_node_index not in self.subgraph.nodes:
            dest_node = self.subgraph.network.nodes[dest_node_index]
            assert src_node
            self.subgraph.nodes[dest_node_index] = dest_node

        return True

            while origin_node != node:
                node.alpha_min.AddFlow(demand)
                node = self.subgraph.nodes[node.alpha_min.src]
