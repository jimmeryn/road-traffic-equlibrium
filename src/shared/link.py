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
    def __init__(self, src: int, dest: int, multip: float):
        self.src = src
        self.dest = dest
        self.multip = multip

    def cost(self, flow: int):
        return flow * self.multip
