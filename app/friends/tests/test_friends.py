from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from coredb.models import Person, Friends, PersonGames
from django.contrib.messages import get_messages

class FriendsFeatureTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = Person.objects.create_user(username="user1", password="password123", email="test1@test.pl")
        self.user2 = Person.objects.create_user(username="user2", password="password123", email="test2@test.pl")
        self.user3 = Person.objects.create_user(username="user3", password="password123", email="test3@test.pl")
        self.client.login(username="user1", password="password123")
        self.send_friend_request_url = reverse("send_friend_request")
        self.invitations_url = reverse("invitations")
        self.friends_list_url = reverse("friends_list")
        self.friends_games_url = lambda friend_id: reverse("friends_games", args=[friend_id])
        self.remove_friend_url = lambda friend_id: reverse("remove_friend", args=[friend_id])

    def test_send_friend_request(self):
        response = self.client.post(self.send_friend_request_url, {"recipient_username": "user2"})
        self.assertEqual(Friends.objects.filter(sender=self.user1, recipient=self.user2).count(), 1)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Friend request sent!")

    def test_send_friend_request_to_self(self):
        response = self.client.post(self.send_friend_request_url, {"recipient_username": "user1"})
        self.assertEqual(Friends.objects.filter(sender=self.user1).count(), 0)


    def test_send_duplicate_friend_request(self):
        Friends.objects.create(sender=self.user1, recipient=self.user2, status="pending")
        response = self.client.post(self.send_friend_request_url, {"recipient_username": "user2"})
        self.assertEqual(Friends.objects.filter(sender=self.user1, recipient=self.user2).count(), 1)


    def test_accept_friend_request(self):
        friend_request = Friends.objects.create(sender=self.user2, recipient=self.user1, status="pending")
        response = self.client.post(self.invitations_url, {"action": "accept", "request_id": friend_request.id})
        friend_request.refresh_from_db()
        self.assertEqual(friend_request.status, "accepted")
        self.assertRedirects(response, self.invitations_url)

    def test_reject_friend_request(self):
        friend_request = Friends.objects.create(sender=self.user2, recipient=self.user1, status="pending")
        response = self.client.post(self.invitations_url, {"action": "reject", "request_id": friend_request.id})
        friend_request.refresh_from_db()
        self.assertEqual(friend_request.status, "rejected")
        self.assertRedirects(response, self.invitations_url)

    def test_view_friends_list(self):
        Friends.objects.create(sender=self.user1, recipient=self.user2, status="accepted")
        response = self.client.get(self.friends_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "user2")

    def test_remove_friend(self):
        friendship = Friends.objects.create(sender=self.user1, recipient=self.user2, status="accepted")
        response = self.client.post(self.remove_friend_url(friendship.id))
        self.assertEqual(Friends.objects.filter(id=friendship.id).count(), 0)


    def test_remove_friend_not_involved(self):
        friendship = Friends.objects.create(sender=self.user2, recipient=self.user3, status="accepted")
        response = self.client.post(self.remove_friend_url(friendship.id))
        self.assertEqual(Friends.objects.filter(id=friendship.id).count(), 1)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "You cannot remove this friend.")

from datetime import datetime

def test_view_friends_games(self):
    friendship = Friends.objects.create(sender=self.user1, recipient=self.user2, status="accepted")
    PersonGames.objects.create(person=self.user2, game="Game 1", date=datetime.now())
    response = self.client.get(self.friends_games_url(friendship.id))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "Game 1")
