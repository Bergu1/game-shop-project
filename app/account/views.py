from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ConfirmPasswordForm
from django.contrib.auth import authenticate
from coredb.models import Person, ExchangeRate
from django.db.models import Q
from django.contrib.auth import logout

@login_required
def account_view(request):
    user = request.user
    user_currency = user.currency
    total_balance_in_user_currency = ExchangeRate.convert(user.total_balance, "PLN", user_currency)
    
    return render(
        request,
        'account/account_view.html',
        {
            'total_balance': total_balance_in_user_currency,
            'currency': user_currency,
        }
    )



@login_required
def delete_account(request):
    if request.method == "POST":
        form = ConfirmPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get("password")
            user = authenticate(username=request.user.username, password=password)
            if user:
                user.delete()
                messages.success(request, "Your account has been successfully deleted!")
                return redirect("login")
            else:
                messages.error(request, "Incorrect password. Please try again.")
    else:
        form = ConfirmPasswordForm()

    return render(request, "account/confirm_delete_account.html", {"form": form})


@login_required
def change_data(request):
    if request.method == 'POST':
        record_to_update = request.POST.get('record')
        new_value = request.POST.get('update')
        user = request.user 

        try:
            if record_to_update == 'first_name':
                user.first_name = new_value
            elif record_to_update == 'last_name':
                user.last_name = new_value
            elif record_to_update == 'email':
                if Person.objects.filter(Q(email=new_value) & ~Q(id=user.id)).exists():
                    messages.error(request, "This email is already in use.")
                    return redirect('change_data')
                user.email = new_value
            elif record_to_update == 'date-of-birth':
                user.date_of_birth = new_value
            elif record_to_update == 'username':
                if Person.objects.filter(Q(username=new_value) & ~Q(id=user.id)).exists():
                    messages.error(request, "This username is already taken.")
                    return redirect('change_data')
                user.username = new_value
            elif record_to_update == 'password':
                user.set_password(new_value)
                messages.success(request, "Password updated successfully. Please log in again.")
                user.save()
                logout(request)
                return redirect('login') 

            user.save()
            messages.success(request, "Record updated successfully.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
        
        return redirect('change_data')

    return render(request, 'account/change_data.html') 