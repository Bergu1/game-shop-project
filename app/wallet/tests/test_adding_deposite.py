from django.test import TestCase, Client
from django.urls import reverse
from coredb.models import AccountHistory, Person
from decimal import Decimal

class WalletOperationsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Person.objects.create_user(username="testuser", password="password123", email="test1@test.pl", total_balance=Decimal("100.00"), currency="PLN")
        self.wallet_operations_url = reverse("wallet_operations")
        self.wallet_view_url = reverse("wallet_view")
        self.client.login(username="testuser", password="password123")

    def test_wallet_operations_get_request(self):
        response = self.client.get(self.wallet_operations_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "wallet/wallet_operations.html")
        self.assertIn("total_balance", response.context)
        self.assertIn("currency", response.context)
        self.assertIn("form", response.context)

    def test_wallet_operations_post_valid_amount(self):
        response = self.client.post(self.wallet_operations_url, {
            "amount": "50.00"
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.total_balance, Decimal("150.00"))
        self.assertEqual(AccountHistory.objects.count(), 1)
        self.assertEqual(AccountHistory.objects.first().amount, Decimal("50.00"))
        self.assertRedirects(response, self.wallet_view_url)

    def test_wallet_operations_post_invalid_amount(self):
        response = self.client.post(self.wallet_operations_url, {
            "amount": "" 
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.total_balance, Decimal("100.00")) 
        self.assertEqual(AccountHistory.objects.count(), 0)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "wallet/wallet_operations.html")

    def test_wallet_operations_post_negative_amount(self):
        response = self.client.post(self.wallet_operations_url, {
            "amount": "-50.00" 
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.total_balance, Decimal("100.00"))  
        self.assertEqual(AccountHistory.objects.count(), 0)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "wallet/wallet_operations.html")

