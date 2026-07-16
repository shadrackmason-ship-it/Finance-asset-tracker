from django.urls import path
from . import views
from users.views import register

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', register, name='register'),

    path('assets/', views.asset_list, name='asset_list'),
    path('assets/add/', views.asset_create, name='asset_create'),
    path('assets/<int:pk>/', views.asset_detail, name='asset_detail'),
    path('assets/<int:pk>/edit/', views.asset_update, name='asset_update'),
    path('assets/<int:pk>/delete/', views.asset_delete, name='asset_delete'),

    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/add/', views.transaction_create, name='transaction_create'),
    path('transactions/<int:pk>/delete/', views.transaction_delete, name='transaction_delete'),

    path('market/', views.market, name='market'),
    path('risk-calculator/', views.risk_calculator, name='risk_calculator'),
]
