from django.shortcuts import render, get_object_or_404, redirect
from coredb.models import Games, AccountHistory, PersonGames, Person, ExchangeRate
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required


@login_required
def store_view(request):
    user_currency = request.user.currency

    games = Games.objects.all()

    for game in games:
        game.display_price = ExchangeRate.convert(game.price, "PLN", user_currency)

    return render(request, 'store/gamestore.html', {'games': games, 'currency': user_currency})


@login_required
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
    user_currency = request.user.currency 

    converted_price = ExchangeRate.convert(game.price, "PLN", user_currency)

    return render(request, 'store/game_detail.html', {
        'game': game,
        'converted_price': converted_price,
        'currency': user_currency
    })


@login_required
def buygame_as_gift(request, id):
    game = get_object_or_404(Games, id=id)

    if request.method == "POST":
        sender = request.user
        recipient_username = request.POST.get("username")

        if not recipient_username:
            messages.error(request, "Recipient username is required.")
            return render(request, 'store/buygameasgift.html', {'game': game})

        try:
            recipient = Person.objects.get(username=recipient_username)
        except Person.DoesNotExist:
            messages.error(request, f"The recipient username '{recipient_username}' does not exist.")
            return render(request, 'store/buygameasgift.html', {'game': game})

        if PersonGames.objects.filter(person=recipient, game=game).exists():
            messages.error(request, f"{recipient.username} already owns this game.")
            return render(request, 'store/buygameasgift.html', {'game': game})

        
        sender_currency = sender.currency
        game_price_in_sender_currency = ExchangeRate.convert(game.price, "PLN", sender_currency)

        if sender.total_balance < game_price_in_sender_currency:
            messages.error(request, "Not enough money in your account.")
            return render(request, 'store/buygameasgift.html', {'game': game})

       
        sender.total_balance -= game_price_in_sender_currency
        sender.save()

        
        PersonGames.objects.create(person=recipient, game=game, date=timezone.now())

       
        AccountHistory.objects.create(
            person=sender,
            game=game,
            date=timezone.now(),
            amount=-game_price_in_sender_currency 
        )
        AccountHistory.objects.create(
            person=recipient,
            game=game,
            date=timezone.now(),
            amount=0,  
        )

        messages.success(request, f"Successfully gifted '{game.tittle}' to {recipient.username}!")
        return redirect('store')

    return render(request, 'store/buygameasgift.html', {'game': game})
