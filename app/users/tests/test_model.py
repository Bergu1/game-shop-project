from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from coredb.models import Person as User


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        username = 'testuser'
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for idx, (email, expected) in enumerate(sample_emails):
            user = get_user_model().objects.create_user(username=f'testuser{idx}', 
                                                        email=email, 
                                                        password='sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(username='testuser', 
                                                 email='', 
                                                 password='test123')

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            'testuser', 'test@example.com', 'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


class UserRegistrationTest(TestCase):
    def test_registration_page_status_code(self):
        response = self.client.get(reverse('registration')) 
        self.assertEqual(response.status_code, 200)

    def test_register_user(self):
        data = {
            'username': 'testuser',
            'password': 'Testpassword123!',
            'email': 'testuser@example.com',
            'first-name': 'Test',
            'last-name': 'User',
            'date-of-birth': '2000-01-01', 
            'confirm_password': 'Testpassword123!'  
        }
        response = self.client.post(reverse('registration'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())


class UserLoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Testpassword123!', email='testuser@example.com')

    def test_login_page_status_code(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_user_login(self):
        login = self.client.login(username='testuser', password='Testpassword123!')
        self.assertTrue(login)
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 302)

        self.assertTrue(response.wsgi_request.user.is_authenticated)

        main_page_response = self.client.get(reverse('mainPage'))
        self.assertEqual(main_page_response.status_code, 200)
