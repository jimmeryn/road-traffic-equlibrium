"""Link"""
import math

from src.shared.consts import ZERO_FLOW
from src.utils.link_utils import create_link_key


class Link:
    """Link class"""

    def __init__(
        self,
        init_node: int | float,
        term_node: int | float,
        capacity: float,
        _length: float,
        free_flow_time: float,
        b: float,
        power: float,
        _speed_limit: float,
        _toll: float,
        _link_type: float,
    ):
        self.src = int(init_node)
        self.dest = int(term_node)
        self.index = create_link_key(self.src, self.dest)
        self.fft = free_flow_time
        self.b = b
        self.k = capacity
        self.p = power
        self.flow = 0.0
        self.cost = free_flow_time
        self.cost_der = free_flow_time

    def AddFlow(self, delta_flow: float):
        # Add flow to the link and update cost and cost derivative
        new_flow = self.flow + delta_flow
        if new_flow <= ZERO_FLOW:
            self.flow = 0.0
            self.cost = self.fft
            self.cost_der = 0.0
            return
        self.flow = new_flow
        self.cost = self.CostFormula(new_flow)
        self.cost_der = self.CostDerivativeFormula(new_flow)

    def CostFormula(self, x: float) -> float:
        # Use only when calculating new link cost or checking link cost for new flow
        return self.fft * (1 + self.b * math.pow(x / self.k, self.p))

    def CostDerivativeFormula(self, x: float) -> float:
        # Use only when calculating new link cost derivative or checking link cost derivative for new flow
        return self.fft * self.b * self.p * math.pow(x / self.k, self.p - 1)
