from django.test import TestCase

from core.models import Coins


class CoinsModelTests(TestCase):
    def setUp(self) -> None:
        """Create the setup of the test."""
        self.coin = Coins.objects.create(name='bitcoin', symbol='btc')

    def test_unicode(self) -> None:
        """Test the model's __str__ method"""
        self.assertEqual(str(self.coin), f'{self.coin.name} - {self.coin.symbol}')
