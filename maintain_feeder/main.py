from maintain_feeder import config
from feeder_utilities.dependencies.rabbitmq import Worker
from maintain_feeder.extensions import setup_loggers, logger
from maintain_feeder.process_message import MessageProcessor
from maintain_feeder.utilities import integrity_check
from kombu import Connection, Exchange, Queue, binding
from feeder_utilities.rpc_message_processor import RpcMessageProcessor
import requests


def run():
    setup_loggers()

    exchange = Exchange(config.EXCHANGE_NAME, type=config.EXCHANGE_TYPE)
    queues = [Queue(config.QUEUE_NAME, exchange,
                    bindings=[binding(exchange, routing_key=key) for key in config.ROUTING_KEYS])]

    rpc_exchange = Exchange(config.RPC_EXCHANGE_NAME, type='direct')
    rpc_queues = [Queue(config.RPC_QUEUE_NAME, rpc_exchange,
                        bindings=[binding(rpc_exchange, routing_key=config.RPC_ROUTING_KEY)])]

    message_processor = MessageProcessor(logger)
    rpc_message_processor = RpcMessageProcessor(logger, config.APP_NAME, integrity_check, config.RABBIT_URL,
                                                config.QUEUE_NAME, config.RPC_QUEUE_NAME,
                                                config.ERROR_QUEUE_NAME, config.REGISTER_URL,
                                                config.ROUTING_KEYS[0])

    try:
        result = rpc_message_processor.startup_integrity_check(requests)
        if result:
            logger.error("Entries were requested from the Register '{}'".format(result))
        else:
            logger.info("No integrity issues detected")
    except Exception as e:
        logger.exception('Unhandled Exception while attempting integrity fixing: %s', repr(e))

    with Connection(config.RABBIT_URL, heartbeat=4) as conn:
        try:
            worker = Worker(
                logger,
                conn,
                queues,
                rpc_queues,
                message_processor.process_message,
                rpc_message_processor.process_rpc_message)
            logger.info("Running worker...")
            worker.run()
        except KeyboardInterrupt:
            logger.debug('KeyboardInterrupt')
        except Exception as e:
            logger.exception('Unhandled Exception: %s', repr(e))
