""" Graph Class """
import math
from typing import Dict

from src.shared.link import Link
from src.shared.node import Node


def createLinkKey(from_node: int, to_node: int):
    return f"{from_node}_{to_node}"


class Graph:
    """
    Class used to store all graph info
    """

    def __init__(self, nodes, links, demands):
        self.A = self.CreateLinksDict(links)
        self.nodes: Dict[int, Node] = self.CreateNodesDict(nodes)
        self.n: int = nodes[-1][0]

        self.SetFlows(demands)
        self.SetLinksCosts()
        self.BuildTrees()

    def CreateLinksDict(self, links):
        return dict(
            map(lambda link: (
                createLinkKey(int(link[0]), int(link[1])),
                Link(link[0], link[1], link[4])
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
                    link = self.A.get(createLinkKey(from_node + 1, to_node + 1))
                    link.flow = demand
                    link.cost = link.CalculateCost()

    def SetLinksCosts(self):
        for link in self.A.values():
            link.cost = link.CalculateCost()

    def BuildTrees(self):
        for i in range(1, self.n + 1):
            self.nodes[i].pi_max = -math.inf
            self.nodes[i].pi_min = math.inf
            self.nodes[i].alpha_max = None
            self.nodes[i].alpha_min = None

        self.nodes[1].pi_max = 0
        self.nodes[1].pi_min = 0

        for _ in range(1, self.n):
            for link in self.A.values():
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
        return self.A.get(createLinkKey(from_node, to_node))

    def GetFlowArray(self):
        flow_array = []
        for _key, link in self.A.items():
            flow_array.append(link.flow)

        return flow_array
