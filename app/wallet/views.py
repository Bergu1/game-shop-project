from django.shortcuts import render, redirect
from django.db import transaction
from coredb.models import AccountHistory, ExchangeRate
from django.contrib.auth.decorators import login_required
from wallet.forms import AmountForm
from django.utils import timezone
from datetime import datetime
from decimal import Decimal
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO

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


'''
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
'''

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import mm

@login_required
def account_history(request):
    user = request.user
    user_currency = user.currency
    current_year = datetime.now().year
    years = list(range(current_year, current_year + 10))

    month = request.GET.get('month')
    year = request.GET.get('year')
    generate_pdf = request.GET.get('pdf', False)

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
            month = None
            year = None


    if generate_pdf and month and year:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        elements.append(Table(
            [[f"Account History for {user.username}"]],
            style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
            ]),
            colWidths=[500]
        ))

        elements.append(Spacer(1, 10 * mm))

        elements.append(Table(
            [["Incomes"]],
            style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
            ]),
            colWidths=[500]
        ))

        income_data = [["Date", "Amount"]]
        for income in incomes:
            income_data.append([income.date, f"{income.amount_converted} {user_currency}"])

        income_table = Table(income_data)
        income_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(income_table)

        elements.append(Spacer(1, 10 * mm))

        elements.append(Table(
            [["Expenses"]],
            style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.pink),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
            ]),
            colWidths=[500]
        ))
        
        expense_data = [["Date", "Game", "Amount"]]
        for expense in expenses:
            expense_data.append([expense.date, expense.game.tittle, f"{expense.amount_converted} {user_currency}"])

        expense_table = Table(expense_data)
        expense_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(expense_table)

        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')

    return render(request, 'wallet/account_history.html', {
        'years': years,
        'incomes': incomes,
        'expenses': expenses,
        'currency': user_currency,
        'month': month,
        'year': year,
    })

