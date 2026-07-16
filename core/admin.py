from django.contrib import admin
from .models import Asset, Transaction


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'asset_type', 'current_price', 'user', 'updated_at')
    list_filter = ('asset_type', 'user')
    search_fields = ('name',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('asset', 'transaction_type', 'quantity', 'price_at_time', 'date', 'user')
    list_filter = ('transaction_type', 'asset', 'user')
    date_hierarchy = 'date'
