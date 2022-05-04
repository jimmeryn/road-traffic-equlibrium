""" Logger """
from typing import Dict

from src.shared.link import Link
from src.shared.node import Node


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
    def LogGraph(nodes: Dict[int, Node]) -> None:
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
