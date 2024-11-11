from django.shortcuts import render, redirect
from coredb.models import PersonGames
from django.contrib.auth.decorators import login_required


@login_required
def library_view(request):
    user = request.user
    user_games = PersonGames.objects.filter(person=user)  
    return render(request, 'library/library.html', {'user_games': user_games})