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
    name = models.CharField(max_length=50)          # e.g. XAUUSD, BTC, Savings
    asset_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    current_price = models.DecimalField(max_digits=20, decimal_places=8)  # DecimalField = financial accuracy
    tv_symbol = models.CharField(
        max_length=50, blank=True,
        help_text='TradingView symbol e.g. BINANCE:BTCUSDT, OANDA:XAUUSD, NASDAQ:AAPL'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'name')
        ordering = ['name']
        indexes = [
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_asset_type_display()})"

    @property
    def total_quantity(self):
        """Net quantity owned: sum of buys/deposits minus sells/withdrawals."""
        from django.db.models import Sum
        buys = self.transactions.filter(
            transaction_type__in=['buy', 'deposit']
        ).aggregate(total=Sum('quantity'))['total'] or 0

        sells = self.transactions.filter(
            transaction_type__in=['sell', 'withdrawal']
        ).aggregate(total=Sum('quantity'))['total'] or 0

        return buys - sells

    @property
    def current_value(self):
        """Current market value of holdings."""
        return self.total_quantity * self.current_price


class Transaction(models.Model):
    TYPE_CHOICES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    quantity = models.DecimalField(max_digits=20, decimal_places=8)   # e.g. 0.5 BTC
    price_at_time = models.DecimalField(max_digits=20, decimal_places=8)  # price when trade happened
    date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)

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
