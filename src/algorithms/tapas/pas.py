""" Pas class """
import math
from typing import Dict, List, Literal

from src.algorithms.tapas.tapas_bush_graph import TapasBushGraph
from src.shared.consts import DIR_TOLERANCE, ZERO_FLOW
from src.shared.link import Link


class Pas():
    """ Paired Alternative Segment """

    def __init__(self) -> None:
        self.cheapCost = 0.0
        self.expCost = 0.0
        self.totalShift = 0.0
        self.cheapSegment: Literal[0, 1] = 0
        self.flowMovesNumber = 0
        self.relevantOrigins: Dict[str, TapasBushGraph] = {}
        self.segments: Dict[str, List[Link]] = {0: [], 1: []}

    def IsUnused(self):
        ret_val = self.flowMovesNumber
        self.flowMovesNumber = 0
        return ret_val < 0

    def PushFrontToCheap(self, link: Link):
        self.segments[self.cheapSegment].insert(0, link)
        self.cheapCost += link.cost

    def PushBackToExp(self, link: Link):
        self.segments[1 - self.cheapSegment].append(link)

    def GetLastCheapLink(self):
        if 1 - self.cheapSegment not in self.segments:
            return None
        return self.segments[1 - self.cheapSegment][-1]

    def GetLastExpLink(self):
        if self.cheapSegment not in self.segments:
            return None
        return self.segments[self.cheapSegment][-1]

    def AddOrigin(self, graph: TapasBushGraph):
        self.relevantOrigins[graph.originIndex] = graph

    def CheckIfEffective(self, cost: float, v: float, index: int, graph: TapasBushGraph):
        return self.CheckIfCostEffective(cost) and self.CheckIfFlowEffective(v, index, graph)

    def CheckIfFlowEffective(self, v: float, index: int, graph: TapasBushGraph):
        min_flow = math.inf
        flow = 0.0
        exp_index = 1 - self.cheapSegment
        for link in self.segments[exp_index]:
            flow = graph.bush_flow[link.index]
            if flow < min_flow:
                min_flow = flow
        return min_flow >= v * graph.bush_flow[index]

    def CheckIfCostEffective(self, cost: float):
        return self.expCost - self.cheapCost >= cost

    def MoveFlow(self):
        self.flowMovesNumber -= 1
        tmp = True
        if self.RecalculateCosts() >= DIR_TOLERANCE:
            shift_flow = self.CalculateFlowShift()
            exp_index = 1 - self.cheapSegment
            for dag in self.relevantOrigins.values():
                if self.totalShift > 0.0:
                    delta_x = dag.min_shift / self.totalShift * shift_flow
                    if delta_x > ZERO_FLOW:
                        tmp = False
                        for link in self.segments[self.cheapSegment]:
                            dag.AddOriginFlowAndCreateLink(link, delta_x)

                        for link in self.segments[exp_index]:
                            if dag.bush_flow[link.index] - delta_x < ZERO_FLOW:
                                dag.bush_flow[link.index] = 0.0
                            else:
                                dag.AddOriginFlowAndCreateLink(link, -delta_x)

            if tmp is False:
                for link in self.segments[self.cheapSegment]:
                    link.AddFlow(shift_flow)
                for link in self.segments[exp_index]:
                    if link.flow - shift_flow < ZERO_FLOW:
                        link.ResetFlow()
                    else:
                        link.AddFlow(-shift_flow)
                self.flowMovesNumber += 1
                return True
        return False

    def CalculateFlowShift(self):
        self.totalShift = 0.0
        for dag in self.relevantOrigins.values():
            min_flow_shift = math.inf
            o_flow = 0.0
            for link in self.segments[1 - self.cheapSegment]:
                o_flow = dag.bush_flow[link.index]
                if o_flow < min_flow_shift:
                    min_flow_shift = o_flow
            dag.min_shift = min_flow_shift
            self.totalShift += min_flow_shift

        d_flow = self.GetFlowShift()
        if d_flow > self.totalShift:
            d_flow = self.totalShift
        return d_flow

    def GetFlowShift(self):
        path_der = self.CalculateDisjointPathDerivative(
            self.cheapSegment, 1 - self.cheapSegment)
        return (self.expCost - self.cheapCost) / path_der

    def CalcSegCost(self, index: int):
        if index not in self.segments:
            return 0.0
        return sum(link.cost for link in self.segments[index])

    def GetCostDiff(self):
        return self.expCost - self.cheapCost

    def RecalculateCosts(self):
        cost0 = self.CalcSegCost(0)
        cost1 = self.CalcSegCost(1)
        condition = cost0 < cost1

        self.cheapSegment = 0 if condition else 1
        self.cheapCost = cost0 if condition else cost1
        self.expCost = cost1 if condition else cost0

        return self.expCost - self.cheapCost

    def CalculateDisjointPathDerivative(self, index1: str, index2: str):
        der_cost = 0.0
        if index1 in self.segments:
            der_cost += sum(link.cost_der for link in self.segments[index1])

        if index2 in self.segments:
            der_cost += sum(link.cost_der for link in self.segments[index2])

        return der_cost
