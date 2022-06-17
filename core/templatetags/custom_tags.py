import decimal
import locale

from django import template

register = template.Library()


@register.filter(name='currency')
def currency(value: int | str) -> str:
    """Format currency."""
    try:
        locale.setlocale(locale.LC_ALL, 'en_NG.UTF-8')
    except (locale.Error, ValueError):
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    loc = locale.localeconv()
    returned_format = (
        locale.currency(decimal.Decimal(value), loc['currency_symbol'], grouping=True)  # type:ignore
        if value
        else '₦0.0'
    )
    return returned_format
