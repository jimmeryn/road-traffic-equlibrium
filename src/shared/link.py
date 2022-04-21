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
    """Link class for testing purpouses"""

    def __init__(self, src: int, dest: int, multip: float):
        self.src = src
        self.dest = dest
        self.multip = multip
        self.flow = 0
        self.cost = 0.0
        self.cost_der = multip

    def CalculateCost(self, flow: int | None = None):
        if flow is None:
            return self.flow * self.multip

        return flow * self.multip

    def CalculateCostDerivative(self, flow: int | None = None):
        return self.multip

    def AddFlow(self, delta_flow):
        self.flow += delta_flow
        self.cost = self.CalculateCost()
        self.cost_der = self.CalculateCostDerivative()
