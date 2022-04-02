"""Link"""


# from typing import TypedDict

# class Link(TypedDict):
#     """Link class"""
#     init_node: int
#     term_node: int
#     capacity: float
#     length: int
#     free_flow_time: int
#     b: float
#     power: int
#     speed_limit: int
#     toll: int
#     link_type: int


class Link:
    # Link class for testing purpouses
    def __init__(self, src, dest, multip):
        self.src = src
        self.dest = dest
        self.multip = multip

    def cost(self, flow):
        return flow * self.multip
