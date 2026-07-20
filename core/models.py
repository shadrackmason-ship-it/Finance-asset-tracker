from django.db import models
from django.conf import settings
from django.utils import timezone


class Asset(models.Model):
    TYPE_CHOICES = [
        ('currency', 'Currency'),
        ('crypto', 'Cryptocurrency'),
        ('commodity', 'Commodity'),
        ('stock', 'Stock'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assets')
    name = models.CharField(max_length=50)
    asset_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    current_price = models.DecimalField(max_digits=20, decimal_places=8)
    tv_symbol = models.CharField(
        max_length=50, blank=True,
        help_text='TradingView symbol e.g. BINANCE:BTCUSDT, OANDA:XAUUSD, NASDAQ:AAPL'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'name')
        ordering = ['name']
        indexes = [models.Index(fields=['user'])]

    def __str__(self):
        return f"{self.name} ({self.get_asset_type_display()})"

    @property
    def total_quantity(self):
        from django.db.models import Sum
        buys  = self.transactions.filter(transaction_type__in=['buy','deposit']).aggregate(total=Sum('quantity'))['total'] or 0
        sells = self.transactions.filter(transaction_type__in=['sell','withdrawal']).aggregate(total=Sum('quantity'))['total'] or 0
        return buys - sells

    @property
    def current_value(self):
        return self.total_quantity * self.current_price


class Transaction(models.Model):
    TYPE_CHOICES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
    ]

    user             = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    asset            = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    quantity         = models.DecimalField(max_digits=20, decimal_places=8)
    price_at_time    = models.DecimalField(max_digits=20, decimal_places=8)
    date             = models.DateTimeField(default=timezone.now)
    notes            = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['asset']),
            models.Index(fields=['user', '-date']),
        ]

    def __str__(self):
        return f"{self.transaction_type.upper()} {self.quantity} {self.asset.name} @ {self.price_at_time}"

    @property
    def total_value(self):
        return self.quantity * self.price_at_time


class TradeJournal(models.Model):
    OUTCOME_CHOICES = [
        ('win',  'Win'),
        ('loss', 'Loss'),
        ('be',   'Break Even'),
        ('open', 'Still Open'),
    ]
    DIRECTION_CHOICES = [
        ('long',  'Long'),
        ('short', 'Short'),
    ]

    user          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='journal_entries')
    symbol        = models.CharField(max_length=30)
    direction     = models.CharField(max_length=10, choices=DIRECTION_CHOICES)
    entry_price   = models.DecimalField(max_digits=20, decimal_places=8)
    exit_price    = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    stop_loss     = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    take_profit   = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    lot_size      = models.DecimalField(max_digits=20, decimal_places=8, default=1)
    outcome       = models.CharField(max_length=10, choices=OUTCOME_CHOICES, default='open')
    pnl           = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    rr_ratio      = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    setup_notes   = models.TextField(blank=True, help_text='Why did you take this trade?')
    lesson        = models.TextField(blank=True, help_text='What did you learn?')
    date          = models.DateTimeField(default=timezone.now)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        indexes  = [models.Index(fields=['user', '-date'])]

    def __str__(self):
        return f"{self.direction.upper()} {self.symbol} — {self.outcome}"


class Watchlist(models.Model):
    user      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='watchlist')
    symbol    = models.CharField(max_length=50)
    tv_symbol = models.CharField(max_length=50, blank=True)
    notes     = models.CharField(max_length=200, blank=True)
    added_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'symbol')
        ordering        = ['symbol']

    def __str__(self):
        return f"{self.user.username} — {self.symbol}"
