from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Customer, Loan
from datetime import date

class CreditSystemTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer_data = {
            "first_name": "John",
            "last_name": "Doe",
            "age": 30,
            "monthly_income": 50000,
            "phone_number": 9876543210
        }

    def test_register_customer(self):
        response = self.client.post('/api/register/', self.customer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "John Doe")
        # approved_limit should be 36 * 50000 = 1,800,000
        self.assertEqual(response.data['approved_limit'], 1800000)

    def test_check_eligibility(self):
        # First register a customer
        reg_resp = self.client.post('/api/register/', self.customer_data, format='json')
        customer_id = reg_resp.data['customer_id']

        eligibility_data = {
            "customer_id": customer_id,
            "loan_amount": 500000,
            "interest_rate": 10,
            "tenure": 12
        }
        response = self.client.post('/api/check-eligibility/', eligibility_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('approval', response.data)
        # With no loans, score should be 100, so approved
        self.assertTrue(response.data['approval'])

    def test_create_loan(self):
        # First register a customer
        reg_resp = self.client.post('/api/register/', self.customer_data, format='json')
        customer_id = reg_resp.data['customer_id']

        loan_data = {
            "customer_id": customer_id,
            "loan_amount": 100000,
            "interest_rate": 10,
            "tenure": 12
        }
        response = self.client.post('/api/create-loan/', loan_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['loan_approved'])

        # Verify loan exists in DB
        loan = Loan.objects.get(loan_id=response.data['loan_id'])
        self.assertEqual(loan.loan_amount, 100000)
