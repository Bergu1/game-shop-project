from django.shortcuts import render, redirect
from django.db import transaction
from coredb.models import AccountHistory
from django.contrib.auth.decorators import login_required
from wallet.forms import AmountForm
from django.utils import timezone
from datetime import datetime

@login_required
def wallet_view(request):
    user = request.user
    total_balance = user.total_balance
    return render(request, 'wallet/wallet_view.html', {'total_balance': total_balance})


@login_required
def wallet_operations(request):
    user = request.user
    total_balance = user.total_balance

    if request.method == 'POST':
        form = AmountForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            with transaction.atomic():
                AccountHistory.objects.create(person=user,
                                              date=timezone.now(),
                                              amount=amount)
                user.total_balance += amount
                user.save()
            return redirect('wallet_view')
    else:
        form = AmountForm()

    context = {
        'total_balance': total_balance,
        'form': form,
    }
    return render(request, 'wallet/wallet_operations.html', context)


@login_required
def account_history(request):
    user = request.user
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
            account_history = AccountHistory.objects.filter(person=user,
                                                            date__year=year,
                                                            date__month=month)
            for entry in account_history:
                if entry.game is None:
                    incomes.append(entry)  
                else:
                    expenses.append(entry)
        except ValueError:
            pass

    return render(request, 'wallet/account_history.html', {'years': years,
        'incomes': incomes,
        'expenses': expenses
        })
