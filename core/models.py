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

    class Meta:
        verbose_name_plural = 'Coins'

    def __str__(self) -> str:
        """Return model string representation."""
        return f'{self.name} - {self.symbol}'


class FullCoin(models.Model):
    coin_id = models.CharField(max_length=100, primary_key=True)
    symbol = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    current_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    market_cap = models.BigIntegerField(null=True, blank=True)
    market_cap_rank = models.IntegerField(null=True, blank=True)
    fully_diluted_valuation = models.BigIntegerField(null=True, blank=True)
    total_volume = models.BigIntegerField(null=True, blank=True)
    high_24h = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    low_24h = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    price_change_24h = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    price_change_percentage_24h = models.DecimalField(max_digits=10, decimal_places=5, null=True, blank=True)
    market_cap_change_24h = models.BigIntegerField(null=True, blank=True)
    market_cap_change_percentage_24h = models.DecimalField(max_digits=10, decimal_places=5, null=True, blank=True)
    circulating_supply = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    total_supply = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    max_supply = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    ath = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    ath_change_percentage = models.DecimalField(max_digits=10, decimal_places=5, null=True, blank=True)
    ath_date = models.DateTimeField(null=True, blank=True)
    atl = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    atl_change_percentage = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True)
    atl_date = models.DateTimeField(null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.symbol.upper()})"
