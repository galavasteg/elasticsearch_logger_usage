import json
import logging
import os

from es_logger import configure_logger


# Elasticsearch-logger settings
APP_NAME = 'PythonApp'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
ENV = os.getenv('ENVIRONMENT', 'DEV')
ES_HOSTS = json.loads(os.getenv('ELASTIC_HOSTS'))

configure_logger(ES_HOSTS, ENV, APP_NAME)

log = logging.getLogger(APP_NAME)


log.info('START')

try:
    some_result = sum(range(10))
    log.info(f'Немного кириллицы and something'
             f' use\u0336f\u0336u\u0336l\u0336lless: {some_result}')

    raise RuntimeError('Hey! What happened?!')

except RuntimeError as e:
    log.exception('Your amazing exception record:'
                  ' "log.exception(\'foo\')"')
    log.error('"log.error(\'bar\', exc_info=True)" is'
              ' an analog of "log.exception(\'bar\')"',
              exc_info=True)
    log.error('"log.error(\'baz\', exc_info=False)" not provides any'
              ' information about the exception. It\'s simple, isn\'t it! =)',
              exc_info=False)

log.info('FINISH')
