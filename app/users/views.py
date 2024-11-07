from django.shortcuts import render


def registration(request):
    return render(request, 'users/registerPage.html')


def login(request):
    return render(request, 'users/loginPage.html')


def mainPage(request):
    return render(request, 'users/mainPage.html')