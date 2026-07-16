from users.models import CURRENCY_SYMBOLS


def user_preferences(request):
    """Inject currency symbol and timezone into every template context."""
    if request.user.is_authenticated:
        symbol = CURRENCY_SYMBOLS.get(request.user.preferred_currency, '$')
        return {
            'currency_symbol': symbol,
            'user_currency': request.user.preferred_currency,
            'user_timezone': request.user.timezone,
        }
    return {
        'currency_symbol': '$',
        'user_currency': 'USD',
        'user_timezone': 'UTC',
    }
