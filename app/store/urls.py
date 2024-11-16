from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('store/', views.store_view, name='store'),
    path('buy_game/<int:id>/', views.buy_game, name='buy_game'),
    path('game_detail/<int:id>/', views.game_detail, name='game_detail'),
    path('buy_gift/<int:id>/', views.buygame_as_gift, name='game_gift'),
]