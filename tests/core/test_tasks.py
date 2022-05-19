from unittest.mock import patch

from django.core import mail
from django.test import TestCase

from core.models import Coins
from core.tasks import (
    export_data_to_excel,
    get_coins_data_from_coingecko_and_store,
    populate_googlesheet_with_coins_data,
)


class CoinTasksTests(TestCase):
    def test_get_coins_data_from_coingecko_and_store(self):
        '''Test get_coins_data_from_coingecko_and_store.'''

        with patch('core.tasks.requests.get') as mock_get:
            mock_get.return_value.coin_data = [
                {
                    'symbol': 'btc',
                    'name': 'Bitcoin',
                    'image': 'https://assets.coingecko.com/coins/images/1/large/bitcoin.png?1547033579',
                    'current_price': 12644080,
                    'market_cap': 240714282203755,
                    'market_cap_rank': 1,
                    'price_change_24h': 197155,
                    'total_supply': 21000000.0,
                }
            ]

            get_coins_data_from_coingecko_and_store()

        mock_get.assert_called_once()

    def test_populate_googlesheet_with_coins_data(self):
        '''Test populate_googlesheet_with_coins_data.'''

        Coins.objects.create(
            name='bitcoin', symbol='btc', current_price=12000000, price_change_within_24_hours=500, market_cap=210000000
        )
        Coins.objects.create(
            name='etherum', symbol='eth', current_price=12000000, price_change_within_24_hours=500, market_cap=210000000
        )
        Coins.objects.create(
            name='xrp', symbol='xrp', current_price=12000000, price_change_within_24_hours=500, market_cap=210000000
        )

        populate_googlesheet_with_coins_data()

    def test_export_data_to_excel(self):
        '''Test export_data_to_excel task.'''
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
