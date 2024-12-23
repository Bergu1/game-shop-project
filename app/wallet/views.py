from django.shortcuts import render, redirect
from django.db import transaction
from coredb.models import AccountHistory, ExchangeRate
from django.contrib.auth.decorators import login_required
from wallet.forms import AmountForm
from django.utils import timezone
from datetime import datetime
from decimal import Decimal

@login_required
def wallet_view(request):
    user = request.user
    user_currency = user.currency 
    total_balance_in_user_currency = ExchangeRate.convert(user.total_balance, "PLN", user_currency)
    return render(request, 'wallet/wallet_view.html', {
        'total_balance': total_balance_in_user_currency,
        'currency': user_currency
    })


@login_required
def wallet_operations(request):
    user = request.user
    user_currency = user.currency
    total_balance_in_user_currency = ExchangeRate.convert(user.total_balance, "PLN", user_currency)

    if request.method == 'POST':
        form = AmountForm(request.POST)
        if form.is_valid():
            amount_in_user_currency = form.cleaned_data['amount']
            amount_in_pln = ExchangeRate.convert(amount_in_user_currency, user_currency, "PLN")

            with transaction.atomic():
                AccountHistory.objects.create(
                    person=user,
                    date=timezone.now(),
                    amount=amount_in_pln 
                )
                user.total_balance += amount_in_pln
                user.save()
            return redirect('wallet_view')
    else:
        form = AmountForm()

    context = {
        'total_balance': total_balance_in_user_currency,
        'currency': user_currency,
        'form': form,
    }
    return render(request, 'wallet/wallet_operations.html', context)



@login_required
def account_history(request):
    user = request.user
    user_currency = user.currency 
    current_year = datetime.now().year
    years = list(range(current_year, current_year + 10))

    month = request.GET.get('month')
    year = request.GET.get('year')

    incomes = []
    expenses = []
    if month and year:
        try:
            month = int(month)
            year = int(year)
            account_history = AccountHistory.objects.filter(
                person=user,
                date__year=year,
                date__month=month
            )

            for entry in account_history:
                amount_in_user_currency = ExchangeRate.convert(
                    entry.amount,
                    "PLN",
                    user_currency
                )
                entry.amount_converted = round(Decimal(amount_in_user_currency), 2)

                if entry.game is None:
                    incomes.append(entry)
                else:
                    expenses.append(entry)
        except ValueError:
            pass

    return render(request, 'wallet/account_history.html', {
        'years': years,
        'incomes': incomes,
        'expenses': expenses,
        'currency': user_currency,
    })
