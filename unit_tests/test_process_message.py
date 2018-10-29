from maintain_feeder.process_message import MessageProcessor
from maintain_feeder import config
import unittest
from unittest.mock import MagicMock, patch, ANY
from unit_tests.data import \
    test_process_message_data_no_item_hash, test_process_message_data_no_item_signature, \
    test_process_message_no_land_charge, test_process_message_data_valid


class TestMessageProcessor(unittest.TestCase):

    @patch('maintain_feeder.process_message.local_land_charge')
    @patch('maintain_feeder.process_message.session')
    @patch('maintain_feeder.process_message.rabbitmq')
    def test_process_message_no_hash(self, mock_rabbitmq, mock_session, mock_local_land_charge):
        mock_message = MagicMock()
        mock_requests = MagicMock()
        mock_message.headers.get.return_value = 0
        MessageProcessor(MagicMock()).process_message(
            test_process_message_data_no_item_hash.process_message_no_item_hash, mock_message, mock_requests)
        mock_local_land_charge.process_land_charge.assert_not_called()
        mock_session.commit.assert_not_called()
        mock_message.reject.assert_called()
        mock_rabbitmq.publish_message.assert_called_with(ANY, ANY, ANY, ANY, config.QUEUE_NAME,
                                                         queue_name=config.QUEUE_NAME,
                                                         headers=ANY)

    @patch('maintain_feeder.process_message.local_land_charge')
    @patch('maintain_feeder.process_message.session')
    @patch('maintain_feeder.process_message.rabbitmq')
    def test_process_message_no_hash_max_retry(self, mock_rabbitmq, mock_session, mock_local_land_charge):
        mock_message = MagicMock()
        mock_requests = MagicMock()
        mock_message.headers.get.return_value = config.MAX_MSG_RETRY + 1
        MessageProcessor(MagicMock()).process_message(
            test_process_message_data_no_item_hash.process_message_no_item_hash, mock_message, mock_requests)
        mock_local_land_charge.process_land_charge.assert_not_called()
        mock_session.commit.assert_not_called()
        mock_message.reject.assert_called()
        mock_rabbitmq.publish_message.assert_called_with(ANY, ANY, ANY, ANY, config.ERROR_QUEUE_NAME,
                                                         queue_name=config.ERROR_QUEUE_NAME,
                                                         headers=ANY)

    @patch('maintain_feeder.process_message.local_land_charge')
    @patch('maintain_feeder.process_message.session')
    @patch('maintain_feeder.process_message.rabbitmq')
    def test_process_message_no_sig(self, mock_rabbitmq, mock_session, mock_local_land_charge):
        mock_message = MagicMock()
        mock_requests = MagicMock()
        mock_message.headers.get.return_value = 0
        MessageProcessor(MagicMock()).process_message(
            test_process_message_data_no_item_signature.process_message_no_item_signature, mock_message, mock_requests)
        mock_local_land_charge.process_land_charge.assert_not_called()
        mock_session.commit.assert_not_called()
        mock_message.reject.assert_called()
        mock_rabbitmq.publish_message.assert_called_with(ANY, ANY, ANY, ANY, config.QUEUE_NAME,
                                                         queue_name=config.QUEUE_NAME,
                                                         headers=ANY)

    @patch('maintain_feeder.process_message.local_land_charge')
    @patch('maintain_feeder.process_message.session')
    @patch('maintain_feeder.process_message.rabbitmq')
    def test_process_message_no_land_charge(self, mock_rabbitmq, mock_session, mock_local_land_charge):
        mock_message = MagicMock()
        mock_requests = MagicMock()
        mock_message.headers.get.return_value = 0
        MessageProcessor(MagicMock()).process_message(
            test_process_message_no_land_charge.process_message_valid_no_land_charge, mock_message, mock_requests)
        mock_local_land_charge.process_land_charge.assert_not_called()
        mock_session.commit.assert_not_called()
        mock_message.reject.assert_called()
        mock_rabbitmq.publish_message.assert_called_with(ANY, ANY, ANY, ANY, config.QUEUE_NAME,
                                                         queue_name=config.QUEUE_NAME,
                                                         headers=ANY)

    @patch('maintain_feeder.process_message.local_land_charge')
    @patch('maintain_feeder.process_message.session')
    @patch('maintain_feeder.process_message.rabbitmq')
    def test_process_message_valid_dupe(self, mock_rabbitmq, mock_session, mock_local_land_charge):
        mock_message = MagicMock()
        mock_requests = MagicMock()
        mock_message.headers.get.return_value = 0
        mock_session.query.return_value.filter_by.return_value.first.return_value = "NOT NONE"
        MessageProcessor(MagicMock()).process_message(
            test_process_message_data_valid.process_message_valid, mock_message, mock_requests)
        mock_local_land_charge.process_land_charge.assert_not_called()
        mock_session.commit.assert_not_called()
        mock_message.reject.assert_not_called()
        mock_message.ack.assert_called()
        mock_rabbitmq.publish_message.assert_not_called()

    @patch('maintain_feeder.process_message.local_land_charge')
    @patch('maintain_feeder.process_message.session')
    @patch('maintain_feeder.process_message.rabbitmq')
    @patch('maintain_feeder.process_message.Register')
    def test_process_message_valid_gap(self, mock_register, mock_rabbitmq, mock_session, mock_local_land_charge):
        mock_message = MagicMock()
        mock_requests = MagicMock()
        mock_message.headers.get.return_value = 0
        mock_session.query.return_value.filter_by.return_value.first.return_value = None
        mock_session.query.return_value.scalar.return_value = 1
        MessageProcessor(MagicMock()).process_message(
            test_process_message_data_valid.process_message_valid, mock_message, mock_requests)
        mock_local_land_charge.process_land_charge.assert_called()
        mock_session.commit.assert_not_called()
        mock_message.reject.assert_not_called()
        mock_message.ack.assert_called()
        mock_rabbitmq.publish_message.assert_not_called()
        mock_register.return_value.republish_entries.assert_called_with(list(range(2, 19)))

    @patch('maintain_feeder.process_message.local_land_charge')
    @patch('maintain_feeder.process_message.session')
    @patch('maintain_feeder.process_message.rabbitmq')
    def test_process_message_valid(self, mock_rabbitmq, mock_session, mock_local_land_charge):
        mock_message = MagicMock()
        mock_requests = MagicMock()
        mock_message.headers.get.return_value = 0
        mock_session.query.return_value.filter_by.return_value.first.return_value = None
        mock_session.query.return_value.scalar.return_value = 18
        MessageProcessor(MagicMock()).process_message(
            test_process_message_data_valid.process_message_valid, mock_message, mock_requests)
        mock_local_land_charge.process_land_charge.assert_called()
        mock_session.commit.assert_not_called()
        mock_message.reject.assert_not_called()
        mock_message.ack.assert_called()
        mock_rabbitmq.publish_message.assert_not_called()

    @patch('maintain_feeder.process_message.local_land_charge')
    @patch('maintain_feeder.process_message.session')
    @patch('maintain_feeder.process_message.rabbitmq')
    def test_process_message_null(self, mock_rabbitmq, mock_session, mock_local_land_charge):
        mock_message = MagicMock()
        mock_requests = MagicMock()
        mock_message.headers.get.return_value = 0
        mock_session.query.return_value.filter_by.return_value.first.return_value = None
        mock_session.query.return_value.scalar.return_value = 18
        MessageProcessor(MagicMock()).process_message(
            test_process_message_data_valid.process_message_null, mock_message, mock_requests)
        mock_local_land_charge.process_land_charge.assert_not_called()
        mock_session.commit.assert_called()
        mock_message.reject.assert_not_called()
        mock_message.ack.assert_called()
        mock_rabbitmq.publish_message.assert_not_called()
