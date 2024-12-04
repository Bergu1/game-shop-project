from django.urls import path
from . import views

urlpatterns = [
    path('friends/', views.friends, name='friends'),
    path('friends_list/', views.friends_list, name='friends_list'),
    path('send_friend_request/', views.send_friend_request, name='send_friend_request'),
    path('invitations/', views.invitations, name='invitations'),
     path('friends/remove/<int:friend_id>/', views.remove_friend, name='remove_friend'),
]