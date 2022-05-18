from django.core import mail
from django.test import TestCase

from core.models import Coins
from core.tasks import export_data_to_excel


class CoinTasksTests(TestCase):
    def test_export_data_to_excel(self):
        """Test export_data_to_excel task."""
        Coins.objects.create(
            name='bitcoin', symbol='btc', current_price=12000000, price_change_within_24_hours=500, market_cap=210000000
        )
        Coins.objects.create(
            name='etherum', symbol='eth', current_price=12000000, price_change_within_24_hours=500, market_cap=210000000
        )
        Coins.objects.create(
            name='xrp', symbol='xrp', current_price=12000000, price_change_within_24_hours=500, market_cap=210000000
        )

        export_data_to_excel('admin@django_excel.com')

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['admin@django_excel.com'])
