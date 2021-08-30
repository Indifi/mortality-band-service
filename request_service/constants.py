from rest_framework import status

MORTALITY_BAND_SERVICE_RESPONSE_OBJ = {
    'success': False,
    'status_code': status.HTTP_200_OK,
    'data': {},
    'error': ''
}

MORTALITY_BAND_SERVICE_ERROR_OBJ = {
    'error_identifier': 'MORTALITY_BAND_SERVICE_ERROR',
    'error_message': '',
    'error_trace': ''
}

INVALID_PAYLOAD_ERROR = 'Invalid/Insufficient payload to process our mortality band sevice'
UNKNOWN_ERROR = 'Unidentified error due to {}. Kindly contact tech support'


class InvalidPayloadError(Exception):
    """Raised when payload sent is invalid"""
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'InvalidPayloadError: {0} '.format(self.message)
        else:
            return INVALID_PAYLOAD_ERROR
