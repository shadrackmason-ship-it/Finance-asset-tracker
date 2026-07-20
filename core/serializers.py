from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import Asset, Transaction, TradeJournal, Watchlist


class AssetSerializer(serializers.ModelSerializer):
    total_quantity = serializers.DecimalField(max_digits=20, decimal_places=8, read_only=True)
    current_value  = serializers.DecimalField(max_digits=20, decimal_places=8, read_only=True)

    @extend_schema_field(serializers.DecimalField(max_digits=20, decimal_places=8))
    def get_total_quantity(self): pass

    @extend_schema_field(serializers.DecimalField(max_digits=20, decimal_places=8))
    def get_current_value(self): pass

    class Meta:
        model  = Asset
        fields = ['id', 'name', 'asset_type', 'current_price', 'tv_symbol',
                  'total_quantity', 'current_value', 'created_at']
        read_only_fields = ['id', 'created_at']


class TransactionSerializer(serializers.ModelSerializer):
    asset_name  = serializers.ReadOnlyField(source='asset.name')
    total_value = serializers.DecimalField(max_digits=20, decimal_places=8, read_only=True)

    class Meta:
        model  = Transaction
        fields = ['id', 'asset', 'asset_name', 'transaction_type',
                  'quantity', 'price_at_time', 'total_value', 'date', 'notes']
        read_only_fields = ['id']

    def validate_asset(self, asset):
        if asset.user != self.context['request'].user:
            raise serializers.ValidationError('Asset not found.')
        return asset


class TradeJournalSerializer(serializers.ModelSerializer):
    class Meta:
        model  = TradeJournal
        fields = ['id', 'symbol', 'direction', 'entry_price', 'exit_price',
                  'stop_loss', 'take_profit', 'lot_size', 'outcome',
                  'pnl', 'rr_ratio', 'setup_notes', 'lesson', 'date']
        read_only_fields = ['id']


class WatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Watchlist
        fields = ['id', 'symbol', 'tv_symbol', 'notes', 'added_at']
        read_only_fields = ['id', 'added_at']
