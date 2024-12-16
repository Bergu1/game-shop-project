from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from coredb.models import Friends, PersonGames
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

            elif Friends.objects.filter(sender=request.user, recipient=recipient, status='accepted').exists() or \
                Friends.objects.filter(sender=recipient, recipient=request.user, status='accepted').exists():
                messages.error(request, "You are already friends with this user.")
                return redirect('send_friend_request')
            else:
                Friends.objects.create(sender=request.user, recipient=recipient)
                messages.success(request, "Friend request sent!")
            return redirect('send_friend_request')
    else:
        form = FriendForm()

    return render(request, 'friends/send_friend_request.html', {'form': form})


@login_required
def invitations(request):
    sent_requests = Friends.objects.filter(sender=request.user)

    received_requests = Friends.objects.filter(recipient=request.user, status='pending')

    if request.method == 'POST':
        action = request.POST.get('action')
        request_id = request.POST.get('request_id')
        friend_request = get_object_or_404(Friends, id=request_id, recipient=request.user)

        if action == 'accept':
            friend_request.status = 'accepted'
        elif action == 'reject':
            friend_request.status = 'rejected'

        friend_request.save()
        return redirect('invitations')

    context = {
        'sent_requests': sent_requests,
        'received_requests': received_requests,
    }
    return render(request, 'friends/invitation_status.html', context)


@login_required
def friends_list(request):
    friends = Friends.objects.filter(
        status='accepted',
        sender=request.user
    ) | Friends.objects.filter(
        status='accepted',
        recipient=request.user
    )

    friends_list = []
    for friend in friends:
        if friend.sender == request.user:
            friends_list.append(friend)
        else:
            friends_list.append(friend) 

    friends_list = list(set(friends_list))

    return render(request, 'friends/friends_list.html', {'friends_list': friends_list})


@login_required
def remove_friend(request, friend_id):
    friend = get_object_or_404(Friends, id=friend_id)

    if friend.sender == request.user or friend.recipient == request.user:
        friend.delete()
        messages.success(request, "Friend removed successfully.")
    else:
        messages.error(request, "You cannot remove this friend.")
    
    return redirect('friends_list')


@login_required
def friends_games(request, friend_id):
    user = get_object_or_404(Friends, id=friend_id)
    print("1")
    if user.sender == request.user:
        user_games = PersonGames.objects.filter(person=user.recipient)
        print("2")
    elif user.recipient == request.user:
        user_games = PersonGames.objects.filter(person=user.sender)
        print("3")
    return render(request, 'friends/friends_games.html', {'user_games': user_games})