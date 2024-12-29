from django.test import TestCase, Client
from coredb.models import Person
from django.urls import reverse
from django.contrib.messages import get_messages

class ChangeCurrencyViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Person.objects.create_user(
            username="testuser",
            password="password123",
            email = 'test@test.pl',
            currency="PLN"
        )
        self.client.login(username="testuser", password="password123")
        self.change_currency_url = reverse("change_currency")
        self.news_list_url = reverse("news_list")

    def test_change_currency_to_valid_currency(self):
        response = self.client.post(self.change_currency_url, {"currency": "USD"})
        self.user.refresh_from_db()
        self.assertEqual(self.user.currency, "USD")
        self.assertRedirects(response, self.news_list_url)

    def test_change_currency_to_invalid_currency(self):
        response = self.client.post(self.change_currency_url, {"currency": "GBP"})
        self.user.refresh_from_db()
        self.assertEqual(self.user.currency, "PLN")
        self.assertRedirects(response, self.news_list_url)


