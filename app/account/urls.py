from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('account_view/', views.account_view, name='account_view'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('change_data/', views.change_data, name='change_data'),
]