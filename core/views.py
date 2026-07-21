from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from decimal import Decimal
import json
import logging

from .models import Asset, Transaction, TradeJournal, Watchlist
from .forms import AssetForm, TransactionForm, TradeJournalForm, WatchlistForm

logger = logging.getLogger('masontrack')


def error_403(request, exception=None):
    return render(request, 'errors/403.html', status=403)

def error_404(request, exception=None):
    return render(request, 'errors/404.html', status=404)

def error_500(request):
    return render(request, 'errors/500.html', status=500)


def landing(request):
    """Public landing page — shown to unauthenticated visitors."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')

@login_required
def dashboard(request):
    assets = Asset.objects.filter(user=request.user).prefetch_related('transactions')

    portfolio = []
    total_value = Decimal('0')
    total_invested = Decimal('0')

    for asset in assets:
        txns = asset.transactions.all()  # uses prefetch cache — no extra queries
        buy_qty = sum(t.quantity for t in txns if t.transaction_type in ('buy', 'deposit'))
        sell_qty = sum(t.quantity for t in txns if t.transaction_type in ('sell', 'withdrawal'))
        quantity = buy_qty - sell_qty
        cost_basis = sum(t.quantity * t.price_at_time for t in txns if t.transaction_type in ('buy', 'deposit'))
        value = quantity * asset.current_price
        pnl = value - cost_basis
        portfolio.append({'asset': asset, 'value': value, 'cost_basis': cost_basis, 'pnl': pnl, 'quantity': quantity})
        total_value += value
        total_invested += cost_basis

    total_pnl = total_value - total_invested
    pnl_pct = (total_pnl / total_invested * 100) if total_invested else Decimal('0')

    chart_labels = [p['asset'].name for p in portfolio if p['value'] > 0]
    chart_data = [float(p['value']) for p in portfolio if p['value'] > 0]

    recent_transactions = Transaction.objects.filter(user=request.user).select_related('asset')[:10]

    context = {
        'portfolio': portfolio,
        'total_value': total_value,
        'total_invested': total_invested,
        'total_pnl': total_pnl,
        'pnl_pct': pnl_pct,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
        'recent_transactions': recent_transactions,
        'currency': request.user.preferred_currency,
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def asset_list(request):
    assets = Asset.objects.filter(user=request.user)
    return render(request, 'core/asset_list.html', {'assets': assets})


@login_required
def asset_create(request):
    examples = [
        {'name':'BTC',     'type':'crypto',    'type_display':'Crypto',    'price':'67000',  'symbol':'BINANCE:BTCUSDT'},
        {'name':'ETH',     'type':'crypto',    'type_display':'Crypto',    'price':'3500',   'symbol':'BINANCE:ETHUSDT'},
        {'name':'XAUUSD',  'type':'commodity', 'type_display':'Commodity', 'price':'2350',   'symbol':'OANDA:XAUUSD'},
        {'name':'EURUSD',  'type':'currency',  'type_display':'Forex',     'price':'1.085',  'symbol':'OANDA:EURUSD'},
        {'name':'AAPL',    'type':'stock',     'type_display':'Stock',     'price':'189',    'symbol':'NASDAQ:AAPL'},
        {'name':'NVDA',    'type':'stock',     'type_display':'Stock',     'price':'875',    'symbol':'NASDAQ:NVDA'},
        {'name':'SOL',     'type':'crypto',    'type_display':'Crypto',    'price':'170',    'symbol':'BINANCE:SOLUSDT'},
        {'name':'OIL',     'type':'commodity', 'type_display':'Commodity', 'price':'78',     'symbol':'NYMEX:CL1!'},
    ]
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.user = request.user
            if Asset.objects.filter(user=request.user, name=asset.name).exists():
                form.add_error('name', 'You already have an asset with this name.')
            else:
                asset.save()
                messages.success(request, f'Asset "{asset.name}" added successfully.')
                return redirect('asset_list')
    else:
        form = AssetForm()
    return render(request, 'core/asset_form.html', {'form': form, 'title': 'Add Asset', 'examples': examples})


@login_required
def asset_update(request, pk):
    asset = get_object_or_404(Asset, pk=pk, user=request.user)  # user=request.user prevents accessing others' data
    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            messages.success(request, f'Asset "{asset.name}" updated.')
            return redirect('asset_list')
    else:
        form = AssetForm(instance=asset)
    return render(request, 'core/asset_form.html', {'form': form, 'title': 'Update Asset'})


@login_required
def asset_delete(request, pk):
    asset = get_object_or_404(Asset, pk=pk, user=request.user)
    if request.method == 'POST':
        asset.delete()
        messages.success(request, 'Asset deleted.')
        return redirect('asset_list')
    return render(request, 'core/confirm_delete.html', {'object': asset, 'type': 'Asset'})


@login_required
def transaction_list(request):
    from django.core.paginator import Paginator
    qs = Transaction.objects.filter(user=request.user).select_related('asset')
    paginator = Paginator(qs, 50)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'core/transaction_list.html', {'transactions': page, 'paginator': paginator})


@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.user, request.POST)
        if form.is_valid():
            txn = form.save(commit=False)
            txn.user = request.user
            txn.save()
            logger.info('Transaction logged: user=%s asset=%s type=%s qty=%s',
                        request.user.username, txn.asset.name,
                        txn.transaction_type, txn.quantity)
            messages.success(request, 'Transaction logged.')
            return redirect('dashboard')
    else:
        form = TransactionForm(request.user)
    return render(request, 'core/transaction_form.html', {'form': form, 'title': 'Log Transaction'})


@login_required
def transaction_delete(request, pk):
    txn = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        txn.delete()
        messages.success(request, 'Transaction deleted.')
        return redirect('transaction_list')
    return render(request, 'core/confirm_delete.html', {'object': txn, 'type': 'Transaction'})


@login_required
def market(request):
    """TradingView full chart page — search any symbol live."""
    symbol = request.GET.get('symbol', 'BINANCE:BTCUSDT')
    assets = Asset.objects.filter(user=request.user).exclude(tv_symbol='')
    popular_symbols = [
        # Crypto
        ('BINANCE:BTCUSDT',  'BTC'),
        ('BINANCE:ETHUSDT',  'ETH'),
        ('BINANCE:SOLUSDT',  'SOL'),
        ('BINANCE:BNBUSDT',  'BNB'),
        ('BINANCE:XRPUSDT',  'XRP'),
        # Commodities
        ('OANDA:XAUUSD',     'Gold'),
        ('OANDA:XAGUSD',     'Silver'),
        ('NYMEX:CL1!',       'Oil'),
        # Forex
        ('OANDA:EURUSD',     'EUR/USD'),
        ('OANDA:GBPUSD',     'GBP/USD'),
        ('OANDA:USDJPY',     'USD/JPY'),
        ('OANDA:USDNGN',     'USD/NGN'),
        ('OANDA:USDZAR',     'USD/ZAR'),
        ('OANDA:USDKES',     'USD/KES'),
        ('OANDA:USDINR',     'USD/INR'),
        ('OANDA:USDBRL',     'USD/BRL'),
        ('OANDA:USDCNY',     'USD/CNY'),
        ('OANDA:USDAED',     'USD/AED'),
        # US Stocks
        ('NASDAQ:AAPL',      'AAPL'),
        ('NASDAQ:TSLA',      'TSLA'),
        ('NASDAQ:NVDA',      'NVDA'),
        ('NASDAQ:MSFT',      'MSFT'),
        ('NYSE:AMZN',        'AMZN'),
        # Global Indices
        ('FOREXCOM:SPXUSD',  'S&P 500'),
        ('FOREXCOM:NSXUSD',  'NASDAQ'),
        ('SPREADEX:UK100',   'FTSE 100'),
        ('FOREXCOM:DEU40',   'DAX'),
        ('TVC:NI225',        'Nikkei'),
        ('TVC:HSI',          'Hang Seng'),
    ]
    return render(request, 'core/market.html', {
        'symbol': symbol,
        'assets': assets,
        'popular_symbols': popular_symbols,
    })


@login_required
def risk_calculator(request):
    return render(request, 'core/risk_calculator.html')


@login_required
def journal_list(request):
    entries = TradeJournal.objects.filter(user=request.user)
    wins    = entries.filter(outcome='win').count()
    losses  = entries.filter(outcome='loss').count()
    total   = entries.count()
    win_rate = round((wins / total * 100), 1) if total else 0
    total_pnl = sum(e.pnl for e in entries if e.pnl) or 0
    return render(request, 'core/journal_list.html', {
        'entries': entries, 'wins': wins, 'losses': losses,
        'total': total, 'win_rate': win_rate, 'total_pnl': total_pnl,
    })


@login_required
def journal_create(request):
    if request.method == 'POST':
        form = TradeJournalForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, 'Trade logged to journal.')
            return redirect('journal_list')
    else:
        form = TradeJournalForm()
    return render(request, 'core/journal_form.html', {'form': form, 'title': 'Log Trade'})


@login_required
def journal_update(request, pk):
    entry = get_object_or_404(TradeJournal, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TradeJournalForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Journal entry updated.')
            return redirect('journal_list')
    else:
        form = TradeJournalForm(instance=entry)
    return render(request, 'core/journal_form.html', {'form': form, 'title': 'Edit Trade'})


@login_required
def journal_delete(request, pk):
    entry = get_object_or_404(TradeJournal, pk=pk, user=request.user)
    if request.method == 'POST':
        entry.delete()
        messages.success(request, 'Journal entry deleted.')
        return redirect('journal_list')
    return render(request, 'core/confirm_delete.html', {'object': entry, 'type': 'Journal Entry'})


@login_required
def watchlist(request):
    items = Watchlist.objects.filter(user=request.user)
    form  = WatchlistForm()
    if request.method == 'POST':
        form = WatchlistForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            messages.success(request, f'{item.symbol} added to watchlist.')
            return redirect('watchlist')
    return render(request, 'core/watchlist.html', {'items': items, 'form': form})


@login_required
def watchlist_delete(request, pk):
    item = get_object_or_404(Watchlist, pk=pk, user=request.user)
    if request.method == 'POST':
        item.delete()
        return redirect('watchlist')
    return redirect('watchlist')


@login_required
def asset_detail(request, pk):
    asset = get_object_or_404(Asset.objects.prefetch_related('transactions'), pk=pk, user=request.user)
    transactions = asset.transactions.all()
    cost_basis = sum(
        t.quantity * t.price_at_time
        for t in transactions if t.transaction_type in ('buy', 'deposit')
    )
    pnl = (asset.total_quantity * asset.current_price) - cost_basis
    return render(request, 'core/asset_detail.html', {
        'asset': asset,
        'transactions': transactions,
        'cost_basis': cost_basis,
        'pnl': pnl,
    })
