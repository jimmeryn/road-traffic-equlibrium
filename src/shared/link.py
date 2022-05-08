"""Link"""


import math


class Link:
    """Link class"""

    def __init__(
        self,
        init_node: int | float,
        term_node: int | float,
        capacity: float,
        _length: int,
        free_flow_time: int,
        b: float,
        power: int,
        _speed_limit: int,
        _toll: int,
        _link_type: int,
    ):
        self.src = int(init_node)
        self.dest = int(term_node)
        self.fft = free_flow_time
        self.b = b
        self.k = capacity
        self.p = power
        self.flow = 0
        self.cost = free_flow_time
        self.cost_der = free_flow_time

    def CalculateCost(self, flow: int | None = None):
        if flow is None:
            return self.CostFormula(self.flow)

        return self.CostFormula(flow)

    def CalculateCostDerivative(self, flow: int | None = None):
        if flow is None:
            return self.CostDerivativeFormula(self.flow)

        return self.CostDerivativeFormula(flow)

    def AddFlow(self, delta_flow):
        # Add flow to the link and update cost and cost derivative
        self.flow += delta_flow
        self.cost = self.CalculateCost()
        self.cost_der = self.CalculateCostDerivative()

    def ResetFlow(self):
        self.flow = 0
        self.cost = self.fft
        self.cost_der = self.fft

    def CostFormula(self, x: int):
        # Use only when calculating new link cost or checking link cost for new flow
        return self.fft * (1 + self.b * math.pow(x / self.k, self.p))

    def CostDerivativeFormula(self, x: int):
        # Use only when calculating new link cost derivative or checking link cost derivative for new flow
        return self.fft * x / self.k
