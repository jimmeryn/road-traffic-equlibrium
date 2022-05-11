""" Logger """
from typing import Dict

from src.shared.graph import Graph
from src.shared.link import Link
from src.shared.node import Node
from src.utils.link_utils import create_link_key


class Logger:
    """ Class used to print graph data """

    @staticmethod
    def LogFlow(links: Dict[int, Link]) -> None:
        for key, link in links.items():
            print(f"{key}: {link.flow}")

    @staticmethod
    def LogCosts(links: Dict[int, Link]) -> None:
        for key, link in links.items():
            print(f"{key}: {link.cost}")

    @staticmethod
    def LogGraphLinks(links: Dict[int, Link]) -> None:
        print("Links:")
        print("source_target: c(flow) = cost")
        for key, link in links.items():
            print(f"{key}: c({link.flow}) = {link.cost}")
        print("\n")

    @staticmethod
    def LogGraphNodes(nodes: Dict[int, Node]) -> None:
        for node in nodes.values():
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

    @staticmethod
    def LogMinPaths(nodes: Dict[int, Node], originIndex: int = 1):
        for node in nodes.values():
            print(f"NODE {node.index} min path")
            current_node = node
            origin_node = nodes[originIndex]
            while current_node.index != origin_node.index:
                print(current_node.index)
                if current_node.alpha_min is None:
                    break
                current_node = nodes[current_node.alpha_min.src]

    @staticmethod
    def LogSolution(solution):
        print("Solution:")
        for link in solution.values:
            print(f"{int(link[0])}_{int(link[1])}: c({link[2]}) = {link[3]}")

    @staticmethod
    def CompareSolution(solution, graph: Graph):
        print("Compare Solution:")
        print("source_target: c(calculated_flow | solution_flow) = calculated_cost | solution_cost")
        for link in solution.values:
            link_key = f"{int(link[0])}_{int(link[1])}"
            graph_link = graph.links[link_key]
            print(
                f"{link_key}: c({graph_link.flow} | {link[2]}) = {graph_link.cost} | {link[3]}"
            )

    @staticmethod
    def TestSolution(solution, graph: Graph):
        print("Testing solution...")
        max_dif = 0
        for link in solution.values:
            link_key = create_link_key(link[0], link[1])
            graph_link = graph.links[link_key]
            diff = abs(graph_link.flow - link[2])
            max_dif = max(max_dif, diff)
            assert diff < 1, f"Expected link flow to be {link[2]}, got {graph_link.flow}."
        print(f"Test passed. Max difference: {max_dif}")
