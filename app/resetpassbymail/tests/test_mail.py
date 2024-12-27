from django.test import TestCase
from django.core.mail import send_mail

class EmailTest(TestCase):
    def test_send_email(self):
        response = send_mail(
            'Test Subject',
            'This is a test email message.',
            'noreply@gmail.com',
            ['konrad-landzberg@wp.pl']
        )
        self.assertEqual(response, 1)
