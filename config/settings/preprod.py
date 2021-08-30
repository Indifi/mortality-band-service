from .base import *

preprod_config = config['preprod']
REDIS_HOST = preprod_config["REDIS_HOST"]

CATCH_UNKNOWN_EXCEPTION = False
