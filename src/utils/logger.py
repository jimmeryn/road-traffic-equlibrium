""" Logger """
from typing import Any, Dict, Literal

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
    def LogPaths(
        nodes: Dict[int, Node],
        path_prop: Literal["min", "max"],
        origin_index: int = 1
    ) -> None:
        path_prop_name = f"alpha_{path_prop}"
        for node in nodes.values():
            current_node = node
            origin_node = nodes[origin_index]
            path = []
            while current_node.index != origin_node.index:
                path.append(current_node.index)
                if current_node[path_prop_name] is None:
                    break
                path_link: Link = current_node[path_prop_name]
                next_index = path_link.src
                current_node = nodes[next_index]
            path.append(origin_index)
            print(f"{node.index}.NODE {path_prop} path: {path}")
        print("\n")

    @staticmethod
    def LogSolution(solution: Any) -> None:
        print("Solution:")
        for link in solution.values:
            print(f"{int(link[0])}_{int(link[1])}: c({link[2]}) = {link[3]}")

    @staticmethod
    def CompareSolution(solution: Any, graph: Graph) -> None:
        print("Compare Solution:")
        print("source_target: c(calculated_flow | solution_flow) = calculated_cost | solution_cost")
        for link in solution.values:
            link_key = f"{int(link[0])}_{int(link[1])}"
            graph_link = graph.links[link_key]
            if abs(graph_link.flow - link[2]) > 1:
                print(
                    f"{link_key}: {abs(graph_link.flow - link[2])} c({graph_link.flow} | {link[2]})"
                )

    @staticmethod
    def TestSolution(solution: Any, graph: Graph) -> None:
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
        print(
            f"Test passed.\nMax difference compared to known solution: {max_dif}")

    @staticmethod
    def LogNodesDifference(nodes: Dict[int, Node]) -> None:
        for node in nodes.values():
            pi_max = node.pi_max
            pi_min = node.pi_min
            diff = pi_max - pi_min
            print(f"{node.index}: {pi_max} - {pi_min} = {diff}")
