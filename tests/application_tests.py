"""Tests for the azure_lightning_flask application"""

import unittest
from mock import patch
from azure.common import AzureMissingResourceHttpError
from azure_lightning_flask.application import create_app
from tests.test_config import TestConfig

class TestApplication(unittest.TestCase):
    """Tests for the azure_lightning_flask application"""
    class ContentRowResponse(object): # pylint: disable=too-few-public-methods
        """Simulated content response from Azure Table"""
        content = '<html></html>'

    class ActiveRowResponse(object): # pylint: disable=too-few-public-methods
        """Simulated active row response indicating active revision"""
        content = '{0}:ActiveRevision'.format(TestConfig.APP_NAME)

    def setUp(self):
        self.active_row_reponse = self.ActiveRowResponse()
        self.content_row_response = self.ContentRowResponse()
        self.default_revision_responses = iter([
            self.ActiveRowResponse(),
            self.ContentRowResponse()
        ])

        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

    @patch('azure_lightning_flask.helpers.TableService.get_entity')
    def test_root_valid_revision(self, mock_get_entity):
        """Test the application returns the revision specified"""
        mock_get_entity.return_value = self.content_row_response

        revision = 'TestRevision'
        url = '/?{0}={1}'.format(TestConfig.REVISION_PARAMETER, revision)
        response = self.client.get(url)

        row_key = '{0}:{1}'.format(TestConfig.APP_NAME, revision)
        mock_get_entity.assert_called_once_with(
            TestConfig.AZURE_STORAGE_TABLE,
            TestConfig.AZURE_STORAGE_TABLE_PARTITION_KEY,
            row_key
        )
        self.assertEqual(response.data, self.content_row_response.content)
        self.assertEqual(response.status_code, 200)

    @patch('azure_lightning_flask.helpers.TableService.get_entity')
    def test_root_default_revision(self, mock_get_entity):
        """Test the application returns the active revision when no revision is specified"""
        mock_get_entity.side_effect = self.default_revision_responses

        url = '/'
        response = self.client.get(url)

        active_row_key = '{0}:current'.format(TestConfig.APP_NAME)
        mock_get_entity.assert_any_call(
            TestConfig.AZURE_STORAGE_TABLE,
            TestConfig.AZURE_STORAGE_TABLE_PARTITION_KEY,
            active_row_key
        )
        mock_get_entity.assert_any_call(
            TestConfig.AZURE_STORAGE_TABLE,
            TestConfig.AZURE_STORAGE_TABLE_PARTITION_KEY,
            self.active_row_reponse.content
        )
        self.assertEqual(mock_get_entity.call_count, 2)
        self.assertEqual(response.data, self.content_row_response.content)
        self.assertEqual(response.status_code, 200)

    @patch('azure_lightning_flask.helpers.TableService.get_entity')
    def test_root_invalid_revision(self, mock_get_entity):
        """Test the application returns a 404 response when a specified revision can't be found"""
        mock_get_entity.side_effect = AzureMissingResourceHttpError("Not Found", 404)

        url = '/?{0}=InvalidRevsion'.format(TestConfig.REVISION_PARAMETER)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    @patch('azure_lightning_flask.helpers.TableService.get_entity')
    def test_root_empty_revision(self, mock_get_entity):
        """Test that an empty/blank but specified revision returns the active revision"""
        mock_get_entity.side_effect = self.default_revision_responses

        url = '/?{0}='.format(TestConfig.REVISION_PARAMETER)
        response = self.client.get(url)

        active_row_key = '{0}:current'.format(TestConfig.APP_NAME)
        mock_get_entity.assert_any_call(
            TestConfig.AZURE_STORAGE_TABLE,
            TestConfig.AZURE_STORAGE_TABLE_PARTITION_KEY,
            active_row_key
        )
        mock_get_entity.assert_any_call(
            TestConfig.AZURE_STORAGE_TABLE,
            TestConfig.AZURE_STORAGE_TABLE_PARTITION_KEY,
            self.active_row_reponse.content
        )
        self.assertEqual(mock_get_entity.call_count, 2)
        self.assertEqual(response.data, self.content_row_response.content)
        self.assertEqual(response.status_code, 200)

    @patch('azure_lightning_flask.helpers.TableService.get_entity')
    def test_nonroot_default_revision(self, mock_get_entity):
        """Test the application handles and responds correctly to arbitrary paths"""
        mock_get_entity.side_effect = self.default_revision_responses

        url = '/directory/much/deep/wow'
        response = self.client.get(url)

        active_row_key = '{0}:current'.format(TestConfig.APP_NAME)
        mock_get_entity.assert_any_call(
            TestConfig.AZURE_STORAGE_TABLE,
            TestConfig.AZURE_STORAGE_TABLE_PARTITION_KEY,
            active_row_key
        )
        mock_get_entity.assert_any_call(
            TestConfig.AZURE_STORAGE_TABLE,
            TestConfig.AZURE_STORAGE_TABLE_PARTITION_KEY,
            self.active_row_reponse.content
        )
        self.assertEqual(mock_get_entity.call_count, 2)
        self.assertEqual(response.data, self.content_row_response.content)
        self.assertEqual(response.status_code, 200)

    @patch('azure_lightning_flask.helpers.TableService.get_entity')
    def test_revision_with_additional_parameters(self, mock_get_entity): # pylint: disable=C0103
        """Test the application returns a requested revision even among other query parameters"""
        mock_get_entity.return_value = self.content_row_response

        revision = 'TestRevision'
        url = '/?index_key=123&{0}={1}&revision=456'.format(
            TestConfig.REVISION_PARAMETER,
            revision
        )
        response = self.client.get(url)

        row_key = '{0}:{1}'.format(TestConfig.APP_NAME, revision)
        mock_get_entity.assert_called_once_with(
            TestConfig.AZURE_STORAGE_TABLE,
            TestConfig.AZURE_STORAGE_TABLE_PARTITION_KEY,
            row_key
        )
        self.assertEqual(response.data, self.content_row_response.content)
        self.assertEqual(response.status_code, 200)

    @patch('azure_lightning_flask.helpers.TableService.get_entity')
    def test_default_with_parameters(self, mock_get_entity):
        """Test that the application ignores query parameters that are not requesting a revision"""
        mock_get_entity.side_effect = self.default_revision_responses

        url = '/?index_key=123&&revision=456'
        response = self.client.get(url)

        active_row_key = '{0}:current'.format(TestConfig.APP_NAME)
        mock_get_entity.assert_any_call(
            TestConfig.AZURE_STORAGE_TABLE,
            TestConfig.AZURE_STORAGE_TABLE_PARTITION_KEY,
            active_row_key
        )
        mock_get_entity.assert_any_call(
            TestConfig.AZURE_STORAGE_TABLE,
            TestConfig.AZURE_STORAGE_TABLE_PARTITION_KEY,
            self.active_row_reponse.content
        )
        self.assertEqual(mock_get_entity.call_count, 2)
        self.assertEqual(response.data, self.content_row_response.content)
        self.assertEqual(response.status_code, 200)
        