""" Base Algorithm """


class Algorithm():
    """
    Base Algorithm abstract class
    All origin based alogrithms should extend this class
    """

    def Iteration(self) -> None:
        raise NotImplementedError

    def GetMaxGap(self) -> None:
        raise NotImplementedError
