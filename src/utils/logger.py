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
        log_string = "{node_index}: max: {alpha_max} ({pi_max}), min: {alpha_min} ({pi_min})"
        default_message_params = {
            "node_index": -1,
            "pi_max": -1,
            "pi_min": -1,
            "alpha_max": None,
            "alpha_min": None,
        }
        print("node_index: max: alpha_max (pi_max), min: alpha_min (pi_min)")
        for node in nodes.values():
            message_params = default_message_params
            message_params["node_index"] = node.index
            message_params["pi_max"] = node.pi_max
            message_params["pi_min"] = node.pi_min
            alpha_max = node.alpha_max
            alpha_min = node.alpha_min
            if alpha_max:
                message_params["alpha_max"] = f"{node.alpha_max.src}_{node.alpha_max.dest}"
            if alpha_min:
                message_params["alpha_min"] = f"{node.alpha_min.src}_{node.alpha_min.dest}"
            print(log_string.format(**message_params))

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
        error_message = "Expected link ({src}_{dest}) flow to be {flow_calc}, got {flow}."
        try:
            for link in solution.values:
                link_key = create_link_key(link[0], link[1])
                graph_link = graph.links[link_key]
                diff = abs(graph_link.flow - link[2])
                max_dif = max(max_dif, diff)
                error_message_params = {
                    "src": graph_link.src,
                    "dest": graph_link.dest,
                    "flow_calc": link[2],
                    "flow": graph_link.flow,
                }
                assert diff < 1, error_message.format(**error_message_params)
        except AssertionError as assertion_error:
            print(f"Test failed. \n{assertion_error}")
            return
        print(f"Test passed. Max difference: {max_dif}")
