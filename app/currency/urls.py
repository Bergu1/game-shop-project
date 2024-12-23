from django.urls import path
from . import views

urlpatterns = [
    path('change-currency/', views.change_currency, name='change_currency'),
]
