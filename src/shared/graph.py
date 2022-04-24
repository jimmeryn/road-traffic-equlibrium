""" Graph Class """
import math
from typing import Dict

from src.shared.link import Link
from src.shared.node import Node
from src.utils.link_utils import create_link_key


class Graph:
    """
    Class used to store all graph info
    """

    def __init__(self, nodes, links, demands):
        self.links = self.CreateLinksDict(links)
        self.nodes: Dict[int, Node] = self.CreateNodesDict(nodes)
        self.n: int = int(nodes[-1][0])

        self.BuildTrees()
        self.SetFlows(demands)

    def CreateLinksDict(self, links):
        return dict(
            map(lambda link: (
                create_link_key(link[0], link[1]),
                Link(*link)
            ), links)
        )

    def CreateNodesDict(self, nodes):
        return dict(
            map(lambda node: (
                int(node[0]),
                Node(node[0])
            ), nodes)
        )

    def SetFlows(self, demands):
        for from_node, demands_array in enumerate(demands):
            for to_node, demand in enumerate(demands_array):
                if demand != 0:
                    link = self.nodes[to_node + 1].alpha_min
                    while link is not None and link.src == from_node + 1:
                        link.AddFlow(demand)
                        link = self.nodes[link.src].alpha_min

    def BuildTrees(self):
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

    def GetLink(self, from_node, to_node):
        return self.links.get(create_link_key(from_node, to_node))

    def GetFlowArray(self):
        flow_array = []
        for link in self.links.values():
            flow_array.append(link.flow)

        return flow_array

    def LogFlow(self) -> None:
        for key, link in self.links.items():
            print(f"{key}: {link.flow}")

    def LogCosts(self) -> None:
        for key, link in self.links.items():
            print(f"{key}: {link.cost}")

    def LogGraph(self) -> None:
        for node in self.nodes.values():
            print(node.index)
            print(f"pi_max: {node.pi_max}")
            print(f"pi_min: {node.pi_min}")
            alpha_max = node.alpha_max
            alpha_min = node.alpha_min
            if alpha_max:
                print(f"alpha_max: {node.alpha_max.src}_{node.alpha_max.dest}")
            if alpha_min:
                print(f"alpha_min: {node.alpha_min.src}_{node.alpha_min.dest}")
            print("\n")
