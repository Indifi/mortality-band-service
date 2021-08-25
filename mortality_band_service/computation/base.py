from .core.pre_fetch_vars import PreFetchData


class ComputationBase:
    def __init__(self, data):
        self.data = data
        self.result = {}
        self.term_loan_result = {}
        self.loc_result = {}

    def compute(self):
        """
        Compute our new line
        :return: Line service result
        """
        # Pre fetch required data
        self.mortality_band = PreFetchData(self.data).fetch()
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
