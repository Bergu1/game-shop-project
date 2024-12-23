import requests
from datetime import datetime
from coredb.models import ExchangeRate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect

@login_required
def change_currency(request):
    if request.method == "POST":
        new_currency = request.POST.get("currency")
        if new_currency in ["PLN", "USD", "EUR"]: 
            user = request.user
            user.currency = new_currency
            user.save()
            messages.success(request, f"Currency has been changed to {new_currency}.")
        else:
            messages.error(request, "Invalid currency selected.")
    return redirect("news_list")