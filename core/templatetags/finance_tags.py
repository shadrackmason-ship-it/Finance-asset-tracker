from django import template
from users.models import CURRENCY_SYMBOLS

register = template.Library()

@register.filter
def currency(value, symbol):
    """Format a number with a currency symbol: {{ value|currency:symbol }}"""
    try:
        val = float(value)
        if abs(val) >= 1_000_000:
            return f"{symbol}{val/1_000_000:,.2f}M"
        return f"{symbol}{val:,.2f}"
    except (TypeError, ValueError):
        return f"{symbol}0.00"

@register.filter
def currency_code(user):
    """Return the user's preferred currency code."""
    return getattr(user, 'preferred_currency', 'USD')

@register.simple_tag(takes_context=True)
def user_symbol(context):
    user = context.get('request') and context['request'].user
    if user and user.is_authenticated:
        return CURRENCY_SYMBOLS.get(user.preferred_currency, '$')
    return '$'
