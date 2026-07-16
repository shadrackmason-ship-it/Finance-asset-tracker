from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, ProfileForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    regions = [
        ('Americas',     '🌎', 'USD, CAD, BRL, MXN...'),
        ('Europe',       '🌍', 'EUR, GBP, CHF, SEK...'),
        ('Africa',       '🌍', 'NGN, ZAR, KES, GHS...'),
        ('Middle East',  '🌏', 'AED, SAR, QAR, ILS...'),
        ('Asia',         '🌏', 'JPY, CNY, INR, KRW...'),
        ('Pacific',      '🌏', 'AUD, NZD, SGD, HKD...'),
        ('Crypto',       '₿',  'BTC, ETH, SOL, BNB...'),
        ('Commodities',  '🥇', 'Gold, Silver, Oil...'),
    ]
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'registration/profile.html', {'form': form, 'regions': regions})
