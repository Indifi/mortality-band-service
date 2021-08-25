from .base import *

stage_config = config['staging']
REDIS_HOST = stage_config["REDIS_HOST"]


CATCH_UNKNOWN_EXCEPTION = False
