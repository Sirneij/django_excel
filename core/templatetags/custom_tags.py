import decimal
import locale

from django import template

register = template.Library()


@register.filter(name='currency')
def currency(value):
    locale.setlocale(locale.LC_ALL, 'en_NG.UTF-8')
    loc = locale.localeconv()
    return locale.currency(decimal.Decimal(value), loc['currency_symbol'], grouping=True)
