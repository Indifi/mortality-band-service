from django.conf.urls import url
from .main import MortalityBandService
from .health_check import Health

urlpatterns = [
    url('get-mortality-band', MortalityBandService.as_view(), name='mortality_band_computation'),
    url('health', Health.as_view(), name='health_check'),
]
