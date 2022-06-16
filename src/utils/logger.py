""" Logger """
import logging
import math
from io import TextIOWrapper
from typing import Any, Dict, Literal

from src.shared.graph import Graph
from src.shared.link import Link
from src.shared.node import Node
from src.utils.link_utils import create_link_key


class Logger:
    """ Class used to print graph data """

    @staticmethod
    def LogFlow(links: Dict[int, Link]) -> None:
        logging.basicConfig(level=logging.DEBUG)
        for key, link in links.items():
            logging.debug("%s: %s", key, link.flow)

    @staticmethod
    def LogCosts(links: Dict[int, Link]) -> None:
        logging.basicConfig(level=logging.DEBUG)
        for key, link in links.items():
            logging.debug("%s: %s", key, link.cost)

    @staticmethod
    def LogGraphLinks(links: Dict[int, Link]) -> None:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Links:")
        logging.debug("source_target: c(flow) = cost")
        for key, link in links.items():
            logging.debug("%s: c(%s) = %s", key, link.flow, link.cost)
        logging.debug("\n")

    @staticmethod
    def LogGraphNodes(nodes: Dict[int, Node]) -> None:
        logging.basicConfig(level=logging.DEBUG)
        log_string = "{node_index}: max: {alpha_max} ({pi_max}), min: {alpha_min} ({pi_min})"
        default_message_params = {
            "node_index": -1,
            "pi_max": -1,
            "pi_min": -1,
            "alpha_max": None,
            "alpha_min": None,
        }
        logging.debug(
            "node_index: max: alpha_max (pi_max), min: alpha_min (pi_min)")
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
            logging.debug(
                log_string,
                message_params["node_index"],
                message_params["alpha_max"],
                message_params["pi_max"],
                message_params["alpha_min"],
                message_params["pi_min"]
            )

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
            logging.debug("%s.NODE %s path: %s", node.index, path_prop, path)
        logging.debug("\n")

    @staticmethod
    def LogSolution(solution: Any) -> None:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Solution:")
        for link in solution.values:
            logging.debug(
                "%s_%s: c(%s = %s)",
                int(link[0]),
                int(link[1]),
                link[2],
                link[3]
            )

    @staticmethod
    def CompareSolution(solution: Any, graph: Graph) -> None:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Compare Solution:")
        logging.debug(
            "source_target: c(calculated_flow | solution_flow) = calculated_cost | solution_cost")
        for link in solution.values:
            link_key = f"{int(link[0])}_{int(link[1])}"
            graph_link = graph.links[link_key]
            if abs(graph_link.flow - link[2]) > 1:
                logging.debug(
                    "%s: %s c(%s | %s)",
                    link_key,
                    abs(graph_link.flow - link[2]),
                    graph_link.flow,
                    link[2]
                )

    @staticmethod
    def CompareSolutionToFile(solution: Any, graph: Graph, file: TextIOWrapper) -> None:
        for link in solution.values:
            link_key = f"{int(link[0])}_{int(link[1])}"
            graph_link = graph.links[link_key]
            file.write(
                f"{link_key},{math.fabs(graph_link.flow - link[2])}\n")

    @staticmethod
    def TestSolution(solution: Any, graph: Graph) -> None:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Testing solution...")
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
            logging.debug("Test failed. \n%s", assertion_error)
            return
        logging.debug(
            "Test passed.\nMax difference compared to known solution: %s",
            max_dif
        )

    @staticmethod
    def LogNodesDifference(nodes: Dict[int, Node]) -> None:
        logging.basicConfig(level=logging.DEBUG)
        for node in nodes.values():
            pi_max = node.pi_max
            pi_min = node.pi_min
            diff = pi_max - pi_min
            logging.debug("%s: %s - %s = %s", node.index, pi_max, pi_min, diff)
