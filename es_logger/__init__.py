"""
Module provides function that configure logger
with two handlers:
    - elsticsearch (cmreslogging.handlers.CMRESHandler
      from https://github.com/cmanaha/python-elasticsearch-logger)
    - console (simple stdout-logger)

"""

from ._config import configure_logger

__version__ = "0.0.1"
