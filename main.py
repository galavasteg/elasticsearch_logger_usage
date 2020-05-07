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


log = logging.getLogger('main_log')


log.info('START')

try:
    some_result = sum(range(10))
    log.info(f'1. Немного кириллицы and something'
             f' use\u0336f\u0336u\u0336l\u0336lless: {some_result}')

    raise RuntimeError('Hey! What happened?!')

except RuntimeError as e:
    log.exception('3. Your amazing exception record:'
                  ' "log.exception(\'foo\')"')
    log.error('4. "log.error(\'bar\', exc_info=True)" is'
              ' an analog of "log.exception(\'bar\')"',
              exc_info=True)
    log.error('5. "log.error(\'baz\', exc_info=False)" not provides any'
              ' information about the exception. It\'s simple, isn\'t it! =)',
              exc_info=False)

log.info('FINISH')
