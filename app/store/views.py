from django.shortcuts import render, get_object_or_404, redirect
from coredb.models import Games, AccountHistory, PersonGames
from django.contrib import messages
from django.utils import timezone

def store_view(request):
    games = Games.objects.all()
    return render(request, 'store/gamestore.html', {'games': games})

def buy_game(request, id):
    user = request.user
    game = get_object_or_404(Games, id=id)
    price = game.price

    if PersonGames.objects.filter(person=user, game=game).exists():
        messages.error(request, "You already own this game.")
        return redirect('store')
    
    if user.total_balance >= price:
        user.total_balance -= price
        user.save()

        AccountHistory.objects.create(
            person=user,
            game=game,
            date=timezone.now(),
            amount=price
        )

        PersonGames.objects.create(person=user, game=game, date=timezone.now())

        messages.success(request, "Successful purchase!")
    else:
        messages.error(request, "Not enough money in your account.")
    return redirect('store')

def game_detail(request, id):
    game = get_object_or_404(Games, id=id)
    return render(request, 'store/game_detail.html', {'game': game})