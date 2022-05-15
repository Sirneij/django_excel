from django.db import models


class Coins(models.Model):
    name = models.CharField(max_length=200, null=True)
    symbol = models.CharField(max_length=200, null=True)
    image_url = models.URLField(null=True)
    current_price = models.DecimalField(decimal_places=2, max_digits=50, null=True)
    price_change_within_24_hours = models.DecimalField(decimal_places=2, max_digits=50, null=True)
    rank = models.IntegerField(null=True)
    market_cap = models.DecimalField(decimal_places=2, max_digits=50, null=True)
    total_supply = models.DecimalField(decimal_places=2, max_digits=50, null=True)

    def __str__(self):
        return f'{self.name} - {self.symbol}'
