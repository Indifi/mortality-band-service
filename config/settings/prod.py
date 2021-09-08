from .base import *

DEBUG = False

prod_config = config['production']
REDIS_HOST = prod_config["REDIS_HOST"]
LOGGING_HANDLERS = ['console', 'logstash']

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(levelname)s:%(name)s: %(message)s '
                      '(%(asctime)s; %(filename)s:%(lineno)d)',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
        'logstash': {
          'level': 'WARNING',
          'class': 'logstash.TCPLogstashHandler',
          'host': 'log-pipeline-service',
          'port': 5044,
          'version': 1,
          'message_type': 'logstash',
          'fqdn': False,  # Fully qualified domain name. Default value: false.
          'tags': ['logs'],  # list of tags. Default: None.
        }
    },
    'loggers': {
        '': {
            'handlers': LOGGING_HANDLERS,
            'propagate': True,
            'level': 'INFO',
        }
    }
})

CATCH_UNKNOWN_EXCEPTION = True
