from django.shortcuts import render, get_object_or_404, redirect
from coredb.models import Games, AccountHistory, PersonGames, Person, ExchangeRate
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import ConfirmPasswordForm
from django.contrib.auth import authenticate
from decimal import Decimal



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

    if request.method == "POST":
        form = ConfirmPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get("password")
            user = authenticate(username=user.username, password=password)
            if user:
                if PersonGames.objects.filter(person=user, game=game).exists():
                    messages.error(request, "You already own this game.")
                    return redirect('store')

                if user.total_balance >= game.price:
                    user.total_balance -= game.price
                    user.save()

                    AccountHistory.objects.create(
                        person=user,
                        game=game,
                        date=timezone.now(),
                        amount=game.price
                    )

                    PersonGames.objects.create(person=user, game=game, date=timezone.now())

                    messages.success(request, "Successful purchase!")
                    return redirect('store')
                else:
                    messages.error(request, "Not enough money in your account.")
                    return redirect('store')
            else:
                messages.error(request, "Incorrect password. Please try again.")
                return redirect('store')
    else:
        form = ConfirmPasswordForm()

    return render(request, 'store/confirm_buy.html', {'form': form, 'game': game})



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

    if request.method == "POST" and "username" in request.POST:
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
        game_price = game.price

        if sender.total_balance < game_price:
            messages.error(request, "Not enough money in your account.")
            return render(request, 'store/buygameasgift.html', {'game': game})

        request.session['gift_transaction'] = {
            'recipient_username': recipient_username,
            'game_id': game.id,
            'game_price': float(game_price)
        }
        return render(request, 'store/confirm_buy.html', {'game': game, 'form': ConfirmPasswordForm()})

    elif request.method == "POST" and "password" in request.POST:
        form = ConfirmPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get("password")
            user = authenticate(username=request.user.username, password=password)

            if user is None:
                messages.error(request, "Invalid password.")
                return render(request, 'store/confirm_buy.html', {'game': game, 'form': form})

            
            transaction = request.session.get('gift_transaction')
            if not transaction:
                messages.error(request, "Transaction details are missing.")
                return redirect('store')

            recipient_username = transaction['recipient_username']
            game_price = Decimal(transaction['game_price'])
            recipient = get_object_or_404(Person, username=recipient_username)

            
            sender = request.user
            sender.total_balance -= game_price
            sender.save()

            PersonGames.objects.create(person=recipient, game=game, date=timezone.now())

            AccountHistory.objects.create(
                person=sender,
                game=game,
                date=timezone.now(),
                amount=game_price
            )
            AccountHistory.objects.create(
                person=recipient,
                game=game,
                date=timezone.now(),
                amount=0,
            )

            del request.session['gift_transaction']  # Clean up session
            messages.success(request, f"Successfully gifted '{game.tittle}' to {recipient.username}!")
            return redirect('store')

        messages.error(request, "Please correct the errors below.")
        return render(request, 'store/confirm_buy.html', {'game': game, 'form': form})

    return render(request, 'store/buygameasgift.html', {'game': game})







