from django.urls import path
from . import views

urlpatterns = [
    path('friends/', views.friends, name='friends'),
    path('send_friend_request/', views.send_friend_request, name='send_friend_request'),
]