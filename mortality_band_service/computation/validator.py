import copy
from .constants import PAYLOAD_VARS, MISSING_PAYLOAD_DATA


class Validator:
    VALIDATOR_RESPONSE = {
        'success': True,
        'error': '',
        'formatted_payload': {}
    }

    def __init__(self, payload):
        self.payload = payload
        self.response = copy.copy(self.VALIDATOR_RESPONSE)
        self.formatted_payload = {}

    def validate_mortality_band_request(self):
        """
        Validate payload
        :return: If valid or not
        """
        # Check all keys if present or not
        for each_var in PAYLOAD_VARS:
            if each_var[0] not in self.payload:
                self.response = {
                    'success': False,
                    'error': MISSING_PAYLOAD_DATA.format(each_var[0])
                }
                return self.response


        self.response.update(formatted_payload=self.formatted_payload)
        return self.response
