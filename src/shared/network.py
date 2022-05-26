""" Graph Class """
from typing import Dict

from src.shared.graph import Graph
from src.shared.link import Link
from src.shared.node import Node
from src.utils.link_utils import create_link_key


class Network(Graph):
    """
    Class used to store all graph info
    """

    def __init__(self, nodes, links):
        super().__init__()
        self.links = self.CreateLinksDict(links)
        self.nodes = self.CreateNodesDict(nodes)
        self.n: int = int(nodes[-1][0])

    def CreateLinksDict(self, links) -> Dict[str, Link]:
        return dict(
            map(lambda link: (
                create_link_key(link[0], link[1]),
                Link(*link)
            ), links)
        )

    def CreateNodesDict(self, nodes) -> Dict[int, Node]:
        return dict(
            map(lambda node: (
                int(node[0]),
                Node(node[0])
            ), nodes)
        )
