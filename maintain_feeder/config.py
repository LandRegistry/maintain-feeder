import os
# RULES OF CONFIG:
# 1. No region specific code. Regions are defined by setting the OS environment variables appropriately to build up the
# desired behaviour.
# 2. No use of defaults when getting OS environment variables. They must all be set to the required values prior to the
# app starting.
# 3. This is the only file in the app where os.environ should be used.

# For logging
LOG_LEVEL = os.environ['LOG_LEVEL']
KOMBU_LOG_LEVEL = os.environ['KOMBU_LOG_LEVEL']

# This APP_NAME variable is to allow changing the app name when the app is running in a cluster. So that
# each app in the cluster will have a unique name.
APP_NAME = os.environ['APP_NAME']

# Rabbitmq
EXCHANGE_NAME = os.environ['EXCHANGE_NAME']
EXCHANGE_TYPE = os.environ['EXCHANGE_TYPE']
QUEUE_NAME = os.environ['QUEUE_NAME']
RABBIT_URL = os.environ['RABBIT_URL']
ROUTING_KEYS = os.environ['ROUTING_KEYS'].split(';')
ERROR_QUEUE_NAME = os.environ['ERROR_QUEUE_NAME']
RPC_QUEUE_NAME = os.environ['RPC_QUEUE_NAME']
RPC_EXCHANGE_NAME = os.environ['RPC_EXCHANGE_NAME']
RPC_ROUTING_KEY = os.environ['RPC_ROUTING_KEY']
MAX_MSG_RETRY = int(os.environ['MAX_MSG_RETRY'])

# --- Database variables start
# These must all be set in the OS environment.
# The password must be the correct one for either the app user or alembic user,
# depending on which will be used (which is controlled by the
# SQL_USE_ALEMBIC_USER variable)
SQL_HOST = os.environ['SQL_HOST']
SQL_DATABASE = os.environ['SQL_DATABASE']
SQL_PASSWORD = os.environ['SQL_PASSWORD']
SQL_USERNAME = os.environ['SQL_USERNAME']
SQLALCHEMY_DATABASE_URI = 'postgres://{0}:{1}@{2}/{3}'.format(
    SQL_USERNAME, SQL_PASSWORD, SQL_HOST, SQL_DATABASE)
# Explicitly set this in order to remove warning on run
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_RECYCLE = int(os.environ['SQLALCHEMY_POOL_RECYCLE'])
# --- Database variables end

REGISTER_URL = os.environ['REGISTER_URL']

SCHEMA_VERSION = "7.0"

LOGCONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            '()': 'maintain_feeder.extensions.JsonFormatter'
        },
        'audit': {
            '()': 'maintain_feeder.extensions.JsonAuditFormatter'
        }
    },
    'filters': {
        'contextual': {
            '()': 'maintain_feeder.extensions.ContextualFilter'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'filters': ['contextual'],
            'stream': 'ext://sys.stdout'
        },
        'audit_console': {
            'class': 'logging.StreamHandler',
            'formatter': 'audit',
            'filters': ['contextual'],
            'stream': 'ext://sys.stdout'
        }
    },
    'loggers': {
        'maintain_feeder': {
            'handlers': ['console'],
            'level': LOG_LEVEL
        },
        'audit': {
            'handlers': ['audit_console'],
            'level': 'INFO'
        }
    }
}
