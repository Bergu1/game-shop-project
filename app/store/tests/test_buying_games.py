from django.test import TestCase, Client
from django.urls import reverse
from coredb.models import Games, PersonGames, AccountHistory, Person
from django.contrib.messages import get_messages
from django.utils import timezone
from decimal import Decimal


class BuyGameTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Person.objects.create_user(username="testuser", password="password123", email="test1@test.pl", total_balance=100)
        self.recipient = Person.objects.create_user(username="recipientuser", password="password123", email="test2@test.pl")
        self.game = Games.objects.create(tittle="Test Game", price=50)
        self.buy_game_url = reverse("buy_game", args=[self.game.id])  # Updated to match your URLs
        self.buy_game_as_gift_url = reverse("game_gift", args=[self.game.id])  # Updated to match "game_gift"
        self.client.login(username="testuser", password="password123")

    def test_buy_game_success(self):
        response = self.client.post(self.buy_game_url, {"password": "password123"})
        self.user.refresh_from_db()
        self.assertEqual(self.user.total_balance, 50)
        self.assertTrue(PersonGames.objects.filter(person=self.user, game=self.game).exists())
        self.assertTrue(AccountHistory.objects.filter(person=self.user, game=self.game, amount=self.game.price).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Successful purchase!")

    def test_buy_game_insufficient_balance(self):
        self.user.total_balance = 40
        self.user.save()
        response = self.client.post(self.buy_game_url, {"password": "password123"})
        self.user.refresh_from_db()
        self.assertEqual(self.user.total_balance, 40)
        self.assertFalse(PersonGames.objects.filter(person=self.user, game=self.game).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Not enough money in your account.")

    def test_buy_game_already_owned(self):
        PersonGames.objects.create(person=self.user, game=self.game, date=timezone.now())
        response = self.client.post(self.buy_game_url, {"password": "password123"})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "You already own this game.")

    def test_buy_game_invalid_password(self):
        response = self.client.post(self.buy_game_url, {"password": "wrongpassword"})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Incorrect password. Please try again.")

    def test_buy_game_as_gift_success(self):

        session = self.client.session
        session['gift_transaction'] = {
            'recipient_username': "recipientuser",
            'game_id': self.game.id,
            'game_price': float(self.game.price)
        }
        session.save()

        response = self.client.post(self.buy_game_as_gift_url, {
            "password": "password123"
        })

 
        self.user.refresh_from_db()
        self.assertEqual(self.user.total_balance, Decimal('50.00'))  


        self.assertTrue(PersonGames.objects.filter(person=self.recipient, game=self.game).exists())

    
        self.assertTrue(AccountHistory.objects.filter(person=self.user, game=self.game, amount=self.game.price).exists())


        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), f"Successfully gifted '{self.game.tittle}' to recipientuser!")


    def test_buy_game_as_gift_insufficient_balance(self):
        self.user.total_balance = 40
        self.user.save()
        response = self.client.post(self.buy_game_as_gift_url, {
            "username": "recipientuser",
            "password": "password123"
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.total_balance, 40)
        self.assertFalse(PersonGames.objects.filter(person=self.recipient, game=self.game).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Not enough money in your account.")

    def test_buy_game_as_gift_invalid_recipient(self):
        response = self.client.post(self.buy_game_as_gift_url, {"username": "nonexistentuser"})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "The recipient username 'nonexistentuser' does not exist.")

    def test_buy_game_as_gift_already_owned(self):
        PersonGames.objects.create(person=self.recipient, game=self.game, date=timezone.now())
        response = self.client.post(self.buy_game_as_gift_url, {"username": "recipientuser"})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "recipientuser already owns this game.")

    def test_buy_game_as_gift_invalid_password(self):
        self.client.post(self.buy_game_as_gift_url, {
            "username": "recipientuser"
        })
        response = self.client.post(self.buy_game_as_gift_url, {
            "password": "wrongpassword"
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Invalid password.")
