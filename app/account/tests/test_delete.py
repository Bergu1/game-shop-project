from django.test import TestCase, Client
from coredb import models
from django.urls import reverse
from django.contrib.messages import get_messages

class DeleteAccountViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = models.Person.objects.create_user(
            username="testuser",
            password="password123",
            email="testuser@example.com"
        )
        self.login_url = reverse("login")
        self.delete_account_url = reverse("delete_account")

    def test_delete_account_page_loads(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.delete_account_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/confirm_delete_account.html")

    def test_delete_account_with_correct_password(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(self.delete_account_url, {
            "password": "password123"
        })
        self.assertRedirects(response, self.login_url)
        self.assertFalse(models.Person.objects.filter(username="testuser").exists())

    def test_delete_account_with_incorrect_password(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(self.delete_account_url, {
            "password": "wrongpassword"
        })
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Incorrect password. Please try again.")
        self.assertTrue(models.Person.objects.filter(username="testuser").exists())