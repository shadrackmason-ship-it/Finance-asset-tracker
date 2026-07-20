from django import forms
from .models import Asset, Transaction, TradeJournal, Watchlist


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ('name', 'asset_type', 'current_price', 'tv_symbol')
        widgets = {
            'name':          forms.TextInput(attrs={'class':'form-control','placeholder':'e.g. BTC, XAUUSD, AAPL'}),
            'asset_type':    forms.Select(attrs={'class':'form-select'}),
            'current_price': forms.NumberInput(attrs={'class':'form-control','step':'0.00000001'}),
            'tv_symbol':     forms.TextInput(attrs={'class':'form-control','placeholder':'e.g. BINANCE:BTCUSDT'}),
        }


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('asset', 'transaction_type', 'quantity', 'price_at_time', 'date', 'notes')
        widgets = {
            'asset':            forms.Select(attrs={'class':'form-select'}),
            'transaction_type': forms.Select(attrs={'class':'form-select'}),
            'quantity':         forms.NumberInput(attrs={'class':'form-control','step':'0.00000001'}),
            'price_at_time':    forms.NumberInput(attrs={'class':'form-control','step':'0.00000001'}),
            'date':             forms.DateTimeInput(attrs={'class':'form-control','type':'datetime-local'}),
            'notes':            forms.Textarea(attrs={'class':'form-control','rows':2}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['asset'].queryset = Asset.objects.filter(user=user)


class TradeJournalForm(forms.ModelForm):
    class Meta:
        model = TradeJournal
        fields = ('symbol','direction','entry_price','exit_price','stop_loss','take_profit','lot_size','outcome','pnl','rr_ratio','setup_notes','lesson','date')
        widgets = {
            'symbol':       forms.TextInput(attrs={'class':'form-control','placeholder':'e.g. EURUSD, BTCUSDT'}),
            'direction':    forms.Select(attrs={'class':'form-select'}),
            'entry_price':  forms.NumberInput(attrs={'class':'form-control','step':'0.00000001'}),
            'exit_price':   forms.NumberInput(attrs={'class':'form-control','step':'0.00000001'}),
            'stop_loss':    forms.NumberInput(attrs={'class':'form-control','step':'0.00000001'}),
            'take_profit':  forms.NumberInput(attrs={'class':'form-control','step':'0.00000001'}),
            'lot_size':     forms.NumberInput(attrs={'class':'form-control','step':'0.00000001'}),
            'outcome':      forms.Select(attrs={'class':'form-select'}),
            'pnl':          forms.NumberInput(attrs={'class':'form-control','step':'0.01'}),
            'rr_ratio':     forms.NumberInput(attrs={'class':'form-control','step':'0.01'}),
            'setup_notes':  forms.Textarea(attrs={'class':'form-control','rows':3,'placeholder':'Why did you take this trade?'}),
            'lesson':       forms.Textarea(attrs={'class':'form-control','rows':3,'placeholder':'What did you learn?'}),
            'date':         forms.DateTimeInput(attrs={'class':'form-control','type':'datetime-local'}),
        }


class WatchlistForm(forms.ModelForm):
    class Meta:
        model = Watchlist
        fields = ('symbol', 'tv_symbol', 'notes')
        widgets = {
            'symbol':    forms.TextInput(attrs={'class':'form-control','placeholder':'e.g. BTCUSDT, XAUUSD'}),
            'tv_symbol': forms.TextInput(attrs={'class':'form-control','placeholder':'e.g. BINANCE:BTCUSDT'}),
            'notes':     forms.TextInput(attrs={'class':'form-control','placeholder':'e.g. Waiting for breakout'}),
        }
