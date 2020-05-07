import json
import logging.config
import os

from cmreslogging.handlers import CMRESHandler
import dotenv


dotenv.load_dotenv()


APP_NAME = 'PythonApp'

# Elasticsearch-logger settings
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
ENV = os.getenv('ENVIRONMENT', 'DEV')
ES_INDEX_NAME = f'{APP_NAME}-{ENV}-log'.lower()
ES_HOSTS = json.loads(os.getenv('ELASTIC_HOSTS'))  # see .env for example

log_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "stream": "ext://sys.stdout",
        },
        'elasticsearch': {
            'level': 'INFO',
            '()': CMRESHandler,
            'hosts': ES_HOSTS,
            'es_index_name': ES_INDEX_NAME,
            'es_additional_fields': {
                'app': APP_NAME,
            },
            'auth_type': CMRESHandler.AuthType.NO_AUTH,
            'use_ssl': False,
        },
    },
    'loggers': {
        'main_log': {
            'level': LOG_LEVEL,
            'handlers': [
                'elasticsearch',
                'console',
            ],
            'propagate': False,
        },
    }
}

logging.config.dictConfig(log_config)

