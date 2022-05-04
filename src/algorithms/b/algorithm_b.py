"""Algorithm B Class"""
from typing import Dict

from src.algorithms.algorithm import Algorithm
from src.algorithms.b.bush import Bush
from src.shared.graph import Graph


class AlgorithmB(Algorithm):
    """ Algorithm B Class """

    def __init__(self, nodes, networks, demands, error: float) -> None:
        self.graph = Graph(nodes, networks)
        self.bushes = self.CreateBushes(demands, self.graph, error)

    def CreateBushes(self, demands, graph: Graph, error: float) -> Dict[int, Bush]:
        bushes: Dict[int, Bush] = {}
        for from_node, demands_array in enumerate(demands):
            from_node_index = from_node + 1
            for to_node, demand in enumerate(demands_array):
                _to_node_index = to_node + 1
                if demand == 0 or from_node_index in bushes:
                    continue
                bushes[from_node_index] = Bush(
                    from_node_index,
                    graph,
                    demands_array,
                    error
                )

        return bushes

    def Iteration(self) -> None:
        for bush in self.bushes.values():
            bush.UpdateTopoSort()
            bush.BuildTrees()
            bush.Equilibrate()

    def GetMaxGap(self):
        for link in self.graph.links.values():
            link.ResetFlow()
        for bush in self.bushes.values():
            for link_key, link in bush.subgraph.links.items():
                self.graph.links[link_key].AddFlow(link.flow)
        self.graph.BuildTrees()
        return self.graph.GetMaxGap()
