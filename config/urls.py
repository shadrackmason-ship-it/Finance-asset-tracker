from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseNotFound
from django.contrib.auth import views as auth_views
from decouple import config
from honeypot.decorators import honeypot_exempt
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core.views import landing, error_403, error_404, error_500
from core.api_views import (
    AssetViewSet, TransactionViewSet,
    TradeJournalViewSet, WatchlistViewSet, portfolio_summary,
)
from users.views import register
from users.forms import EmailOrUsernameAuthForm

# Secret admin path — only you know this from .env
ADMIN_URL = config('ADMIN_URL', default='mt-admin-x9k2')

# Anything hitting /admin/ or /wp-admin/ gets a 404 — looks like a normal site
def fake_404(request, *args, **kwargs):
    return HttpResponseNotFound()

# ── API Router (5 schemes) ──
router = DefaultRouter()
router.register(r'assets',       AssetViewSet,        basename='api-assets')
router.register(r'transactions', TransactionViewSet,  basename='api-transactions')
router.register(r'journal',      TradeJournalViewSet, basename='api-journal')
router.register(r'watchlist',    WatchlistViewSet,    basename='api-watchlist')

urlpatterns = [
    # ── Secret admin (only accessible via your secret URL) ──
    path(f'{ADMIN_URL}/', admin.site.urls),

    # ── Honeypot traps ──
    path('admin/', fake_404),
    path('admin/<path:rest>', fake_404),
    path('wp-admin/', fake_404),
    path('wp-login.php', fake_404),
    path('.env', fake_404),
    path('config.php', fake_404),

    # ── Public routes ──
    path('', landing, name='landing'),
    path('register/', register, name='register'),
    path('app/', include('core.urls')),
    # Override login with email-or-username form
    path('accounts/login/', auth_views.LoginView.as_view(
        authentication_form=EmailOrUsernameAuthForm
    ), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('users.urls')),

    # ── REST API ──
    path('api/', include(router.urls)),
    path('api/portfolio/', portfolio_summary, name='api-portfolio'),
    path('api/auth/token/', TokenObtainPairView.as_view(),  name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# Custom error handlers
handler403 = error_403
handler404 = error_404
handler500 = error_500
