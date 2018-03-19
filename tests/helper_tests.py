"""Tests for functions defined in helpers.py"""

import unittest
from mock import patch
from azure_lightning_flask.application import create_app
from azure_lightning_flask.helpers import format_row_key, get_table_service
from tests.test_config import TestConfig

class TestFormatRowKey(unittest.TestCase):
    """Tests for the format_row_key function from helpers.py"""
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

    def test_formats_revision(self):
        """Test that format_row_key formats a given revision"""
        with self.app.app_context():
            self.assertEqual(
                format_row_key(''),
                'TestApplicationRowKeyAppName:'
            )
            self.assertEqual(
                format_row_key('TestRevision'),
                'TestApplicationRowKeyAppName:TestRevision'
            )

class TestGetTableService(unittest.TestCase):
    """Tests for the get_table_service function from helpers.py"""
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

    @patch('azure_lightning_flask.helpers.TableService')
    def test_inits(self, mock_table_service):
        """Test that get_table_service returns an instance of TableService"""
        with self.app.app_context():
            get_table_service()

        mock_table_service.assert_called_once_with(
            account_name=TestConfig.AZURE_STORAGE_ACCOUNT,
            account_key=TestConfig.AZURE_STORAGE_KEY
        )

    @patch('azure_lightning_flask.helpers.TableService')
    def test_inits_only_once(self, mock_table_service):
        """Test that get_table_service only initalizes one instance of TableService per request"""
        with self.app.app_context():
            get_table_service()
            get_table_service()

        mock_table_service.assert_called_once()
