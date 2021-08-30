import traceback
import logging
import copy

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from mortality_band_service.main import CalculateMortalityBandService
from mortality_band_service.computation.validator import Validator

from .constants import MORTALITY_BAND_SERVICE_RESPONSE_OBJ, MORTALITY_BAND_SERVICE_ERROR_OBJ, UNKNOWN_ERROR, \
    InvalidPayloadError

logger = logging.getLogger(__name__)


class MortalityBandService(APIView):
    """
    View to handle all requests for our mortality band service
    """
    def post(self, request):
        """
        post line from our mortality band service
        """
        # Get response and error objects
        response_obj = copy.copy(MORTALITY_BAND_SERVICE_RESPONSE_OBJ)
        error_obj = copy.copy(MORTALITY_BAND_SERVICE_ERROR_OBJ)
        # Compute line
        try:
            payload = request.POST
            # Validate data on post call
            validate_obj = Validator(request.data)
            validator_response = validate_obj.validate_mortality_band_request()
            if not validator_response['success']:
                raise InvalidPayloadError(validator_response['error'])
            payload = validator_response['formatted_payload']
            executor = CalculateMortalityBandService(request.data)
            data = executor.execute()
            response_obj.update(success=True, data=data)
        except InvalidPayloadError as e:
            error_msg = e.message
            error_trace = traceback.format_exc()
            error_obj.update(error_message=error_msg)
            error_obj.update(error_trace=error_trace)
            logger.error(error_obj)
            response_obj.update(status_code=status.HTTP_400_BAD_REQUEST)
            response_obj.update(error=error_msg)
        except Exception as e:
            if settings.CATCH_UNKNOWN_EXCEPTION:
                error_msg = UNKNOWN_ERROR
                error_trace = traceback.format_exc()
                error_obj.update(error_message=error_msg)
                error_obj.update(error_trace=error_trace)
                logger.error(error_obj)
                response_obj.update(error=UNKNOWN_ERROR.format(e))
            else:
                # Let it raise on local and staging env
                raise e

        return Response(response_obj, status=response_obj['status_code'])
