"""Node"""


import math

from src.shared.link import Link


class Node:
    """Node class"""

    def __init__(self, index: int):
        self.index = index
        self.pi_max: float = -math.inf
        self.pi_min: float = math.inf
        self.alpha_max: Link | None = None
        self.alpha_min: Link | None = None

    def __getitem__(self, item: str):
        return getattr(self, item)
