from django import forms
from .models import Asset, Transaction


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ('name', 'asset_type', 'current_price', 'tv_symbol')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. BTC, XAUUSD, AAPL'}),
            'asset_type': forms.Select(attrs={'class': 'form-select'}),
            'current_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.00000001'}),
            'tv_symbol': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. BINANCE:BTCUSDT or OANDA:XAUUSD'}),
        }


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('asset', 'transaction_type', 'quantity', 'price_at_time', 'date', 'notes')
        widgets = {
            'asset': forms.Select(attrs={'class': 'form-select'}),
            'transaction_type': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.00000001'}),
            'price_at_time': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.00000001'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Users only see their own assets in the dropdown — security by design
        self.fields['asset'].queryset = Asset.objects.filter(user=user)
