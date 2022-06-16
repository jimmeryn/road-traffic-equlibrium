""" Pas class """
import math
from operator import attrgetter
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
        self.flowMovesNumber: int = 0
        self.relevantOrigins: List[TapasBushGraph] = []
        self.segments: Dict[Literal[0, 1], List[Link]] = {0: [], 1: []}

    def IsUnused(self):
        ret_val = self.flowMovesNumber
        self.flowMovesNumber = 0
        return ret_val < 0

    def PushFrontToCheap(self, link: Link):
        self.segments[self.cheapSegment].insert(0, link)
        self.cheapCost += link.cost

    def PushBackToExp(self, link: Link):
        self.segments[1 - self.cheapSegment].append(link)
        self.expCost += link.cost

    def GetLastCheapLink(self):
        if self.cheapSegment not in self.segments:
            return None
        return self.segments[self.cheapSegment][-1]

    def GetLastExpLink(self):
        if 1 - self.cheapSegment not in self.segments:
            return None
        return self.segments[1 - self.cheapSegment][-1]

    def AddOrigin(self, graph: TapasBushGraph):
        self.relevantOrigins.append(graph)

    def CheckIfEffective(self, cost: float, v: float, index: int, graph: TapasBushGraph):
        return self.CheckIfCostEffective(cost) and self.CheckIfFlowEffective(v, index, graph)

    def CheckIfFlowEffective(self, v: float, index: int, graph: TapasBushGraph):
        min_flow = math.inf
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
        self.RecalculateCosts()
        if self.GetCostDiff() < DIR_TOLERANCE:
            return
        moved_flow = False
        shift_flow = self.CalculateFlowShift()
        exp_index = 1 - self.cheapSegment
        for graph in self.relevantOrigins:
            if self.totalShift <= 0.0:
                continue

            delta_x = graph.min_shift / self.totalShift * shift_flow
            if delta_x <= ZERO_FLOW:
                continue

            moved_flow = True
            for link in self.segments[self.cheapSegment]:
                graph.AddOriginFlowAndCreateLink(link, delta_x)

            for link in self.segments[exp_index]:
                if graph.bush_flow[link.index] - delta_x < ZERO_FLOW:
                    graph.bush_flow[link.index] = 0.0
                else:
                    graph.AddOriginFlowAndCreateLink(link, -delta_x)

        if not moved_flow:
            return

        for link in self.segments[self.cheapSegment]:
            link.AddFlow(shift_flow)
        for link in self.segments[exp_index]:
            link.AddFlow(-shift_flow)
        self.flowMovesNumber += 1

    def CalculateFlowShift(self) -> float:
        self.totalShift = 0.0
        exp_segment = self.segments[1 - self.cheapSegment]
        for graph in self.relevantOrigins:
            min_flow_shift = math.inf
            for link in exp_segment:
                bush_flow = graph.bush_flow[link.index]
                if bush_flow < min_flow_shift:
                    min_flow_shift = bush_flow

            graph.min_shift = min_flow_shift
            self.totalShift += min_flow_shift

        flow_shift = self.GetFlowShift()
        if flow_shift > self.totalShift:
            flow_shift = self.totalShift

        return flow_shift

    def GetFlowShift(self) -> float:
        return (self.expCost - self.cheapCost) / self.CalculateDisjointPathDerivative()

    def GetCostDiff(self) -> float:
        return self.expCost - self.cheapCost

    def RecalculateCosts(self) -> float:
        cost0 = math.fsum(map(attrgetter('cost'), self.segments[0]))
        cost1 = math.fsum(map(attrgetter('cost'), self.segments[1]))

        if cost0 < cost1:
            self.cheapSegment = 0
            self.cheapCost = cost0
            self.expCost = cost1
        else:
            self.cheapSegment = 1
            self.cheapCost = cost1
            self.expCost = cost0

    def CalculateDisjointPathDerivative(self) -> float:
        return (
            math.fsum(map(attrgetter('cost_der'), self.segments[0])) +
            math.fsum(map(attrgetter('cost_der'), self.segments[1]))
        )
