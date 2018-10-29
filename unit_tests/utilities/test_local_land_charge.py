import unittest
from unittest.mock import MagicMock, patch
from unit_tests.data import \
    test_process_message_data_valid, \
    test_process_message_no_feature_collection
from maintain_feeder.utilities.local_land_charge import process_land_charge
from maintain_feeder.models import LocalLandChargeHistory, LocalLandCharge
from maintain_feeder.exceptions import ApplicationError

message = MagicMock()


class TestLocalLandCharge(unittest.TestCase):

    def setUp(self):
        self.merge_called_with = None

    def mock_convert(self, charge, version):
        return charge

    def mock_merge(self, obj):
        self.merge_called_with = obj
        return obj

    @patch('maintain_feeder.utilities.local_land_charge.session')
    def test_process_land_charge_prev_version(self, mock_session):
        mock_session.query.return_value.filter.return_value.first.return_value = MagicMock()
        process_land_charge(MagicMock(), test_process_message_data_valid.process_message_valid)
        mock_session.add.assert_called_with(Any(LocalLandChargeHistory))
        mock_session.merge.assert_not_called()
        mock_session.commit.assert_called()

    @patch('maintain_feeder.utilities.local_land_charge.session')
    def test_process_land_charge_ok(self, mock_session):
        mock_session.query.return_value.filter.return_value.first.return_value = None
        mock_session.merge = self.mock_merge
        process_land_charge(MagicMock(), test_process_message_data_valid.process_message_valid)
        mock_session.add.assert_called_with(Any(LocalLandChargeHistory))
        self.assertTrue(isinstance(self.merge_called_with, LocalLandCharge))
        mock_session.commit.assert_called()

    @patch('maintain_feeder.utilities.local_land_charge.session')
    def test_process_land_charge_vary(self, mock_session):
        mock_session.query.return_value.filter.return_value.first.return_value = None
        mock_session.merge = self.mock_merge
        process_land_charge(MagicMock(), test_process_message_data_valid.process_message_valid_vary)
        mock_session.add.assert_called_with(Any(LocalLandChargeHistory))
        self.assertTrue(isinstance(self.merge_called_with, LocalLandCharge))
        mock_session.commit.assert_called()

    @patch('maintain_feeder.utilities.local_land_charge.session')
    def test_process_land_charge_invalid_geo(self, mock_session):
        mock_session.query.return_value.filter.return_value.first.return_value = None
        mock_session.merge = self.mock_merge
        with self.assertRaises(ApplicationError) as exc:
            process_land_charge(
                MagicMock(), test_process_message_no_feature_collection.process_message_no_feature_collection)
        mock_session.add.assert_called_with(Any(LocalLandChargeHistory))
        self.assertTrue(isinstance(self.merge_called_with, LocalLandCharge))
        mock_session.commit.assert_not_called()
        mock_session.rollback.assert_called()
        self.assertEqual(str(exc.exception), "No FeatureCollection found in entry")


class Any(object):
    def __init__(self, cls):
        self.cls = cls

    def __eq__(self, other):
        return isinstance(other, self.cls)
