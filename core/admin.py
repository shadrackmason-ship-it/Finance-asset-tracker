from django.contrib import admin
from .models import Asset, Transaction, TradeJournal, Watchlist


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display  = ('name', 'asset_type', 'current_price', 'user', 'updated_at')
    list_filter   = ('asset_type',)
    search_fields = ('name', 'user__username')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display  = ('asset', 'transaction_type', 'quantity', 'price_at_time', 'date', 'user')
    list_filter   = ('transaction_type',)
    date_hierarchy = 'date'
    search_fields = ('asset__name', 'user__username')


@admin.register(TradeJournal)
class TradeJournalAdmin(admin.ModelAdmin):
    list_display  = ('symbol', 'direction', 'outcome', 'pnl', 'rr_ratio', 'date', 'user')
    list_filter   = ('outcome', 'direction')
    date_hierarchy = 'date'
    search_fields = ('symbol', 'user__username')


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display  = ('symbol', 'user', 'added_at')
    search_fields = ('symbol', 'user__username')
