from unittest.mock import patch

from django.test import Client, TestCase
from django.urls import reverse


class IndexViewTests(TestCase):
    def setUp(self) -> None:
        """Create the setup of the test."""
        self.client = Client()

    def test_context(self) -> None:
        """Test index context and template."""
        response = self.client.get(reverse('core:index'))
        self.assertEqual(response.templates[0].name, 'coin_data.html')


class ExtractAndSendCoinDataViaEmailTests(TestCase):
    def setUp(self) -> None:
        """Create the setup of the test."""
        self.client = Client()
        self.data = {'userEmail': 'django_excel@django.com'}

    def test_extract_and_send_coin_data_via_email_success(self):
        """Test extract and send extracted data."""

        with patch('core.views.export_data_to_excel.delay') as mock_export_data_to_excel:
            response = self.client.post(reverse('core:extract_data'), self.data, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        mock_export_data_to_excel.assert_called_once()

    def test_extract_and_send_coin_data_via_email_failure(self):
        response = self.client.get(reverse('core:extract_data'), self.data, content_type='application/json')
        self.assertEqual(response.status_code, 500)
