from .computation.base import ComputationBase


class CalculateMortalityBandService:
    def __init__(self, data):
        self.data = data

    def execute(self):
        """
        Execute our new line service
        """
        # Compute our new line
        result = ComputationBase(self.data).compute()
        return result
