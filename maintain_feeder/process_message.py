from maintain_feeder.extensions import session
from maintain_feeder.models import LocalLandChargeHistory
from maintain_feeder.exceptions import ApplicationError
from maintain_feeder import config
from maintain_feeder.utilities import local_land_charge
from feeder_utilities.dependencies.register import Register
from feeder_utilities.dependencies import rabbitmq
from sqlalchemy import func
from datetime import datetime


class MessageProcessor(object):
    def __init__(self, logger):
        self.logger = logger

    def process_message(self, body, message, requests):
        self.logger.info("Processing message")
        null_entry = False
        try:
            # Check for null entry
            if 'item' not in body and 'entry-number' in body and body['entry-number']:
                entry_number = body['entry-number']
                null_entry = True
                self.logger.warn("Entry {} is null entry".format(entry_number))
            else:
                # Basic message checks
                if 'item' in body and 'item-hash' in body and 'item-signature' in body:
                    if 'local-land-charge' not in body['item']:
                        raise ApplicationError("Invalid register in message body.")
                else:
                    raise ApplicationError("Payload missing one of item, item-hash or item-signature")

            # Make sure we've not already got the entry
            entry_number = body['entry-number']
            if session.query(LocalLandChargeHistory).filter_by(entry_number=entry_number).first():
                self.logger.warn("Entry number {} already in database, ignoring message".format(entry_number))
            else:

                # Entry gap detection
                max_entry = session.query(
                    func.max(LocalLandChargeHistory.entry_number)).scalar() or 0
                exp_entry = max_entry + 1
                if entry_number > exp_entry:
                    missing_entries = list(range(exp_entry, entry_number))
                    self.logger.error(
                        "Entry {} is greater than expected entry {}, requesting missing entries {}".format(
                            entry_number, exp_entry, missing_entries))
                    Register(config.REGISTER_URL, config.ROUTING_KEYS[0], requests).republish_entries(missing_entries)

                if not null_entry:
                    # Process land charge
                    local_land_charge.process_land_charge(self.logger, body)
                else:
                    null_entry = LocalLandChargeHistory(-1, {}, False, entry_number, datetime.fromtimestamp(0))
                    session.add(null_entry)
                    session.commit()
                    self.logger.info("Null entry stored. Entry number {}".format(entry_number))

            message.ack()

        except Exception as err:
            self.logger.exception("Error occurred during message handling", err)
            session.rollback()
            attempt_count = message.headers.get('x-processing-attempt', 0)
            if attempt_count > config.MAX_MSG_RETRY:
                self.logger.error("Message exceeded maximum retries, sending to error queue")
                rabbitmq.publish_message(self.logger, body, config.RABBIT_URL, '', config.ERROR_QUEUE_NAME,
                                         queue_name=config.ERROR_QUEUE_NAME,
                                         headers={"x-error-message": repr(err)})
            else:
                self.logger.warn("Queuing message again for attempt at re-processing")
                rabbitmq.publish_message(self.logger, body, config.RABBIT_URL, '', config.QUEUE_NAME,
                                         queue_name=config.QUEUE_NAME,
                                         headers={"x-processing-attempt": attempt_count + 1})
            message.reject()
