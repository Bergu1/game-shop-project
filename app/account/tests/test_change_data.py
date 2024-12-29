from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.messages import get_messages
from coredb.models import Person
from datetime import datetime

class ChangeDataViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Person.objects.create_user(
            username="testuser",
            password="password123",
            email="testuser@example.com",
            first_name="John",
            last_name="Doe"
        )
        self.user.date_of_birth = "1990-01-01"
        self.user.save()

        self.login_url = reverse("login")
        self.change_data_url = reverse("change_data")
        self.client.login(username="testuser", password="password123")

    def test_change_first_name(self):
        response = self.client.post(self.change_data_url, {
            "record": "first_name",
            "update": "Jane"
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Jane")
        self.assertRedirects(response, self.change_data_url)

    def test_change_last_name(self):
        response = self.client.post(self.change_data_url, {
            "record": "last_name",
            "update": "Smith"
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.last_name, "Smith")
        self.assertRedirects(response, self.change_data_url)

    def test_change_email_success(self):
        response = self.client.post(self.change_data_url, {
            "record": "email",
            "update": "newemail@example.com"
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "newemail@example.com")
        self.assertRedirects(response, self.change_data_url)

    def test_change_email_duplicate(self):
        Person.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="password123"
        )
        response = self.client.post(self.change_data_url, {
            "record": "email",
            "update": "other@example.com"
        })
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "This email is already in use.")

    def test_change_username_success(self):
        response = self.client.post(self.change_data_url, {
            "record": "username",
            "update": "newusername"
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "newusername")
        self.assertRedirects(response, self.change_data_url)

    def test_change_username_duplicate(self):
        Person.objects.create_user(
            username="existinguser",
            email="existinguser@example.com",
            password="password123"
        )
        response = self.client.post(self.change_data_url, {
            "record": "username",
            "update": "existinguser"
        })
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "This username is already taken.")

    def test_change_password(self):
        response = self.client.post(self.change_data_url, {
            "record": "password",
            "update": "newpassword123"
        })
        self.assertRedirects(response, self.login_url)
        self.client.logout()
        login_success = self.client.login(username="testuser", password="newpassword123")
        self.assertTrue(login_success)

    def test_change_date_of_birth(self):
        response = self.client.post(self.change_data_url, {
            "record": "date-of-birth",
            "update": "2000-01-01"
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.date_of_birth, datetime.strptime("2000-01-01", "%Y-%m-%d").date())
        self.assertRedirects(response, self.change_data_url)
