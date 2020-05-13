import logging.config
from typing import TypedDict, Iterable, Optional

from cmreslogging.handlers import CMRESHandler


class ESHost(TypedDict):
    host: str
    port: int


def configure_logger(es_hosts: Optional[Iterable[ESHost]] = None,
                     env: str = '', app_name: str = 'MAIN',
                     log_level: str = 'INFO') -> None:
    """
    Configures logger with two handlers:
        - elsticsearch (cmreslogging.handlers.CMRESHandler
          from https://github.com/cmanaha/python-elasticsearch-logger)
        - console (simple stdout-logger)
    The ElasticSearch index is created automatically. The index
    name (lowercased) example (if **env** provided):
    *someapp-dev-log*

    :param es_hosts: iterable of dicts, ElasticSearch hosts. Default is
            [{'host': 'localhost', 'port': 9200}].
    :param env: string, environment prefix (e.g. dev, tst, prd...) for
            ElasticSearch index name. Empty by default.
    :param app_name: string, name of the logger to configure.
            'MAIN' by default
    :param log_level: string, logging level. 'INFO' by Default.
    :return: nothing

    """
    env_ = (f'-{env}' if env else '').lower()
    es_index_name = f'{app_name}{env_}-log'.lower()
    es_hosts = es_hosts or ({'host': 'localhost', 'port': 9200},)

    log_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "stream": "ext://sys.stdout",
            },
            'elasticsearch': {
                'level': log_level,
                '()': CMRESHandler,
                'hosts': es_hosts,
                'es_index_name': es_index_name,
                'es_additional_fields': {
                    'app': app_name,
                },
                'auth_type': CMRESHandler.AuthType.NO_AUTH,
                'use_ssl': False,
            },
        },
        'loggers': {
            app_name: {
                'level': log_level,
                'handlers': [
                    'elasticsearch',
                    'console',
                ],
                'propagate': False,
            },
        }
    }

    logging.config.dictConfig(log_config)
