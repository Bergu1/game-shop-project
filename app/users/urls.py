from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('mainPage/', views.mainPage, name='mainPage'),
    path('news_list/', views.news_list, name='news_list'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
]