import copy
from .constants import PAYLOAD_VARS, MISSING_PAYLOAD_DATA, BOOL, FLOAT, LIST, STRING, INT, \
    BOOL_TRUE_STRINGS


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

        for each_var in PAYLOAD_VARS:
            try:
                if each_var[1] == BOOL:
                    self.formatted_payload[each_var[0]] = \
                        self.payload.get(each_var[0], '').lower() in BOOL_TRUE_STRINGS
                elif each_var[1] == FLOAT:
                    self.formatted_payload[each_var[0]] = float(
                        self.payload.get(each_var[0], 0.0))
                elif each_var[1] == LIST:
                    self.formatted_payload[each_var[0]] = self.payload.get(
                        each_var[0], '')
                elif each_var[1] == STRING:
                    self.formatted_payload[each_var[0]] = self.payload.get(
                        each_var[0], '')
                elif each_var[1] == INT:
                    self.formatted_payload[each_var[0]] = int(
                        self.payload.get(each_var[0], 0))
            except ValueError:
                self.response = {
                    'success': False,
                    'error': INVALID_PAYLOAD_DATA.format(each_var[0])
                }
                return self.response


        self.response.update(formatted_payload=self.formatted_payload)
        return self.response
