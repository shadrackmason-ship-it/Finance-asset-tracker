from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
from drf_spectacular.openapi import OpenApiTypes
from drf_spectacular.utils import OpenApiResponse
from rest_framework import serializers as drf_serializers
from decimal import Decimal

from .models import Asset, Transaction, TradeJournal, Watchlist
from .serializers import (
    AssetSerializer, TransactionSerializer,
    TradeJournalSerializer, WatchlistSerializer,
)


# ── Scheme 1: Assets ──────────────────────────────────────────────────────────
@extend_schema_view(
    list=extend_schema(tags=['assets'], summary='List your assets'),
    create=extend_schema(tags=['assets'], summary='Add a new asset'),
    retrieve=extend_schema(tags=['assets'], summary='Get asset detail'),
    update=extend_schema(tags=['assets'], summary='Update asset'),
    partial_update=extend_schema(tags=['assets'], summary='Partially update asset'),
    destroy=extend_schema(tags=['assets'], summary='Delete asset'),
)
class AssetViewSet(viewsets.ModelViewSet):
    serializer_class   = AssetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Asset.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ── Scheme 2: Transactions ────────────────────────────────────────────────────
@extend_schema_view(
    list=extend_schema(tags=['transactions'], summary='List transactions'),
    create=extend_schema(tags=['transactions'], summary='Log a transaction'),
    retrieve=extend_schema(tags=['transactions'], summary='Get transaction detail'),
    update=extend_schema(tags=['transactions'], summary='Update transaction'),
    partial_update=extend_schema(tags=['transactions'], summary='Partially update transaction'),
    destroy=extend_schema(tags=['transactions'], summary='Delete transaction'),
)
class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class   = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).select_related('asset')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ── Scheme 3: Trade Journal ───────────────────────────────────────────────────
@extend_schema_view(
    list=extend_schema(tags=['journal'], summary='List journal entries'),
    create=extend_schema(tags=['journal'], summary='Log a trade'),
    retrieve=extend_schema(tags=['journal'], summary='Get journal entry'),
    update=extend_schema(tags=['journal'], summary='Update journal entry'),
    partial_update=extend_schema(tags=['journal'], summary='Partially update entry'),
    destroy=extend_schema(tags=['journal'], summary='Delete journal entry'),
)
class TradeJournalViewSet(viewsets.ModelViewSet):
    serializer_class   = TradeJournalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TradeJournal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ── Scheme 4: Watchlist ───────────────────────────────────────────────────────
@extend_schema_view(
    list=extend_schema(tags=['watchlist'], summary='List watchlist'),
    create=extend_schema(tags=['watchlist'], summary='Add to watchlist'),
    retrieve=extend_schema(tags=['watchlist'], summary='Get watchlist item'),
    update=extend_schema(tags=['watchlist'], summary='Update watchlist item'),
    partial_update=extend_schema(tags=['watchlist'], summary='Partially update item'),
    destroy=extend_schema(tags=['watchlist'], summary='Remove from watchlist'),
)
class WatchlistViewSet(viewsets.ModelViewSet):
    serializer_class   = WatchlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Watchlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ── Scheme 5: Portfolio Summary ───────────────────────────────────────────────
@extend_schema(
    tags=['portfolio'],
    summary='Full portfolio P&L summary',
    responses={
        200: {
            'type': 'object',
            'properties': {
                'total_value':    {'type': 'number'},
                'total_invested': {'type': 'number'},
                'total_pnl':      {'type': 'number'},
                'pnl_pct':        {'type': 'number'},
                'holdings':       {'type': 'array', 'items': {'type': 'object'}},
            }
        }
    }
)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def portfolio_summary(request):
    assets = Asset.objects.filter(user=request.user).prefetch_related('transactions')
    total_value, total_invested = Decimal('0'), Decimal('0')
    holdings = []

    for asset in assets:
        txns       = asset.transactions.all()
        buy_qty    = sum(t.quantity for t in txns if t.transaction_type in ('buy', 'deposit'))
        sell_qty   = sum(t.quantity for t in txns if t.transaction_type in ('sell', 'withdrawal'))
        quantity   = buy_qty - sell_qty
        cost_basis = sum(t.quantity * t.price_at_time for t in txns if t.transaction_type in ('buy', 'deposit'))
        value      = quantity * asset.current_price
        pnl        = value - cost_basis
        total_value    += value
        total_invested += cost_basis
        holdings.append({
            'asset': asset.name,
            'type': asset.asset_type,
            'quantity': quantity,
            'current_price': asset.current_price,
            'value': value,
            'cost_basis': cost_basis,
            'pnl': pnl,
            'pnl_pct': round(pnl / cost_basis * 100, 2) if cost_basis else 0,
        })

    total_pnl = total_value - total_invested
    return Response({
        'total_value': total_value,
        'total_invested': total_invested,
        'total_pnl': total_pnl,
        'pnl_pct': round(total_pnl / total_invested * 100, 2) if total_invested else 0,
        'holdings': holdings,
    })
