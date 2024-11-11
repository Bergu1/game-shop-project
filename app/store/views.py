from django.shortcuts import render, get_object_or_404
from coredb.models import Games

def store_view(request):
    games = Games.objects.all()
    return render(request, 'store/gamestore.html', {'games': games})

def buy_game(request, id):
    return render(request, 'users/mainPage.html')

def game_detail(request, id):
    game = get_object_or_404(Games, id=id)
    return render(request, 'store/game_detail.html', {'game': game})