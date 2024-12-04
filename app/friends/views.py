from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from coredb.models import Friends
from friends.forms import FriendForm
from django.contrib import messages

@login_required
def friends(request):
    return render(request, 'friends/main_friends.html')


@login_required
def send_friend_request(request):
    if request.method == "POST":
        form = FriendForm(request.POST)
        if form.is_valid():
            recipient = form.cleaned_data['recipient_username']
            if not recipient:
                messages.error(request, "User with this username does not exist.")
            elif Friends.objects.filter(sender=request.user, recipient=recipient).exists():
                messages.error(request, "You have already sent a friend request to this user.")
            elif request.user == recipient:
                messages.error(request, "You cannot send a friend request to yourself.")
            else:
                Friends.objects.create(sender=request.user, recipient=recipient)
                messages.success(request, "Friend request sent!")
            return redirect('send_friend_request')
    else:
        form = FriendForm()

    return render(request, 'friends/send_friend_request.html', {'form': form})