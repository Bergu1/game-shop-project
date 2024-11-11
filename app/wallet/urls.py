from django.urls import path
from . import views

urlpatterns = [
    path('wallet_view/', views.wallet_view, name='wallet_view'),
    path('wallet_operations/', views.wallet_operations, name='wallet_operations'),
    path('account_history/', views.account_history, name='account_history'),
]