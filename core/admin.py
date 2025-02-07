from django.contrib import admin

from core.models import Coins, FullCoin


@admin.register(Coins)
class CoinsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'symbol',
        'current_price',
        'price_change_within_24_hours',
        'rank',
        'market_cap',
        'total_supply',
    )


@admin.register(FullCoin)
class FullCoinAdmin(admin.ModelAdmin):
    list_display = (
        'coin_id',
        'symbol',
        'name',
        'current_price',
        'market_cap',
        'market_cap_rank',
        'fully_diluted_valuation',
        'total_volume',
        'high_24h',
        'low_24h',
        'price_change_24h',
        'price_change_percentage_24h',
        'market_cap_change_24h',
        'market_cap_change_percentage_24h',
        'circulating_supply',
        'total_supply',
        'max_supply',
        'ath',
        'ath_change_percentage',
        'ath_date',
        'atl',
        'atl_change_percentage',
        'atl_date',
        'last_updated',
    )
    list_filter = ('coin_id', 'symbol', 'name', 'market_cap_rank')
