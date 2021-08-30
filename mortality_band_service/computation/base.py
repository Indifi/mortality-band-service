from .core.mortality_band import CalculateMortalityBand


class ComputationBase:
    def __init__(self, data):
        self.data = data
        self.result = {}
        self.mortality_band = None

    def compute(self):
        """
        Compute our new line
        :return: Mortality Band service result
        """
        # Calculate Mortality Band
        self.mortality_band = CalculateMortalityBand(self.data).calculate()
        # Get final result
        self.get_final_result()

        return self.result

    def get_final_result(self):
        """
        Get final result
        """
        self.result = {
            'mortality_band': self.mortality_band
        }
