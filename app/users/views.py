from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from coredb.models import Person, News
from django.contrib.auth.decorators import login_required

def registration(request):
    if request.method == 'POST':
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        email = request.POST.get('email')
        date_of_birth = request.POST.get('date-of-birth')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if not username:
            messages.error(request, "Recipient username is required.")
            return render(request, 'users/registerPage.html')
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'users/registerPage.html')

        try:
            user = Person.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                currency='PLN' 
            )
            return redirect('login') 
        except Exception as e:
            messages.error(request, f"Error during user creation: {str(e)}")
            return render(request, 'users/registerPage.html')

    return render(request, 'users/registerPage.html')



def login_view(request):

    if request.user.is_authenticated:
        return redirect('news_list')
    
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('news_list')
        else:
            messages.error(request, "Invalid username or password")
            return render(request, 'users/loginPage.html')
    
    return render(request, 'users/loginPage.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def mainPage(request):
    return render(request, 'users/mainPage.html')

@login_required
def news_list(request):
    news = News.objects.all().order_by('-date')
    return render(request, 'users/news_list.html', {'news': news})

def news_detail(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    return render(request, 'users/news_detail.html', {'news_item': news_item})