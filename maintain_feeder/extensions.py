from logging.config import dictConfig
from kombu.utils.debug import setup_logging
from maintain_feeder.config import KOMBU_LOG_LEVEL, LOGCONFIG, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_POOL_RECYCLE
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
import json
import traceback
import collections

logger = logging.getLogger("maintain_feeder")
audit_logger = logging.getLogger("audit")
Session = sessionmaker()


def setup_loggers():
    # Add kombu loggers
    setup_logging(loglevel=KOMBU_LOG_LEVEL)

    # Set up the loggers formatters and handlers from the LOGCONFIG dict
    dictConfig(LOGCONFIG)


class ContextualFilter(logging.Filter):
    def filter(self, log_record):
        """Provide some extra variables to be placed into the log message"""
        log_record.msg = "Caller: {}.{}[{}], {}".format(
            log_record.module, log_record.funcName, log_record.lineno, log_record.msg)
        return True


class JsonFormatter(logging.Formatter):
    def format(self, record):
        exc = traceback.format_exception(*record.exc_info) if record.exc_info else None
        trace_id = record.trace_id if hasattr(record, 'trace_id') else "N/A"

        # Timestamp must be first (webops request)
        log_entry = collections.OrderedDict(
            [('timestamp', self.formatTime(record)),
             ('level', record.levelname),
             ('traceid', trace_id),
             ('message', super().format(record)),
             ('exception', exc)])
        return json.dumps(log_entry)


class JsonAuditFormatter(logging.Formatter):
    def format(self, record):
        trace_id = record.trace_id if hasattr(record, 'trace_id') else "N/A"

        # Timestamp must be first (webops request)
        log_entry = collections.OrderedDict(
            [('timestamp', self.formatTime(record)),
             ('level', 'AUDIT'),
             ('traceid', trace_id),
             ('message', super().format(record))])
        return json.dumps(log_entry)


def setup_session():
    engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_recycle=SQLALCHEMY_POOL_RECYCLE)
    Session.configure(bind=engine)
    sess = Session()
    return sess


session = setup_session()
